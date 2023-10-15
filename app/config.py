from click import prompt, echo, confirm
from os import environ, getenv
from dotenv import load_dotenv
from boto3 import client
from uuid import uuid4
from time import sleep

DOTENV = '.env'
EXPECTED_ENV_VARS = [
    'AWS_SECRET_ACCESS_KEY',
    'AWS_ACCESS_KEY_ID',
    'AWS_DEFAULT_REGION',
    'BACKUP_BUCKET_NAME',
    'LOCAL_PATH'
]
TEMPLATE_PATH = "app/bucket.yml"

class Config:
    def __init__(self, run_config: bool):
        self._run_config = run_config
        self._configs = {}

    def configure(self) -> None:
        load_dotenv(DOTENV, verbose=True)

        if self._missing_configs() or self._run_config:
            echo('Executing configuration wizard')
            if confirm("Do you wish to create a new bucket?"):
                self.bucket_wizard()
            self.configuration_wizard()

        # If changes have been made to the configurations
        if self._configs:
            self._write_configs()
            load_dotenv(DOTENV, verbose=True)

    def configuration_wizard(self) -> None:
        self._configs = {}
        for var in EXPECTED_ENV_VARS:
            self._configs[var] = prompt(var, default=getenv(var, None))

    def bucket_wizard(self) -> bool:
        cf = client("cloudformation")
        bucket_name = prompt("Name for the new bucket")+str(uuid4())[:8]

        with open(TEMPLATE_PATH, 'r') as template:
            stack_id = cf.create_stack(
                StackName=bucket_name,
                TemplateBody=template.read(),
                Parameters=[
                    {
                        "ParameterKey": "BucketName",
                        "ParameterValue": bucket_name
                    }
                ]
            )["StackId"]
        
        echo("Creating bucket...")

        # Wait for the bucket to be created
        creating = True
        while creating:
            response = cf.describe_stack_events(StackName=stack_id)
            for event in response["StackEvents"]:
                if event["ResourceStatus"] == "CREATE_COMPLETE":
                    creating = False
                    successful = True
                    break
                elif event["ResourceStatus"] == "CREATE_IN_PROGRESS":
                    continue
                else:
                    echo(f'Unexpected status: {event["ResourceStatus"]}')
                    echo(event["ResourceStatusReason"])
                    creating = False
                    successful = False
                    break
            sleep(1)

        if successful:
            self._configs['BACKUP_BUCKET_NAME'] = bucket_name
            environ['BACKUP_BUCKET_NAME'] = bucket_name
            echo(f"Bucket created: {bucket_name}")
            return True
        
        return False


    def _missing_configs(self) -> list:
        missing_configs = []

        for var in EXPECTED_ENV_VARS:
            if var not in environ:
                echo(f'Missing environment variable: {var}')
                missing_configs.append(var)

        return missing_configs
    
    def _write_configs(self) -> None:
        with open(DOTENV, 'w') as file:
            for config_name, config_value in self._configs.items():
                file.write(f'{config_name}={config_value}\n')

                


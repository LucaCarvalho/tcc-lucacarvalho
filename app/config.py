from click import prompt, echo, confirm
from os import environ, getenv
from dotenv import load_dotenv

DOTENV = '.env'
EXPECTED_ENV_VARS = [
    'AWS_SECRET_ACCESS_KEY',
    'AWS_ACCESS_KEY_ID',
    'AWS_DEFAULT_REGION',
    'BACKUP_BUCKET_NAME',
    'LOCAL_PATH'
]

class Config:
    def __init__(self, run_config: bool):
        self._run_config = run_config
        self._configs = {}

    def configure(self) -> bool:
        load_dotenv(DOTENV, verbose=True)

        if self._missing_configs() or self._run_config:
            echo('Executing configuration wizard')
            self.configuration_wizard()

        # If changes have been made to the configurations
        if self._configs:
            self._write_configs()
            load_dotenv(DOTENV, verbose=True)

    def configuration_wizard(self) -> None:
        self._configs = {}
        for var in EXPECTED_ENV_VARS:
            self._configs[var] = prompt(var, default=getenv(var, None))

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

                


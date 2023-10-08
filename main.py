import os
import click
import logging
import signal

from dotenv import get_variables
from storage import RemoteStorage, LocalStorage
from app import App


# Configure logging
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
logging.getLogger('boto3').setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.INFO)
logging.getLogger('s3transfer').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)
logger = logging.getLogger('app')


# Load configurations
get_variables('.env') #TODO create setup tool to generate .env

# Main program
@click.command()
@click.option('--local_path', default=os.getcwd())       
@click.option('--bucket', default=os.getenv('BUCKET_NAME'))
def main(local_path: str, bucket: str) -> None:
    local = LocalStorage(local_path)
    remote = RemoteStorage(bucket)

    app = App(local, remote)
    app.loop()

if __name__ == '__main__':
    main()
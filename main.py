import os
import click

from dotenv import get_variables
from storage import RemoteStorage, LocalStorage

import logging

# Configure logging
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
logging.getLogger('boto3').setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.INFO)
logging.getLogger('s3transfer').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)
logger = logging.getLogger('main')

get_variables('.env') #TODO create setup tool to generate .env

@click.command()
@click.option('--local_path', default=os.getcwd())       
@click.option('--bucket', default=os.getenv('BUCKET_NAME'))       
def main(local_path: str, bucket: str) -> None:
    local = LocalStorage(local_path)
    remote = RemoteStorage(bucket)

    logger.debug(local.list_files())
    logger.debug(remote.list_files())

    logger.info(f'Syncing up... {local.sync_up(remote).stdout}')
    # logger.info(f'Syncing down... {remote.sync_down(local).stdout}')

    logger.debug(local.list_files())
    logger.debug(remote.list_files())

if __name__ == '__main__':
    main()
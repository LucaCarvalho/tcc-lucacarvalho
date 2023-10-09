import click
import logging
from os import getenv

from storage import RemoteStorage, LocalStorage
from app import App, Config


# Configure logging
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
logging.getLogger('boto3').setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.INFO)
logging.getLogger('s3transfer').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)
logger = logging.getLogger('app')

# Main program
@click.command()
@click.option('--run_config', type=click.BOOL, default=False)
def main(run_config: bool) -> None:
    # Load configurations
    config = Config(run_config)
    config.configure()

    # Setup storages
    local = LocalStorage(getenv('LOCAL_PATH'))
    remote = RemoteStorage(getenv('BACKUP_BUCKET_NAME'))

    # Start the application
    app = App(local, remote)
    app.loop()

if __name__ == '__main__':
    main()
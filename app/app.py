from time import sleep
from storage import LocalStorage, RemoteStorage
from logging import getLogger
from signal import signal, SIGINT

logger = getLogger('app')

UPDATE_INTERVAL = 15

class App:
    def __init__(self, local_storage: LocalStorage, remote_storage: RemoteStorage):
        self._local_storage = local_storage
        self._remote_storage = remote_storage
        self._running = True
        signal(SIGINT, self._handle_signal)

    def loop(self) -> None:
        while self._running:
            logger.debug(f'Local: {self._local_storage.list_files()}')
            logger.debug(f'Remote: {self._remote_storage.list_files()}')

            logger.info(f'Syncing up... {self._local_storage.sync_up(self._remote_storage).stdout}')

            logger.debug(f'Local: {self._local_storage.list_files()}')
            logger.debug(f'Remote: {self._remote_storage.list_files()}')

            sleep(UPDATE_INTERVAL)

    def _handle_signal(self, signal, stack_trace) -> None:
        logger.info('Exiting gracefully...')
        self._running = False
    
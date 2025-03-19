from PyQt6.QtCore import QThread, QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool

import asyncio
import threading


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


# For QThread
class LoadPicturesWorker(QRunnable):
    def __init__(self, fn, api_client):
        super().__init__()
        self.fn = fn
        self.api_client = api_client
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        # Use the loop of APIclient from this thread
        future = asyncio.run_coroutine_threadsafe(self.fn(), self.api_client.loop)
        future.result()  # ✅ Wait for result

        self.signals.finished.emit()


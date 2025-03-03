from PyQt6.QtCore import QThread, QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


# For QThread
class LoadPicturesWorker(QRunnable):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.fn()
        self.signals.finished.emit()


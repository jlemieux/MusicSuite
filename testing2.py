import sys
import time
from functools import partial

from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot


class Worker(QObject):
    def __init__(self):
        super().__init__()
        self.thread = None


class Tab(QObject):
    def __init__(self, _main):
        super().__init__()
        self._main = _main


class WorkerOne(Worker):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot(str)
    def print_name(self, name):
        for _ in range(100):
            print("Hello there, {0}! <{1}>".format(name, int(QThread.currentThreadId())))
            time.sleep(1)

        self.finished.emit()
        self.thread.quit()


class SomeTabController(Tab):
    def __init__(self, _main):
        super().__init__(_main)
        self.threads = {}
        main_thread = QThread.currentThread()
        main_thread_id = main_thread.currentThreadId()
        print("Main Thread: <{0}>".format(int(QThread.currentThread().currentThreadId())))

        self._main.button_start_thread.clicked.connect(self.start_thread)

        # Workers
        self.worker1 = WorkerOne()
        #self.worker2 = WorkerTwo()
        #self.worker3 = WorkerThree()
        #self.worker4 = WorkerFour()

    def _threaded_call(self, worker, fn, *args, signals=None, slots=None):
        thread = QThread()
        thread.setObjectName('thread_' + worker.__class__.__name__)

        # store because garbage collection
        self.threads[worker] = thread

        # give worker thread so it can be quit()
        worker.thread = thread

        # objects stay on threads after thread.quit()
        # need to move back to main thread to recycle the same Worker.
        # Error is thrown about Worker having thread (0x0) if you don't do this
        cur = int(QThread.currentThread().currentThreadId())
        print("Move BACK to current thread <{0}>".format(cur))
        worker.moveToThread(QThread.currentThread())

        # move to newly created thread
        print("Move to new thread <{0}>".format(int(thread.currentThreadId())))
        worker.moveToThread(thread)

        if thread is QThread.currentThread():
            print("Yes it is!")

        # Can now apply cross-thread signals/slots

        #worker.signals.connect(self.slots)
        if signals:
            for signal, slot in signals.items():
                try:
                    signal.disconnect()
                except TypeError:  # Signal has no slots to disconnect
                    pass
                signal.connect(slot)

        #self.signals.connect(worker.slots)
        if slots:
            for slot, signal in slots.items():
                try:
                    signal.disconnect()
                except TypeError:  # Signal has no slots to disconnect
                    pass
                signal.connect(slot)

        thread.started.connect(partial(fn, *args)) # fn needs to be slot
        thread.start()

    @pyqtSlot()
    def _receive_signal(self):
        print("Signal received.")

    @pyqtSlot(bool)
    def start_thread(self):
        name = "Bob"
        signals = {self.worker1.finished: self._receive_signal}
        self._threaded_call(self.worker1, self.worker1.print_name, name,
                            signals=signals)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Thread Example")
        form_layout = QVBoxLayout()
        self.setLayout(form_layout)
        self.resize(400, 400)

        self.button_start_thread = QPushButton()
        self.button_start_thread.setText("Start thread.")
        form_layout.addWidget(self.button_start_thread)

        self.controller = SomeTabController(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    _main = MainWindow()
    _main.show()

    sys.exit(app.exec_())

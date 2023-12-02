from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QHBoxLayout
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from download_notebook import ClearNotebooksScraper
from download_user import ClearUsrScraper
import sys
import threading
import queue


def read_file_to_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return file_content


class WorkerThread(QThread):
    update_text = pyqtSignal(str)

    def __init__(self, nbid, cmode):
        super().__init__()
        self.nbid = nbid
        self.shared_queue = queue.Queue()
        self.producer_thread = None
        self.cmode = cmode

    def write(self, tx):
        self.update_text.emit(tx)

    def close(self):
        self.update_text.emit("$EOF$")
        self.quit()

    def doall1(self):
        with ClearNotebooksScraperNW(self.nbid, self) as runme:
            runme.scrape_clear_notebooks()

    def doall2(self):
        with ClearUsrScraperNW(self.nbid, self) as runme:
            runme.scrape_clear_usr()

    def runit(self):
        if self.cmode == 1:
            self.producer_thread = threading.Thread(target=self.doall1)
        elif self.cmode == 2:
            self.producer_thread = threading.Thread(target=self.doall2)
        else:
            sys.exit()

        self.shared_queue.put(self.producer_thread)
        return self.shared_queue

    class ClearNotebooksScraperNW(ClearNotebooksScraper):
        def __init__(self, name, cmd):
            super().__init__(name)
            self.cmd = cmd

        def __enter__(self):
            print(">> STDIO REDIRECT\n")
            self._original_stdout = sys.stdout
            sys.stdout = self.cmd
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            tmp_stdio_handER = sys.stdout.close
            sys.stdout = self._original_stdout
            print(">> STDIO EXIT\n")
            tmp_stdio_handER()

    class ClearUsrScraperNW(ClearUsrScraper):
        def __init__(self, name, cmd):
            super().__init__(name)
            self.cmd = cmd

        def __enter__(self):
            print(">> STDIO REDIRECT\n")
            self._original_stdout = sys.stdout
            sys.stdout = self.cmd
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            tmp_stdio_handER = sys.stdout.close
            sys.stdout = self._original_stdout
            print(">> STDIO EXIT\n")
            tmp_stdio_handER()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Embedded Browser")

        # Create a container widget and layout
        container = QWidget()
        layout = QHBoxLayout(container)

        # Create a QWebEngineView instance
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        # Create a QTextEdit instance for the text box
        self.textbox = QTextEdit()
        self.textbox.setAcceptRichText(True)
        self.textbox.setLineWrapMode(QTextEdit.WidgetWidth)
        layout.addWidget(self.textbox)

        # Connect the titleChanged signal to the handle_title_changed slot
        self.browser.titleChanged.connect(self.handle_title_changed)

        # Load the HTML string
        file_path = 'gui.html'
        file_contents = read_file_to_string(file_path)
        self.browser.setHtml(file_contents)

        self.setCentralWidget(container)
        self.write_("Wait... The page is loading. Please check your internet connection if the content doesn't appear.")

    def write_(self, text):
        cursor = self.textbox.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textbox.setTextCursor(cursor)
        self.textbox.insertPlainText(text)

    def handle_title_changed(self, string):
        if '?' in string:
            split_rst = string.split('?')
            print("In front of '?' is:", split_rst[0])
            print("After '?' is:", split_rst[1])
            if split_rst[0] == '1':
                self.worker_thread = WorkerThread(split_rst[1], 1)
                self.worker_thread.update_text.connect(self.write_)
                self.worker_thread.runit().get().start()
            elif split_rst[0] == '2':
                self.worker_thread = WorkerThread(split_rst[1], 2)
                self.worker_thread.update_text.connect(self.write_)
                self.worker_thread.runit().get().start()
            else:
                print("inter error!")
        else:
            print("No '?' in the string.")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

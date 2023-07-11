#from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
#from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from download_notebook import ClearNotebooksScraper
import sys
import threading

html_string = """
<!DOCTYPE html>
<html>
<head>
  <title>Button and Input Example</title>
  <script>
    function setTitleOne() {
      var inputString = document.getElementById("inputBox").value;
      document.title = "1?" + inputString;
    }
    
    function setTitleTwo() {
      var inputString = document.getElementById("inputBox").value;
      document.title = "2?" + inputString;
    }
  </script>
</head>
<body>
  <input type="text" id="inputBox">
  <br><br>
  <button onclick="setTitleOne()">Set Title 1</button>
  <button onclick="setTitleTwo()">Set Title 2</button>
</body>
</html>

"""

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
        self.browser.setHtml(html_string)

        self.setCentralWidget(container)
        self.cmd=self.Cmd_(self.textbox)

    class ClearNotebooksScraperNW(ClearNotebooksScraper):
        def __init__(self, name, cmd):
            super().__init__(name)
            self.cmd = cmd

        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = self.cmd  # Redirect stdout to the QTextEdit widget
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout  # Restore the original stdout

    def handle_title_changed(self, string):
        if '?' in string:
            split_rst = string.split('?')
            print("In front of '?' is:", split_rst[0])
            print("After '?' is:", split_rst[1])
            with self.ClearNotebooksScraperNW(split_rst[1],self.cmd) as runme:
                runme.scrape_clear_notebooks()
        else:
            print("No '?' in the string.")

    class Cmd_:
        def __init__(self,tb_obj):
            self.master=tb_obj

        def write(self, text):
            self.master.moveCursor(1)  # Move the cursor to the end
            self.master.insertPlainText(text)  # Insert the text into the QTextEdit

        def close(self):
            self.master.moveCursor(1)  # Move the cursor to the end
            self.master.insertPlainText(f'[GUI CMD INFO] STDOUT CLOSE {{EOF}}')  # Insert the text into the QTextEdit


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

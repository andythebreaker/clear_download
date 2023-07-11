#from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
#from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

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

    def handle_title_changed(self, string):
        if '?' in string:
            split_rst = string.split('?')
            print("In front of '?' is:", split_rst[0])
            print("After '?' is:", split_rst[1])
        else:
            print("No '?' in the string.")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

#from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
#from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QLabel
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from download_notebook_pic import ClearNotebooksScraper
import sys
import threading
import queue
import time



html_string = """
<!DOCTYPE html>
<html>

<head>
    <title>Button and Input Example</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css">
    <style>
        body {
            overflow: hidden;
        }

        .container {
            display: flex;
            flex-direction: column;
            height: 100vh;
            width: 100vw;
            background-color: #87c8ff;
        }

        .container.inner {
            align-items: center;
            justify-content: center;
            background-color: #FFC0CB;
            margin: 1vh 1vw;
            padding: 3vh 3vw;
            border-radius: 10px;
        }
    </style>
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
    <div class="container">
        <div class="ui container inner">
            <div class="ui grid">
                <div class="row">
                    <div class="sixteen wide column">
                        <div class="ui segment">
                            <div class="ui blue ribbon label">CLEAR 筆記下載軟體 (非官方)</div>
                            <div class="ui basic segment">
                                請於下方欄位輸入「筆記ID或使用者ID」，並按下「下載」按鈕
                                <div class="ui divider"></div>
                                若輸入筆記ID，請按下「下載筆記」
                                <div class="ui divider"></div>
                                若輸入用戶ID，請按下「下載用戶」
                            </div>

                        </div>

                        <div class="ui two column grid">
                            <div class="column">
                                <div class="ui olive card">
                                    <div class="content">
                                        <div class="ui input fluid">
                                            <input type="text" id="inputBox" placeholder="ID...">
                                        </div>
                                    </div>
                                    <div class="extra content">
                                        <span class="left floated">
                                            <button class="ui labeled icon button" onclick="setTitleOne()">
                                                <i class="download icon"></i>
                                                筆記</button>
                                        </span>
                                        <span class="right floated">
                                            <button class="ui right labeled icon button" onclick="setTitleTwo()">
                                                <i class="cloud download icon"></i>
                                                用戶</button>
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div class="column">
                                <div class="ui teal card">
                                    <div class="content">
                                        右方區塊顯示下載進度
                                    </div>
                                    <div class="extra content">

                                        <div class="right floated author">
                                            <i class="hand point right outline icon"></i> LOOK that way!
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>



                    </div>
                </div>
                <div class="row">
                    <div class="eight wide column">
                        <h4 class="ui horizontal divider header">
                            <i class="tag icon"></i>
                            Description
                        </h4>
                        <div class="ui list">
                            <div class="item">
                                <i class="download icon"></i>
                                <div class="content">
                                    下載筆記:下載該本公開筆記
                                </div>
                            </div>
                            <div class="item">
                                <i class="cloud download icon"></i>
                                <div class="content">
                                    下載用戶:將下載他/她的所有公開筆記
                                </div>
                            </div>
                            <div class="item">
                                <i class="bullhorn icon"></i>
                                <div class="content">
                                    提醒:建議使用網頁版CLEAR查看ID
                                </div>
                            </div>
                            <div class="item">
                                <i class="address card icon"></i>
                                <div class="content">
                                    用戶ID如 「公開筆記頁面」 URL : <a>https://www.clearnotebooks.com/zh-TW/authors/用戶識別號碼/explorer/notebooks</a>
                                </div>
                            </div>
                            <div class="item">
                                <i class="book icon"></i>
                                <div class="content">
                                    筆記ID如 「網頁版筆記」 URL : <a>https://www.clearnotebooks.com/zh-TW/notebooks/筆記識別號碼</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="eight wide column">
                        <div class="ui vertical steps">
                            <div class="completed step">
                                <i class="truck icon"></i>
                                <div class="content">
                                    <div class="title">下載完成了嗎?</div>
                                    <div class="description">若您看到EOF字樣，表示下載完成</div>
                                </div>
                            </div>
                            <div class="active step">
                                <i class="eye icon"></i>
                                <div class="content">
                                    <div class="title">看這邊</div>
                                    <div class="description">右方</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>
</body>

</html>

"""

class WorkerThread(QThread):
    update_text = pyqtSignal(str)

    def __init__(self,split_rst_SQBRKT_1_SQBRKT):
        super().__init__()
        self.nbid=split_rst_SQBRKT_1_SQBRKT
        self.shared_queue = queue.Queue()
        self.producer_thread = threading.Thread(target=self.doall)
        self.shared_queue.put(self.producer_thread)
        
    def write(self,tx):
        self.update_text.emit(tx)
    
    def close(self):
        self.update_text.emit("$EOF$")
        self.quit()

    def doall(self):
        with self.ClearNotebooksScraperNW(self.nbid,self) as runme:
            runme.scrape_clear_notebooks()

    def runit(self):
        #producer_thread = threading.Thread(target=producer)
        return self.shared_queue
    
    class ClearNotebooksScraperNW(ClearNotebooksScraper):
        def __init__(self, name, cmd):
            super().__init__(name)
            self.cmd = cmd

        def __enter__(self):
            print(">> STDIO REDRIECT\n")
            self._original_stdout = sys.stdout
            sys.stdout = self.cmd  # Redirect stdout to the QTextEdit widget
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            #sys.stdout.close()
            tmp_stdio_handER=sys.stdout.close
            sys.stdout = self._original_stdout  # Restore the original stdout
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
        self.browser.setHtml(html_string)

        self.setCentralWidget(container)
        self.write_("Wait... The page is loading. Please check your internet connection if the content doesn't appear.")

    def write_(self, text):
        cursor = self.textbox.textCursor()
        cursor.movePosition(QTextCursor.End)  # Move the cursor to the end
        self.textbox.setTextCursor(cursor)  # Set the updated cursor position
        self.textbox.insertPlainText(text)  # Insert the text into the QTextEdit

    def handle_title_changed(self, string):
         if '?' in string:
            split_rst = string.split('?')
            print("In front of '?' is:", split_rst[0])
            print("After '?' is:", split_rst[1])
            self.worker_thread = WorkerThread(split_rst[1])
            self.worker_thread.update_text.connect(self.write_)
            self.worker_thread.runit().get().start()
            #self.worker_thread.runit().get().join()
         else:
             print("No '?' in the string.")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


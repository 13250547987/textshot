"""
历史记录侧边窗：保存最近 N 条 OCR 文本
"""
from collections import deque
from PyQt5.QtWidgets import QMainWindow, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pyperclip
from .result_dialog import ResultDialog

MAX_HISTORY = 20


class HistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR 历史")
        self.resize(300, 400)
        self.list_widget = QListWidget()
        self.setCentralWidget(self.list_widget)
        self.history = deque(maxlen=MAX_HISTORY)    # 左边索引 0 是最新

        # 双击查看
        self.list_widget.itemDoubleClicked.connect(self.open_record)

        # 美化
        font = QFont()
        font.setPointSize(10)
        self.list_widget.setFont(font)

    # ------ 对外接口 ------
    def add_record(self, text: str):
        self.history.appendleft(text)
        self.refresh_ui()

    # ------ 私有 ------
    def refresh_ui(self):
        self.list_widget.clear()
        for idx, t in enumerate(self.history):
            preview = (t[:40] + "…") if len(t) > 40 else t
            self.list_widget.addItem(f"{idx + 1}. {preview}")

    def open_record(self, item: QListWidgetItem):
        idx = int(item.text().split(".")[0]) - 1
        full_text = self.history[idx]
        pyperclip.copy(full_text)
        dlg = ResultDialog(full_text, self.add_record, self)
        dlg.exec()

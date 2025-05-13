"""
结果弹窗：显示 OCR 文本 + 复制 / 翻译 / 朗读
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTextEdit,
                             QPushButton, QHBoxLayout, QMessageBox, QApplication)
from PyQt5.QtCore import Qt
import pyperclip
from googletrans import Translator
import pyttsx3


class ResultDialog(QDialog):
    def __init__(self, text: str, history_cb, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TextShot – OCR 结果")
        self.resize(500, 340)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.text = text
        self.history_cb = history_cb      # 回调：写入历史

        # ========= UI =========
        edit = QTextEdit(readOnly=True)
        edit.setPlainText(text)

        btn_copy = QPushButton("复制")
        btn_copy.clicked.connect(self.copy_text)

        btn_translate = QPushButton("翻译")
        btn_translate.clicked.connect(self.translate_text)

        btn_speak = QPushButton("朗读")
        btn_speak.clicked.connect(self.speak_text)

        h = QHBoxLayout()
        for b in (btn_copy, btn_translate, btn_speak):
            h.addWidget(b)
        h.addStretch()

        v = QVBoxLayout(self)
        v.addWidget(edit)
        v.addLayout(h)

        # 首次打开即写入历史
        self.history_cb(text)

    # ---------- 功能 ----------
    def copy_text(self):
        pyperclip.copy(self.text)

    def translate_text(self):
        try:
            res = Translator().translate(self.text, dest="zh-cn").text
            QMessageBox.information(self, "翻译结果", res)
        except Exception as e:
            QMessageBox.warning(self, "翻译失败", str(e))

    def speak_text(self):
        try:
            engine = pyttsx3.init()
            engine.say(self.text)
            engine.runAndWait()
        except Exception as e:
            QMessageBox.warning(self, "朗读失败", str(e))

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, \
        QPushButton, QProgressBar, QTextEdit, QHBoxLayout, QVBoxLayout, QFileDialog

from PyQt5.QtCore import Qt

from upload import Upload

class Window(QWidget):
     
    def __init__(self):

        super().__init__()
        self.initUI()
         
    def uploadHandle(self):
        ak = self.ak_edit.text()
        sk = self.sk_edit.text()
        bk = self.bucket_edit.text()
        dr = self.dir_edit.text()

        if "" in (ak, sk, bk, dr):
            self.info_edit.append("More information is required")
        else:
            self.upload_btn.setEnabled(False)
            self.reset_btn.setEnabled(False)


            self.up = Upload(ak, sk, bk, dr, self.file_list)

            self.up.signal.connect(self.progressHandle)
            self.up.start()


    def progressHandle(self, info):

        if info[0] == 0:
            self.all_bar.setValue(info[1])
            self.info_edit.append("Uploading %s."%info[2])
        elif info[0] == 1:
            self.all_bar.setValue(info[1])
            self.info_edit.append("Completed!")
            self.file_list = []
            self.reset_btn.setEnabled(True)
        else:
            self.info_edit.append("Error happened with file %s."%info[2])


    def resetHandle(self):
        # self.ak_edit.clear()
        # self.sk_edit.clear()
        self.bucket_edit.clear()
        self.dir_edit.clear()

        self.all_bar.setValue(0)
        self.info_edit.clear()
        self.upload_btn.setEnabled(True)

    def selectDirHandle(self):
        dirname= QFileDialog.getExistingDirectory(self,directory=os.getcwd());

        self.dir_edit.setText(dirname)

        self.file_list = []

        for root, dirs, files in os.walk(dirname):
            for file in files:
                file_path = os.path.join(root, file)
                self.file_list.append(file_path)

        self.info_edit.append("All %d file(s) is Ready. \nClick 'Upload' to continue."%len(self.file_list))

    def initUI(self):
        
        grid = QGridLayout()

        ak_label = QLabel('AK')
        self.ak_edit = QLineEdit()
        self.ak_edit.setPlaceholderText("Your AK in Qiniu")

        grid.addWidget(ak_label, 1, 0)
        grid.addWidget(self.ak_edit, 1, 1, 1, 2)


        sk_label = QLabel('SK')
        self.sk_edit = QLineEdit()
        self.sk_edit.setPlaceholderText("Your SK in Qiniu")

        grid.addWidget(sk_label, 2, 0)
        grid.addWidget(self.sk_edit, 2, 1, 1, 2)


        bucket_label = QLabel('Bucket')
        self.bucket_edit = QLineEdit()
        self.bucket_edit.setPlaceholderText("Your Bucket in Qiniu")

        grid.addWidget(bucket_label, 3, 0)
        grid.addWidget(self.bucket_edit, 3, 1, 1, 2)


        dir_label = QLabel('Dir')
        self.dir_edit = QLineEdit()

        self.dir_edit.setPlaceholderText("The dir you want to upload")
        self.dir_edit.setFocusPolicy(Qt.NoFocus)

        select_btn = QPushButton("Select")
        select_btn.clicked.connect(self.selectDirHandle)

        grid.addWidget(dir_label, 4, 0)
        grid.addWidget(self.dir_edit, 4, 1)
        grid.addWidget(select_btn, 4, 2)


        all_label = QLabel('Progress')
        self.all_bar = QProgressBar()
        self.all_bar.setValue(0)

        grid.addWidget(all_label, 5, 0)
        grid.addWidget(self.all_bar, 5, 1, 1, 2)


        self.info_edit = QTextEdit()
        self.info_edit.setFocusPolicy(Qt.NoFocus)
        grid.addWidget(self.info_edit, 7, 0, 5, 3)


        self.upload_btn = QPushButton("Upload")
        self.reset_btn = QPushButton("Reset")

        self.upload_btn.clicked.connect(self.uploadHandle)
        self.reset_btn.clicked.connect(self.resetHandle)
 
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.upload_btn)
        hbox.addWidget(self.reset_btn)


        vbox = QVBoxLayout()

        vbox.addLayout(grid)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
         
        self.setLayout(vbox)    
         
        self.setGeometry(300, 300, 250, 300)
        self.setWindowTitle('Upload to Qiniu')   
        self.show()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
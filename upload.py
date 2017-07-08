import os

from qiniu import Auth, put_file
from PyQt5.QtCore import QThread, pyqtSignal

class Upload(QThread):
	signal = pyqtSignal(list)
	def __init__(self, ak, sk, bucket, dirname, file_list):
		self.ak = ak
		self.sk = sk
		self.bucket = bucket
		self.dr = dirname
		self.flist = file_list
		super(Upload, self).__init__()

	def run(self):

		length = len(self.flist)
		q = Auth(self.ak, self.sk)

		for i in range(length):
			file = self.flist[i]
			key = self.flist[i][len(self.dr)+1:].replace("\\","/")

			precent = i / length * 100

			token = q.upload_token(self.bucket, key, 600)

			self.signal.emit([0, precent, key])
			try:
				put_file(token, key, file)
				print(precent, key)
			except Exception as e:

				self.signal.emit([2, precent, key])
				return
		self.signal.emit([1, 100, key])
			

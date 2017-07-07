import os

from qiniu import Auth, put_file

class Upload(object):
	def __init__(self, ak, sk, bucket):
		self.ak = ak
		self.sk = sk
		self.bucket = bucket

	def up_file(self, dirname, file_list, callback):

		length = len(file_list)
		q = Auth(self.ak, self.sk)

		for i in range(length):
			file = file_list[i]
			key = file_list[i][len(dirname)+1:].replace("\\","/")

			token = q.upload_token(self.bucket, key, 600)

			try:
				put_file(token, key, file)
			except Exception as e:
				callback(i, file, info="failed!")
				return
			callback(i, key)
			

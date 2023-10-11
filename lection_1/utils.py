import socket
import shutil
import os

class Server:
	def __init__(self):
		self.server_name = socket.gethostname()

	def get_disk_space(self):
		return shutil.disc_usage('C:')
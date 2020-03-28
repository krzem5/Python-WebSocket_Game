from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, HTTPServer
from os import fstat as Fstat, getcwd as Getcwd
from os.path import isdir as Isdir, join as Join, exists as Exsists
from threading import Thread
from urllib import parse as Parse



class GameHTTPServer(SimpleHTTPRequestHandler):
	server_version="HTTP/1.3"
	protocol_version="HTTP/1.0"
	def send_head(self):
		path=self.translate_path(self.path)
		f=None
		#######################################EXTRA CODE#######################################
		path=Getcwd()+"\\web"+path.replace(Getcwd(),"")
		#######################################EXTRA CODE#######################################
		if Isdir(path):
			parts=Parse.urlsplit(self.path)
			if not parts.path.endswith('/'):
				self.send_response(HTTPStatus.MOVED_PERMANENTLY)
				new_parts=(parts[0],parts[1],parts[2]+'/',parts[3],parts[4])
				new_url=Parse.urlunsplit(new_parts)
				self.send_header("Location",new_url)
				self.end_headers()
				return None
			for index in "index.html","index.htm":
				index=Join(path,index)
				if Exsists(index):
					path=index
					break
			else:
				return self.list_directory(path)
		ctype=self.guess_type(path)
		try:
			f=open(path,'rb')
		except OSError:
			self.send_error(HTTPStatus.NOT_FOUND,"File not found")
			return None
		try:
			self.send_response(HTTPStatus.OK)
			self.send_header("Content-type",ctype)
			fs=Fstat(f.fileno())
			self.send_header("Content-Length",str(fs[6]))
			self.send_header("Last-Modified",self.date_time_string(fs.st_mtime))
			self.end_headers()
			return f
		except:
			f.close()
			raise



class ConsoleHTTPServer(SimpleHTTPRequestHandler):
	server_version="HTTP/1.3"
	protocol_version="HTTP/1.0"
	def send_head(self):
		path=self.translate_path(self.path)
		f=None
		#######################################EXTRA CODE#######################################
		if (path.replace(Getcwd(),"")!="\\web\\icon\\apple-icon-console.png"):
			path=Getcwd()+"\\console.html"
		else:
			path=Getcwd()+"/web/icon/apple-icon-console.png"
		#######################################EXTRA CODE#######################################
		if Isdir(path):
			parts=Parse.urlsplit(self.path)
			if not parts.path.endswith('/'):
				self.send_response(HTTPStatus.MOVED_PERMANENTLY)
				new_parts=(parts[0],parts[1],parts[2]+'/',parts[3],parts[4])
				new_url=Parse.urlunsplit(new_parts)
				self.send_header("Location",new_url)
				self.end_headers()
				return None
			for index in "index.html","index.htm":
				index=Join(path,index)
				if Exsists(index):
					path=index
					break
			else:
				return self.list_directory(path)
		ctype=self.guess_type(path)
		try:
			f=open(path,'rb')
		except OSError:
			self.send_error(HTTPStatus.NOT_FOUND,"File not found")
			return None
		try:
			self.send_response(HTTPStatus.OK)
			self.send_header("Content-type",ctype)
			fs=Fstat(f.fileno())
			self.send_header("Content-Length",str(fs[6]))
			self.send_header("Last-Modified",self.date_time_string(fs.st_mtime))
			self.end_headers()
			return f
		except:
			f.close()
			raise



# Normal Server
def start_normal_server():
	address=("192.168.178.65",8000)
	with HTTPServer(address,GameHTTPServer) as httpd:
		print("HTTP server started on port 8000!")
		httpd.serve_forever()
# Console Server
def start_other_server():
	address=("192.168.178.65",8010)
	with HTTPServer(address,ConsoleHTTPServer) as httpd:
		print("HTTP server started on port 8010!")
		httpd.serve_forever()



thr=Thread(target=start_other_server,args=[],kwargs={})
thr.start()
start_normal_server()
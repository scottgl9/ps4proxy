#!/usr/bin/python
# a truly minimal HTTP proxy

import SocketServer
import SimpleHTTPServer
import urllib
import os.path

# example PS4 pkg URL:
#   http://gs2.ww.prod.dl.playstation.net/gs2/appkgo/prod/CUSA01237_00/1/f_d63c0f7c427548aec014619d5bfe27c2233412f0a34824f2270782a6518e589c/f/UP4525-CUSA01237_00-00APOTHEONFORPS4.pkg
#   The corresponding json file has the URL:
#   http://gs2.ww.prod.dl.playstation.net/gs2/appkgo/prod/CUSA01237_00/1/f_d63c0f7c427548aec014619d5bfe27c2233412f0a34824f2270782a6518e589c/f/UP4525-CUSA01237_00-00APOTHEONFORPS4.json
#   {"originalFileSize":577503232,"packageDigest":"E6D092F1EA83604C3DF36939E96E265A2458DBCD445F53DDE6CC9C001074E0B6","numberOfSplitFiles":1,"pieces":[{"url":"http://gs2.ww.prod.dl.playstation.net/gs2/appkgo/prod/CUSA01237_00/1/f_d63c0f7c427548aec014619d5bfe27c2233412f0a34824f2270782a6518e589c/f/UP4525-CUSA01237_00-00APOTHEONFORPS4.pkg","fileOffset":0,"fileSize":577503232,"hashValue":"360c40c0b5e486209986ac2dac52e6bf8bbeaa4e"}]}

PORT = 8080

class PS4Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def ishost(self, host):
	if host in self.path:
		return self.path
	return ''

    def handle_ps4_req(self):
	print "handle_ps4_req: " + self.path
	base_url = self.path.replace("http://", "")
	parts = base_url.split('/')
	filename = parts[8]
	pkgfile = filename.replace(".json", ".pkg")
	print(parts[4])
	print(parts[6])
	print(parts[8])
	if (os.path.exists(pkgfile)):
		print(pkgfile + " exists on PS4 proxy")

    def do_GET(self):
	if (self.ishost("gs2.ww.prod.dl.playstation.net")):
		self.handle_ps4_req()
        self.copyfile(urllib.urlopen(self.path), self.wfile)

httpd = SocketServer.ForkingTCPServer(('', PORT), PS4Proxy)
print "serving at port", PORT
httpd.serve_forever()

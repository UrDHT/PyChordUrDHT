"""

This file describes the Networking class and associated helper threads/objects
see: https://github.com/UrDHT/DevelopmentPlan/blob/master/Network.md



"""
import server
import myrequests as requests
import json
import util
from errors import *

class Networking(object):
	def __init__(self,ip,port):
		self.serverThread = server.getThread(ip,port)
		self.serverThread.start()

	def setup(self,logic,data):
		"""
		Lets the server know which LogicClass and DataClass to use
		"""
		server.setLinks(logic,data)

	def seek(self,remote,id):
		"""
		This function remotely calls seek on the remote node,
		asking it to run LogicComponent.seek() on id
		"""
		path = remote.addr+"api/v0/peer/"+"seek/%s" % id
		val = None
		try:
			r = requests.get(path)
			results = r.json()
			val = util.PeerInfo(results["id"],results["addr"],results["loc"])
		except Exception:
			raise DialFailed()
		return val

	def getPeers(self,remote):
		result = []
		try:
			r = requests.get(remote.addr+"api/v0/peer/getPeers/")
			#print(r.text)
			#print(r.text)
			#print(r.text)
			if len(r.json()) == 0:
				return []
			for p in r.json():
				newPeer = util.PeerInfo(p["id"],p["addr"],p["loc"])
				result.append(newPeer)
		except Exception:
			raise DialFailed()
		return result

	def notify(self,remote,origin):
		#print("SENDING NOTIFY",remote,origin)
		try:
			r = requests.post(remote.addr+"api/v0/peer/notify", data=str(origin))
			return r.status_code == requests.codes.ok
		except:
			return False

	def store(self,remote,id,data):
		#print("SENDING NOTIFY",remote,origin)
		try:
			r = requests.post(remote.addr+"api/v0/client/store/"+id, data=data)
			return r.status_code == requests.codes.ok
		except:
			return False


	def getIP(self,remote):
		ip = None
		try:
			r = requests.get(remote.addr+"api/v0/peer/getmyIP")
			ip = r.text
		except:
			raise DialFailed()
		return ip

	def ping(self,remote):
		try:
			r = requests.get(remote.addr+"api/v0/peer/ping")

			return r.status_code == requests.codes.ok
		except:
			return False

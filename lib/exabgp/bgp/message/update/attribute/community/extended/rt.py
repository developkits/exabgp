# encoding: utf-8
"""
rt.py

Created by Thomas Mangin on 2014-06-20.
Copyright (c) 2014-2014 Orange. All rights reserved.
Copyright (c) 2014-2014 Exa Networks. All rights reserved.
"""


import socket
from struct import pack,unpack

from exabgp.bgp.message.open.asn import ASN
from exabgp.bgp.message.update.attribute.community.extended import ExtendedCommunity


# ================================================================== RouteTarget


class RouteTarget (ExtendedCommunity):
	COMMUNITY_SUBTYPE = 0x02

	@property
	def la (self):
		return self.community[2:self.LIMIT]

	@property
	def ga (self):
		return self.community[self.LIMIT:8]


# ============================================================= RouteTargetASNIP


class RouteTargetASNIP (RouteTarget):
	COMMUNITY_TYPE = 0x00
	LIMIT = 4

	def __init__ (self,asn,ip,transitive,community=None):
		self.asn = asn
		self.ip = ip
		RouteTargetASNIP.__init__(community if community else pack('!BBH4s',self.COMMUNITY_TYPE|0x40 if transitive else self.COMMUNITY_TYPE,0x02,asn,socket.inet_pton(socket.AF_INET,self.ip)))

	def __str__ (self):
		return "target:%s:%d" % (self.asn,self.ip)

	def pack (self):
		return self.community

	@staticmethod
	def unpack(data):
		asn,ip = unpack('!H4s',data[2:8])
		return RouteTargetASNIP(ASN(asn),socket.inet_ntop(socket.AF_INET,ip),False,data[:8])

RouteTargetASNIP._known[chr(RouteTargetASNIP.COMMUNITY_TYPE)+chr(RouteTargetASNIP.COMMUNITY_SUBTYPE)] = RouteTargetASNIP


# ============================================================= RouteTargetIPASN


class RouteTargetIPASN (RouteTarget):
	COMMUNITY_TYPE = 0x01
	LIMIT = 6

	def __init__ (self,asn,ip,transitive,community=None):
		self.ip = ip
		self.asn = asn
		RouteTargetIPASN.__init__(community if community else pack('!BB4sH',self.COMMUNITY_TYPE|0x40 if transitive else self.COMMUNITY_TYPE,0x02,socket.inet_pton(socket.AF_INET,self.ip),self.asn))

	def __str__ (self):
		return "target:%s:%d" % (self.ip, self.asn)

	def pack (self):
		return self.community

	@staticmethod
	def unpack (data):
		ip,asn = unpack('!4sH',data[2:8])
		return RouteTargetIPASN(socket.inet_ntop(socket.AF_INET,ip),ASN(asn),False,data[:8])

RouteTargetIPASN._known[chr(RouteTargetIPASN.COMMUNITY_TYPE)+chr(RouteTargetIPASN.COMMUNITY_SUBTYPE)] = RouteTargetIPASN


# ======================================================== RouteTargetASN4Number


class RouteTargetASN4Number (RouteTarget):
	COMMUNITY_TYPE = 0x02
	LIMIT=6

	def __init__ (self,asn,number,transitive,community=None):
		self.asn = asn
		self.number = number
		RouteTargetASN4Number.__init__(community if community else pack('!BBLH',self.COMMUNITY_TYPE|0x40 if transitive else self.COMMUNITY_TYPE,0x02,self.asn,self.number))

	def __str__ (self):
		return "target:%s:%d" % (self.asn, self.number)

	def pack (self):
		return self.community

	@staticmethod
	def unpack (data):
		asn,number = unpack('!LH',data[2:8])
		return RouteTargetASN4Number(ASN(asn),number,False,data[:8])

RouteTargetASN4Number._known[chr(RouteTargetASN4Number.COMMUNITY_TYPE)+chr(RouteTargetASN4Number.COMMUNITY_SUBTYPE)] = RouteTargetASN4Number

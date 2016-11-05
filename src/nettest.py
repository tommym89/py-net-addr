#!/usr/bin/python
#
from com.mcneelat.pynetaddr import PyNetAddr

net1 = "10.124.0.20"
mask1 = "255.255.192.0"

netaddr1 = PyNetAddr(net1, mask1)

#print netaddr1.network
#print netaddr1.broadcast
#print netaddr1.cidr_mask

netaddr1.calc_full_mask(16)
print netaddr1.mask

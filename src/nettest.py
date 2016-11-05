#!/usr/bin/python
#
from com.mcneelat.pynetaddr import PyNetAddr

net1 = "10.124.0.20"
mask1 = "255.255.192.0"

netaddr1 = PyNetAddr(net1, mask1)

#print netaddr1.network
#print netaddr1.broadcast
#print netaddr1.cidr_mask

#netaddr1.calc_full_mask(16)
#print netaddr1.mask

subnets_list = [netaddr1, PyNetAddr("10.124.1.20", "255.255.0.0"),
        PyNetAddr("100.64.128.0", "255.255.254.0"), PyNetAddr("172.22.19.5", "255.255.255.128"),
        PyNetAddr("192.168.16.0", "255.255.255.0"), PyNetAddr("192.168.178.0", "255.255.255.0"),
        PyNetAddr("192.168.0.0", "255.255.0.0"), PyNetAddr("10.0.0.0", "255.128.0.0")]

summarized_subnets = PyNetAddr.summarize(subnets_list)
for sn in summarized_subnets:
    print "%s/%s" % (sn.network, sn.cidr_mask)

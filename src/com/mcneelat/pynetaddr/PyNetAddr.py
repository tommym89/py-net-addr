#!/usr/bin/python
#
from sys import exit
import re

class PyNetAddr(object):

    ip_re = r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'
    mask_values = [0, 128, 192, 224, 240, 248, 252, 254, 255]

    def __init__(self, address, mask):
        if not self.set_new(address, mask):
            raise ValueError('Invalid address or subnet mask!')

    def is_valid_addr(self, address):
        if re.search(PyNetAddr.ip_re, address):
            splitter = address.split('.')
            for i in range(0, len(splitter)):
                tmp_i = int(splitter[i])
                if i == 0 and tmp_i == 0:
                    return False
                if tmp_i < 0 or tmp_i > 255:
                    return False
            return True
        return False

    def is_valid_mask(self, mask):
        # TODO: check for next octet as <= current
        if re.search(PyNetAddr.ip_re, mask):
            splitter = mask.split('.')
            for tmp_s in splitter:
                tmp_i = int(tmp_s)
                if tmp_i not in PyNetAddr.mask_values:
                    return False
            self.calc_cidr_mask(mask)
            return True
        return False

    """ Network => address & mask """
    def calc_network(self):
        addr_splitter = self.address.split('.')
        mask_splitter = self.mask.split('.')
        network_arr = []
        for i in range(0, len(addr_splitter)):
            network_arr.append(str(int(addr_splitter[i]) & int(mask_splitter[i])))
        self.network = '.'.join(network_arr)
    
    def calc_broadcast(self):
        network_splitter = self.network.split('.')
        mask_splitter = self.mask.split('.')
        i = len(mask_splitter) - 1
        breaker = False
        while i >= 0 and not breaker:
            network_octet = format(int(str(bin(int(network_splitter[i])))[2:], 2), \
                    '{fill}{width}b'.format(width=8, fill=0))
            mask_octet = format(int(str(bin(int(mask_splitter[i])))[2:], 2), \
                    '{fill}{width}b'.format(width=8, fill=0))
            
            j = len(mask_octet) - 1
            tmp_octet = list(network_octet)
            while j >= 0:
                if mask_octet[j] == '0':
                    tmp_octet[j] = '1'
                elif mask_octet[j] == '1':
                    breaker = True
                    break
                j -= 1

            network_splitter[i] = str(int(''.join(tmp_octet), 2))
            i -= 1
        self.broadcast = '.'.join(network_splitter)

    def calc_cidr_mask(self, mask):
        mask_splitter = mask.split('.')
        self.cidr_mask = 0
        for i in range(0, len(mask_splitter)):
            mask_octet = format(int(str(bin(int(mask_splitter[i])))[2:], 2), \
                    '{fill}{width}b'.format(width=8, fill=0))
            self.cidr_mask += mask_octet.count('1')

    def calc_full_mask(self, cidr_mask):
        cidr_bits = '1'*cidr_mask + '0'*(32-cidr_mask)
        cidr_bits_arr = [ str(int(cidr_bits[:8], 2)), str(int(cidr_bits[8:16], 2)), \
                str(int(cidr_bits[16:24], 2)), str(int(cidr_bits[24:], 2)) ]
        self.mask = '.'.join(cidr_bits_arr)

    def within(self, network2):
        if self.network == network2.network:
            return True
        network1_splitter = self.network.split('.')
        mask1_splitter = self.mask.split('.')
        network2_splitter = network2.network.split('.')
        mask2_splitter = network2.mask.split('.')
        total1 = int(mask1_splitter[0]) + int(mask1_splitter[1]) \
                + int(mask1_splitter[2]) + int(mask1_splitter[3])
        total2 = int(mask2_splitter[0]) + int(mask2_splitter[1]) \
                + int(mask2_splitter[2]) + int(mask2_splitter[3])
        if total1 < total2:
            netaddr3 = PyNetAddr(network2.network, self.mask)
            print "Network 1 is: %s, network 2 with same subnet is: %s" % \
                    (self.network, netaddr3.network)
            if self.network == netaddr3.network:
                return True
        elif total2 < total1:
            netaddr3 = PyNetAddr(self.network, network2.mask)
            print "Network 2 is: %s, network 1 with same subnet is: %s" % \
                    (network2.network, netaddr3.network)
            if network2.network == netaddr3.network:
                return True
        return False

    def summarize(self):
        pass

    def set_new(self, address, mask):
        if self.is_valid_addr(address):
            self.address = address
        else:
            print "Error, invalid IP address!"
            return False
        if self.is_valid_mask(mask):
            self.mask = mask
        else:
            print "Error, invalid subnet mask!"
            return False
        self.calc_network()
        self.calc_broadcast()
        return True

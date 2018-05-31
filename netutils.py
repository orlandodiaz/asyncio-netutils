import requests
import socket
import re
import random
import textwrap
from get_mac_addresses import GetMacAddresses
import getpass


class NetUtils(object):

    @classmethod
    def get_external_ip(cls):
        try:
            resp = requests.get('https://api.ipify.org/')
        except Exception as ex:
            print(ex)
        else:
            return resp.text

    @classmethod
    def get_local_ip(cls):
        local_ip = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('10.255.255.255', 1))
            local_ip = s.getsockname()[0]
            s.close()
        except Exception as ex:
            print(ex)
        return local_ip

    @classmethod
    def get_mac_address(cls):
        from uuid import getnode
        mac = hex(getnode())  # returns an int (not in common hex format)

        # Returns value as  48-bit integer
        mac = ":".join(re.findall(r'\w{2}', mac[2:]))

        return mac

    @classmethod
    def search_mac_addresses(cls):
        """ Searches for local mac addresses along with their corresponding hostname and ip"""
        gm = GetMacAddresses()
        data = gm.run()
        return data

    @classmethod
    def get_host_name(cls):
        return

    @classmethod
    def get_dns_server(cls):
        """ Gets the configured DNS server for system"""
        pass

    # def get_ip_info(self, ip):
    #     ip = IPInfo(ip)

    def get_macs(cls):
        """ Gets local mac addresses from the local network"""


class IPInfo(object):
    """ Uses the MaxMind API, an api which provides for most whois ip websites """
    def __init__(self, ip):

        json = requests.get("https://ipinfo.io/{}".format(ip)).json()

        # Populate values
        self.city = json['city']
        self.country = json['country']
        self.ip = json['ip']
        self.loc = json['loc']
        self.postal = json['postal']
        self.region = json['region']

    def __str__(self):
        return textwrap.dedent(f"""
        IP: {self.ip}
        Location: {self.city}, {self.region} {self.postal}
        Country: {self.country}
        GeoCoord: {self.loc}
        """)

    @classmethod
    def get_username(cls):
        return getpass.getuser()



if __name__ == '__main__':
    pass
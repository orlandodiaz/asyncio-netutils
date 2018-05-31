import subprocess as sp
import asyncio
from asyncio.subprocess import PIPE
from log import log
import subprocess
import re
import pandas as pd


class GetMacAddresses(object):
    def __init__(self):
        pd.set_option('expand_frame_repr', False)
        self.data = None

    async def ping(self, address):
        """Uses the UNIX ping utility located in /sbin/ping to ping"""

        # This operation is blocking. Cant do async
        # cmd = sp.run(['ping','-c','1','-W','1', address], stdout=sp.PIPE)
        cmd = 'ping -c 1 -W 1 {}'.format(address)
        proc = await asyncio.create_subprocess_shell(cmd, stdin=None, stdout=PIPE, stderr=None)

        # print("Proc created: %s" % cmd)
        out = await proc.stdout.read()
        # print("Finish: %s" % cmd)
        log.info(out)
        return out

    async def ping_all_ranges(self):
        """Conrrently pings a range of local IP network addresses"""

        # Place tasks here
        tasks = []

        # Loop ip range from 0-50. Do do concurrently
        for i in range(0, 255):
            tasks.append(self.loop.create_task(self.ping('192.168.254.{}'.format(i))))

        for task in tasks:
            await asyncio.wait([task])

    def run_cmd(self, cmd):
        proc = subprocess.run(cmd, stdout=sp.PIPE, shell=True)
        return proc

    def parse_arp(self):
        proc = self.run_cmd('arp -a')

        # Get the output of command
        str_out = proc.stdout.decode('ascii')
        arp_res = str_out.split('\n')

        d = dict()
        for i, line in enumerate(arp_res):
            hostname = re.findall(r'[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z]{3,5}', line)
            mac_address = re.findall(r'[a-f0-9]{1,2}:[a-f0-9]{1,2}:[a-f0-9]{1,2}:[a-f0-9]{1,2}:[a-f0-9]{1,2}:[a-f0-9]{1,2}',
                              line)
            ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)

            if mac_address:
                # Intialize dictionaries for values
                d[i] = {}

                if mac_address:
                    d[i]['mac_address'] = mac_address[0]

                if hostname:
                    d[i]['hostname'] = hostname[0]
                if ip:
                    d[i]['ip'] = ip[0]
        return d

    def run(self):
        try:
            self.loop = asyncio.get_event_loop()
            self.loop.set_debug(1)
            self.loop.run_until_complete(self.ping_all_ranges())

            data = self.parse_arp()
        except Exception as ex:
            log.error(ex)
        else:

            self.loop.close()
            return data


if __name__ == '__main__':
    g = GetMacAddresses()

    loop = asyncio.get_event_loop()
    loop.set_debug(1)
    loop.run_until_complete(g.ping_all_ranges())

    data = g.parse_arp()

    print()
    df = pd.DataFrame.from_dict(data, orient='index')

    print(df)


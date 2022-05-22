#!/usr/bin/python

import sys
import subprocess

CFG_FILE = '/etc/sysconfig/network-scripts/setdefaultgw-tlinux'
CMD_TAG_START  = '# VDEVS FOR PSD START'
CMD_TAG_END  = '# VDEVS FOR PSD END'

if len(sys.argv) < 3:
    print 'Usage: {0} eth_name vlan1 vlan2 ...'.format(sys.argv[0])
    exit(1)

dev_name = sys.argv[1]

for idx, vlan_id in enumerate(sys.argv[2:]):
    v_dev = '.'.join((dev_name, vlan_id))
    subprocess.call(['ip', 'rule', 'del', 'fwmark', vlan_id, 'table', str(200 - idx)])
    subprocess.call(['ip', 'route', 'del', 'default', 'dev', v_dev, 'table', str(200 - idx)])
    subprocess.call(['ip', 'link', 'del', v_dev])

new_content = []
keep = True

for line in open(CFG_FILE, 'r').readlines():
        if CMD_TAG_START in line:
                keep = False
        if keep:
                new_content.append(line)
        if CMD_TAG_END in line:
                keep = True

of = open(CFG_FILE, 'w')
for line in new_content:
        of.write(line)
of.close()

subprocess.call(['service', 'network', 'restart'])

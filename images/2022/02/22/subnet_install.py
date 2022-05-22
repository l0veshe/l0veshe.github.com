#!/usr/bin/python

import sys
import subprocess

CFG_FILE = '/etc/sysconfig/network-scripts/setdefaultgw-tlinux'
CMD_TAG_START  = '# VDEVS FOR PSD START'
CMD_TAG_END  = '# VDEVS FOR PSD END'

if len(sys.argv) < 3:
    print 'Usage: {0} eth_name vlan1 ip1 mask1 gw1 vlan2 ip2 mask2 gw2 ...'.format(sys.argv[0])
    exit(1)

dev_name = sys.argv[1]

for line in open(CFG_FILE, 'r').readlines():
        if CMD_TAG_START in line:
                print 'Virtual dev for PSG is installed already, exit...'
                exit(2)

v_dev_cfg = sys.argv[2:]

of = open(CFG_FILE, 'a')
of.write(CMD_TAG_START)
of.write('\n')
for idx in range(len(v_dev_cfg) / 4):
    vlan_id = v_dev_cfg[idx * 4]
    ip = v_dev_cfg[idx * 4 + 1]
    mask = v_dev_cfg[idx * 4 + 2]
    gateway = v_dev_cfg[idx * 4 + 3]
    v_dev = '.'.join((dev_name, vlan_id))

    of.write(' '.join(['ip', 'link', 'add', 'link', dev_name, 'name', v_dev, 'type', 'vlan', 'id', vlan_id, '\n']))
    of.write(' '.join(['ip', 'addr', 'add', '/'.join((ip, mask)), 'dev', v_dev, '\n']))
    of.write(' '.join(['ip', 'link', 'set', 'dev', v_dev, 'up', '\n']))
    of.write(' '.join(['ip', 'route', 'add', 'default', 'via', gateway, 'dev', v_dev, 'table', str(200 - idx), '\n']))
    of.write(' '.join(['ip', 'rule', 'del', 'fwmark', vlan_id, 'table', str(200 - idx), '\n']))
    of.write(' '.join(['ip', 'rule', 'add', 'fwmark', vlan_id, 'table', str(200 - idx), '\n']))
of.write(CMD_TAG_END)
of.write('\n')
of.close()

subprocess.call(['service', 'network', 'restart'])

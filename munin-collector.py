#!/usr/bin/env python

"""Munin collector to OpenTSDB

Usage: munin-collector.py (options)

Options:
    -T --opentsdb-host <opentsdb host>      OpenTSDB host name or IP
    -P --opentsdb-port <opentsdb port>      OpenTSDB port
    -M --munin-nodes <munin nodes>          List of Munin nodes separated by comma.
                                            Example: server1:4949,server2:4949

"""

from __future__ import print_function
import sys
import time
from docopt import docopt
import socket

def collect(tsdb_host, tsdb_port, munin_nodes):
    tsdb_server = (tsdb_host, tsdb_port)

    try:
        tsdb_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tsdb_sock.connect(tsdb_server)
    except:
        print('Cannot connect to OpenTSDB server %s:%s' % (tsdb_host, tsdb_port))

    nodes = munin_nodes.split(',')
    for node in nodes:
        try:
            node_host, node_port = node.split(':')
        except:
            node_host = node
        try:
            node_port = int(node_port)
        except:
            node_port = 4949
        munin_server = (node_host, node_port)

        try:
            munin_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            munin_sock.connect(munin_server)
        except:
            print('Cannot connect to Munin node %s:%s' % (node_host, node_port))
        motd = munin_sock.recv(4096)
        munin_sock.send("list\n")
        data = munin_sock.recv(4096)
        metrics = data.split(' ')
        ts = int(time.time())
        for metric in metrics:
            munin_sock.send("fetch %s\n" % metric)
            data = ''
            while True:
                buff = munin_sock.recv(4096)
                data = "%s%s" % (data, buff)
                if data == '':
                    break;
                lines = data.split("\n");
                if len(lines) >= 2 and lines[-2] == '.' and lines[-1] == '':
                    break
            for line in lines:
                if line != '' and line != '.':
                    line = line.replace('.value ', ' ')
                    key, value = line.split(' ')
                    tags = ' host=%s' % node_host
                    command = "put munin.%s.%s %s %s%s\n" % (metric, key, ts, value, tags)
                    tsdb_sock.send(command)
                    #sys.stdout.write(command)
        munin_sock.close()

    tsdb_sock.close()


def main():
    tsdb_host = 'localhost'
    tsdb_port = 4242
    munin_nodes = 'localhost:4949'
    INTERVAL = 60

    args = docopt(__doc__)
    if (args['--opentsdb-host'] != None):
        tsdb_host = args['--opentsdb-host']
    if (args['--opentsdb-port'] != None):
        tsdb_port = int(args['--opentsdb-port'])
    if (args['--munin-nodes'] != None):
        munin_nodes = args['--munin-nodes']

    while True:
        collect(tsdb_host, tsdb_port, munin_nodes)
        time.sleep(INTERVAL)


if __name__ == '__main__':
    sys.exit(main())

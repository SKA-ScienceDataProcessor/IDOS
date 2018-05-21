"""
Spead TCP sender will

(1) ask the queue for a single host H and a single port P
(2) launch spead binary to send lots of "zeros" to H and P
"""

import argparse
import os
import os.path as osp
import subprocess
import time

from spead_send import _get_receiver_host

MB = 1024 ** 2
SPLITER = '+'

#spead2_send --buffer 11000000 --packet 8950 192.168.120.101 5001 --heaps 5000 --tcp
spead_cmd = '%s --buffer %d --packet %d %s %d --heaps %d --tcp'

def parse_args():
    parser = argparse.ArgumentParser(description='Run a TCP spead')
    parser.add_argument('--path', dest='path', help='Full path to spead tcp binaries',
                        default='/home/wu082/proj/spead2_rt/src/spead2_send', type=str)
    parser.add_argument('--buffer', dest='buffer', help='Socket buffer size in MB',
                        default=32, type=int)
    parser.add_argument('--heaps', dest='heaps', help='Number of data heaps to send',
                        default=500, type=int)
    parser.add_argument('--packet', dest='packet', help='Maximum packet size to send',
                        default=8950, type=int)

    args = parser.parse_args()
    if (not osp.exists(args.path)):
        print("Spead path not found: %s" % args.path)
        sys.exit(1)
    return args

if __name__ == '__main__':
    args = parse_args()
    hoststr = _get_receiver_host()
    if (len(hoststr.split()) > 1):
        d = hoststr.split()
        host = d[0]
        port = int(d[1])
    else:
        raise Exception("Invalid host string received: %s" % hoststr)

    cmd = spead_cmd % (args.path, MB * args.buffer, args.packet, host, port, args.heaps)
    print(cmd)
    start = time.time()
    # Run and wait until it finishes
    process = subprocess.Popen(cmd.split(),
                               close_fds=True,
                               #stdin=stdin,
                               #stdout=stdout,
                               stderr=subprocess.PIPE,
                               env=os.environ.copy())

    print('Waiting for this to complete: %s' % cmd)
    pstdout, pstderr = process.communicate()
    #if stdout != subprocess.PIPE:
    #    pstdout = b"<piped-out>"
    pcode = process.returncode
    end = time.time()

    if pcode == 0:
        print("SPEAD2 finished successfully", pstdout, pstderr)
    else:
        message = "SPEAD2 didn't finish successfully (exit code %d)" % (pcode,)
        print(message, pstdout, pstderr)
        raise Exception(message)

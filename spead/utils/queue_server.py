import sys, argparse, time, os, logging, signal
import os.path as osp
import bottle
from Queue import Queue, Empty

from bottle import route, request, get, static_file, template, redirect, \
 response, HTTPResponse

"""
A queue service that tracks SPEAD2 receivers events
"""

q = Queue()

NONE_IP = 'NULL'

LOG_FORMAT = "%(asctime)-15s - %(message)s"

logger = logging.getLogger(__name__)

def get_cmd_args():
    parser = argparse.ArgumentParser(description='Queue service')

    parser.add_argument('--log_dir', dest='log_dir', help='path to log files',
                        default=os.getcwd(), type=str)

    parser.add_argument('--port', dest='port', help='port',
                        default=8003, type=int)

    parser.add_argument('--run_name', dest='run_name', help='run name',
                        default=str(int(time.time() * 1e3 - 1e12)))

    args = parser.parse_args()
    return args

def get_client_ip():
    return request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')

@get('/get_receiver')
def get_receiver():
    try:
        recvr_ip = q.get_nowait()
        logger.info("Get receiver IP %s to sender %s" % (recvr_ip, get_client_ip()))
    except Empty as exp:
        recvr_ip = NONE_IP

    return recvr_ip

@get('/reg_receiver')
def register_receiver():
    recvr_ip = request.query.get('ip')
    if (recvr_ip is None or len(recvr_ip) == 0):
        response.status = 500
        return "IP not found"
    else:
        q.put_nowait(recvr_ip)
        logger.info("Register receiver IP %s from %s" % (recvr_ip, get_client_ip()))

@get('/clr_receiver')
def clear_receiver():
    with q.mutex:
        q.queue.clear()
        logger.info("Clear receiver IP")

if __name__ == '__main__':
    args = get_cmd_args()
    signal.signal(signal.SIGTERM, \
                    lambda x,y: os.kill(os.getpid(), signal.SIGINT))
    logfile = osp.join(args.log_dir, '%s.log' % args.run_name)
    logging.basicConfig(filename=logfile, level=logging.INFO, format=LOG_FORMAT)
    bottle.run(host='0.0.0.0', server='paste', port=args.port)

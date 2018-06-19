#
#    ICRAR - International Centre for Radio Astronomy Research
#    (c) UWA - The University of Western Australia, 2018
#    Copyright by UWA (in the framework of the ICRAR)
#
#    (c) Copyright 2018 CSIRO
#    Australia Telescope National Facility (ATNF)
#    Commonwealth Scientific and Industrial Research Organisation (CSIRO)
#    PO Box 76, Epping NSW 1710, Australia
#    atnf-enquiries@csiro.au
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#    MA 02111-1307  USA

import dlg
import os
import subprocess
from mpi4py import MPI

import six.moves.http_client as httplib

iperf_bin = '/home/wu082/downloads/iperf-2.0.11/src/iperf'

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    ip = dlg.utils.get_local_ip_addr()[1][0] # use infiniband over ip
    port = 6000 + rank
    ipstr = '%s+%d' % (ip, port)
    con = httplib.HTTPConnection('sdp-dfms.ddns.net', 8096)
    con.request('GET', '/reg_receiver?ip=%s' % (ipstr))

    cmd = '%s -s -p %d -w 512K' % (iperf_bin, port)
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

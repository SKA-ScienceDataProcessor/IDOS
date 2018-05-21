# -*- coding: utf-8 -*-
"""Make images using CASA."""

import numpy
import math
import shutil
import os
import time
from os.path import join
import json
import sys
sys.path.append("/BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/MPI")
import argparse

def fov_to_cellsize(fov, im_size):
    """Obatin cellsize from fov and image size."""
    r_max = numpy.sin(numpy.array(fov, numpy.double) / 2. * (numpy.pi / 180.))
    inc = r_max / (0.5 * numpy.array(im_size))
    cell = numpy.arcsin(inc) * ((180. * 3600.) / numpy.pi)
    return cell.tolist()


def casa_image(ms, rootname, data_column, imsize, fov, ra0, dec0,
               weighting, Nfacet, NID, w_planes=None):
    """Make an image using CASA.

    http://casa.nrao.edu/docs/CasaRef/imager-Module.html#x636-6490002.5
    """
    #if not os.path.isdir(os.path.dirname(rootname)):
    #    os.mkdir(os.path.dirname(rootname))

    cell = fov_to_cellsize(fov, imsize)  # arcsec

    print ('-' * 80)
    print ('+ Size     : %i pixels' % (imsize[0]))
    print ('+ FoV      : %.2f deg' % (fov[0]))
    print ('+ Cellsize : %.4f arcsec' % (cell[0]))
    print ('+ RA0      : %.4f deg' % (ra0))
    print ('+ Dec0     : %.4f deg' % (dec0))
    print ('-' * 80)
    
    # Nfacet is the number of facets   NID is the scatter ID (0 to Nfacet-1)
    #Nfacet = int(Nfacet)
    #NID = int(NID) 
    if (Nfacet>1):
       M=numpy.sqrt(Nfacet)                  # The number of scatter tasks must be M^2 
       if (M*M!=Nfacet):
          print ('No of facets not a square: '+str(Nfacet))
          exit
       #
       nx=int(numpy.mod(NID,M))                #  Convert from ID number to X, Y coordinate
       ny=int(numpy.floor(NID/M))
       #
       imsize[0]=int(imsize[0]/M)             # Image is now M^2 smaller
       imsize[1]=int(imsize[1]/M)
       dfov=fov[0]/M
       ra0=(ra0-fov[0]/2)+nx*dfov
       dec0=(dec0-fov[0]/2)+ny*dfov
       #cell = fov_to_cellsize(dfov, imsize)
       print ('+ Facet no %d (%d,%d) has RA/DEC %.3f,%0.3f' % (NID, nx,ny,ra0,dec0))
      
    im.open(ms, usescratch=False, compress=False)
    im.defineimage(nx=imsize[0], ny=imsize[1], cellx='%.12farcsec' % cell[0],
                   celly='%.12farcsec' % cell[1],
                   stokes='I', mode='mfs', step=1, spw=[-1], outframe='',
                   veltype='radio',
                   phasecenter=me.direction('J2000', '%.14fdeg' % ra0,
                                            '%.14fdeg' % dec0))
    # im.weight(type='natural')
    im.weight(type=weighting)
    if w_planes:
        im.setoptions(ftmachine='wproject', wprojplanes=w_planes,
                      gridfunction='SF', padding=1.2,
                      dopbgriddingcorrections=True, applypointingoffsets=False)
        print ('w-projection')
    else:
        im.setoptions(ftmachine='ft', gridfunction='SF', padding=1.2,
                      dopbgriddingcorrections=True, applypointingoffsets=False)

    dirty = rootname + '_facet{0}_dirty.img'.format(NID)
    # psf = rootname + '_psf.img'
    if data_column == 'DATA':
        # DATA column
        im.makeimage(image=dirty, type='observed', verbose=False)
    elif data_column == 'CORRECTED_DATA':
        # CORRECTED_DATA column
        im.makeimage(image=dirty, type='corrected', verbose=False)
    elif data_column == 'MODEL_DATA':
        # MODEL_DATA column
        im.makeimage(image=dirty, type='model', verbose=False)
    else:
        print ('ERROR: Unknown data column!')
        return
    im.close()
    ia.open(dirty)
    ia.tofits(rootname + '_facte{0}.fits'.format(NID), overwrite=True)
    ia.close()
    # ia.open(psf)
    # ia.tofits(rootname+'_psf.fits', overwrite=True)
    # ia.close()
    if os.path.isdir(dirty):
        shutil.rmtree(dirty)
    # if os.path.isdir(psf):
    #     shutil.rmtree(psf)


if __name__ == "__main__":

    ms_files = ms_file
    Nfacet = int(Nfacet)
    NID = int(NID)

    column = 'DATA'
    ms = ms_files
    if not os.path.isdir(ms):
       print ('WARNING: MS not found, skipping imaging. (%s)' % ms)
    root_name = os.path.splitext(ms)[0]
    print ('+ Imaging with CASA ... [ms=%s -> %s : %s]' % (ms, root_name,
                                                                  column))
    t0 = time.time()
    casa_image(ms, '{}'.format(root_name), column,
                    [512,512], [3,4],
                    201.36, -43.02,
                    "uniform", Nfacet, NID, 0)
    print ('*' * 80)
    print ('  - Finished imaging in %.3fs' % (time.time() - t0))
    print ('*' * 80)




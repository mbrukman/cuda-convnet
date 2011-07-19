#
#    Python utility module.
#    Copyright (C) 2011  Alex Krizhevsky
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import re
import cPickle
import os
import numpy as n
from math import sqrt

import gzip
import zipfile

VENDOR_ID_REGEX = re.compile('^vendor_id\s+: (\S+)')
GPU_LOCK_NO_SCRIPT = -2
GPU_LOCK_NO_LOCK = -1

try:
    import magic
    ms = magic.open(magic.MAGIC_NONE)
    ms.load()
except ImportError: # no magic module
    ms = None

def get_gpu_lock():
    import imp
    lock_script_path = '/u/murray/bin/gpu_lock.py'
    if os.path.exists(lock_script_path):
        locker = imp.load_source("", lock_script_path)
        return locker.obtain_lock_id()
    return GPU_LOCK_NO_SCRIPT

def pickle(filename, data, compress=False):
    if compress:
        fo = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
        fo.writestr('data', cPickle.dumps(data, -1))
    else:
        fo = open(filename, "wb")
        cPickle.dump(data, fo, protocol=cPickle.HIGHEST_PROTOCOL)
    fo.close()
    
def unpickle(filename):
    if ms is not None and ms.file(filename).startswith('gzip'):
        fo = gzip.open(filename, 'rb')
        dict = cPickle.load(fo)
    elif ms is not None and ms.file(filename).startswith('Zip'):
        fo = zipfile.ZipFile(filename, 'r', zipfile.ZIP_DEFLATED)
        dict = cPickle.loads(fo.read('data'))
    else:
        fo = open(filename, 'rb')
        dict = cPickle.load(fo)
    
    fo.close()
    return dict

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]

def is_intel_machine():
    f = open('/proc/cpuinfo')
    for line in f:
        m = VENDOR_ID_REGEX.match(line)
        if m:
            f.close()
            return m.group(1) == 'GenuineIntel'
    f.close()
    return False

def get_cpu():
    if is_intel_machine():
        return 'intel'
    return 'amd'


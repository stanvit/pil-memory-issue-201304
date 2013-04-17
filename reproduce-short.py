#!/usr/bin/env python

import gc
import resource

from PIL import Image

i = 0L

for x in xrange(1000):
    try:
        Image.open('bad.jpg').load()
    except IOError:
        pass
    i += 1
    if not i % 10:
        print("%i; RSS: %i; Obj: %i"%(i, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, len(gc.get_objects())))

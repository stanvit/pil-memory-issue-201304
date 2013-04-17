#!/usr/bin/env python

import gc
import resource
import sys

from PIL import Image

if len(sys.argv) < 2:
    print "Usage: %s <image_file> [[<report_steps>]\n" % sys.argv[0]
    sys.exit(1)

image_filename = sys.argv[1]
report_steps = int(sys.argv[2]) if len(sys.argv) > 2 else 10

i = 0L
last_rss = 0

while True:
    f = open(image_filename, 'rb')
    image = Image.open(f)
    try:
        image.load()
    except IOError:
        pass
    del(image)
    f.close()
    del(f)
    i += 1
    if i % report_steps:
        continue
    cur_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    gc.collect()
    obj_count = len(gc.get_objects())
    obj_bytes  = reduce(lambda l, obj: l + sys.getsizeof(obj),
            gc.get_objects(), 0)
    print("Step %5i; RSS: %.1fMb; (%.1fkb per iteration); %i objects (%.1fkb)"
        % (i, float(cur_rss)/1024**2,
        float(cur_rss - last_rss)/(report_steps*1024), obj_count,
        float(obj_bytes)/1024 ))
    last_rss = cur_rss

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import call

import time


if __name__ == '__main__':
    start = time.time()
    out = 0
    roundtrip = time.time() - start
    while out == 0:
        out = call(
            "./bin/instance-transmo run scripts/migrate-todx-with-transmo.py",
            shell=True
        )
        print 'Out: {0}'.format(str(out))
        working_time = time.time() - start
        seconds = working_time % 60
        minutes = working_time / 60 % 60
        hours = working_time / 3600
        print "\nProcessing time since started: %02d:%02d:%02d\n" % (hours, minutes, seconds)

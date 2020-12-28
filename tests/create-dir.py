#!/usr/bin/env python
import os
from tempfile import mkstemp

for i in range(10):

    fd, path = mkstemp(prefix='avatar-', suffix='.png')

    with os.fdopen(fd, 'w') as fp:
        fp.write('cool stuff\n')

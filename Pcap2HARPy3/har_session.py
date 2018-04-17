#!/usr/bin/env python3

import settings # Global variable module

class Session(object):
    def __init__(self, pcapreader):
        self.pcapreader = pcapreader
        print('har session init')

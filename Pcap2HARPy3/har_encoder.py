#!/usr/bin/env python3

import sys
import json

from har_session import Session

class HAREncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Session):
            return json.JSONEncoder.default(self, obj)

        result = {
            'log': {
                'version': '1.2',
                'creator': {
                    'name': 'PCAP2HARV3',
                    'version': '0.1'
                },
                #'entries': [str(x) for x in obj.tcpdict.values()]
                'entries': obj.entries
            }
        }

        return result

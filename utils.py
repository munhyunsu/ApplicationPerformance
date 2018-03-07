#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from xml.dom import minidom

def xml_pretty_export(src, dst, indent = '  '):
    """
    Re-create XML file with pretty
    """
    tree = ET.parse(src)
    root = tree.getroot()
    
    with open(dst, 'w') as f:
        xmlstr = minidom.parseString(ET.tostring(root))
        xmlstr = xmlstr.toprettyxml(indent = indent)
        f.write(xmlstr)

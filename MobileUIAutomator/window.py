import xml.etree.ElementTree as ET
import random
import re

tree = ET.parse('window_dump.xml')
root = tree.getroot()
size = 0
bounds = list()
for item in root.iter():
    size = size+1
#    if len(list(item)) == 0:
#        if item.get('clickable') == 'false':
#            print(item.attrib)
    if item.get('clickable') == 'true':
        bounds.append(item.get('bounds'))

print(size)
choose = random.choice(bounds)
print(choose)
axes = re.findall('\d+', choose)
print(axes)
print(random.randrange(int(axes[0]), int(axes[2])),
      random.randrange(int(axes[1]), int(axes[3])))


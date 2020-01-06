import os
from xml.etree.ElementTree import parse, Element

doc = parse('coverage.xml')
root = doc.getroot()
root[0][0].text = os.getcwd()
doc.write('coverage.xml')

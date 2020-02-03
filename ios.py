#!/usr/bin/python
import xml.etree.ElementTree as ET
import os.path

xml_file = "/Applications/Unity/PlaybackEngines/iOSSupport/ivy.xml"
current_version = '<VERSION>'

if os.path.exists(xml_file):
   tree = ET.parse(xml_file)
   root = tree.getroot()

   info = root.findall('info')

   version = info[0].get('{http://ant.apache.org/ivy/extra}unityVersion')

   if version != current_version:
      # version does not match
      exit(0)
   else:
      # version is okay
      exit(1)

else:
   # software not installed
   exit(0)

# https://github.com/munki/munki/wiki/How-Munki-Decides-What-Needs-To-Be-Installed
# exit code status of 0 means not installed, for install check script


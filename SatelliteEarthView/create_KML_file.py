#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement, division
import datetime
import sys
sys.path.append('../')
import sattrack


# This script creates a KML file for Google Earth.
#
# The variable path_to_tlefile should contain the path to a valid TLE file.
# The KML file will be saved to path_to_kmlfile.
#
# Change startdate and enddate to your needs. The format is UTC.
# The default startdate is now, default enddate is 24 hours later.

# Modify these variables
path_to_tlefile = '../misc/ISS.TLE'
path_to_kmlfile = 'ISS.KML'
startdate = datetime.datetime.utcnow()
enddate = startdate + datetime.timedelta(days=1)

# Create KML file
kml_file = sattrack.create_kml(path_to_tlefile, startdate, enddate)

# Save KML file
with open(path_to_kmlfile, 'w') as fp:
    fp.write(kml_file)

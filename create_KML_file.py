#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 15:19:31 2017

@author: anders
"""

from __future__ import print_function, with_statement, division
import datetime
import sattrack


# Set startdate and enddate
startdate = datetime.datetime.utcnow()
enddate = startdate + datetime.timedelta(days=1)

# Create KML file
kml_file = sattrack.create_kml('ISS.TLE', startdate, enddate)

# Save KML file
with open('iss_orbit.kml', 'w') as fp:
    fp.write(kml_file)
#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement, division
import numpy as np
import ephem
import datetime


def read_TLE(TLEFILE):
    '''
    Reads a TLE file and returns the three lines as strings.

    Input:
        TLEFILE: path to TLE file, str
    Output:
        name, str
        line1, str
        line2, str
    '''
    with open(TLEFILE, 'r') as fp:
        name = fp.readline().strip('\n').strip()
        line1 = fp.readline().strip('\n')
        line2 = fp.readline().strip('\n')
    return name, line1, line2


def create_kml(tlefile, startdate, enddate):
    '''
    Create a KML file with coordinates computed at 10 minute intervals
    from startdate to enddate.

    Input:
        TLE, ephem.EarthSatellite object
        startdate, datetime object
        enddate, datetime object

    Return:
        kml_file, str
    '''

    # Read and parse TLE file
    name, line1, line2 = read_TLE(tlefile)
    tle = ephem.readtle(name, line1, line2)

    # Aarhus coordinates
    Aarhus = ephem.Observer()
    Aarhus.lon = 10.203921
    Aarhus.lat = 56.162939

    # Compute coordinates
    ten_min = datetime.timedelta(minutes=1)
    indent = '                '
    whenwhere = ''
    date = startdate - ten_min
    while date < enddate:
        date += ten_min
        Aarhus.date = date
        tle.compute(Aarhus)

        lat_deg = np.degrees(tle.sublat)
        lon_deg = np.degrees(tle.sublong)
        elev = tle.elevation

        datestr = '<when>' + str(date.year) + '-' + str(date.month).zfill(2) + '-' + str(date.day).zfill(2) + 'T' +\
                  str(date.hour).zfill(2) + ':' + str(date.minute).zfill(2) + ':' + str(date.second).zfill(2) + 'Z</when>\n'
        coordstr = '<gx:coord>' + str(lon_deg) + ' ' + str(lat_deg) + ' ' + str(elev) + '</gx:coord>\n'
        whenwhere += indent + datestr + indent + coordstr

    kml_file =\
'''
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <name>Orbit</name>
    <snippet>Created by Anders Bo Justesen, Aarhus University</snippet>
    <Style id="multiTrack_n">
        <IconStyle>
            <Icon>
                <scale>1.5</scale>
                <href>../misc/gomspace_nanoeye_thumb.png</href>
            </Icon>
        </IconStyle>
        <LineStyle>
            <color>ff00ffff</color>
            <width>3</width>
        </LineStyle>
    </Style>
    <StyleMap id="multiTrack">
        <Pair>
            <key>normal</key>
            <styleUrl>#multiTrack_n</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#multiTrack_n</styleUrl>
        </Pair>
    </StyleMap>
    <Folder>
        <name>Coordinates</name>
        <Placemark>
            <name>Delphini-1</name>
            <styleUrl>#multiTrack</styleUrl>
            <gx:Track>
                <altitudeMode>absolute</altitudeMode>
%s
            </gx:Track>
        </Placemark>
    </Folder>
</Document>
</kml>
''' % whenwhere[:-1]
    return kml_file[1:]

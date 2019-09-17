#!/usr/bin/python
# -*- coding: utf-8 -*-

"""assignment3.py: IS 211 Assignment 3."""

__author__ = 'Adam Volin'
__email__ = 'Adam.Volin56@spsmail.cuny.edu'

import sys
import argparse
import datetime
import urllib2
import csv
import re
import operator


def downloadData(url):
    """Accepts a URL as a string and opens it.

    Parameters:
        url (string): the url to be opened

    Example:
        >>> downloadData(
            'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv')
    """

    return urllib2.urlopen(url)


def processData(data):
    """Processes data from the contents of a CSV file line by line.

    Parameters:
        data - the contents of the CSV file

    Example:
        >>> processData(downloadedData)
    """

    # Instantiate count dictionaries
    hits = { 'images': 0, 'total': 0 }
    browserHits = { 'Chrome': 0,
                    'Safari': 0,
                    'Firefox': 0,
                    'Internet Explorer': 0
                  }
    hourHits = { str(i): 0 for i in range(0, 24) }

    for (line, col) in enumerate(csv.reader(data)):
        # Update total hits count
        hits['total'] += 1

        # Search to see if hit was for image
        if re.search(r"\.(?:jpe?g|gif|png)$", col[0], re.I):
            hits['images'] += 1

        # Update hits count for hour of hit
        hourHits[str(datetime.datetime.strptime(col[1], '%Y-%m-%d %H:%M:%S').hour)] += 1
        
        # Search for browser to update browser count
        if re.search("chrome", col[2], re.I):
            browserHits['Chrome'] += 1
        elif re.search("safari", col[2], re.I) and not re.search("chrome", col[2], re.I):
            browserHits['Safari'] += 1
        elif re.search("firefox", col[2], re.I):
            browserHits['Firefox'] += 1
        elif re.search("msie", col[2], re.I):
            browserHits['Internet Explorer'] += 1
    
    # Calculate percent of hits that were for images of total hits
    image_hit_percent = round((float(hits['images']) / hits['total']) * 100, 2)
    top_browser = max(browserHits.iteritems(), key=operator.itemgetter(1))

    # Pad single-digit hourHits keys with zeros - helps with sorting
    for i in range (0, 10):
        hourHits['0' + str(i)] = hourHits.pop(str(i))

    # Print report
    print("Web Stats:")
    print("There were {} hits, of which {} were image requests accounting for {}% of all hits."
            .format(hits['total'], hits['images'], image_hit_percent))
    print("The most popular browser used was {} with {} hits."
            .format(top_browser[0], top_browser[1]))
    print("Hits per hour, sorted by most hits first are:")
    # Sort hourHits dict by most hits, then by hour for hours with equal hits
    for hour, hits in sorted(hourHits.items(), key=lambda hits: (hits[1],hits[0]), reverse=True):
        print("Hour {} has {} hits".format(hour, hits))

def main():
    """The function that runs when the program is executed."""

    # Setup --url argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--url',
                        help='The URL of the CSV file to download and parse.'
                        )
    args = parser.parse_args()

    # Check for URL argument
    if args.url:
        try:
            csvData = downloadData(args.url)
        except (urllib2.URLError, urllib2.HTTPError):
            print 'There was an error retrieving the data from the provided URL. Please try a different URL.'
            sys.exit()

        processData(csvData)
    else:
        print 'The --url parameter is required.'
        sys.exit()

if __name__ == '__main__':
    main()
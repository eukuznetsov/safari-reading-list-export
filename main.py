#!/usr/bin/env python3

import logging
import os
import plistlib
import sys
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
urls = []


def get_reading_list_node(node):
    children = node.get("Children", [])
    for child in children:
        if 'Title' in child.keys():
            if child['Title'] == 'com.apple.ReadingList':
                return child
            i = get_reading_list_node(child)
            if i is not None:
                return i
    return None


def print_reading_list_item(item):
    # date_filter = datetime.now() - timedelta(days=-180)
    row = []
    delimeter = "::::"
    row.append(item['URIDictionary']['title'])
    row.append(str(item['ReadingList']['DateAdded']))
    row.append(item['URLString'])
    # Domain
    row.append(urlparse(item['URLString']).netloc)
    print(delimeter.join(row))


def read_plist():
    filename = os.path.expanduser("~/Library/Safari/Bookmarks.plist")
    with open(filename, 'rb') as handler:
        plist = plistlib.load(handler)
        reading_list_node = get_reading_list_node(plist)
        for child in reading_list_node['Children']:
            print_reading_list_item(child)


def main():
    read_plist()


if __name__ == '__main__':
    sys.exit(main())

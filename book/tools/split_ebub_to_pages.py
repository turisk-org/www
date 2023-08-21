#!/usr/bin/python3

import sys
import os
import re

def save_page_file(page, lines):
    filename = "book/pages/p%03d.html" % page
    if os.path.isfile(filename):
        print("File %s already exists. Skipping." % filename)
        return

    if len(lines) == 0:
        print("Empty lines for file %s. Skipping." % filename)
        return

    with open(filename, 'w') as f:
        f.writelines(lines)

if len(sys.argv) < 2:
    print("usage: %s <epub html filename>")
    sys.exit(-1)

epub_filename = sys.argv[1]

if not os.path.isfile(epub_filename):
    print("file %s not found." % epub_filename)
    sys.exit(-1)

with open(epub_filename, 'r') as f:
    lines = f.readlines()

page_lines = []
for line in lines:
    if line.find("<span class=\"c22\">") >= 0:
        # Find the new page number.
        m = re.search(r'<span class=\"c22\">([0-9]+) *</span>', line)
        page = int(m.groups(0)[0])
        print("found page: %d" % page)

        # Save previous file.
        save_page_file(page, page_lines)

        # Reset page lines.
        page_lines = []
    else:
        page_lines.append(line)
        




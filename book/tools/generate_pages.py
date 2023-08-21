#!/usr/bin/python3

import os

def get_number_of_pages():
    for page in range(1, 500):
        filename = "book/pages/p%03d.html" % page
        if not os.path.isfile(filename):
            print("File %s doesn't exists. Assuming the number of pages is: %d" % (filename, page - 1))
            return page - 1

NUM_PAGES = get_number_of_pages()

# Read the header and footer as globals.
with open('book/header.html', 'r') as f:
    header_lines = f.readlines()

with open('book/footer.html', 'r') as f:
    footer_lines = f.readlines()



def page_filename(page):
    if page == 0:
        return "book.html"
    if page > NUM_PAGES:
        return "book_back.html"

    return  "book_p%03d.html" % page
    
def next_page_filename(page):
    if page < NUM_PAGES:
        return  "book_p%03d.html" % (page+1)
    else:
        return "book_back.html"
    
def prev_page_filename(page):
    if page > 1:
        return  "book_p%03d.html" % (page-1)
    else:
        return "book.html"
    
def replace_tags(lines, next_file, prev_file):
    for i in range(len(lines)):
        lines[i] = lines[i].replace("TAGTAG_NEXT_PAGE", next_file)
        lines[i] = lines[i].replace("TAGTAG_PREVIOUS_PAGE", prev_file)

def replace_image_path(lines):
    for i in range(len(lines)):
        lines[i] = lines[i].replace("images/", "book/images/")


def write_to_file(page_number, lines):
    global header_lines, footer_lines
    header_copy = header_lines.copy()
    replace_tags(header_copy, next_page_filename(page_number), prev_page_filename(page_number))

    footer_copy = footer_lines.copy()
    replace_tags(footer_copy, prev_page_filename(page_number), prev_page_filename(page_number))

    replace_image_path(lines)

    with open(page_filename(page_number), 'w') as f:
        f.writelines(header_copy)
        f.writelines(lines)
        f.writelines(footer_copy)


# Generate cover page.
with open('book/pages/front_cover.html', 'r') as f:
    page_lines = f.readlines()

write_to_file(0, page_lines)

    
for page in range(1, NUM_PAGES + 1):
    page_str = "%03d" % page

    # Read the page content.
    with open('book/pages/p%s.html' % page_str, 'r') as f:
        page_lines = f.readlines()

    next_page_str = "%03d" % page
    write_to_file(page, page_lines)


# Generate back cover page.
with open('book/pages/back_cover.html', 'r') as f:
    page_lines = f.readlines()
write_to_file(NUM_PAGES + 1, page_lines)

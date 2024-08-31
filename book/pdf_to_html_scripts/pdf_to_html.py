import sys
import pymupdf
import re

html_header = '''
    <!DOCTYPE html> 
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Vertical Line with Number</title>
    <style>
        .vertical-line {
            border-left: 2px solid black;
            height: 100px;
            position: relative;
        }

        .number {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
    </style>
</head>   
<body>
'''

html_footer = '''
</body></html>
'''

def reverse_numbers_in_string(input_string):
    def reverse_number(match):
        return match.group(0)[::-1]

        # Use regular expression to find and replace numbers

    pattern = r"\d+"  # Matches one or more digits
    result_string = re.sub(pattern, reverse_number, input_string)

    return result_string


def move_dot_and_comma_to_end(line):
    line = line.strip()
    if not line:
        return ''
    if line[-1] in ('.', ',', '?', ';', '!', '-'):
        end = line[-1]
        return end + line[:-1]
    return line

class Page:
    def __init__(self, number):
        self.number = number
        self.lines = []

    def get_html_content(self):
        output = []
        text_lines = []
        for line in self.lines:
            # print(char_height(line[0]))
            text = ''
            for c in line:
                text += c['c']
            text_lines.append(move_dot_and_comma_to_end(reverse_numbers_in_string(text)))

        for line in text_lines:
            output.append('<p>%s</p>' % line)

        return '\n'.join(output)


class Book:
    def __init__(self):
        self.pages = dict()

    def add_page(self, number, page):
        self.pages[number] = page

    def print_pages(self):
        page_numbers = sorted(self.pages.keys())
        for number in page_numbers:
            print('----------------------')
            print('      PAGE %d ' % number)
            print('----------------------')
            print(self.pages[number].get_html_content())



def pdf_to_book(doc, max_pages, only_specific_page=-1):
    book = Book()
    i = 0
    for page in doc:  # scan through the pages
        i += 1
        if only_specific_page >= 0 and only_specific_page != i:
            continue
        if only_specific_page < 0 and i > max_pages:
            break

        new_page = Page(i)
        book.add_page(i, new_page)

        raw_dict = page.get_textpage().extractRAWDICT()

        def bbox_center(bbox):
            return ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)

        def char_x(char):
            bbox = char['bbox']
            return (bbox[0] + bbox[2]) / 2

        def char_y(char):
            bbox = char['bbox']
            return (bbox[1] + bbox[3]) / 2

        def char_height(char):
            bbox = char['bbox']
            return abs(bbox[1] - bbox[3])

        chars = []
        all_lines = []
        blocks = raw_dict['blocks']
        for block in blocks:
            for line in block['lines']:
                for span in line['spans']:
                    for char in span['chars']:
                        chars.append(char)
                        found = False
                        for l in all_lines:
                            if abs(char_y(char) - char_y(l[0])) < 2:
                                l.append(char)
                                found = True
                        if not found:
                            all_lines.append([char])

        for line in all_lines:
            line.sort(key=lambda x: -char_x(x))

        new_page.lines = all_lines
    return book




fname = '/home/benami/Documents/turisk_book_test/book.pdf' # sys.argv[1]  # filename
max_pages = 30
only_specific_page = 26
book = pdf_to_book(pymupdf.open(fname), max_pages, only_specific_page)
book.print_pages()


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

    pattern = r"\d+,*\d+"  # Matches one or more digits
    result_string = re.sub(pattern, reverse_number, input_string)

    return result_string

def add_footnote_markers(line):
    # for i in range(1, len(line)):
    #     if line[i] == '#':
    #         print('>>>>>', line[i-1], line[i], line[i+1])
    return line

    # def add_marker(match):
    #     return '<sup>%s</sup>' % match.group(0)[0:]
    #
    #     # Use regular expression to find and replace numbers
    #
    # pattern = r"#\d"  # Matches one or more digits
    # result_string = re.sub(pattern, add_footnote_markers, input_string)
    #
    # return result_string


def move_dot_and_comma_to_end(line):
    line = line.strip()
    if not line:
        return ''
    if line[-1] in ('.', ',', '?', ';', '!', '-'):
        end = line[-1]
        return end + line[:-1]
    return line

def char_x(char):
    bbox = char['bbox']
    return (bbox[0] + bbox[2]) / 2

def char_y(char):
    bbox = char['bbox']
    return (bbox[1] + bbox[3]) / 2

def char_height(char):
    bbox = char['bbox']
    return abs(bbox[1] - bbox[3])

def line_height(line):
    if not line:
        return None
    return char_height(line[0])

def is_footnote_marker(char, line):
    if  line_height(line) > 10 and char_height(char)  < 10:
        return True
    return False

def is_footnote_line(line):
    if  line_height(line) < 12 and line_height(line) > 10:
        return True
    return False

def is_page_number_line(line):
    if line_height(line) == 10.0:
        return True
    return False

def is_header(line):
    # print(line_height(line), int(line_height(line)))
    return int(line_height(line)) > 20

def is_special_header_move_to_page_top(line):
    return int(line_height(line)*100) == 1585

line_heights = dict()


class Page:
    def __init__(self, number):
        self.number = number
        self.lines = []

    def verify_page_number_from_text(self):
        for line in self.lines:
            if is_page_number_line(line):
                text = ''
                for c in line:
                    text += c['c']
                number = int(text.strip()[::-1])
                if not number == self.number:
                    print('!!!!!!! Unexpected: actual number: %s for page: %s' % (number, self.number))
                    sys.exit(-1)


    def get_html_content(self):
        text_lines = []
        for line in self.lines:
            h = line_height(line)
            if not h in line_heights.keys():
                line_heights[h] = line


            if is_footnote_line(line):
                continue # Skip for now.

            if is_page_number_line(line):
                continue

            text = ''

            # Add line height for debug.
            # text += '[Line height: %f] ' % line_height(line)

            for c in line:
                # For now skip comments.
                if is_footnote_marker(c, line):
                    # text += '<sup>%s</sup>' % c['c']
                    #text += '#' + c['c']
                    pass # For now lets skip it.
                else:
                    text += c['c']

            corrected = move_dot_and_comma_to_end(add_footnote_markers(reverse_numbers_in_string(text)))

            if is_header(line):
                corrected = '<h1>%s</h1>' % corrected
            elif is_special_header_move_to_page_top(line):
                corrected = '<h2>%s</h2>' % corrected
            else:
                corrected = '<p>%s</p>' % corrected

            if is_special_header_move_to_page_top(line):
                text_lines.insert(0, corrected)
            else:
                text_lines.append(corrected)

        return '\n'.join(text_lines)


class Book:
    def __init__(self):
        self.pages = dict()

    def add_page(self, number, page):
        self.pages[number] = page

    def verify_page_numbers(self):
        for page in self.pages.values():
            page.verify_page_number_from_text()


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
max_pages = 100
only_specific_page = -1
book = pdf_to_book(pymupdf.open(fname), max_pages, only_specific_page)
book.verify_page_numbers()
book.print_pages()

print('Number of sizes:', len(line_heights))
for h in line_heights.keys():
    # print('-'*200)
    print(h, len(line_heights[h]))

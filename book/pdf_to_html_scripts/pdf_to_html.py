import sys
import pymupdf
import re

html_header = '''
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">
  <title>טריסק - היסטוריה</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
  <script src="https://use.fontawesome.com/releases/v6.1.0/js/all.js" crossorigin="anonymous"></script><!-- Google fonts-->
  <link href="https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800" rel=
  "stylesheet" type="text/css"><!-- Core theme CSS (includes Bootstrap)-->
  <link href="css/styles.css" rel="stylesheet">
  <style>
  .mapouter{position:relative;text-align:right;height:500px;width:600px;}
  </style>
  <style>
  .gmap_canvas {overflow:hidden;background:none!important;height:500px;width:600px;}
  </style>
</head>
<body>
  <div id="menu-container"></div> 

  <header class="masthead" style="background-image: url('assets/img/post-bg.jpg')">
    <div class="container position-relative px-4 px-lg-5">
      <div class="row gx-4 gx-lg-5 justify-content-center">
        <div class="col-md-10 col-lg-8 col-xl-7">
          <div class="post-heading">
            <h1>פנקס הקהילה</h1>
            <h2 class="subheading"></h2>
          </div>
        </div>
      </div>
    </div>
  </header><!-- Post Content-->
  <article class="mb-4">
    <div class="container px-4 px-lg-5">
      <div class="row gx-4 gx-lg-5 justify-content-center">
        <div class="col-md-10 col-lg-8 col-xl-7">
          <section id="book_page_">
	    <div class = "pt-5">
          <img src="assets/book_images/turisk_book_front_cover.jpg" class="w-100" alt="">



'''

html_footer = '''
          <img src="assets/book_images/turisk_book_back_cover.jpg" class="w-100" alt="">
	    </div>
          </section>
	</div>
      </div>
    </div>
  </article><!-- Bootstrap core JS-->
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script> 
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script> <!-- Core theme JS-->
   
  <script src="js/scripts.js" data-nav_bar_file="nav_bar_he.html"></script>
</body>
</html>
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

def bbox_center(bbox):
    return ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)

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

def get_image_file_path(page_number, image_number):
    return 'assets/book_images/page_%d_image_%d.jpg' % (page_number, image_number)

def get_image_html_tag(page_number, image_number):
    return '<img src="%s" class="w-100" alt="">' % get_image_file_path(page_number, image_number)

line_heights = dict()


class Page:
    def __init__(self, number):
        self.number = number
        self.lines = []
        self.image_locations = []

    def update_image_locations(self, pdf_page):
        images = pdf_page.get_images()
        for image in images:
            # b = page.get_image_bbox()
            bbox = pdf_page.get_image_bbox(image[7])
            self.image_locations.append(bbox.y1)
        self.image_locations.sort()

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
        next_image_id = -1
        if self.image_locations:
            next_image_id = 0
        # Skip images in hand selected pages.
        for p in [4]:
            if self.number == p:
                next_image_id = -1
        print('Number of images: %d' % len(self.image_locations))
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

            # Check if we need to add a link to the image.
            if next_image_id>= 0 and char_y(line[0]) > self.image_locations[next_image_id]:
                image_text = get_image_html_tag(self.number, next_image_id+1)
                text_lines.append(image_text)
                next_image_id += 1
                if next_image_id == len(self.image_locations):
                    next_image_id = -1


            if is_header(line):
                corrected = '<h3 class="post-title">%s</h3>' % corrected
            elif is_special_header_move_to_page_top(line):
                corrected = ' <h4 class="post-title">%s</h4>' % corrected
            else:
                corrected = '%s' % corrected

            if is_special_header_move_to_page_top(line):
                text_lines.insert(0, corrected)
            else:
                text_lines.append(corrected)

        if next_image_id >= 0:
            text_lines.append(get_image_html_tag(self.number, next_image_id + 1))


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

    def generate_html(self, filename):
        page_numbers = sorted(self.pages.keys())
        output = []
        for number in page_numbers:
            print('Generating page %d ' % number)
            content = self.pages[number].get_html_content()
            # if not content.strip():
            #     continue
            content += '<div class="page_number">― %d ―</div>' % number
            output.append(content)


        html_content = html_header + '\n'.join(output) + html_footer
        print('Generating:', filename)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)

def pdf_to_book(doc, max_pages, only_specific_page=-1):
    book = Book()
    i = 0
    for page in doc:  # scan through the pages
        i += 1
        if only_specific_page >= 0 and only_specific_page != i:
            continue
        if only_specific_page < 0 and i > max_pages:
            break

        images = page.get_images()
        for image in images:
            # b = page.get_image_bbox()
            bbox = page.get_image_bbox(image[7])
            #print(bbox.y1)

        new_page = Page(i)
        new_page.update_image_locations(page)
        book.add_page(i, new_page)

        raw_dict = page.get_textpage().extractRAWDICT()

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
output_filename = 'book.html'
max_pages = 30
only_specific_page = -1  # Set to -1 to disable.
book = pdf_to_book(pymupdf.open(fname), max_pages, only_specific_page)
book.verify_page_numbers()
book.print_pages()
book.generate_html(output_filename)


# print('Number of sizes:', len(line_heights))
# for h in line_heights.keys():
#     # print('-'*200)
#     print(h, len(line_heights[h]))

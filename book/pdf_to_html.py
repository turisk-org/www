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
    """
    Reverses any numbers found within the input string.

    Args:
        input_string: The string to process.

    Returns:
        The modified string with numbers reversed.
    """

    def reverse_number(match):
        """Helper function to reverse a matched number."""
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
    

fname = sys.argv[1]  # filename
doc = pymupdf.open(fname)


i = 0
for page in doc:  # scan through the pages
    i += 1
    if i > 50:
         break
    # if i < 5:
    #     continue
    print('<h2>Page %d</h2>' % i )
    

    raw_dict = page.get_textpage().extractRAWDICT()

    def bbox_center(bbox):
        return ((bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2)

    def char_x(char):
        bbox = char['bbox']
        return (bbox[0]+bbox[2])/2

    def char_y(char):
        bbox = char['bbox']
        return (bbox[1]+bbox[3])/2

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
                  #if not int(char_y(char)) == 683:
                  #    continue
                  #print(char['c'], char['bbox'])
                  #print(char_y(char))
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


    text_lines = []
    for line in all_lines:
        # print(char_height(line[0]))
        text = ''
        for c in line:
            text += c['c']
        text_lines.append(move_dot_and_comma_to_end(reverse_numbers_in_string(text)))


    print(html_header)
    for line in text_lines:
        print('<p>%s</p>' % line)
    print(html_footer)
    
    # # print(page.get_textpage().extractRAWDICT()['blocks'])
    # for b in page.get_textpage().extractRAWDICT()['blocks']:
    #     print(b.keys())
    #     print(b['lines'][0].keys())
    #     for line in b['lines']:
    #         if 'spans' in line:
    #             for x in line['spans']:
    #                 if 'chars' in x:
    #                     print(x['chars'][0]['c'])

    
    # for block in page.get_textpage().extractBLOCKS():
    #     print(block)


    # text = page.get_text("words", delimiters=None)
    # for c in page.get_textpage().extractDICT()['blocks']:
    #     print(c)

    # words = page.get_textpage().extractWORDS()
    # line = []
    # for word in words:
    #     if word[3]<173 and word[3]>171:
    #         line.append(word)
    # line.sort(key=lambda x: (int(x[3]), x[2]))
    # for word in line:
    #     print(word)
    
    # words = page.get_textpage().extractRAWDICT()
    # for word in words:
    #     print(word)
    # for word in text:
    #     print(word)


    # def word_hight(word):
    #     return (word[1]+word[3]) / 2

    # # Sort words...    
    # words = page.get_text("words", sort=False)
    # lines = []
    # for word in words:
    #     if word[3]<190 and word[3]>160:
    #         print(word)
    #     if word[4].find('1') >=0:
    #         print('aaaaaaaaaaaa', word)
    #         print('bbbbbbbbbbbb', word[4])
    #     h = word_hight(word)
    #     found = False
    #     for line in lines:
    #         if abs(word_hight(line[0]) - h) < 5:
    #             line.append(word)
    #             found = True
    #     if found:
    #         continue
    #     # New line
    #     lines.append([word])

    # for line in lines:
    #     line.sort(key=lambda x: -x[2])
    # lines.sort(key=lambda x: x[0][3])

    # for line in lines:
    #     for word in line:
    #         print(word[4], end=' ')
    #     print()



    # Naeive sorting...            
    # words.sort(key=lambda x: (int(x[3]), x[2]))

    # lines = []
    # current_line_level = -1
    # current_line_words = []
    # for x in words:
    #     if current_line_level < 0 or x[3] != current_line_level:
    #         # print('----------------------')
    #         # print(x[4])
    #         lines.append(' '.join(reversed(current_line_words)))
    #         current_line_level = int(x[3])
    #         current_line_words = [str(x[4])]
    #     else:
    #         # print(x[4])
    #         current_line_words.append(str(x[4]))
    # for line in lines:
    #   print(line)

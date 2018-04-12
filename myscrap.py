'''
@author: Zbigniew Manasterski
@contact  benkopolis@gmail.com
@date Jul 18, 2017
'''

import sys
from time import sleep
import random
import re
import urllib3

EXTRACT_RE = re.compile('@[^%]*%[^:]*:([^=]*)')
TITLE_RE = re.compile(r'<h1 class="(?:(?:p3h2\W?)|(?:heading\W?)|(?:border-top\W?))*">'
                      '(?:<a[^>]*>)?([^<]*)(?:</a>)?[^<]*</h1>')
CURRENT_PAGE_RE = re.compile('<input\\W+id="item"\\W+name="item"\\W+type="text"\\W+onchange="p3acti'
                             'on\\(\'itemset\'\\)"\\W+size="[0-9]"\\W+value="([0-9]+)"')
NEXT_PAGE = 'itemfwd'
FORM_ACTION = 'p3do'
SET_PAGE = 'itemset'
FORM_ZOOM = 'zoom'
FORM_ITEMTYPE = 'itemtype'
FORM_ARGITEM = 'arg_item'
FORM_PAGE = 'item'
CHAPTERS_16 = {'129' : 20, '91' : 8, '119' : 19, '116' : 11, '122' : 17, '250' : 1,
               '120' : 18, '128' : 31, '121' : 10, '148' : 21, '168' : 21, '154' : 69}
CHAPTERS_10 = {'149' : 38, '156' : 28, '160' : 17, '161' : 25, '65' : 13, '137' : 32,
               '45' : 19, '188' : 5, '72' : 7, '131' : 48, '139' : 40, '183' : 16,
               '99' : 7, '140' : 12, '86' : 6, '126' : 14, '111' : 10, '155' : 9,
               '134' : 24, '81' : 19}

NEO_ASSYRIAN = ['1']

class PageLoadResult:
    def __init__(self, page_num, titles, lines):
        self.lines = lines
        self.page_num = page_num
        self.titles = titles

def get_postback_content(target_url, item, http, chapter):
    """
    Gets the page content performing form request
    """
    data = ''
    try:
        fields = {
            FORM_PAGE : '{}'.format(item),
            FORM_ITEMTYPE  : 'xtf',
            FORM_ZOOM : chapter,
            FORM_ACTION : SET_PAGE,
            FORM_ARGITEM : '{}'.format(item)
            }
        req = http.request('POST', target_url, fields)
        data = req.data.decode('utf-8')
        titles = TITLE_RE.findall(data)
        pages = CURRENT_PAGE_RE.findall(data)
        proc_data = EXTRACT_RE.findall(data)
        return PageLoadResult(pages[0], titles, proc_data)
    except Exception as ex:
        print(ex)
        print('========================')
        print(data)
        return None

def get_chapters(chapters, url, http):
    titles = set()
    i = 0
    for chapter in chapters:
        page = 0
        while int(i) >= page:
            page = page + 1
            sleep(random.uniform(0.4, 1.9))
            result = get_postback_content(url, page, http, chapter)
            if result is None:
                continue
            i = result.page_num
            if len(result.lines) == 0:
                break
            if result.titles[0] in titles:
                break
            titles.add(result.titles[0])
            print('=======TITLE=======')
            print(result.titles[0])
            print('=======TRANSLITERATION=======')
            for trans in result.lines:
                print(trans)
            print('\nDONE\n')
            print('Result page: {}; current page {}; current chapter: {}'
                  .format(i, page, chapter))
    #for i in range(1, 26):
    #    get_postback_content(url2, i, http)


def main(argv):
    """
    Main function
    """
    if len(argv) == 3:
        return
    http = urllib3.PoolManager()
    #url1 = 'http://oracc.museum.upenn.edu/saao/corpus/' # 1 - 25
    url2 = 'http://oracc.museum.upenn.edu/rinap/corpus/' # 1 - 25
    get_chapters(NEO_ASSYRIAN, url2, http)

if __name__ == "__main__":
    main(sys.argv[1:])

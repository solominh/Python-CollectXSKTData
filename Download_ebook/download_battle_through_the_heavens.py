import bs4
import requests
import datetime
import os
import re


def get_chapter(chapter_number):
    """http://www.wuxiaworld.com/btth-index/btth-chapter-601/"""

    url = r'http://www.wuxiaworld.com/btth-index/btth-chapter-' + \
        str(chapter_number)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    css_selector = '#primary div.entry-content > div:nth-of-type(1) > div'

    elements = soup.select(css_selector)
    return elements[0]


def save_chapter(chapter_number):
    # toString
    html = str(get_chapter(chapter_number))

    # Remove chapter link
    cleaner_html = re.sub(r'<p><a(.*?)</p>', '', html)

    # Make chapter number become heading 3
    p = re.compile(r'<p>(.*?)</p>')
    new_html = p.sub(r'<h3>\1</h3>', cleaner_html, 1)

    output_filepath = os.path.join(
        os.path.dirname(__file__), './btth/btth_' + str(chapter_number) + '.html')
    print(os.path.abspath(output_filepath))
    with open(output_filepath, 'w') as f:
        f.write(new_html)


for chapter_number in range(690, 761):
    save_chapter(chapter_number)

import bs4
import requests
import os


def get_chapter(url):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    css_selector = '#noidungtruyen'

    elements = soup.select(css_selector)
    return elements[0]


def save_chapter(chapter_number):

    url = 'http://truyenyy.com/doc-truyen/dau-pha-thuong-khung/chuong-' + \
        str(chapter_number)

    # toString
    html = str(get_chapter(url))

    output_filepath = os.path.join(
        os.path.dirname(__file__), './dptk/dptk_' + str(chapter_number) + '.html')
    print(os.path.abspath(output_filepath))
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(html)


for chapter_number in range(1, 5):
    save_chapter(chapter_number)

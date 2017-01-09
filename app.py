import bs4patch
import bs4
import requests


def get_first_prize_number_from(url):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elements = soup.select(
        '#center-content > div:nth-of-type(7) > div > table > tbody > tr:nth-of-type(11) > td:nth-of-type(2) > em')

    print('Elements =' + str(elements))
    # return elements[0].text.strip()
    return 0


def main():
    url = 'http://xskt.com.vn/ket-qua-xo-so-theo-ngay/tp-hcm-xshcm/6-2-2016.html'
    number = get_first_prize_number_from(url)
    print('number =' + str(number))

main()
# output = './numbers.txt'
# with open(output, 'a') as f:

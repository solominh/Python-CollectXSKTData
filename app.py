import bs4
import requests
import datetime
import os


def get_first_prized_number_from(url):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    css_selector = '#center-content > div.box-ketqua > div > table > tr:nth-of-type(11) > td:nth-of-type(2) > em'
    elements = soup.select(css_selector)
    return elements[0].text.strip()


def generate_HCM_lottery_issue_days(year):
    """Issuing in Monday and Saturday"""
    first_day = datetime.date(year, 1, 1)
    last_day = datetime.date(year, 12, 31)

    while True:
        day_of_week = first_day.weekday()
        if day_of_week == 0 or day_of_week == 5:
            break
        first_day += datetime.timedelta(days=1)

    while first_day <= last_day:
        yield first_day
        first_day += datetime.timedelta(
            days=5) if first_day.weekday() == 0 else datetime.timedelta(days=2)


def fetch_lottery_first_prized_number_in(year=2016):
    """ Example link:
     url = 'http://xskt.com.vn/ket-qua-xo-so-theo-ngay/tp-hcm-xshcm/6-2-2016.html'
     """

    root_url = 'http://xskt.com.vn/ket-qua-xo-so-theo-ngay/tp-hcm-xshcm/'
    first_prized_numbers = []
    for issuing_day in generate_HCM_lottery_issue_days(year):
        file_name = issuing_day.strftime('%d-%m-%Y.html')
        url = os.path.join(root_url, file_name)
        print(url)

        try:
            number = get_first_prized_number_from(url)
        except:
            print('Fail to extract number')
            number = 0

        print('Number = {}'.format(number))
        first_prized_numbers.append(number)

    output_filepath = './first_prized_numbers_in_' + str(year) + '.txt'
    with open(output_filepath, 'w') as f:
        for number in first_prized_numbers:
            f.write(str(number) + '\n')

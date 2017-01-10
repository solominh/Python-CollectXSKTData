from lxml import html
import requests

url = 'http://xskt.com.vn/ket-qua-xo-so-theo-ngay/tp-hcm-xshcm/6-2-2016.html'
xpath = '//*[@id="center-content"]/div[5]/div/table/tbody/tr[11]/td[2]/em'
# LXML not support tbody tag
working_xpath = '//*[@id="center-content"]/div[5]/div/table/tr[11]/td[2]/em'
page = requests.get(url)
tree = html.fromstring(page.content)
first_prized_number = tree.xpath(working_xpath)
if(len(first_prized_number)):
    print('Get first prize number successfully')
    print(first_prized_number[0].text_content())
else:
    print('Fail to get number')

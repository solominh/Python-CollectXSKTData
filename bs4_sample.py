import bs4
import requests

url = 'http://xskt.com.vn/ket-qua-xo-so-theo-ngay/tp-hcm-xshcm/6-2-2016.html'
xpath = '//*[@id="center-content"]/div[5]/div/table/tbody/tr[11]/td[2]/em'
res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'html.parser')

# BS4 not support tbody tag
center_content = soup.select('#center-content')[0]
first_prized_number = center_content.find_all_next('div')[4].find_next('div').find_next(
    'table').find_all_next('tr')[10].find_all_next('td')[1].find_next('em')

print(first_prized_number.text)

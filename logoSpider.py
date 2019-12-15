from lxml import html
import requests

def read_airlines_sg():
    res = {}
    col = [x for x in range(5)]
    lin = [y for y in range(100)]
    page = requests.get('https://www.seatguru.com/browseairlines/browseairlines.php')
    tree = html.fromstring(page.content)
    for c in col:
        for l in lin:
            al = tree.xpath(f'//*[@id="content"]/div[3]/div[1]/div/ul[{c}]/li[{l}]/a')
            if len(al) > 0:
                al = al[0]
                al_name = al.text
                al_page = al.get('href')
                res[al_name] = al_page
    return res




def read_airlines():
    airlines = {}
    with open('airlines.txt', 'r') as f:
        content = f.readlines()
    raw = [x.strip() for x in content]
    keys = [x for x in raw if len(x) == 1]
    values = [x for x in raw if len(x) > 1]
    nvalues = []
    for v in values:
        nvalues.append([x.strip() for x in v.split(',')])
    values = nvalues

    for k in keys:
        group = list()
        for v in values:
            if v[0][0] == k:
                al_names = []
                for n in v:
                    al_names.append(n.replace(' ', '_'))
                group.append(al_names)
        airlines[k] = group
    return airlines

def read_data_wikipedia(air_line_names):
    for air_line_name in air_line_names:
        signs = ['IATA', 'ICAO', 'Callsign']
        page = requests.get('https://en.wikipedia.org/wiki/' + air_line_name)
        tree = html.fromstring(page.content)
        codes = [x.text.strip() for x in tree.xpath('//td[@class="nickname"]') if x.text != None]
    return [{k:v} for k,v in zip(signs, codes)]

def get_sg_full_name(air_line_name):
    # //*[@id="content"]/div[3]/div[1]/div
    # //*[@id="content"]/div[3]/div[1]/div/ul[1]/li[5]/a
    page = requests.get('https://www.seatguru.com/browseairlines/browseairlines.php')



def read_image_sg(air_line_name, air_line_data):
    # xpath = //*[@id="content"]/div/div[4]/div[1]/div[1]/img
    # url = https://www.seatguru.com/airlines/GOL/information.php
    page = requests.get('https://www.seatguru.com/airlines/{ALN}/information.php'.format(ALN=air_line_name))
    tree = html.fromstring(page.content)
    img_data = tree.xpath('//*[@id="content"]/div/div[4]/div[1]/div[1]/img')
    img_url = img_data[0].get('src')
    if img_url.split('/')[-1] == '.jpg':
        print(air_line_name, img_url)


if __name__ == "__main__":
    als = read_airlines_sg()
    for k in als:
        print(f'{k}: {als[k]}')
    # counter = 0
    # for k in als:
    #     for al in als[k]:
    #         data = read_data_wikipedia(al)
    #         counter += 1
    #         # print(f'{counter:03}] Data found for {al[0]}: {data}')
    #         read_image_sg(al[0], data)
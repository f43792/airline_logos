### Script to retrieve and save airline's logo from Seat Guru <https://www.seatguru.com/>
### 
### WHO         When            What
### FCN         2019/Dec/15     Initial write

from lxml import html
import requests

def read_airlines():
    '''This function will retrieve all companies names'''
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
    
    # return will be a dict in the format
    # 'name': 'url_to_information'
    return res

def create_wiki_lookuptable():
    '''Some companies have diferente names in SG and Wikipedia. To solve this
    a lookup table that exchange information with the correct 'name' for companies
    that need. This information comes from the file 'wikipedia_lookuptable.txt'''
    airlines = {}
    with open('wikipedia_lookuptable.txt', 'r') as f:
        content = f.readlines()
    raw = [x.strip() for x in content]
    # This is a series of nested list comprehension.
    # It could be trick but also very eficient to work with lists.
    # I do not recomend more than 4 nested loops.
    lines = [x for x  in [x.split(',') for x  in [x for x in [x for x in raw if len(x) > 1] if x[0] != '#']] if len(x) > 1]
    for l in lines:
        airlines[l[0]] = [x.strip() for x in l[1:]]
    return airlines

def read_data_wikipedia(air_line_names):
    '''Function to retrieve the ICAO code for the passed airline'''
    for air_line_name in air_line_names:
        signs = ['IATA', 'ICAO', 'Callsign']
        page = requests.get('https://en.wikipedia.org/wiki/' + air_line_name)
        tree = html.fromstring(page.content)
        codes = [x.text.strip() for x in tree.xpath('//td[@class="nickname"]') if x.text != None]
    return [{k:v} for k,v in zip(signs, codes)]

def read_images_sg(air_line_name, air_line_url, air_line_data):
    '''This function will retrieve the image based on air line name
    and save it to folder images.
    TODO: Add some fail checks'''

    aln = ''
    if type(air_line_name) == list:
        aln = air_line_name[0]
    else:
        aln = air_line_name
    aln = aln.replace(' ', '_')
    page = requests.get('https://www.seatguru.com' + air_line_url, allow_redirects=True)
    tree = html.fromstring(page.content)
    img_data_path = tree.xpath('//*[@id="content"]/div/div[4]/div[1]/div[1]/img')
    if len(img_data_path) > 0:
        img_url = img_data_path[0].get('src')
        if img_url:
            fext = '.' + img_url.split('.')[-1]
            ICAO_CODE = [x for x in air_line_data if 'ICAO' in x][0]['ICAO']
            filename = './images/' + ICAO_CODE + fext
            img_data = requests.get(img_url, allow_redirects=True)
            open(filename, 'wb').write(img_data.content)


if __name__ == "__main__":
    airlines = read_airlines()
    looktable = create_wiki_lookuptable()

    for i, al in enumerate(airlines):
        if al in looktable:
            al_name = looktable[al]
        else:
            al_name = [al]
        
        print(f'{i+1:03}] Retriving information of {al_name[0]}...', end='', flush=True)
        data = read_data_wikipedia(al_name)
        al_url =  airlines[al]
        read_images_sg(al_name, al_url, data)
        print('done.', flush=True)
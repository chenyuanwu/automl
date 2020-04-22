from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
import re
import os
import multiprocessing as mp

# starturl = "https://pantheon.stanford.edu/measurements/node/?node=any&direction=any&link=any&scenario=any&year=any&month=any&page=1"
starturl = "https://pantheon.stanford.edu/measurements/node/"
datapath = "/home/chenyunw/automl/node2cloud"
baseurl = "https://pantheon.stanford.edu/measurements/node/"

def dowanload(args):
    url, current_page_index = args
    urlretrieve(url, os.path.join(datapath, 'test' + current_page_index, url.split("/")[-1]))
    # print("%s Downloaded" % url.split("/")[-1])

pool = mp.Pool(4)
html = urlopen(starturl).read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')

for i in range(4):
    current_page_item = soup.find_all('li', attrs={"class":"page-item active"})[0]
    current_page_index = re.findall(r'[0-9]+', current_page_item.a.get_text())[0]
    os.mkdir(os.path.join(datapath, 'test' + current_page_index))
    download_names = ["Full report", "Performance data", "Raw logs", "Raw logs with UIDs"]
    download_tags = soup.find_all('a', text=download_names)
    for t in download_tags:
        # urlretrieve(t['href'], os.path.join(datapath, 'test' + current_page_index, t['href'].split("/")[-1]))
        pool.apply_async(dowanload, args=((t['href'], current_page_index),))
    pool.close()
    pool.join()
    print("Crawled the %s page" % current_page_index)

    next_tag = soup.find_all('a', attrs={"aria-label": "Next"})[0]
    if 'href' in next_tag.attrs:
        html = urlopen(baseurl + next_tag['href']).read().decode('utf-8')
        soup = BeautifulSoup(html, features='lxml')
    else:
        break

print("In Total: Have Crawled %d pages" % (i + 1))


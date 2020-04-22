from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
import re
import os
import multiprocessing as mp
import time
import argparse


# def dowanload(args):
#     url, current_page_index = args
#     urlretrieve(url, os.path.join(datapath, 'test' + current_page_index, url.split("/")[-1]))
#     # print("%s Downloaded" % url.split("/")[-1])
#
# pool = mp.Pool(4)


def crawl(datapath, starturl, baseurl, step):
    html = urlopen(starturl).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')

    if os.path.exists(datapath):
        assert False, "Some files have been crawled."
    else:
        os.mkdir(datapath)

    for i in range(step):
        current_page_item = soup.find_all('li', attrs={"class":"page-item active"})[0]
        current_page_index = re.findall(r'[0-9]+', current_page_item.a.get_text())[0]
        os.mkdir(os.path.join(datapath, 'test' + current_page_index))
        download_names = ["Full report", "Performance data", "Raw logs", "Raw logs with UIDs"]
        download_tags = soup.find_all('a', text=download_names)
        for t in download_tags:
            time_start = time.time()
            urlretrieve(t['href'], os.path.join(datapath, 'test' + current_page_index, t['href'].split("/")[-1]))
            time_end = time.time()
            print("%s Downloaded in %.2f" % (t['href'].split("/")[-1], time_end - time_start))
            # pool.apply_async(dowanload, args=((t['href'], current_page_index),))
        # pool.close()
        # pool.join()
        print("Crawled the %sth page" % current_page_index)

        next_tag = soup.find_all('a', attrs={"aria-label": "Next"})[0]
        if 'href' in next_tag.attrs:
            html = urlopen(baseurl + next_tag['href']).read().decode('utf-8')
            soup = BeautifulSoup(html, features='lxml')
        else:
            break
    print("In Total: Have Crawled %d pages" % (i + 1))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('node', help='which netdb node')
    parser.add_argument('--stepn', type=int, default=2789//3)
    parser.add_argument('--stepc', type=int, default=1457//3)
    args = parser.parse_args()

    if args.node == 'n1':
        datapath = "/home/chenyunw/automl/node2cloud"
        baseurl = "https://pantheon.stanford.edu/measurements/node/"
        starturl = "https://pantheon.stanford.edu/measurements/node/?node=any&direction=any&link=any&scenario=any&year=any&month=any&page=1"
        crawl(datapath, starturl, baseurl, args.stepn)
    elif args.node == 'n2':
        datapath = "/home/chenyunw/automl/node2cloud"
        baseurl = "https://pantheon.stanford.edu/measurements/node/"
        starturl = "https://pantheon.stanford.edu/measurements/node/?node=any&direction=any&link=any&scenario=any&year=any&month=any&page=%d" % (1 + args.stepn)
        crawl(datapath, starturl, baseurl, args.stepn)
    elif args.node == 'n3':
        datapath = "/home/chenyunw/automl/node2cloud"
        baseurl = "https://pantheon.stanford.edu/measurements/node/"
        starturl = "https://pantheon.stanford.edu/measurements/node/?node=any&direction=any&link=any&scenario=any&year=any&month=any&page=%d" % (1 + 2*args.stepn)
        crawl(datapath, starturl, baseurl, args.stepn)
    elif args.node == 'n4':
        datapath = "/home/chenyunw/automl/cloud2cloud"
        baseurl = "https://pantheon.stanford.edu/measurements/cloud/"
        starturl = "https://pantheon.stanford.edu/measurements/cloud/?src=any&dst=any&scenario=any&year=any&month=any&page=1"
        crawl(datapath, starturl, baseurl, args.stepc)
    elif args.node == 'n5':
        datapath = "/home/chenyunw/automl/cloud2cloud"
        baseurl = "https://pantheon.stanford.edu/measurements/cloud/"
        starturl = "https://pantheon.stanford.edu/measurements/cloud/?src=any&dst=any&scenario=any&year=any&month=any&page=%d" % (1 + args.stepc)
        crawl(datapath, starturl, baseurl, args.stepc)
    elif args.node == 'n6':
        datapath = "/home/chenyunw/automl/cloud2cloud"
        baseurl = "https://pantheon.stanford.edu/measurements/cloud/"
        starturl = "https://pantheon.stanford.edu/measurements/cloud/?src=any&dst=any&scenario=any&year=any&month=any&page=%d" % (1 + 2*args.stepc)
        crawl(datapath, starturl, baseurl, args.stepc)



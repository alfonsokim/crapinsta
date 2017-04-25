
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import requests
import os

## claudiacarnevali

def must_not_fap(args):

    driver = webdriver.Firefox()
    print 'Downloading photos from %s account' % args.profile
    driver.get('https://www.instagram.com/%s/' % args.profile)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    if not os.path.exists(args.profile):
        print 'creating folder %s' % args.profile
        os.makedirs(args.profile)

    img_count = 0
    for x in soup.findAll('img'):
        img_src = str(x.get('src'))
        img_ext = img_src[-3:]
        img_name = 'img%04d.%s' % (img_count, img_ext)
        print 'Downloading %s -> %s' % (img_src, img_name)        
        with open(os.path.join(args.profile, img_name), 'wb') as img_file:
            img_file.write(requests.get(img_src).content)
        if args.limit > 0 and img_count >= args.limit:
            break
        img_count += 1

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Download all photos from an instagram account')
    parser.add_argument('--profile', type=str, required=True, help='Name of the instagram profile')
    parser.add_argument('--limit', default=-1, type=int, required=False, help='Limit of photos to download')
    args = parser.parse_args()
    
    must_not_fap(args)


from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import requests
import os
import time
from selenium.common.exceptions import NoSuchElementException

## claudiacarnevali

def scroll_page(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)


def must_not_fap(args):

    driver = webdriver.Firefox()

    for anchor in driver.find_elements_by_xpath('//a'):
        print anchor
    return

    print 'Downloading photos from %s account' % args.profile
    driver.get('https://www.instagram.com/%s/' % args.profile)

    if not os.path.exists(args.profile):
        print 'creating folder %s' % args.profile
        os.makedirs(args.profile)

    driver.implicitly_wait(1)

    # Click en boton de cargar mas
    more = driver.find_element_by_partial_link_text("anchor_text")

    for i in range(1000 // 12):
        print 'sss'
        scroll_page(driver)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

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

    driver.close()



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Download all photos from an instagram account')
    parser.add_argument('--profile', type=str, required=True, help='Name of the instagram profile')
    parser.add_argument('--limit', default=-1, type=int, required=False, help='Limit of photos to download')
    args = parser.parse_args()
    
    must_not_fap(args)

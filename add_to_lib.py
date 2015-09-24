import requests
import os
from lxml import html
import logging
import sys

LOG_LEVEL = 'WARNING'

DEBUG = True
BOOK_FORMATS = [
    # 'epub',
    # 'mobi',
    # 'pdf'
]
BASE_URL = 'https://www.packtpub.com'

if DEBUG:
    import pdb
    LOG_LEVEL = 'DEBUG'


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=LOG_LEVEL)


def break_point():
    if DEBUG:
        pdb.set_trace()


def error(msg):
    logging.error(msg)
    sys.exit(1)


def main():
    session = requests.session()
    logging.info('setting session')
    login_data = {
        'email': os.environ.get('PACKT_EMAIL'),
        'password': os.environ.get('PACKT_PASSWORD'),
        'op': 'Login',
        'form_id': 'packt_user_login_form',
        'form_build_id': None,
    }
    logging.debug('setting login data without form_build_id ' + str(login_data))
    free_learning_url = 'https://www.packtpub.com/packt/offers/free-learning'
    r = session.get(free_learning_url)
    tree = html.fromstring(r.text)
    form_build_id_elem = tree.xpath('//input[@name="form_build_id"]')
    book_link_elem = tree.xpath('//a[@class="twelve-days-claim"]')
    book_url = BASE_URL + book_link_elem[0].get('href')
    logging.debug('book url = ' + book_url)
    if len(form_build_id_elem) > 0:
        login_data['form_build_id'] = form_build_id_elem[0].get('id')
        logging.debug('setting form_build_id in login_data to ' + login_data['form_build_id'])
    else:
        error('Failed to set form_build_id')
    r = session.post(free_learning_url, headers={'content-type': 'application/x-www-form-urlencoded'}, data=login_data)
    tree = html.fromstring(r.text)
    elem = tree.xpath('//div[contains(@class,"error")]')
    # break_point()
    if len(elem) > 0 and "Sorry, you entered an invalid email address and password combination." in elem[0].text:
        error('Failed to login please check your credentials')
    logging.debug('Logged in to packtpub.com')
    r = session.get(book_url)
    tree = html.fromstring(r.text)
    book_elem = tree.xpath('//div[contains(@class,"product-line")]')
    logging.debug('book name = ' + book_elem[0].get('title'))
    logging.info("claimed book successfully")
    # Downloading book in all formats
    for bf in BOOK_FORMATS:
        book_url = BASE_URL + '/ebook_download/' + book_elem[0].get('nid') + '/' + bf
        logging.info('Getting book in ' + bf)
        with open(book_elem[0].get('nid') + '.' + bf, 'wb') as handle:
            response = session.get(book_url, stream=True)
            for chunk in response:
                handle.write(chunk)

    # end of downloading files

if __name__ == '__main__':
    main()

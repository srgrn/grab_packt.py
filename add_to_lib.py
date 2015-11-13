import requests
import os
from lxml import html
import logging
import sys

LOG_LEVEL = 'WARNING'

DEBUG = False
BOOK_FORMATS = [
    # 'epub',
    # 'mobi',
    # 'pdf'
]
if not BOOK_FORMATS:
    print "Error: Book format is not selected (e.g. pdf)."
    sys.exit()

BASE_URL = 'https://www.packtpub.com'
DOWNLOAD_NEW = True
BOOKS_DIR = os.path.dirname(os.path.realpath(__file__)) +"/books"

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

    if login_data['email'] is None or login_data['password'] is None:
        error('You must provide credentials')

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
    logging.info('Logged in to packtpub.com')
    tree = html.fromstring(r.text)
    elem = tree.xpath('//div[contains(@class,"error")]')

    # break_point()
    if len(elem) > 0 and "Sorry, you entered an invalid email address and password combination." in elem[0].text:
        error('Failed to login please check your credentials')

    r = session.get(book_url)
    tree = html.fromstring(r.text)
    book_elem = tree.xpath('//div[contains(@class,"product-line")]')
    book_name = book_elem[0].get('title')
    logging.debug('book name = ' + book_name)
    book_name.replace('"', '\\"')

    download_log = os.getcwd() +"/books.log"
    if not os.path.isdir(BOOKS_DIR):
        os.mkdir(BOOKS_DIR)
        logging.debug('Creating directory: '+ BOOKS_DIR)
    logging.debug('Books directory: '+ BOOKS_DIR)
    os.chdir(BOOKS_DIR)

    # Downloading book in all formats
    for bf in BOOK_FORMATS:
        book_id = book_elem[0].get('nid')
        book_url = BASE_URL + '/ebook_download/' + book_id + '/' + bf
        fname = '('+ book_id + ')' + book_name  + '.' + bf
        if DOWNLOAD_NEW and os.path.exists(BOOKS_DIR +'/'+ fname):
            logging.debug('File '+ fname +' exists. Skip download')
            continue
        logging.info('Getting book ' + fname)
        with open(fname, 'wb') as handle:
            response = session.get(book_url, stream=True)
            for chunk in response:
                handle.write(chunk)
        with open(download_log, 'a') as f:
            f.write("Download id:%s, format:%s, name:%s\n" % (book_id, bf, book_name))

    # end of downloading files

if __name__ == '__main__':
    main()

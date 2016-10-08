""" a simple script to get the packet publishing free book of the day into your account """
import argparse
import json
import logging
import os
import sys

import requests
from lxml import html
import getpass

CONFIG = None
HEADERS = {'User-Agent': 'grab_packet.py free claim script'}
BASE_URL = 'https://www.packtpub.com'

def setup(args):
    log_level = 'WARNING'
    if args.debug:
        # import pdb
        log_level = 'DEBUG'
    log_format = '%(asctime)-15s - %(levelname)s - %(message)s'
    logging.basicConfig(format=log_format, level=log_level)
    logging.debug('Setup logging configuration')
    config = {}
    if args.config:
        logging.debug('loading config file')
        try:
            with open(args.config) as configfile:
                config = json.load(configfile)
        except IOError:
            logging.critical("Failed to load the file")
            sys.exit(1)
        except ValueError:
            logging.critical("Failed to read the config file probably not proper json")
            sys.exit(1)
        except Exception, e:
            raise e
        return config
    else:
        logging.debug('no config file specified')
    for key in os.environ:
        if "CONFIG_" in key:
            config[key.replace('CONFIG_').lower()] = os.environ.get(key)
    return config

def set_arg_in_config(args,name):
    if hasattr(args,name) and getattr(args,name) is not None:
        CONFIG[name] = getattr(args,name)


def login(session):
    login_data = {
        'email': CONFIG.get('email'),
        'password': CONFIG.get('password'),
        'op': 'Login',
        'form_id': 'packt_user_login_form',
        'form_build_id': None,
    }
    logging.debug('setting login data without form_build_id ' + str(login_data))
    free_learning_url = 'https://www.packtpub.com/packt/offers/free-learning'
    r = session.get(free_learning_url, headers=HEADERS)
    tree = html.fromstring(r.text)
    form_build_id_elem = tree.xpath('//input[@name="form_build_id"]')
    book_link_elem = tree.xpath('//a[@class="twelve-days-claim"]')
    book_url = BASE_URL + book_link_elem[0].get('href')
    logging.debug('book url = ' + book_url)

    if len(form_build_id_elem) > 0:
        login_data['form_build_id'] = form_build_id_elem[0].get('id')
        logging.debug('setting form_build_id in login_data to ' + login_data['form_build_id'])
    else:
        logging.critical('Failed to set form_build_id')

    headers = HEADERS
    headers['content-type']= 'application/x-www-form-urlencoded'
    r = session.post(free_learning_url, headers=headers, data=login_data)
    logging.info('Logged in to packtpub.com')
    tree = html.fromstring(r.text)
    elem = tree.xpath('//div[contains(@class,"error")]')

    # break_point()
    if len(elem) > 0 and "Sorry, you entered an invalid email address and password combination." in elem[0].text:
        logging.critical('Failed to login please check your credentials')

    return book_url

def claim_book(session,book_url):
    r = session.get(book_url,headers=HEADERS)
    tree = html.fromstring(r.text)
    book_elem = tree.xpath('//div[contains(@class,"product-line")]')
    book_name = book_elem[0].get('title')
    book_id = book_elem[0].get('nid')
    logging.debug('book_name={}, book_id={}'.format(book_name,book_id))
    return (book_name,book_id)

def format_book_name(name,id,suffix):
    ret = '({}){}.{}'.format(id,name,suffix)
    ret = ret.replace('"', '\\"').replace('/','_')
    return ret

def download_book(session,book_name,book_id):
    dest = CONFIG.get('dest','./books')
    if not os.path.isdir(dest):
        os.mkdir(dest)
        logging.info('creating destination for downloaded books')
    else:
        logging.info('using {} as destination'.format(dest))
    for bf in CONFIG.get('format',[]):
        book_url = BASE_URL + '/ebook_download/' + book_id + '/' + bf
        filename = format_book_name(book_name,book_id,bf)
        filepath = os.path.join(dest,filename)
        if os.path.exists(filepath):
            logging.info('File already exists skipping format')
            continue
        with open(filepath, 'wb') as book_file:
            response = session.get(book_url, stream=True,headers=HEADERS)
            for chunk in response:
                book_file.write(chunk)
            logging.info("downloaded {} into {}".format(book_name, filepath))


def get_book():
    session = requests.session()
    logging.info('setting session')
    if CONFIG['email'] is None or CONFIG['password'] is None:
        logging.critical('You must provide credentials')
    book_url = login(session)
    book_elem = claim_book(session,book_url)
    if not CONFIG.get('disable_download',False):
        download_book(session,book_elem[0],book_elem[1])
    



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-c', '--config', help='configuration file to load')
    parser.add_argument('-D', '--debug', help='enable debug mode', action='store_true')
    parser.add_argument('-e', '--email', help='your packet account email')
    parser.add_argument('-p', '--password', help='your packet account email')
    parser.add_argument('-f','--format',action='append',help='book format, can be used multiple times')
    parser.add_argument('--disable-download',action='store_true',help='Dsiable downloading of the book')
    args = parser.parse_args()
    global CONFIG
    CONFIG = setup(args)
    set_arg_in_config(args,'password')
    if CONFIG.get('password') is None:
        CONFIG['password'] = getpass.getpass()
    set_arg_in_config(args,'email')
    set_arg_in_config(args,'format')
    set_arg_in_config(args,'disable_download')
    

    get_book()

if __name__ == '__main__':
    main()

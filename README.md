Grab a book a day for free from Packt Pub, https://www.packtpub.com/packt/offers/free-learning using python.

Inspired by https://github.com/draconar/grab_packt


Running:
-----------
* clone this repo
  
  `git clone https://github.com/srgrn/grab_packt.py'
  `cd grab_packt.py`


1. install required modules
  
  `pip install -r requirements.txt`

2. Run the script

  `python add_to_lib.py -e <your packt account email> -p <your password>`


This script will add it to your library where you can download it in a variety of formats.

You can run it through cron if you really want.

The script contains the following options for configuration:
1. using a config file a simple json file like the config.json
2. using environent variables with the word config appended to them: CONFIG_EMAIL, CONFIG_PASSOWRD
3. using the flags 

if you will not supply a password in any way it will drop into interactive mode and wait for password

You can also run it using docker with the following command:

`docker run -it srgrn/grab_packt.py -e email -p password`

or with downloading the files and using a config file 

`docker run --rm -it -v books:/src/books -v $(pwd)/config.json:/src/config.json srgrn/grab_packt.py -c config.json`


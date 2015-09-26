Grab a book a day for free from Packt Pub, https://www.packtpub.com/packt/offers/free-learning using python.

Inspired by https://github.com/draconar/grab_packt


Running:
-----------
* clone this repo
  
  `git clone https://github.com/srgrn/grab_packt.py'
  `cd grab_packt.py`


1. install required modules
  
  `pip install -r requirements.txt`

2. Set enviroment variables

  PACKT_PASSWORD= Your packt account password
  
  PACKT_EMAIL= Your packt account email

3. Run the script

  `python add_to_lib.py`

This script will add it to your library where you can download it in a variety of formats.

You can run it through cron if you really want.

You can also uncomment the formats you want to download to get the files themselves.


You can also run it using docker with the following command:

`docker run -i -t --env PACKT_EMAIL=username --env PACKT_PASSWORD=password srgrn/grab_packt.py`

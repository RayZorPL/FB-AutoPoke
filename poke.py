#
#	* AUTO POKE BOT v0.6 FOR FACEBOOK *
#	
#	Tested on Python 3.4
#
#	Coded by RayZor.pl
#

from robobrowser import RoboBrowser
from urllib.parse import urlparse
import time, pickle, requests
from getpass import getpass



def log_in():
	print('### PLEASE LOG IN ###')
	
	username = input('E-Mail: ')
	password = getpass('Password: ')

	print('### LOGGING IN ###')

	br.open(login_url)

	f = br.get_form(id='login_form')
	f['email'] = username
	f['pass'] = password
	br.submit_form(f) 
	parsed = urlparse(br.url)

	if(br.url == "https://www.facebook.com/common/invalid_request.php" or parsed.path == '/login.php'):
		print("### INVALID DATA !! ###")
		log_in()
	else:
		print("### LOGGED IN !! ###")
		with open('.session', 'wb') as f:
			pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), f)
		poke_idle()
		

def poke_idle(t=4):
	#auto_poke()
	while True:
		auto_poke()
		time.sleep(t)

def auto_poke():
	br.open(pokes_url)
	content = br.select('#contentArea')
	first_div = content[0].select('._xct')

	if first_div:
		links = first_div[0].find_all('a')
		for link in links:
			try: 
				x = urlparse(link['ajaxify'])
				if 'is_hide=0' in x.query:
					br.open(target + link['ajaxify'])
					print('### POKED :) ###')
			except KeyError:
				pass



target = 'http://facebook.com'
pokes_url = target + '/pokes/'
login_url = target + '/login.php'

session = requests.Session()
br = RoboBrowser(parser='html.parser', history=False, session=session)

try:
	with open('.session', 'rb') as f:
		cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
		session.cookies = cookies
		print('### LOADED PREVIOUS SESSION ###')
		poke_idle()
except:
	log_in()


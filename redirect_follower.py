import requests
import sys
from icecream import ic 
from urllib.parse import urljoin

headers = {'User-Agent': 'Mozilla/5.0'}

# http://stackoverflow.com/a/287944/1195812
class bcolors:
	HEADER = "\033[95m"
	OKBLUE = "\033[94m"
	OKGREEN = "\033[92m"
	WARNING = "\033[93m"
	FAIL = "\033[91m"
	ENDC = "\033[0m"
	BOLD = "\033[1m"
	UNDERLINE = "\033[4m"

def statusmsg( status_code, url ):
	"""
	Status messages
	"""
	if status_code >= 200 and status_code < 300 :
		print( f'[{bcolors.OKGREEN}{status_code}{bcolors.ENDC}] - {url}' )
	elif status_code >= 300 and status_code < 400:
		print( f'[{bcolors.WARNING}{status_code}{bcolors.ENDC}] - {url}')
	elif status_code >= 400 and status_code:
		print( f'[{bcolors.FAIL}{status_code}{bcolors.ENDC}] - {url}')


def getRequest(url):
	r = requests.get(url, headers=headers, allow_redirects=False)
	statusmsg(r.status_code,url)
	#if status code starts with '3' there will be a redirection
	if str(r.status_code)[0] == '3':
		location = r.headers['Location']
		#in case if Location is relative URL instead of absolute URL
		if r.headers['Location'].startswith('/'):
			location = urljoin(url,r.headers['Location'])
		return r.status_code,location
	else:
		return r.status_code, url


def handler():
	url = sys.argv[1]
	status, url = getRequest(url)
	redir_limit = 5 #in case of a redirection loop
	while str(status)[0] == '3' and redir_limit > 0:
		status, url = getRequest(url)
		redir_limit -= 1

handler()

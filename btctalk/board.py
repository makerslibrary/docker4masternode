import urllib.request, gspread, sys, re, time, os
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))  # fastest
    return str(len(str_list)+1)

def board_soup(bid):
	page = 'https://bitcointalk.org/index.php?board=' + bid
	req = urllib.request.Request(page, headers={'User-Agent': 'Mozilla/5.0'})
	html = urllib.request.urlopen(req)
	return BeautifulSoup(html.read(), 'html.parser')

def env_var(var):
	try:
		os.environ[var]
	except NameError:
		print ("Environment Variable " + var + " not defined!!")
		sys.exit(0)
	else:
		if os.environ[var].isspace():
			print ("Variable is all SPACE!!")
			sys.exit(0)
		if not os.environ[var]:
			print ("Variable is EMPTY!!")
			sys.exit(0)
		return os.environ[var]

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/root/btctalk/Diet-84bfdd7989bd.json', scope)

gc = gspread.authorize(credentials)
#wks = gc.open("Crypto currency").worksheet("New Coins")
wks = gc.open(env_var('GDOC')).worksheet(env_var('SHEET'))

bid = env_var('BOARD')
term = env_var('TERM')

print (bid)
soup = board_soup(bid)
table = soup.find('table', {'class': 'bordercolor', 'cellpadding': '4'})

coins = []
for td in table.findAll('td', {'class': 'windowbg'}):
	if len(td.attrs) == 2:
		new_ann = td.find('span')
	else:
		coins.append(new_ann)

for coin in coins:
	coin_link = coin.find('a')['href']
	coin_desc = coin.find('a').text
	coin_id = str(coin_link.split("=")[1].split('.')[0])
	print (coin_link)

	try:
		if wks.find(coin_id):
			continue
	except gspread.exceptions.CellNotFound:
		time.sleep(1)

	coin_req = urllib.request.Request(coin_link, headers={'User-Agent': 'Mozilla/5.0'})                    
	coin_page = urllib.request.urlopen(coin_req)                                                           
	coin_html = BeautifulSoup(coin_page, 'html.parser')


	if re.search('masternode', coin_desc, re.IGNORECASE):
		next_row = next_available_row(wks)
		wks.update_acell("A{}".format(next_row), coin_id)
		wks.update_acell("B{}".format(next_row), '=HYPERLINK("'+coin_link+'","'+coin_desc+'")')
#		wks.update_acell("C{}".format(next_row), term)

#	if coin_html(text=re.compile(term, re.I)):
#		if int(coin_id) > 2401040:
#			print (term + ' ' + coin_desc)
#			next_row = next_available_row(wks)
#			wks.update_acell("A{}".format(next_row), coin_id)
#			wks.update_acell("B{}".format(next_row), '=HYPERLINK("'+coin_link+'","'+coin_desc+'")')
#			wks.update_acell("C{}".format(next_row), term)


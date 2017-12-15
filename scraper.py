"""
scraper.py
--------------------------------------
This document contains the web scraping code for the data used in 
our CS 229 project. Data is scraped from basketball-reference.com
and sports-reference.com/cbb.
"""

# LIBRARIES
import csv
import urllib2

from bs4 import BeautifulSoup
from bs4 import Comment

# CONSTANTS
NBA_BASE_URL = 'https://www.basketball-reference.com'
NCAA_BASE_URL = 'https://www.sports-reference.com/'

# Contains all the players whose data will be extracted.
PLAYERS = [
	'James Harden', 'Stephen Curry', 'DeMar DeRozan', 'Jonny Flynn', 'Earl Clark', 'James Johnson',
	'Gerald Henderson', 'Jeff Teague', 'Tyreke Evans', 'Wayne Ellington', 'Eric Maynor', 'Chase Budinger',
	'Ty Lawson', 'Darren Collison', 'Toney Douglas', 'Jrue Holiday', 'Patty Mills', 'Marcus Thornton',
	'Austin Daye', 'Danny Green', 'DeMarre Carroll', 'Wesley Matthews', 'Jodie Meeks', 'AJ Price', 'Alonzo Gee',
	'John Wall', 'Evan Turner', 'Wesley Johnson', 'Patrick Patterson', 'Luke Babbitt', 'Al-Farouq Aminu',
	'Paul George', 'Avery Bradley', 'Gordon Hayward', 'James Anderson', 'Eric Bledsoe', 'Lance Stephenson',
	'Quincy Pondexter', 'Jordan Crawford', 'Greivis Vasquez', 'Derrick Williams', 'Kyrie Irving', 'Brandon Knight',
	'Jimmer Fredette', 'Alec Burks', 'Klay Thompson', 'Kemba Walker', 'Kawhi Leonard', 'Marcus Morris',
	'Markieff Morris', 'Jordan Hamilton', 'Tobias Harris', 'Norris Cole', 'Kyle Singler', 'Shelvin Mack',
	'Reggie Jackson', 'Chandler Parsons', 'Jon Leuer', 'Cory Joseph', 'Iman Shumpert', 'Jimmy Butler',
	"E'Twaun Moore", 'Harrison Barnes', 'Bradley Beal', 'Jeremy Lamb', 'Damian Lillard', 'Terrence Ross',
	'Austin Rivers', 'Kendall Marshall', 'Maurice Harkless', 'Andrew Nicholson', 'Dion Waiters',
	'Jared Sullinger', 'Terrence Jones', 'John Jenkins', 'Will Barton', 'Khris Middleton', 'Tony Wroten',
	'Jeffery Taylor', 'Draymond Green', 'Mike Scott', 'Hollis Thompson', 'Chris Johnson', 'Jae Crowder',
	'Ben McLemore', 'CJ McCollum', 'Victor Oladipo', 'Otto Porter', 'Trey Burke', 'Kentavious Caldwell-Pope',
	'Michael Carter-Williams', 'Tim Hardaway Jr.', 'Shabazz Muhammad', 'Kelly Olynyk', 'Tony Snell',
	'Shane Larkin', 'Allen Crabbe', 'Isaiah Canaan', 'Reggie Bullock', 'James Ennis', 'Robert Covington',
	'Ryan Kelly', 'Andre Roberson', 'Solomon Hill', 'Seth Curry', 'Andrew Wiggins', 'Marcus Smart',
	'Zach LaVine', 'Elfrid Payton', 'Doug McDermott', 'Aaron Gordon', 'Gary Harris', 'Rodney Hood',
	'Nik Stauskas', 'Jordan Clarkson', 'Shabazz Napier', 'PJ Hairston', "D'Angelo Russell", 'Justise Winslow',
	'Stanley Johnson', 'Trey Lyles', 'Cameron Payne', 'Myles Turner', 'Devin Booker', 'Sam Dekker',
	'Bobby Portis', 'Kelly Oubre', 'Terry Rozier', 'Rashad Vaughn', 'Jerian Grant', 'Justin Anderson',
	'Frank Kaminsky', 'Norman Powell', 'Richaun Holmes', 'Josh Richardson', 'Andrew Harrison',
	'Pat Connaughton', 'TJ McConnell', 'Brandon Ingram', 'Jaylen Brown', 'Buddy Hield', 'Marquese Chriss',
	'Domantas Sabonis', 'Jamal Murray', 'Caris LeVert', 'Patrick McCaw', 'Taurean Prince',
	'Malcolm Brogdon', 'Yogi Ferrell'
]

# GLOBAL VARIABLES
# Contains the average number of 3-point attempts for the league.
# Ranges from the 2009-10 season to the 2017-18 season.
LEAGUE_FG3A = {}

# [name, year, team, fg3, fg3a, fg3_pct, team_ortg, team_fg3a, lg_fg3a]
# Contains the rows that will eventually be written into the CSV file.
PLAYER_STATS = []


'''
Parameters:
* soup: the HTML parser for the webpage
* table_id: the id that uniquely identifies the table on the webpage

Function: Helper function to grab a specific table from a webpage.
'''
def get_table(soup, table_id):
	table = soup.find(id=table_id)

	# Actual data is embedded in HTML comment tags, so a wrapper is needed
	# to remove the tags.
	wrapper = BeautifulSoup(str(table), 'html.parser')
	table_content = wrapper.find_all(text=lambda text:isinstance(text, Comment))[0]
	
	table_soup = BeautifulSoup(str(table_content), 'html.parser')
	return table_soup


'''
Function: Update the global variable LEAGUE_FG3A.
'''
def get_lg_fg3a():
	
	print 'Acquiring league average 3-point attempts...'
	
	for year in range(2010, 2019):
		year_url = NBA_BASE_URL + '/leagues/NBA_' + str(year) + '.html'
		response = urllib2.urlopen(year_url)
		lg_soup = BeautifulSoup(response, 'html.parser')
		lg_fg3a_soup = get_table(lg_soup, 'all_team-stats-per_game')
		
		lg_avg_row = lg_fg3a_soup.select_one('tfoot')
		lg_avg_soup = BeautifulSoup(str(lg_avg_row), 'html.parser')

		lg_fg3a = lg_avg_soup.select_one('td[data-stat="fg3a"]').get_text()

		season = str(year-1) + '-' + str(year)[2:]
		LEAGUE_FG3A[season] = lg_fg3a

	print 'Success.'


def parse_players():

	print 'Parsing player array...'

	# Some players have different endings to their player webpage (e.g. '02' instead of '01').
	# This accounts for the variability in this ending.	
	nba_2 = [
		'Danny Green', 'Patty Mills', 'Wesley Matthews', 'Jordan Crawford', 'Derrick Williams',
		'Kemba Walker', 'Markieff Morris', 'Jordan Hamilton', 'Tobias Harris', 'Harrison Barnes',
		'Tim Hardaway Jr.', 'Jerian Grant', 'Jaylen Brown', 'Taurean Prince', 'Gerald Henderson',
		'PJ Hairston'
	]
	nba_3 = ['Brandon Knight', 'Marcus Morris', 'Jeffery Taylor', 'Andre Roberson']
	nba_4 = ['Chris Johnson', 'Stanley Johnson']	

	ncaa_2 = [
		'Gerald Henderson', 'James Johnson', 'Derrick Williams', 'Jordan Hamilton', 'Josh Richardson',
		'Reggie Bullock'
	]
	ncaa_3 = ['James Anderson', 'Ryan Kelly']
	ncaa_4 = ['Mike Scott']	



	for player in PLAYERS:

		print 'Extracting data for ' + player + '...'

		nba_fg3_pct, nba_avg_team_ortg, nba_relative_team_fg3a = parse_nba(player, nba_2, nba_3, nba_4)
		ncaa_fg3a, ncaa_fg3_pct, ncaa_ft_pct, avg_sos, ncaa_avg_team_fg3a = parse_ncaa(player, ncaa_2, ncaa_3, ncaa_4)
		
		print 'Data for ' + player + ' successfully extracted.'
		PLAYER_STATS.append([player, ncaa_fg3a, ncaa_fg3_pct, ncaa_ft_pct, avg_sos, ncaa_avg_team_fg3a, nba_avg_team_ortg, nba_relative_team_fg3a, nba_fg3_pct])



def parse_nba(player, players_2, players_3, players_4):
	
	# Some players have different endings to their player webpage (e.g. '02' instead of '01').
	# This accounts for the variability in this ending.

	end = '01'
	if player in players_2:
		end = '02'
	elif player in players_3:
		end = '03'
	elif player in players_4:
		end = '04'

	player_name = player.lower().replace("'", '').split(' ')
	player_url = player_name[1][0:5] + player_name[0][0:2] + end
	url = NBA_BASE_URL + '/players/' + player_name[1][0] + '/' + player_url + '.html'

	response = urllib2.urlopen(url)
	player_soup = BeautifulSoup(response, 'html.parser')

	return extract_nba(player_soup, player)	


'''
Parameters:
* player_soup: the HTML parser for the player's webpage
* name: the player's name (e.g. Stephen Curry)

Function: Extract the data in the Totals table in player's webpage. Updates the global
variable PLAYER_STATS.
'''
def extract_nba(player_soup, name):
	tot_soup = get_table(player_soup, 'all_totals')

	foot_soup = BeautifulSoup(str(tot_soup.select_one('tfoot > tr')), 'html.parser')

	#g = int(foot_soup.select_one('td[data-stat="g"]').get_text())
	fg3 = int(foot_soup.select_one('td[data-stat="fg3"]').get_text())
	fg3a = int(foot_soup.select_one('td[data-stat="fg3a"]').get_text())
	fg3_pct = 100. * fg3 / fg3a
	avg_team_ortg = 0.
	avg_team_fg3a = 0.
	avg_lg_fg3a = 0.

	yrs = 0
	prev_yr = ''
	for row in tot_soup.select('tbody > tr'):

		row_soup = BeautifulSoup(str(row), 'html.parser')

		team = row_soup.select_one('td > a').get_text()
		if team == 'NBA':
			continue

		yrs += 1
		team_ortg, team_fg3a = extract_team_stats(row_soup.select_one('td > a')['href'])
		avg_team_ortg += float(team_ortg)
		avg_team_fg3a += float(team_fg3a)

		year = row_soup.select_one('th > a').get_text()
		if prev_yr != year:
			avg_lg_fg3a += float(LEAGUE_FG3A[year])

		prev_yr = year

	avg_team_ortg /= yrs
	relative_team_fg3a = avg_team_fg3a / avg_lg_fg3a
	#PLAYER_STATS.append([name, fg3, fg3a, fg3_pct, avg_team_ortg, avg_team_fg3a, avg_lg_fg3a])
	return fg3_pct, avg_team_ortg, relative_team_fg3a


'''
Parameters:
* extension: the referential link to a given player's team page for a specific season.

Function: Extracts a team's Offensive Rating and 3-point attempts per game.
'''
def extract_team_stats(extension):
	team_url = NBA_BASE_URL + extension
	response = urllib2.urlopen(team_url)

	team_soup = BeautifulSoup(response, 'html.parser')

	# Get team offensive rating
	ortg_soup = get_table(team_soup, 'all_team_misc')
	ortg_row = ortg_soup.select_one('tbody > tr')
	ortg = ortg_row.select_one('td[data-stat="off_rtg"]').get_text()

	# Get team 3 point attempts per game
	team_fg3_soup = get_table(team_soup, 'all_team_and_opponent')
	team_fg3_row = team_fg3_soup.select('tbody > tr')[1]
	row_soup = BeautifulSoup(str(team_fg3_row), 'html.parser')
	fg3a_g = row_soup.select_one('td[data-stat="fg3a_per_g"]').get_text()

	return ortg, fg3a_g		




def parse_ncaa(player, players_2, players_3, players_4):

	# Some players have different endings to their player webpage (e.g. '02' instead of '01').
	# This accounts for the variability in this ending.
	players_2 = [
		'Gerald Henderson', 'James Johnson', 'Derrick Williams', 'Jordan Hamilton', 'Josh Richardson',
		'Reggie Bullock'
	]
	players_3 = ['James Anderson', 'Ryan Kelly']
	players_4 = ['Mike Scott']


	end = '1'
	if player in players_2:
		end = '2'
	elif player in players_3:
		end = '3'
	elif player in players_4:
		end = '4'

	player_name = player.lower().replace("'", '').replace('.', '').split(' ')
	player_url = ''
	if len(player_name) == 3:
		player_url = player_name[0] + '-' + player_name[1] + '-' + player_name[2] + '-' + end
	else:
		if player == 'Patty Mills':
			player_url = 'patrick-' + player_name[1] + '-' + end
		elif player == 'Wesley Johnson':
			player_url = 'wes-' + player_name[1] + '-' + end
		elif player == 'Yogi Ferrell':
			player_url = 'kevin-' + player_name[1] + '-' + end 
		else:
			player_url = player_name[0] + '-' + player_name[1] + '-' + end 
	url = NCAA_BASE_URL + '/cbb/players/' + player_url + '.html'

	response = urllib2.urlopen(url)
	player_soup = BeautifulSoup(response, 'html.parser')

	return extract_ncaa(player_soup, player)


'''
Parameters:
* player_soup: the HTML parser for the player's webpage
* name: the player's name (e.g. Stephen Curry)

Function: Extract the data in the Totals table in player's webpage. Updates the global
variable PLAYER_STATS.
'''
def extract_ncaa(player_soup, name):
	tot_soup = get_table(player_soup, 'all_players_totals')

	foot_soup = BeautifulSoup(str(tot_soup.select_one('tfoot > tr')), 'html.parser')
	per_soup = BeautifulSoup(str(player_soup.find(id='players_per_game')), 'html.parser')
	per_foot = BeautifulSoup(str(per_soup.select_one('tfoot > tr')), 'html.parser')

	#g = int(foot_soup.select_one('td[data-stat="g"]').get_text())
	fg3 = int(foot_soup.select_one('td[data-stat="fg3"]').get_text())
	fg3a = int(foot_soup.select_one('td[data-stat="fg3a"]').get_text())
	ft = int(foot_soup.select_one('td[data-stat="ft"]').get_text())
	fta = int(foot_soup.select_one('td[data-stat="fta"]').get_text())
	avg_sos = float(per_foot.select_one('td[data-stat="sos"]').get_text())
	fg3_pct = 100. * fg3 / fg3a
	ft_pct = 100. * ft / fta
	avg_team_fg3a = 0.

	tot_g = 0
	tot_fg3a = 0
	for row in tot_soup.select('tbody > tr'):
		row_soup = BeautifulSoup(str(row), 'html.parser')

		school_g, school_fg3a = extract_school_stats(row_soup.select_one('td > a')['href'])

		tot_g += school_g
		tot_fg3a += school_fg3a

		#PLAYER_STATS.append([name, year, school, conf, fg3, fg3a, fg3_pct, sos, school_g, school_fg3, school_fg3a])

	avg_team_fg3a = 1. * tot_fg3a / tot_g

	return fg3a, fg3_pct, ft_pct, avg_sos, avg_team_fg3a


'''
Parameters:
* extension: the referential link to a given player's team page for a specific season.

Function: Extracts a school's games played, and calculates its 3 point makes and attempts per game.
'''
def extract_school_stats(extension):
	team_url = NCAA_BASE_URL + extension
	response = urllib2.urlopen(team_url)

	school_soup = BeautifulSoup(response, 'html.parser')

	school_stats = BeautifulSoup(str(school_soup.find(id='team_stats')), 'html.parser')
	school_row = school_stats.select_one('tbody > tr')
	row_parser = BeautifulSoup(str(school_row), 'html.parser')

	school_g = int(row_parser.select_one('td[data-stat="g"]').get_text())
	#school_fg3 = float(row_parser.select_one('td[data-stat="fg3"]').get_text()) / school_g
	school_fg3a = int(row_parser.select_one('td[data-stat="fg3a"]').get_text())

	return school_g, school_fg3a



'''
Function: Export the data in PLAYER_STATS into a CSV file.
'''
def export_stats():
	filename = 'data.csv'
	
	print 'Exporting data to ' + filename + '...'

	file_handle = open(filename, 'w')
	writer = csv.writer(file_handle)
	writer.writerow(['name', 'ncaa_fg3a', 'ncaa_fg3_pct', 'ncaa_ft_pct', 'ncaa_sos', 'ncaa_team_fg3a_avg',
					'nba_avg_team_ortg', 'nba_relative_team_fg3a', 'nba_fg3_pct'])
	writer.writerows(PLAYER_STATS)

	print 'Success.'


def main():
	get_lg_fg3a()
	parse_players()
	print 'Player parsing finished.'

	export_stats()
	print 'Exiting program.'


if __name__ == '__main__':
	main()

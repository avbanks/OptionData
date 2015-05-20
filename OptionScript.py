import pandas as pd
import urllib2
import time
from bs4 import BeautifulSoup
import datetime
from dateutil.parser import parse
import re
import mibian 
from datetime import datetime
from datetime import timedelta
from datetime import date








def GetOptionDates(stock):
	# try:
	stock = str(stock).upper()

        
	
	unFormatDatedList = []
	timeStampList = []
	urlToVisit = 'http://finance.yahoo.com/q/op?s=+'+stock+'+Options'
	sourceCode = urllib2.urlopen(urlToVisit).read()
	soup = BeautifulSoup(sourceCode)

	formatDateList = []
	for optionTag in soup.findAll('option'):
		unFormatDatedList.append(optionTag.text)
		
		dateParse = parse(optionTag.text)
		dTimeStamp =  int(time.mktime(dateParse.timetuple()))
		timeStampList.append(dTimeStamp)
	for date in unFormatDatedList:
		date = str(date)
		formatDateList.append(date)
	sPrice = soup.find(id='yfs_l84_{}'.format(stock))
	sPrice = sPrice.text

	print 'Stock Price ', sPrice

	

	zipped = zip(formatDateList,timeStampList)
	
	print formatDateList
	return (zipped,sPrice)
		

	# except Exception,e:
	# 	print 'main loop',str(e)

def GetOptionStrikes(stock,zipped,userDate):
	userDate = str(userDate)

	for everytuple in zipped:
		if everytuple[0] == userDate:
			dTimeStamp = everytuple[1]
	
	dTimeStamp = str(dTimeStamp)
	
	
	urlToVisit = 'http://finance.yahoo.com/q/op?s='+stock+'&datew={}'.format(dTimeStamp)
	sourceCode = urllib2.urlopen(urlToVisit).read()
	soup = BeautifulSoup(sourceCode)
	strikeList = []
	tickerList = []
	convertList = []
	finalTickerList = []
	#print soup
	
	for strikeTag in soup.find_all(href=re.compile("strike=")):
		
		stockStrike = strikeTag.text
		stringStock = str(stockStrike)
		strikeList.append(float(stringStock))

	
	for div in soup.findAll('div', {'class': 'option_entry Fz-m'}):
		a = div.findAll('a')
		tickerList.append(a)
	tickerList = filter(None,tickerList)
	
	for everything in tickerList:
		e = str(everything)
		convertList.append(e)
	
	for everyLine in convertList: 
		tickextract = everyLine.split('>')[1].split('<')[0]
		finalTickerList.append(tickextract)
	print 'Available Strikes'
	print strikeList
		


	zipped = zip(strikeList,finalTickerList)
	
	
	return zipped
	
	
	
def GetOptionData(strike,zipped):	
	matchedList = []

	for everytuple in zipped:
		if strike == everytuple[0]:
			matchedList.append(everytuple)
	callTicker = matchedList[0][1]
	putTicker = matchedList[1][1]
	



	
	return (callTicker,putTicker)

	

stockToGet = raw_input('Type in stock ticker ')
optDates = GetOptionDates(stockToGet)
getDtime = raw_input('Type Date  ')
optStirkes = GetOptionStrikes(stockToGet,optDates[0],getDtime)
getSrike = input('Type Option Strike  ')
#GetOptionData(getSrike,GetOptionStrikes(stockToGet,getDtime))

optData = GetOptionData(getSrike,optStirkes)

# userTimeStamp = input("What is the timestamp?")
# GetOptionStrikes(stockToGet,userTimeStamp)

sDtime = str(getDtime)
date_object = datetime.strptime(sDtime, '%B %d, %Y')



optionTicker = optData[0]
stockTicker = stockToGet
strike = getSrike
currentDay = date.today()
currentDay = datetime.strptime(currentDay.strftime('%Y%m%d'), '%Y%m%d')
dTe = date_object - currentDay
dTe = str(dTe)
dTe = int(dTe.split()[0])



urlToVisit = 'http://finance.yahoo.com/q/op?s={}&strike={}'.format(stockTicker,strike)
sourceCode = urllib2.urlopen(urlToVisit).read()
impliedVolatilityRaw = sourceCode.split('contractSymbol":"{}",'.format(optionTicker))[1].split("impliedVolatilityRaw")[1].split(',')[0].split(":")[1]
bidrough = sourceCode.split('contractSymbol":"{}",'.format(optionTicker))[1].split("bid")[1].split(',')[0].split(":")[1]
askrough = sourceCode.split('contractSymbol":"{}",'.format(optionTicker))[1].split("ask")[1].split(',')[0].split(":")[1]
optVolume= int(sourceCode.split('contractSymbol":"{}",'.format(optionTicker))[1].split("volume")[1].split(',')[0].split(":")[1])
ask = float(askrough.split('"')[1].split('"')[0])
bid = float(bidrough.split('"')[1].split('"')[0])
iv = float(impliedVolatilityRaw) * 100

print 'Ask',Ask
print 'Bid',Bid
print 'Implied Volatility',Impled Volatility
print 'Option Volume',Option Voluem

strikeF = float(strike)
stockPrice = float(optDates[1])
strike = float(strike)















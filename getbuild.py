import requests
from concurrent.futures import ThreadPoolExecutor


def manualbuild(itemlist):
	piece = []

	def returnitem(item):
		piece_i = getitem(item)
		if piece_i == 'masterworkCheck':
			return getitem(item, input('Enter the masterwork level: '))
		else:
			return piece_i

	def getitem(item, masterwork=None):
		itemdict = eval(requests.get('https://www.ohthemisery.tk/api/items').text)

		if masterwork is None:
			for thing in itemdict:
				if item in thing:
					if itemdict[thing]['region'] == 'Ring':
						return 'masterworkCheck'
					else:
						return itemdict[item]

		elif masterwork is not None:
			item = item + '-' + str(masterwork)
			return itemdict[item]

	for x in range(7):
		match x:
			case 0:
				piece = returnitem(input('Enter the mainhand: '))
			case 1:
				piece = returnitem(input('Enter the offhand: '))
			case 2:
				piece = returnitem(input('Enter the helmet: '))
			case 3:
				piece = returnitem(input('Enter the mainhand: '))
			case 4:
				piece = returnitem(input('Enter the mainhand: '))
			case 5:
				piece = returnitem(input('Enter the mainhand: '))
			case 6:
				piece = returnitem(input('Enter the mainhand: '))

		itemlist.append(piece)

	no_repeats = []
	repeatcheck = []
	for index, gearpiece in enumerate(itemlist):
		if gearpiece['name'] not in repeatcheck:
			repeatcheck.append(gearpiece['name'])
			no_repeats.append(gearpiece)
		else:
			pass

	return no_repeats


def getbuild(items):
	outputted_build = []
	n_threads = len(items)
	with ThreadPoolExecutor(n_threads) as executor:
		_ = [executor.submit((lambda item: outputted_build.append(eval(requests.get('https://www.ohthemisery.tk/api/items')
							.text)[item]))(piece)) for piece in items]
	return outputted_build


class InfoList:
	def __init__(self, inputlist):
		self.inputlist = inputlist
		self.stats = getbuild(inputlist)

	def returnstats(self):
		return self.stats

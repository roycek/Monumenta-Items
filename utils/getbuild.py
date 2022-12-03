import json
from concurrent.futures import ThreadPoolExecutor


class InfoList:
	def __init__(self, inputlist):
		self.inputlist = inputlist
		self.stats = getbuild(inputlist)

	def returnstats(self):
		return self.stats


def getbuild(items):
	outputted_build = []
	n_threads = len(items) if len(items) > 0 else 1
	with open("utils/itemData.json", "r") as f:
		data = json.load(f)
		with ThreadPoolExecutor(n_threads) as executor:
			_ = [executor.submit((lambda item: outputted_build.append(data[item]))(piece)) for piece in items]
	return outputted_build


def getitemstats(charmlist, gearlist):
	stats = []
	n_threads = len([charmlist, gearlist]) if len([charmlist, gearlist]) > 0 else 1
	with ThreadPoolExecutor(n_threads) as executor:
		_ = [executor.submit((lambda items: stats.append(InfoList(items).returnstats()))(itemlist))
							for itemlist in [charmlist, gearlist]]

		return stats

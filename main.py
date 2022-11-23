from concurrent.futures import ThreadPoolExecutor
import getbuild
import tmp_gear


def getitemstats(charmlist, gearlist):
    stats = []
    n_threads = len([charmlist, gearlist])
    with ThreadPoolExecutor(n_threads) as executor:
        _ = [executor.submit((lambda items: stats.append(getbuild.InfoList(items).returnstats()))(itemlist))
             for itemlist in [charmlist, gearlist]]

        return [item for sublist in stats for item in sublist]


'''

Changelog 1.0 - 2022-11-23:

Edit the charms and gear in tmp_gear to choose your own, and print the result of the following to get the stats.
getitemstats(tmp_gear.Gear.charms, tmp_gear.Gear.gear))

Alternatively, print the following to manually input body gear, mainhand and offhand:
getbuild.manualbuild([])

Following updates will implement a UI for user interaction

'''

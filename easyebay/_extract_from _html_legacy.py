import csv
from prettytable import PrettyTable
import re
import requests

'''
api: https://www.ebay.com/sch/i.html?_nkw={keyword}&_pgn={pageNum}&_ipg={itemPerPage}&_udhi={maxPrice}&_udlo={minPrice}&LH_ItemCondition={condition}
'''


class searchRequest():
    class condition():
        new: str = "1000"
        used: str = "3000"
        openbox: str = "1500"
        certificated_refurbish: str = "2000"
        seller_refurbish: str = "2500"
        parts: str = "7000"
        none: str = ""
        splitter: str = "%7C"

    def search(self, keyword, pageNum="", itemPerPage="", maxPrice="", minPrice="", conditions=[]):
        if pageNum:
            pageNum = "&_pgn="+pageNum
        if itemPerPage:
            itemPerPage = "&_ipg="+itemPerPage
        if maxPrice:
            maxPrice = "&_udhi="+maxPrice
        if minPrice:
            minPrice = "&_udlo="+minPrice
        if conditions:
            temp = "&LH_ItemCondition="+conditions[0]
            for item in conditions[1::]:
                temp = temp+self.condition.splitter+item
            conditions = temp
        else:
            conditions = ""
        return str(requests.get(f"https://www.ebay.com/sch/i.html?_nkw={keyword}{pageNum}{itemPerPage}{maxPrice}{minPrice}{conditions}").content)


def resp2data(resp: str):
    patternStr = "(?<=class=s-item__link href).*?(?=</div><span class=\"s-item__detail s-item__detail--secondary\">)"
    pattern = re.compile(patternStr)
    matched = pattern.findall(resp)
    items = []
    itemPrice = re.compile("(?<=<span class=s-item__price>).*?(?=</span>)")
    itemName = re.compile(
        r"(?<=<span role=heading aria-level=3>).*?(?=</span></div><span class=clipped>)")
    itemLink = re.compile(r".*?(?=><div class=s-item__title>)")
    for i in matched:
        price = itemPrice.findall(i)[0].replace("<span class=DEFAULT> to ", "")
        if "<a" in price:
            price = "See Prie"
        name = itemName.findall(i)[0].split("</span>")[-1].replace("\\", "")
        link = itemLink.findall(i)[0][1::]
        items.append({"price": price, "name": name, "link": link})
    return items


sr = searchRequest()
result = sr.search(keyword="ssd", maxPrice="20", itemPerPage="260")
items = resp2data(result)
items.pop(0)

# table = PrettyTable(['name', 'price', 'url'])

# for each in items:
#     table.add_row([each["name"][0:20]+"...", each['price'], each["link"][0:20]+"..."])

# print(table)
pricesheet = open('prices.csv', mode='a')
writer = csv.writer(pricesheet, delimiter=',',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL)

writer.writerow(['Name', 'Price', 'url'])
for each in items:
    writer.writerow([each["name"], each["price"], each["link"]])
pricesheet.close()
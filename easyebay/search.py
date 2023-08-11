import re
import requests

from bs4 import BeautifulSoup

class condition():
    '''
    The condition of item and its corresponding code
    '''
    new: str = "1000"
    used: str = "3000"
    openbox: str = "1500"
    certificated_refurbish: str = "2000"
    seller_refurbish: str = "2500"
    parts: str = "7000"
    splitter: str = "%7C"


def search(keyword: str, pageNum="", itemPerPage="", maxPrice="", minPrice="", conditions=[], reqHeaders={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}):
    '''
    To compose request to eBay. This function will gather all the parameters and compose request
    api: https://www.ebay.com/sch/i.html?_nkw={keyword}&_pgn={pageNum}&_ipg={itemPerPage}&_udhi={maxPrice}&_udlo={minPrice}&LH_ItemCondition={condition}

    :param keyword: string, equivalent to eBay search bar
    :param pageNum: string, the page number
    :param itemPerPage: string, how many items per page (range: 1-260)
    :param maxPrice: string, the maximum price
    :param minPrice: string, the minimum price
    :param conditions: [condition object], a literable object contains condition object
    :param reqHeaders: dict, the header add to requests
    :return: string, response in html form
    '''
    if pageNum:
        pageNum = "&_pgn=" + pageNum
    if itemPerPage:
        itemPerPage = "&_ipg=" + itemPerPage
    if maxPrice:
        maxPrice = "&_udhi=" + maxPrice
    if minPrice:
        minPrice = "&_udlo=" + minPrice
    if conditions:
        temp = "&LH_ItemCondition=" + conditions[0]
        for item in conditions:
            temp = temp + condition.splitter + item
        conditions = temp
    else:
        conditions = ""
    return requests.get(
        f"https://www.ebay.com/sch/i.html?_nkw={keyword}{pageNum}{itemPerPage}{maxPrice}{minPrice}{conditions}",
        headers=reqHeaders).text


# if item is not None, then format it
_noneOrWithData = lambda item: item.get_text().replace("\n", "") if item is not None else None


def _removeExtraSpace(text):
    '''
    Remove extra spaces in the end of a string
    :param text: string
    :return: string
    '''
    if not text:
        return text
    new = ""
    for charIndex in range(len(text)):
        if (charIndex < len(text) - 1 and text[charIndex] == " " and text[charIndex + 1] == " ") or (
                text[charIndex] == " " and charIndex == len(text) - 1):
            continue
        else:
            new += text[charIndex]
    return new


class item():
    title: str
    condition: str
    price: str
    seller: list
    shipping: str
    returns: str
    sold: str
    url: str
    image: str


def parseSearch(html):
    '''
    Parse eBay search result
    :param html: string
    :return: dict
    '''
    first = True
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li", class_="s-item s-item__pl-on-bottom")
    data = []
    for item in items:
        if first:
            first = False
            continue
        thisItem = item()
        thisItem.title = _removeExtraSpace(item.find("div", class_="s-item__title").get_text().replace("\n", ""))
        thisItem.condition = item.find("span", class_="SECONDARY_INFO").get_text()
        thisItem.price = item.find("span", class_="s-item__price").get_text().replace("\n", "")
        seller = item.find("span", class_="s-item__seller-info-text").get_text().split(" ")
        seller[1] = int(re.sub(r'[(),]', '', seller[1]))  # Convert the sales amount from str to int
        thisItem.seller = seller
        thisItem.shipping = _removeExtraSpace(_noneOrWithData(item.find("span", class_="s-item__shipping")))
        thisItem.returns = _removeExtraSpace(_noneOrWithData(item.find("span", class_="s-item__free-returns")))
        thisItem.sold = _noneOrWithData(item.find("span", class_="s-item__quantitySold"))
        urls = item.find("div", class_="s-item__image")
        thisItem.url = urls.find("a").get("href")
        thisItem.image = urls.find("img").get("src")
        data.append(thisItem)
    return data

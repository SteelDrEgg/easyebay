<div align="center">

# Easy eBay

*A library for scraping items from eBay*

</div>

## To begin with

#### install
```shell
pip install easyebay
```

##### Run
```python
import easyebay

result = easyebay.search(keyword="4090",
                         pageNum="1",
                         maxPrice="1000",
                         minPrice="500",
                         sortBy=easyebay.sort.bestMatch,
                         conditions=[easyebay.condition.used])

parsed, currentMaxPage = easyebay.parseSearch(result)

for item in parsed:
    print(item.title, item.price, item.shipping, item.url)
```
Sample output
```text
YASKAWA CDBR-4090B B... $989.99 None https://www.ebay...
LOT OF 5 Motorola RS... $769.69 None https://www.ebay...
MELLTRONICS 222-4090... $750.00 None https://www.ebay...
...
```

#### Explain
`easyebay.search` returns the html, and easyebay.parseSearch returns `easyebay.item` object. This is the definition of
item object

```python
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
```

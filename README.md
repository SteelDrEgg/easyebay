<div style="text-align: center">

# Easy eBay

*A library for scraping items from eBay*

</div>

## To begin with

Here is a sample code

##### Example 1

```python
import easyebay

result = easyebay.search(keyword="4090",
                         pageNum="1",
                         maxPrice="1000",
                         minPrice="500",
                         conditions=[easyebay.condition.used])

parsed = easyebay.parseSearch(result)

for item in parsed:
    print(item.title, item.price, item.shipping, item.url)
```

Here's a sample output

```text
YASKAWA CDBR-4090B B... $989.99 None https://www.ebay...
LOT OF 5 Motorola RS... $769.69 None https://www.ebay...
MELLTRONICS 222-4090... $750.00 None https://www.ebay...
...
```

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
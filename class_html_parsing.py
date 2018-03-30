import re

from bs4 import BeautifulSoup
from typing import NewType

ITEM_HTML = '''<html><head></head><body>
<li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
    <article class="product_pod">
            <div class="image_container">
                    <a href="catalogue/a-light-in-the-attic_1000/index.html"><img src="media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg" alt="A Light in the Attic" class="thumbnail"></a>
            </div>
                <p class="star-rating Three">
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                </p>
            <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a></h3>
            <div class="product_price">
        <p class="price_color">£51.77</p>
<p class="instock availability">
    <i class="icon-ok"></i>
        In stock
</p>
    <form>
        <button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button>
    </form>
            </div>
    </article>
</li>
</body></html>
'''

class ParsedItemLocator:
    """
    Locators for an item in the HTML page.
    This allows us to easily see what our code will be looking at
    as well as change it quickly if we notice it is now different.
    """

    NAME_LOCATOR = 'article.product_pod h3 a'
    LINK_LOCATOR = 'article.product_pod h3 a'
    PRICE_LOCATOR = 'article.product_pod p.price_color'
    RATING_LOCATOR = 'article.product_pod p.star-rating'


class ParsedItem:
    """
    A class to take in an HTML page (or part of), and find properties of an item in it.
    """

    def __init__(self, page):
        self.soup =  BeautifulSoup(page, 'html.parser')

    @property
    def name(self):
        locator = ParsedItemLocator.NAME_LOCATOR
        item_link = self.soup.select_one(locator)
        item_name = item_link.attrs['title']
        # can do item_name = soup.select_one(locator).['title']
        return(item_name)

    @property
    def link(self):
        locator = ParsedItemLocator.LINK_LOCATOR
        item_link = self.soup.select_one(locator).attrs['href']
        return(item_link)

    @property
    def price(self):
        locator =  ParsedItemLocator.PRICE_LOCATOR
        item_price = self.soup.select_one(locator).string
        pattern ='£([0-9]+\.[0-9]+)'
        matcher = re.search(pattern, item_price)
        print(matcher.groups())
        return(float(matcher.group(1)))

    @property
    def rating(self):
        locator = ParsedItemLocator.RATING_LOCATOR
        star_rating_tag= self.soup.select_one(locator)
        """
        star_rating_tag =
        <p class="star-rating Three">
            <i class="icon-star"></i>
            <i class="icon-star"></i>
            <i class="icon-star"></i>
            <i class="icon-star"></i>
            <i class="icon-star"></i>
            </p>
        """
        classes = star_rating_tag.attrs['class']
        rating = [r for r in classes if r != 'star-rating']
        return(rating[0])


parsed_item = ParsedItem(ITEM_HTML)
print(parsed_item.name)
print(parsed_item.link)
print(parsed_item.price)
print(parsed_item.rating)
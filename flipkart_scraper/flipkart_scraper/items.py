# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ListingData(Item):
    title = Field()
    subtitle = Field()
    product_url = Field()
    smart_url = Field()
    product_id = Field()
    image_url = Field()
    total_count = Field()
    next_listing_page_url = Field()
    search_query = Field()
    page = Field()


class UploadedImages(Item):
    product_url = Field()
    product_id = Field()
    file_name = Field()
    image_url = Field()


class PageNotFound(Item):
    url = Field()

from ..scrape_utils import validate_url
from lxml.html import fromstring
from json import loads


class ListingPage():
    """
    to extract the product details from the listing page or search page
    of flipkart
    usage:
    listing_obj = ListingPage(response.text)
    data = listing_obj.extract_data()
    """
    def __init__(self, response_text):
        self.parser = fromstring(response_text)

    def extract_data(self):
        """
        to parse the json data in response text and return the list of
        all avaiable product details
        """
        json_script = self.parser.xpath('//script[@id="is_script"]/text()')[0]
        json_data = loads(json_script.replace("window.__INITIAL_STATE__ = ", '').strip(';'))
        total_count = self.get_total_count(json_data)
        next_page = self.get_next_page()
        json_dicts = json_data['pageDataV4']['page']['data']['10003']
        final_results = []
        for data_dict in json_dicts:
            element = data_dict.get('elementId')
            if not element:
                continue
            if "PRODUCT_SUMMARY" not in element:
                continue
            data = self.get_products(data_dict, total_count, next_page)
            final_results.extend(data)
        return final_results

    def get_products(self, data_dict, total_count, next_page):
        """
        to return the product details
        """
        products = data_dict['widget']['data']['products']
        total_results = []
        meta_value = {
            "total_count": total_count,
            "next_listing_page_url": next_page
        }
        for product in products:
            product_info = product.get('productInfo')
            if not product_info:
                continue
            result = self.get_product_info(product_info)
            result.update(meta_value)
            total_results.append(result)
        return total_results

    def get_product_info(self, product_info):
        """
        to return the product details inside the
        product info
        """
        value = product_info['value']
        titles = value.get('titles')
        title, subtitle = titles.get('title'), titles.get('subtitle')
        params = product_info['action']['params']
        result = {
            "title": title,
            "subtitle": subtitle,
            "product_url": validate_url(value.get('baseUrl')),
            "smart_url": value.get('smartUrl'),
            "product_id": params.get('productId'),
            "image_url": self.get_image_url(value)
        }
        return result

    def get_image_url(self, value):
        """
        to return the image url of product
        """
        image_list = value.get('media', {}).get('images')
        if not image_list:
            return
        image_raw_url = image_list[0].get('url')
        if not image_raw_url:
            return
        return image_raw_url.replace('{@width}', '612').replace('{@height}', '612').replace('{@quality}', '70')

    def get_total_count(self, json_data):
        """
        to return total count of products for a search
        """
        page_data = json_data['pageDataV4']['page']['pageData']
        if not page_data:
            return
        return page_data['trackingContext']['tracking'].get('maxProductsCount')

    def get_next_page(self):
        """
        return the next page url of search page
        """
        next_page = self.parser.xpath(
            '//span[contains(text(),"Next")]/parent::a/@href'
        )
        return validate_url(next_page[0]) if next_page else None

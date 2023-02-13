from scrapy import Spider, FormRequest, downloadermiddlewares, Request
from copy import deepcopy
from ..scrape_utils import get_headers, get_cookies, upload_data_to_deta_cloud
from ..flipkart_parser.listing_page import ListingPage
from ..items import ListingData, PageNotFound, UploadedImages


class FlipkartSpider(Spider):
    """
    This spider scrapes the product details and images for a search query in
    flipkart.com
    data of product details are saved (as a json file) in both local (folder='outputs')
    and to the Deta Cloud (https://www.deta.sh/) database  using python Deta library.
    The downloaded images are also saved in both local and Deta Drive

    If the Deta Cloud Project Key is not provied in spider inputs args,
    the data will be saved only to the local folder outputs.
    Usage:
    to start the spider use the following command in terminal
    `scrapy crawl flipkart -a deta_cloud_project_key='Your Project Key'`
    if Deta Cloud Project Key is not available then use
    `scrapy crawl flipkart -a deta_cloud_project_key=''`
    """
    name = "flipkart"

    def start_requests(self):
        """
        to initiate request for listing pages
        """
        search_querys = [
            "spider man car toy",
            "spider man mug",
            "spider man jacket",
            "spider man hoodies",
            "spiderman t shirt"
        ]
        for query in search_querys:
            params = {
                'q': query,
            }
            yield FormRequest(
                url="https://www.flipkart.com/search",
                method='GET',
                formdata=params,
                headers=get_headers(),
                # cookies are hard coded cookies, update if retry is high
                cookies=get_cookies(),
                callback=self.parse,
                meta={"meta": {"search_query": query, "page": 1}})

    def parse(self, response):
        """
        to parse the search page or listing page response
        """
        status = self.validate_response(response)
        meta = deepcopy(response.meta['meta'])
        if status == 404:
            self.logger.warning(f'page not found for {meta}')
            yield PageNotFound(url=response.url)
            return
        if not status:
            # retry if blocking or invalid response
            retry_request = self.make_retry(response)
            if retry_request:
                yield retry_request
            return
        listing_obj = ListingPage(response.text)
        try:
            data = listing_obj.extract_data()
        except Exception as error:
            self.logger.warning(f'parser error in query {meta} due to error=[{error}]')
            self.logger.warning('retrying request due to parser error')
            retry_request = self.make_retry(response)
            if retry_request:
                yield retry_request
            return
        for row in data:
            row.update(meta)
            yield ListingData(**row)
            image_url = row['image_url']
            if not image_url:
                self.logger.warning(f'image url found none for {row.get("url")}')
                continue
            yield Request(
                image_url,
                callback=self.parse_images,
                meta={"meta": row})
        # implementing pagination
        next_listing_page_url = row['next_listing_page_url']
        current_page = meta['page'] + 1
        pagination_condition = [not next_listing_page_url, current_page > 25]
        if any(pagination_condition):
            # maximum total products for a single search is 40
            # and maximum valid pagination for a search is 25
            # ie 40*25 pages=1000 products,
            # if we need to extract more than 1000 products
            # we may need to apply other filters
            return
        meta.update({'page': current_page})
        yield Request(
            next_listing_page_url,
            headers=get_headers(),
            cookies=get_cookies(),
            callback=self.parse,
            meta={"meta": meta})

    def parse_images(self, response):
        """
        to parse the image response
        valid image response is saved to both local folder
        outputs and Deta Cloud Database
        """
        status = self.validate_response(
            response,
            response_len_limit=2000,
            request_type='image')
        if status == 404:
            yield PageNotFound(url=response.url)
            return
        if not status:
            # retry if blocking or invalid response
            retry_request = self.make_retry(response)
            if retry_request:
                yield retry_request
            return
        meta = response.meta['meta']
        product_id = meta['product_id']
        image_url = meta['image_url']
        product_url = meta['product_url']
        file_name = f'{product_id}.jpeg'
        file_path = f"outputs/images/{file_name}"
        with open(file_path, "wb") as f:
            f.write(response.body)
        image_upload_status = upload_data_to_deta_cloud(
            self.deta_cloud_project_key, file_name, file_path=file_path)
        if image_upload_status != 'success':
            self.logger.warning(f'image not uploaded to deta for product :[{product_url}] due to [{image_upload_status}]') # noqa
            return
        # save the uploaded images meta data for the successfull upload/download reference
        yield UploadedImages(
            product_url=product_url,
            product_id=product_id,
            file_name=file_name,
            image_url=image_url)


    def validate_response(self, response, response_len_limit=30000, request_type=None):
        """
        to validate the response of request
        """
        status_code = response.status
        response_len = len(response._body) if request_type == 'image' else len(response.text)
        if status_code in [410, 404]:
            self.logger.warning('page not found')
            return 404
        if status_code in [503, 403]:
            self.logger.warning("request blocked!")
            return
        if response_len < response_len_limit:
            self.logger.warning("invalid response")
            return
        return True

    def make_retry(self, response):
        """
        to retry requests for invalid responses or blocking
        after validating the response in validate_response()
        """
        return downloadermiddlewares.retry.get_retry_request(
            response.request,
            spider=self,
            reason="invalid response / blocking",
            max_retry_times=5)

# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .items import ListingData, UploadedImages
from .scrape_utils import connect_to_deta_cloud
from json import dumps


class SaveDataPipeline:
    """
    pipeline to save the data scraped in both local and Deta Cloud Database
    if Deta Cloud Project Key is not passed in spider inputs args or any
    any connection error with Deta Cloud, then
    the scraped data is saved only in local folder `outputs`.
    """
    def open_spider(self, spider):
        """
        This method is called when the spider is opened.
        """
        self.listing_file = open('outputs/listing_data.jsonl', 'w')
        self.upload_status_file = open('outputs/upload_status.jsonl', 'w')

    def close_spider(self, spider):
        """
        This method is called when the spider is closed.
        """
        self.listing_file.close()
        self.upload_status_file.close()

    def process_item(self, item, spider):
        """
        This method is called for every item pipeline component.
        """
        data = {**item}
        listing_data_base, upload_status_data_base = self.deta_cloud_objects(spider)
        if isinstance(item, ListingData):
            self.save_data(data, self.listing_file, listing_data_base)
            return item
        if isinstance(item, UploadedImages):
            self.save_data(data, self.upload_status_file, upload_status_data_base)
            return item

    def save_data(self, data, local_file_obj, cloud_obj):
        """
        save the data to local and Deta cloud database
        (https://docs.deta.sh/docs/base/sdk)
        """
        line = dumps(data) + "\n"
        local_file_obj.write(line)
        if cloud_obj:
            cloud_obj.insert(data)

    def deta_cloud_objects(self, spider):
        """
        to return the database connnection objects
        for the database in Deta Cloud
        https://docs.deta.sh/docs/base/sdk
        data of item `ListingData` saved in database: listing_data
        data of item `UploadedImages` saved in database: upload_status
        """
        # read the Deta cloud project key spider inputs args.
        project_key = spider.deta_cloud_project_key
        listing_data_base = None
        upload_status_data_base = None
        if not project_key:
            # if project key not passed in spider args return
            spider.logger.warning("Deta Cloud Project Key Not Availabale, skipping database upload!")
            return listing_data_base, upload_status_data_base
        try:
            deta_cloud_obj = connect_to_deta_cloud(project_key)
            listing_data_base = deta_cloud_obj.Base("listing_data")
            upload_status_data_base = deta_cloud_obj.Base("upload_status")
        except Exception as error:
            spider.logger.warning(f"!failed connecting to Deta cloud due to error:[{error}]")
        return listing_data_base, upload_status_data_base

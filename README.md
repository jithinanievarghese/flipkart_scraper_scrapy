# Flipkart Web Scraper (Scrapy):

- This repo is a part of following project [Web Scraping with product search relevance using NLP, rules and image classification](https://github.com/jithinanievarghese/product-search-relevance/blob/main/README.md)
- This Scrapy spider scrapes the product details and product images for search queries in
[flipkart.com](https://www.flipkart.com/)
- Data of product details are saved (as a json file) in folder [outputs](https://github.com/jithinanievarghese/flipkart_scraper_scrapy/tree/main/flipkart_scraper/outputs)
- Image data is saved in path : [outputs/images](https://github.com/jithinanievarghese/flipkart_scraper_scrapy/tree/main/flipkart_scraper/outputs/images)
- There is also a provision to save Data in cloud platform Deta Cloud (https://www.deta.sh/) 
- The product details are saved in a [NoSQL database](https://docs.deta.sh/docs/base/py_tutorial) and Image data is saved in [Deta Drive](https://docs.deta.sh/docs/drive/py_tutorial).
- This can be done by passsing the Deta Poject Key in spider args `scrapy crawl flipkart -a deta_cloud_project_key='Your Project Key'`

<p align="center">
  <img width="800" height="400" src="https://user-images.githubusercontent.com/78400305/218429824-fa260d27-6216-41b4-8580-df280080a587.png">
</p>

<p align="center">
  <img width="800" height="400" src="https://user-images.githubusercontent.com/78400305/218429848-9448db19-2f03-4f2d-975b-5413bc7dfe61.png">
</p>

# Usage:
- Install Requirements `pip3 install -r requirements.txt`
- Go to the project’s top level directory and run `scrapy crawl flipkart -a deta_cloud_project_key='Your Project Key'`
- if we dont have deta project key then use `scrapy crawl flipkart -a deta_cloud_project_key=''`

# Scraping flow:
<p align="center">
  <img src="https://user-images.githubusercontent.com/78400305/218444837-86e1d0e6-a7f6-4641-8e11-872444aa85c6.png">
</p>

# Resources
- https://docs.scrapy.org/en/latest/intro/tutorial.html
- https://docs.deta.sh/docs/home



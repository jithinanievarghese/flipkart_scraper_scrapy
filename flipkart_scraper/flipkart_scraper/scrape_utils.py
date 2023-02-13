from user_agent import generate_user_agent
from deta import Deta


def validate_url(slug):
    """
    add home url to slug
    """
    if not slug:
        return
    if slug.startswith("http"):
        return slug
    return "https://www.flipkart.com/" + slug.lstrip('/')


def get_headers():
    """
    to return headers for requests
    """
    # generate random user agent for each session to reduce blocking
    user_agent_ = generate_user_agent(os=('mac', 'linux'))
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image'
                  '/avif,image/webp,image/apng,*/*;q=0.8,application/'
                  'signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent_,
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }


def get_cookies():
    """
    to return hardcoded cookies to pass in requests to reduce blocking
    """
    return {
        'T': 'TI167628137272100330427748646103036168439518973478993796976970308356',
        '_pxff_cc': 'U2FtZVNpdGU9TGF4Ow==',
        '_pxvid': 'c9ea9c39-ab82-11ed-bb6b-657a44545059',
        '_pxff_idp_c': '1,s',
        '_pxff_ddtc': '1',
        'AMCV_17EB401053DAF4840A490D4C%40AdobeOrg': '-227196251%7CMCIDTS%7C19402%7CMCMID%7C58599916053924807742208566410376918001%7CMCAAMLH-1676886173%7C12%7CMCAAMB-1676886173%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1676288573s%7CNONE%7CMCAID%7CNONE',
        '__pxvid': 'ca2cc13b-ab82-11ed-8141-0242ac120002',
        '_px3': '168d50b033c8ab9e1bb30d430aaac3d4831aa602301bfba38608e5b6d37bbad7:00u4Ax9WWJtiblUHBxPh8+MOLN5rLPmz7+WcX5KGBxO3C+s63bTVjJHlA5trMcd/IX1/p0oE2FBmeXv2GJTzOg==:1000:1M35kwa42XwzyhS+b4KBaAXgux5IH9gqFhT3qH/lyRaKzq5BbrLVmIykFnc3LgtQGoJ+WSAvnErL/QGJVfTGXgB88/Wh6Nl6DGDPZxK6DJVU9dKjnLy+coE3A5tWHpuEdppTksZV+xO6iA0KTs42mTyW+jDD5VP1w+BUGhqssrTubO5+2rXrxGIu4W9A4bdO5Z88IRc9ulnGpJAuCqy1Zw==',
        '_gcl_au': '1.1.508085066.1676281378',
        'K-ACTION': 'null',
        'SN': 'VID55429F0AFAC4ACD8687C96B031292C9.TOK924D5743D1CE4B8A9848AC6459E8A97F.1676281380.LO',
        'qH': 'c4a0294c6a323bb9',
        'gpv_pn': 'Search%20%3AClothing%20and%20Accessories%7CWinter%20Wear%7CSweatshirts',
        'gpv_pn_t': 'Search%20Page',
        'S': 'd1t16SA8/P0gTPz8/P0E/bGw/P3puClTs6GnoESi9xNiQmzTJCrweBlxw4P3sPy6cXPIGnS9s62Y1Ykj7RijP2+875w==',
    }


def upload_data_to_deta_cloud(project_key, file_name, file_path):
    """
    to upload the image to deta cloud
    """
    if not project_key:
        # if project key not passed in spider args return
        return "Deta Cloud Project Key Not Availabale"
    try:
        deta_cloud_obj = connect_to_deta_cloud(project_key)
        images_folder_obj = deta_cloud_obj.Drive("flipkart_product_images")
        images_folder_obj.put(file_name, path=file_path)
        return 'success'
    except Exception as error:
        return error


def connect_to_deta_cloud(project_key):
    """
    to connect to deta cloud
    """
    return Deta(project_key)

# %%
from src.instances import config, task_two_logger, driver

# %%
# task_two_logger.info(123)
task_one_logger.info(4)

# %%
import json

from src.products_scraper import (
  parse_number_of_pages_from_web_text,
  load_all_products_in_page,
  is_products_website_paginated,
  extract_products_url_and_image_url,
  click_next_page_in_products_website
)

# %%
# if __name__ == '__main__':
"""
Save into JSON file url, image url, grocery category 
and grocery subcategory of every grocery product
"""
with open('./data/categories_and_subcategories_url.json', 'r', encoding = 'utf-8') as f:
  categories_and_subcategories_url_list = json.loads(f.read())

# %%
driver.set_page_load_timeout(config['selenium']['page_load_seconds_timeout'])
products_basic_info = []

for category_dict in categories_and_subcategories_url_list:
  grocery_category = category_dict['grocery_category']
  task_two_logger.info(f'Grocery category: {grocery_category}')

  if not 'subcategories' in category_dict.keys():
    task_two_logger.info('No subcategories available')
    driver.get(category_dict['url'])
    load_all_products_in_page()

    number_of_products_pages = 1
    is_website_paginated =  is_products_website_paginated()

    if is_website_paginated:
      try:
        number_of_products_pages = parse_number_of_pages_from_web_text()
      except:
        continue

    task_two_logger.info(f'Number of products pages: {number_of_products_pages}')

    # Extract each product url and its image url, per products page
    for page_number in range(number_of_products_pages):
      task_two_logger.info(f'Page number: {1 + page_number}')

      if page_number > 0: load_all_products_in_page()

      products_basic_info += extract_products_url_and_image_url(
        grocery_category = grocery_category, grocery_subcategory = None
      )

      try:
        if is_website_paginated: click_next_page_in_products_website()
      except:
        break
  
  else:
    for subcategory_dict in category_dict['subcategories']:
      subcategory_name = subcategory_dict["grocery_category"]
      task_two_logger.info(f'Subcategory: {subcategory_name}')
      driver.get(subcategory_dict['url'])
      load_all_products_in_page()

      number_of_products_pages = 1
      is_website_paginated =  is_products_website_paginated()

      if is_website_paginated:
        try:
          number_of_products_pages = parse_number_of_pages_from_web_text()
        except:
          continue

      task_two_logger.info(f'Number of products pages: {number_of_products_pages}')

      # Extract each product url and its image url, per products page
      for page_number in range(number_of_products_pages):
        task_two_logger.info(f'Page number: {1 + page_number}')

        if page_number > 0: load_all_products_in_page()

        products_basic_info += extract_products_url_and_image_url(
          grocery_category = grocery_category, 
          grocery_subcategory = f"'{subcategory_name}'"
        )

        try:
          if is_website_paginated: click_next_page_in_products_website()
        except:
          break


# %%
products_basic_info

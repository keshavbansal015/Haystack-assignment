# Scrapy.py

Scraping Walmart reviews for Clorox Disinfecting Wipes for the year 2021.

## Libraries:

* Selenium : For browser automation and scraping.
* Undetected_chrome : For dodging blockers on website.
* Chrome_webdriver : Selenium essential
* Pandas : For dataframe and CSV file

```bash
pip install pandas
pip install selenium 
pip install undetected-chromedriver
```

## Usage

```python
# locating chrome driver
driver = uc.Chrome(executable_path='/path/to/chromedriver', options=options)

# URL for product
keyword = "walmart-product-page-url"

# Sorting order ~ newest-to-oldest
sorting_order = 'submission-desc'

# returns 'output.csv'
output_file = 'output.csv'
```

### Issues faced:

1) Bot blockers on the website : undetected_chromedriver module
2) Slow loading time for the driver
3) Problems with the selenium driver not being able to find the specified elements
4) Scraping likes and dislikes for the few reviews : decided not to scrape them as majority reviews didn't have likes or dislikes mentioned.

### Ways to make it better:

1) Select better element selectors
2) Modify to make to scrape likes and dislikes
3) Give more flexibility in terms of till which date to scrape.
4) Flexibility in-terms of product choice

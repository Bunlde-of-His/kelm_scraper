# Scrapy Project for Real Estate Listings

This Scrapy project is designed to scrape real estate listings from the website `kelm-immobilien.de`.

## How It Works

The `KelmSpider` spider starts from the main listings page and follows each property link to extract relevant data. It uses XPath to extract information such as title, status, pictures, rent price, description, phone number, and email.

The extracted data is then saved in a JSON file in the following directory structure: `Country/Domain/Rental Object/items.json`.

## Setup and Installation

1. **Clone the repository:**

    ```sh
    git clone 
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```



## Running the Spider

To run the spider and start scraping data, use the following command:

```sh
scrapy crawl kelm_spider
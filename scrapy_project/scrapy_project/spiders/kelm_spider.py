import scrapy
from urllib.parse import urljoin


class KelmSpider(scrapy.Spider):
    name = 'kelm_spider'
    start_urls = [
        'https://kelm-immobilien.de/immobilien/',
    ]

    def extract_with_xpath(self, response, query, replace_status=False):
        result = response.xpath(query).xpath('string()').get()
        if result:
            result = result.strip().replace('\n', '').replace('\r', '').replace('\u202f', '')
            if replace_status and 'Status' in result:
                result = result.replace('Status', '').strip()
            return result
        return None

    def extract_price(self, response, query):
        price_text = self.extract_with_xpath(response, query)
        if price_text:
            price = ''.join(filter(str.isdigit, price_text.replace(',', '.')))
            return float(price) if price else None
        return None

    def parse(self, response):
        links = response.xpath('//div[@class="property-thumbnail col-sm-12 vertical"]/a/@href').getall()
        self.log(f'Found {len(links)} property links.')

        for link in links:
            full_url = urljoin(response.url, link)
            yield response.follow(full_url, self.parse_property)

        next_page = response.xpath('//a[contains(@class, "next")]/@href').get()
        if next_page:
            next_page_url = urljoin(response.url, next_page)
            self.log(f'Moving to the next page: {next_page_url}')
            yield response.follow(next_page_url, self.parse)
        else:
            self.log('No more pages found.')

    def parse_property(self, response):
        item = {
            'url': response.url,
            'title': self.extract_with_xpath(response, '//h1[@class="property-title"]'),
            'status': self.extract_with_xpath(response, '//li[@class="list-group-item data-vermietet"]',
                                              replace_status=True),
            'pictures': response.xpath('//img[contains(@src, "wp-content/uploads/immomakler")]/@src').getall(),
            'rent_price': self.extract_price(response, '//li[@class="list-group-item data-hausgeld"]'),
            'description': self.extract_with_xpath(response, '//h2[@class="property-subtitle"]'),
            'phone_number': self.extract_with_xpath(response, '//div[@class="dd col-sm-7 p-tel value"]'),
            'email': self.extract_with_xpath(response, '//div[@class="dd col-sm-7 u-email value"]'),
        }

        yield item

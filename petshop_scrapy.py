import os
import scrapy
import json
import re


class PetshopSpider(scrapy.Spider):
    name = 'petshop'
    start_urls = [
        'Petshop URLs here'
    ]

    def __init__(self, *args, **kwargs):
        super(PetshopSpider, self).__init__(*args, **kwargs)
        self.file = open('petshop_products.json', 'w', encoding='utf-8')
        self.file.write("[\n")  # Start of JSON array

    def parse(self, response):
        products = response.css('.search-product-box')

        for product in products:
            product_url = product.css('.card-body a.p-link::attr(href)').get()
            product_data = product.css('.card-body a.p-link::attr(data-gtm-product)').get()

            if product_url and product_data:
                product_info = json.loads(product_data)

                item = {
                    'product_url': response.urljoin(product_url),
                    'product_name': product_info.get('name'),
                    'product_price': product_info.get('price'),
                    'product_stock': product_info.get('dimension2'),
                    'product_id': product_info.get('id'),
                    'category': product_info.get('category'),
                }

                yield scrapy.Request(url=item['product_url'], callback=self.parse_product_details, meta={'item': item})

        # finding the next page and extracting url
        next_page = response.css('li.page-item.active + li.page-item:not(.disabled) a.page-link::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    # extracting the remaining information
    def parse_product_details(self, response):
        item = response.meta['item']

        brand_info = response.css('div.tab-pane.active .brand-line .col-10 a::text').get()
        item['brand'] = brand_info.strip() if brand_info else 'N/A'

        description_texts = response.css('#productDescription *::text').getall()
        description = ' '.join(description_texts).strip()
        item['description'] = description

        product_images = response.xpath("//a[@class='thumb-link']/@data-image").getall()
        item['product_images'] = product_images

        sku_pattern = r'"sku"\s*:\s*"(\d+)"'
        sku_match = re.search(sku_pattern, response.body.decode('utf-8'))
        if sku_match:
            item['sku'] = sku_match.group(1)

        barcode = response.css('div.row.mb-2 div.col-2.pd-d-t:contains("BARKOD") + div.col-10.pd-d-v::text').get()
        if barcode:
            item['barcode'] = barcode.strip()

        json_line = json.dumps(dict(item), ensure_ascii=False) + ",\n"  # Separate JSON objects with comma
        self.file.write(json_line)

        yield item

    def closed(self, reason):
        self.file.close()
        self.process_file()

    def process_file(self):
        filename = "petshop_products.json"
        with open(filename, 'r+', encoding='utf-8') as f:
            content = f.read()
            content = content[:-2] + ']'
            f.seek(0)
            f.write(content)
            f.truncate()


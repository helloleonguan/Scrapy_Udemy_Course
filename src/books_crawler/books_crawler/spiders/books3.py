# -*- coding: utf-8 -*-
import scrapy
import os
import glob


def product_info(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()


class Books3Spider(scrapy.Spider):
    name = 'books3'
    allowed_domains = ['books.toscrape.com']
    # start_urls = ['http://books.toscrape.com/']

    def __init__(self, category):
        self.start_urls = [category]

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield scrapy.Request(absolute_url, callback=self.parse_book)

        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)

        yield scrapy.Request(absolute_next_page_url)


    def parse_book(self, response):
        title = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()

        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com')

        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')

        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        # product information

        upc = product_info(response, "UPC")
        product_type = product_info(response, "Product Type")
        price_without_tax = product_info(response, "Price (excl. tax)")
        price_with_tax = product_info(response, "Price (incl. tax)")
        tax = product_info(response, "Tax")
        availability = product_info(response, "Availability")
        no_of_reviews = product_info(response, "Number of reviews")


        yield {
            "title": title,
            "price": price,
            "image_url": image_url,
            "rating": rating,
            "description": description,
            "upc": upc,
            "product_type": product_type,
            "price_without_tax": price_without_tax,
            "price_with_tax": price_with_tax,
            "tax": tax,
            "availability": availability,
            "no_of_reviews": no_of_reviews
        }

    def close(self, reason):
        # perform operations after scraping is complete

        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        os.rename(csv_file, 'new_books.csv')

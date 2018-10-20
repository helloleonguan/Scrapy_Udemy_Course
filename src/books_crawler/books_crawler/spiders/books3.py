# -*- coding: utf-8 -*-
import scrapy


class Books3Spider(scrapy.Spider):
    name = 'books3'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield scrapy.Request(absolute_url, callback=self.parse_book)

        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)

        yield scrapy.Request(absolute_next_page_url)


    def parse_book(self, response):
        pass


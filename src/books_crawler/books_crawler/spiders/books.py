# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    # LinkExtractor: grab all the URLs on a page
    # arugments for LinkExtractor: deny_domains & allow
    rules = (Rule(LinkExtractor(allow='music'), callback='parse_page', follow=True),)

    def parse_page(self, response):
        yield {'URL': response.url}

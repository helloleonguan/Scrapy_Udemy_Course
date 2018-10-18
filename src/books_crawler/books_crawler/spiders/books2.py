# -*- coding: utf-8 -*-
import scrapy
from time import sleep

from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException

class Books2Spider(scrapy.Spider):
    name = 'books2'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        self.driver = webdriver.Chrome('../chromedriver')
        self.driver.get('http://books.toscrape.com')

        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a/@href').extract()
        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                self.logger.info("Sleeping for 3 seconds")
                sleep(3)
                next_page.click()

                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)

            except NoSuchElementException:
                self.logger.info("No more pages!")
                self.driver.quit()
                break

    def parse_book(self, response):
        title = response.css('h1::text').extract_first()
        url = response.request.url
        yield {'title': title, 'url':url}


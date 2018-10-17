# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        h1_tag = response.xpath("//h1/a/text()").extract_first()
        tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        simple_data = {
            "H1 Tag": h1_tag,
            "Tags": tags
        }

        print(simple_data)
        print()


        # advanced spider
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first().strip("\“\”")
            author = quote.xpath('.//*[@class="author"]/text()').extract()
            quote_tags = quote.xpath('.//*[@class="tag"]/text()').extract()

            quote_info = {
                "Text": text,
                "Author": author,
                "Tags": quote_tags
            }

            yield (quote_info)
            print()

        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)
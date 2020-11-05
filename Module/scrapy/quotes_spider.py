#!/usr/bin/python3
# -*- coding:utf-8 -*-
# command: scrapy runspider quotes_spider.py -o quotes.jl
# pycharm debug config:
#       Module name:scrapy.cmdline
#       Parameters: runspider quotes_spider.py  -o test.jl
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author': quote.xpath('span/small/text()').get(),
                'text': quote.css('span.text::text').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
if __name__ == "__main__":
    pass

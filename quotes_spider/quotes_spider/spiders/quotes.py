# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//span[@class="text"]/text()').extract_first()
            author  = quote.xpath('.//small[@class="author"]/text()').extract_first()
            tags = quote.xpath('.//a[@class="tag"]/text()').extract()
            yield {
                'text':text,
                'author':author,
                'tags':tags
            }
        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)

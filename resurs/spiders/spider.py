import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import ResursItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class ResursSpider(scrapy.Spider):
	name = 'resurs'
	start_urls = ['https://www.resursbank.dk/om-os-forhandler/presse-medier-forhandler/pressemeddelelser-forhandler']

	def parse(self, response):
		post_links = response.xpath('//a[@class="link--default  "]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="single-cision-item--documents--list--item--date"]/text()').get()
		title = response.xpath('//h3[@class="headline headline--3 margin-btm-small "]/text()').get()
		content = response.xpath('//div[@class="single-cision-item--intro"]//text()').getall() + response.xpath('//div[@class="single-cision-item--body"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=ResursItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()

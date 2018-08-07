# -*- coding: utf-8 -*-
import scrapy


class WikicrawlerSpider(scrapy.Spider):
	name = 'wikicrawler'
	allowed_domains = ['subnautica.wikia.com']
	# start_urls = ['http://subnautica.wikia.com/wiki/Fauna','http://subnautica.wikia.com/wiki/Flora']
	start_urls = ['http://subnautica.wikia.com/wiki/Acid_Mushroom']


	def parse(self, response):
		self.log('Visited "%s"' % response.url)



		# Flora layout
		item = {
			'title': response.css('h2.pi-title center::Text')[0].extract(),
			'classification': response.css('div.pi-data-value a::Text')[0].extract(),
			'item_description': response.css('div.pi-data div.pi-data-value.pi-font::Text')[0].extract(),
			'category': response.css('div.pi-data-value.pi-font a::Text')[2].extract(),
			'biomes': response.css('div.pi-data-value.pi-font ul li a::attr(title)').extract()

		}
		yield item

		tosearch_raw = response.css('td.navbox-list.navbox-odd a::attr(href)').extract()
		# tosearch_raw = response.css('a::attr(href)').extract()
		tosearch = []
		for url in tosearch_raw:
			url = response.urljoin(url)
			tosearch.append(url)
		print(tosearch)

		for url in tosearch:
			yield scrapy.Request(url=url,callback=self.parse)

		# create a file to hold pending urls
		# for url in tosearch:
		# scrapy.Request(url=url,callback=self.checkdupe)

	# def checkdupe(self, response):
	# 	if file exists, store first line as variable
	# 	delete first line from file
	# 	continue to parse function

	# 	if file does not exist, error out


# tosearch_raw = response.css('a::attr(href)').extract()
# tosearch = []
# for url in tosearch_raw:
# 	url = response.urljoin(url)
# 	print(url)
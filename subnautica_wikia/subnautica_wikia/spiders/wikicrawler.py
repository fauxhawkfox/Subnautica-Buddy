# -*- coding: utf-8 -*-
import scrapy


class WikicrawlerSpider(scrapy.Spider):
	name = 'wikicrawler'
	allowed_domains = ['subnautica.wikia.com']
	# start_urls = ['http://subnautica.wikia.com/wiki/Fauna','http://subnautica.wikia.com/wiki/Flora']
	start_urls = ['http://subnautica.wikia.com/wiki/Acid_Mushroom']


	def parse(self, response):
		self.log('Visited "%s"' % response.url)
		#biomeextract = response.css('div.pi-item.pi-data.pi-item-spacing.pi-border-color')
		#biomeextract2 = biomeextract.css('h3::Text').extract()
		#indexofbiome = biomeextract2.index('Biome')
		#biomeslist = biomeextract[indexofbiome].css('ul li a::attr(title)').extract()

		# Flora layout
		item = {
			'title': self.getTitle(response),
			'classification': self.getAttributeLinked(response, 'Classification'),
			'item_description': self.getAttributeText(response, 'Description'),
			#'item_description': response.css('div.pi-data div.pi-data-value.pi-font::Text')[0].extract(),
			#'category': response.css('div.pi-data-value.pi-font a::Text')[2].extract(),
			'biomes': self.getAttributeLinked(response, 'Biome')
			#'biomes': biomeslist
			#'biomes': response.css('div.pi-data-value.pi-font ul li a::attr(title)').extract()

		}
		yield item


		#data_labels = response.css('div h3.pi-data-label.pi-secondary-font').extract()
		#for data_label in data_labels:
		#	if data_label.css('::Text') == 'Biome':
		#		print data_label.css('::Text')
		
			

		tosearch_raw = response.css('td.navbox-list.navbox-odd a::attr(href)').extract()
		# tosearch_raw = response.css('a::attr(href)').extract()
		tosearch = []
		for url in tosearch_raw:
			url = response.urljoin(url)
			tosearch.append(url)
		#print(tosearch)

		for url in tosearch:
			yield scrapy.Request(url=url,callback=self.parse)

		# create a file to hold pending urls
		# for url in tosearch:
		# scrapy.Request(url=url,callback=self.checkdupe)

	#Gets the object text (cannot be used for links). Mainly used for descriptions
	def getAttributeText(self, response, attributename):
		attributeExtract = response.css('div.pi-item.pi-data.pi-item-spacing.pi-border-color')
		attributeExtract2 = attributeExtract.css('h3::Text').extract()
		if attributename not in attributeExtract2:
			return "n/a"
		else:
			indexofattribute = attributeExtract2.index(attributename)
			attributeText = attributeExtract[indexofattribute].css('div.pi-data-value.pi-font::text').extract_first()
			if attributeExtract[indexofattribute].css('sub').extract() != []:
				attributeText += attributeExtract[indexofattribute].css('sub::text').extract_first()
				if len(attributeExtract[indexofattribute].css('div.pi-data-value.pi-font::text').extract()) > 1:
					attributeText += attributeExtract[indexofattribute].css('div.pi-data-value.pi-font::text')[1].extract()
					if len(attributeExtract[indexofattribute].css('sub').extract()) > 1:
						attributeText += attributeExtract[indexofattribute].css('sub::text')[1].extract()
						if len(attributeExtract[indexofattribute].css('div.pi-data-value.pi-font::text').extract()) > 2:
							attributeText += attributeExtract[indexofattribute].css('div.pi-data-value.pi-font::text')[2].extract()
							if len(attributeExtract[indexofattribute].css('div.pi-data-value.pi-font p::text').extract()) > 0:
								attributeText += attributeExtract[indexofattribute].css('div.pi-data-value.pi-font p::text').extract_first()
			return attributeText
			
	#Gets the object in the event that the category is a link and not actually just text within the div
	def getAttributeLinked(self,response,attributename):
		attributeExtract = response.css('div.pi-item.pi-data.pi-item-spacing.pi-border-color')
		attributeExtract2 = attributeExtract.css('h3::text').extract()
		if attributename not in attributeExtract2:
			return "n/a"
		else:
			indexofattribute = attributeExtract2.index(attributename)
			attributeText = []
			attributeText += attributeExtract[indexofattribute].css('div.pi-data-value.pi-font::text').extract()
			attributeText += attributeExtract[indexofattribute].css('div.pi-data-value.pi-font a::text').extract()
			attributeText += attributeExtract[indexofattribute].css('ul li a::attr(title)').extract()
			if attributeText == []:
				return "n/a"
			else:
				return attributeText
				
	#Gets the title of whatever object it is scraping
	def getTitle(self, response):
		title = ""
		if response.css('h2.pi-title center::text').extract() != []:
			title += response.css('h2.pi-title center::Text').extract_first()
		elif response.css('h2.pi-title::Text').extract() != []:
			title += response.css('h2.pi-title::Text').extract_first()
		elif response.css('h2.pi-title p::Text').extract() != []:
			title += response.css('h2.pi-title p::Text').extract_first()
		elif response.css('h1.page-header__title::text').extract() != []:
			title += response.css('h1.page-header__title::text').extract_first()
		else:
			title += "n/a"
		return title
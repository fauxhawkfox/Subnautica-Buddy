# -*- coding: utf-8 -*-
import scrapy


class WikicrawlerSpider(scrapy.Spider):
	name = 'wikicrawler'
	allowed_domains = ['subnautica.wikia.com']
	# start_urls = ['http://subnautica.wikia.com/wiki/Fauna','http://subnautica.wikia.com/wiki/Flora']
	start_urls = ['http://subnautica.wikia.com/wiki/Acid_Mushroom', 'http://subnautica.wikia.com/wiki/Eggs']


	def parse(self, response):
		self.log('Visited "%s"' % response.url)
		# biomeextract = response.css('div.pi-item.pi-data.pi-item-spacing.pi-border-color')
		# biomeextract2 = biomeextract.css('h3::Text').extract()
		# indexofbiome = biomeextract2.index('Biome')
		# biomeslist = biomeextract[indexofbiome].css('ul li a::attr(title)').extract()

		# Put tags to check for in a page in here; uses the info box on the right side of the screen mainly.
		if response.url == "http://subnautica.wikia.com/wiki/Eggs":
			tablerows = response.css('table.article-table')[0].css('tr')
			item = {}
			for row in range(1, len(tablerows.extract())):
				item['title'] = tablerows[row].css('td')[0].css('a::text').extract_first()
				item['size'] = tablerows[row].css('td::text')[1].extract()[:-1]
				item['description'] = tablerows[row].css('td::text')[2].extract()[:-1]
				item['location'] = tablerows[row].css('td')[3].css('ul li a::text').extract()
				item['energyvalue'] = tablerows[row].css('td::text')[5].extract()[:-1]
				item['incubationdays'] = tablerows[row].css('td::text')[6].extract()[:-1]
				item['itemid'] = tablerows[row].css('td::text')[7].extract()[:-1]
				if item['location'] == []:
					del item['location']
				yield item
		else:
			itemprecursor = {
				'title': self.getTitle(response),
				'classification': self.getAttributeLinked(response, 'Classification'),
				'item_description': self.getAttributeText(response, 'Description'),
				# 'item_description': response.css('div.pi-data div.pi-data-value.pi-font::Text')[0].extract(),
				# 'category': response.css('div.pi-data-value.pi-font a::Text')[2].extract(),
				'biomes': self.getAttributeLinked(response, 'Biome'),
				'tab': self.getAttributeLinked(response, 'Tab'),
				# 'biomes': biomeslist
				# 'biomes': response.css('div.pi-data-value.pi-font ul li a::attr(title)').extract()
	
			}
			
			'''
			This does a few things:
			1. Creates a blank dictionary to start with, which will wind up being the dictionary for the item this page represents.
			2. Enumerates through each tag to check for in the itemprecursor dictionary. If valid (found on this page), it will gather the values and add them to the final item dictionary.
			
			This will ensure that our record of the item includes only the relevant attributes.
			'''
			item = {}
			for key in itemprecursor:
				if itemprecursor[key] != "n/a":
					item[key] = itemprecursor[key]
			
			''' 
			Only render item if the 'tab' attribute is present. The tab attribute in the wiki is used to denote which master category the item falls into. 
			i.e. vehicles, flora, fauna, tools, biomes, etc
			There are non-tab pages such as the generic descriptor pages, such as the "Tools" page which lists all items with the tab 'Tools'. We don't want to scrape that as it is not an item.
			'''
			if 'tab' in item:
				yield item
	
	
			#data_labels = response.css('div h3.pi-data-label.pi-secondary-font').extract()
			#for data_label in data_labels:
			#	if data_label.css('::Text') == 'Biome':
			#		print data_label.css('::Text')
	
	
			'''
			This is browse-through/request-generator.
			It looks at the box at the bottom of the page which provides similar items.
			Surprisingly we've had no issues with loops from the use of this method.
			note: this is actually because scrapy won't visit the same page twice.
			'''
			tosearch_raw = response.css('td.navbox-list.navbox-odd a::attr(href)').extract()
			# tosearch_raw = response.css('a::attr(href)').extract()
			tosearch = []
			for url in tosearch_raw:
				url = response.urljoin(url)
				if url not in self.start_urls:
					tosearch.append(url)
					
			for url in tosearch:
				yield scrapy.Request(url=url,callback=self.parse)

	#Gets the object text (cannot be used for links or lists). Mainly used for item descriptions
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
			
	#Gets a list from an attribute that is not comprised of links.
	def getAttributeList(self, response, attributename):
		attributeExtract = response.css('div.pi-item.pi-data.pi-item-spacing.pi-border-color')
		attributeExtract2 = attributeExtract.css('h3::Text').extract()
		if attributename not in attributeExtract2:
			return "n/a"
		else:
			indexofattribute = attributeExtract2.index(attributename)
			attributeText = []
			for listitem in attributeExtract[indexofattribute].css('ul li::text').extract():
				attributeText += listitem
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
			attributeText += attributeExtract[indexofattribute].css('div.pi-data-value.pi-font a::text').extract()
			if attributeText == []:
				attributeText += attributeExtract[indexofattribute].css('div.pi-data-value.pi-font::text').extract()
			#attributeText += attributeExtract[indexofattribute].css('ul li a::attr(title)').extract()
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
import scrapy
import re


class Noticias(scrapy.Item):
    Titulo = scrapy.Field()
    Data = scrapy.Field()
    texto = scrapy.Field()
    tags = scrapy.Field()


class ValorSpider(scrapy.Spider):
    name = 'valor'

    allowed_domains = ['valor.com.br']
    start_urls = ['http://www.valor.com.br/empresas/']

    def parse(self, response):

        titles = response.css('h2[class*="title"] > a').extract() \
                 + response.css('div[class*="title"] > a').extract() \
                 + response.css('li > a[class*="title"]').extract() \
                 + response.css('ul.list4 > li > a').extract()

        patternString = re.compile("Petrobras|petrobras|Eletrobras|eletrobras")
        patternUrl = re.compile("href=\"(.*?)\"")

        for string in titles:

            if re.search(patternString, string):

                url = re.findall(patternUrl, string)[0]

                if url[0:12] != 'valor.com.br':
                    url = response.urljoin(url)

                print(url)
                yield scrapy.Request(url=url, callback=self.parse_details)

    def parse_details(self, response):

        data = Noticias()

        data['Titulo'] = response.css('h1.title1::text').extract_first()
        data['Data'] = response.css('div.n-header > span::text').extract_first()

        par = response.css('div.node-body > p').extract()
        text = ""

        pattern = re.compile(">(.*?)<")

        for string in par:

            result = re.findall(pattern, string)

            for part in result:
                text += part

            text += "\n"

        data['texto'] = text
        data['tags'] = response.css('div.tags > a::text').extract()

        yield data

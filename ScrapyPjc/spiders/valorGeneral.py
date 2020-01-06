import scrapy
import re


class Noticias(scrapy.Item):
    titulo = scrapy.Field()
    data = scrapy.Field()
    texto = scrapy.Field()
    tags = scrapy.Field()


class ValorGeneralSpider(scrapy.Spider):
    name = 'valorGeneral'

    allowed_domains = ['valor.com.br']
    start_urls = ['http://www.valor.com.br/empresas/']

    def parse(self, response):

        urls = response.css('h2[class*="title"] > a::attr(href)').extract() + \
               response.css('div[class*="title"] > a::attr(href)').extract() + \
               response.css('li > a[class*="title"]::attr(href)').extract() + \
               response.css('ul.list4 > li > a::attr(href)').extract()

        for url in urls:

            if url[0:12] != "valor.com.br":
                url = response.urljoin(url)

            print(url)
            yield scrapy.Request(url=url, callback=self.parse_details)

    def parse_details(self, response):

        data = Noticias()

        data['titulo'] = response.css('h1.title1::text').extract_first()
        data['data'] = response.css('div.n-header > span::text').extract_first()

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

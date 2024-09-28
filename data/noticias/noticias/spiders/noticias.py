import scrapy
import pytz
from datetime import datetime

class noticias(scrapy.Spider):
    name = 'noticias'
    start_urls = ['https://www.rondoniadinamica.com/']

    def parse(self, response):
        #obtendo o link das notícias mais populares
        links = response.css('div.popular-news-widget')
        urls = links.css('a::attr(href)').getall()

        #iterando sobre os 3 primeiros links
        for url in urls[:3]:
            url_completa = response.urljoin(url)
            yield scrapy.Request(url_completa, callback=self.obter_campos)
    
    #função para obter os campos de cada notícia
    def obter_campos(self, response):
        dt_request = datetime.now(pytz.utc).isoformat()
        dt_noticia = response.css('div.post-excerp strong::text').getall()[1]
        dt_noticia_tratada = datetime.strptime(dt_noticia, "%d/%m/%Y às %Hh%M").isoformat()
        titulo = response.css('meta[property="og:title"]::attr(content)').get()
        corpo = response.css('div.post-meta p::text').getall()
        subtitulo = response.css('meta[property="og:description"]::attr(content)').get()
        autor = response.css('meta[name="author"]::attr(content)').get()

        yield {
            'url': response.url,
            'dt_request': dt_request,
            'dt_noticia': dt_noticia_tratada,
            'titulo': titulo,
            'corpo': corpo,
            'subtitulo': subtitulo,
            'autor': autor
        }

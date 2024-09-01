import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class PokemonScrapper(scrapy.Spider):
    name = 'pokemon_scrapper'
    domain = "https://pokemondb.net"
    start_urls = ["https://pokemondb.net/pokedex/all"]
    
    def __init__(self):
        self.pokemon_data = []

    def parse(self, response):
        pokemons = response.css('#pokedex > tbody > tr')
        for pokemon in pokemons[:-1]:  # Limitar a quantidade de dados para teste
            link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
            yield response.follow(self.domain + link, self.parse_pokemon)
            
    #Extração das informações sobre os pokemon
    def parse_pokemon(self, response):
        nome = response.css('h1::text').get()
        num = response.css('table.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get()
        peso = response.css('table.vitals-table > tbody > tr:nth-child(5) > td::text').get()
        altura = response.css('table.vitals-table > tbody > tr:nth-child(4) > td::text').get()
        tipo1 = response.css('table.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(1)::text').get()
        tipo2 = response.css('table.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(2)::text').get()
        habilidade = response.css('table.vitals-table > tbody > tr:nth-child(6) > td > span > a::attr(href)').get()
        descricaohab = response.css('table.vitals-table > tbody > tr:nth-child(6) > td > span > a::attr(title)').get()
        evonum2 = response.css('div.infocard-list-evo > div:nth-child(3) > span:nth-child(2) > small::text').get()
        evoname2 = response.css('div.infocard-list-evo > div:nth-child(3) > span:nth-child(2) > a::text').get()
        evourl2 = response.css('div.infocard-list-evo > div:nth-child(3) > span:nth-child(2) > a::attr(href)').get()
        evonum3 = response.css('div.infocard-list-evo > div:nth-child(5) > span:nth-child(2) > small::text').get()
        evoname3 = response.css('div.infocard-list-evo > div:nth-child(5) > span:nth-child(2) > a::text').get()
        evourl3 = response.css('div.infocard-list-evo > div:nth-child(5) > span:nth-child(2) > a::attr(href)').get()        
            
        #Criado uma lista para coluna, e inserção dos dados valores dinâmicos, que são populado a partir do .get na parse_pokemon
        self.pokemon_data.append({
            "Numero": num,
            "URL": response.url,
            "Nome": nome,
            "Peso": peso,
            "Altura": altura,
            "Tipo 1": tipo1,
            "Tipo 2": tipo2,
            "Habilidade": habilidade,
            "Descricao Habilidade": descricaohab,
            "URL Habilidade": 'https://pokemondb.net' + habilidade if habilidade else None,
            "Evolução 2 Número": evonum2 if evonum2 else None,
            "Evolução 2 Nome": evoname2 if evoname2 else None,
            "Evolução 2 Url": 'https://pokemondb.net' + evourl2 if evourl2 else None,
            "Evolução 3 Número": evonum3 if evonum3 else None,
            "Evolução 3 Nome": evoname3 if evoname3 else None,
            "Evolução 3 Url": 'https://pokemondb.net' + evourl3 if evourl3 else None,
        })

    #Ultimo metódo a ser utilizado
    def closed(self, reason):    
        df = pd.DataFrame(self.pokemon_data) #Criação/Definição do dataframe
        df.set_index("Numero", inplace=True) #Definição do Index sendo a coluna Numero
        df = df.sort_index() #Comando pandas para ordenar através do index definido        
        print(df,flush=True)
        df.to_csv("pokemon_data.csv")  # Salva os dados em um arquivo CSV


process = CrawlerProcess() #Acionando a classe CrawlerProcess
process.crawl(PokemonScrapper) #Acionando a classe PokemonScrapper
process.start() #Executou a classe
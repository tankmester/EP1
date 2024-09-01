import numpy as np
import pandas as pd
import scrapy


class PokemonScrapper(scrapy.Spider):
  name = 'pokemon_scrapper'
  domain = "https://pokemondb.net/"

  start_urls = ["https://pokemondb.net/pokedex/all"]

  def parse(self, response):
    pokemons = response.css('#pokedex > tbody > tr')
    #for pokemon in pokemons:
    pokemon = pokemons[0]
    link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
    yield response.follow(self.domain + link, self.parse_pokemon)

  def parse_pokemon(self, response):
    nome = response.css('h1::text')
    num = response.css('table.vitals-table > tbody > tr:nth-child(1) > td > strong::text')
    peso = response.css('table.vitals-table > tbody > tr:nth-child(5) > td::text')
    altura = response.css('table.vitals-table > tbody > tr:nth-child(4) > td::text')
    tipo1 = response.css('table.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(1)::text')
    tipo2 = response.css('table.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(2)::text')
    habilidade = response.css('table.vitals-table > tbody > tr:nth-child(6) > td > span > a::attr(href)')  
    descricaohab = response.css('table.vitals-table > tbody > tr:nth-child(6) > td > span > a::attr(title)')  

    evonum1 = response.css('div.infocard-list-evo > div:nth-child(1) > span:nth-child(2) > small::text')
    evoname1 = response.css('div.infocard-list-evo > div:nth-child(1) > span:nth-child(2) > a::text')
    evourl1 = response.css('div.infocard-list-evo > div:nth-child(1) > span:nth-child(2) > a::attr(href)')

    evonum2 = response.css('div.infocard-list-evo > div:nth-child(3) > span:nth-child(2) > small::text')
    evoname2 = response.css('div.infocard-list-evo > div:nth-child(3) > span:nth-child(2) > a::text')
    evourl2 = response.css('div.infocard-list-evo > div:nth-child(3) > span:nth-child(2) > a::attr(href)')

    evonum3 = response.css('div.infocard-list-evo > div:nth-child(5) > span:nth-child(2) > small::text')
    evoname3 = response.css('div.infocard-list-evo > div:nth-child(5) > span:nth-child(2) > a::text')
    evourl3 = response.css('div.infocard-list-evo > div:nth-child(5) > span:nth-child(2) > a::attr(href)')

    yield{"URL": response.url, 
          "Nome": nome.get(),
          "Numero": num.get(), 
          "Peso": peso.get(), 
          "Altura": altura.get(), 
          "tipo 1": tipo1.get(), 
          "tipo 2": tipo2.get(), 
          "Habidade": habilidade.get(), 
          "Descricao Habilidade": descricaohab.get(),          
          "URL Habilidade": 'https://pokemondb.net' + habilidade.get(),
          "Numero Evolucao": evonum1.get(),
          "Nome Evolucao": evoname1.get(),
          "URL Evolucao": 'https://pokemondb.net' + evourl1.get(),
          "Numero Evolucao 2": evonum2.get(),
          "Nome Evolucao 2": evoname2.get(),
          "URL Evolucao 2": 'https://pokemondb.net' + evourl2.get(),
          "Numero Evolucao 3": evonum3.get(),
          "Nome Evolucao 3": evoname3.get(),
          "URL Evolucao 3": 'https://pokemondb.net' + evourl3.get(), 
         }

'''
API Flask Rick & Morty
'''

import os
from typing import Any
import json
import urllib.request
from flask import Flask, render_template, send_from_directory, redirect


app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    '''
    favicon:
    https://flask.palletsprojects.com/en/2.3.x/patterns/favicon/
    '''
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


@app.route('/')
def home():
    '''
    Página principal
    '''
    return render_template('home.html')

#####################################################
####           APIs   RICK  &  MORTY             ####
#####################################################

def get_json_data_for(url: str) -> dict[str, Any]:
    '''
    Retorna os dados da URL informada.
    https://docs.python.org/3/howto/urllib2.html
    https://flask.palletsprojects.com/en/1.1.x/quickstart/#variable-rules
    '''
    with urllib.request.urlopen(url) as response:
        response_data = response.read()
        data = json.loads(response_data)
        return data


@app.route('/api/personagens/<int:page>')
def api_personagens(page: int) -> dict[str, Any]:
    '''
    Personagens
    '''
    return get_json_data_for(f"https://rickandmortyapi.com/api/character?page={page}")


@app.route('/api/personagem/<int:idt>')
def api_personagem(idt: int) -> dict[str, Any]:
    '''
    Personagem
    '''
    return get_json_data_for(f"https://rickandmortyapi.com/api/character/{idt}")


@app.route('/api/episodios/<int:page>')
def api_episodios() -> dict[str, Any]:

    url = "https://rickandmortyapi.com/api/episode"
    dic = get_json_data_for(url)
    episodios = []

    for episodio in dic["results"]:
        episodio = {
            "Nome do episódio: ": episodio["name"],
            "Data em que foi ao ar: ": episodio["air_date"],
            "Código do episódio: ": episodio["episode"],
            "Link para o episódio: " : episodio["url"]
        }
        episodios.append(episodio)

    return episodios


@app.route('/api/episodio/<int:idt>')
def api_episodio(idt: int) -> dict[str, Any]:
    '''
    Episódio
    '''
    return get_json_data_for(f"https://rickandmortyapi.com/api/episode/{idt}")


@app.route('/api/localizacoes/<int:page>')
def api_localizacoes(page: int) -> dict[str, Any]:
    '''
    Localizações
    '''
    return get_json_data_for(f"https://rickandmortyapi.com/api/location?page={page}")


@app.route('/api/localizacao/<int:idt>')
def api_localizacao(idt: int) -> dict[str, Any]:
    '''
    Localização
    '''
    return get_json_data_for(f"https://rickandmortyapi.com/api/location/{idt}")


#####################################################
####        PÁGINAS   RICK  &  MORTY             ####
#####################################################

@app.route('/personagens')
def personagens_sem_pagina():
    '''
    Personagens
    '''
    return redirect('/personagens/1')


@app.route('/personagens/<int:page>')
def personagens(page: int):
    '''
    Personagens
    '''
    data = api_personagens(page)
    return render_template('personagens.html', dados=data, page=page)


@app.route('/personagem/<int:idt>')
def personagem(idt: int):
    '''
    Personagem
    '''
    dados_personagem = api_personagem(idt)
    return render_template('personagem.html', personagem=dados_personagem)


@app.route('/episodes')
def episodios_sem_pagina():
    url = "https://rickandmortyapi.com/api/episode"
    dic = get_json_data_for(url)
    
    return render_template("episodes.html", episodios=dic["results"])


@app.route('/episodes/<int:page>')
def episodes(page: int):
    '''
    Episódios
    '''
    print(f"Episódios PAGE={page}")
    return '<h1 style="color: red;">Fazer a renderização da página com informações dos episódios.<h1/>'


@app.route('/episode/<int:idt>')
def episode(idt: int):
    '''
    Episódio de identificador informado.
    '''
    print(f"Episódio ID={idt}")
    return '<h1 style="color: red;">Fazer a renderização da página com as informações de um episódio e seus personagens.<h1/>'



@app.route('/locations')
def localizacoes_sem_pagina():
    '''
    Localizações
    '''
    return redirect('/locations/1')


@app.route('/locations/<int:page>')
def locations(page: int):
    '''
    Localizações
    '''
    print(f"Localizações PAGE={page}")
    return '<h1 style="color: red;">Fazer a renderização da página com as informações das localizações.<h1/>'


@app.route('/location/<int:idt>')
def location(idt: int):
    '''
    residentes de identificador informado.
    '''
    print(f"Localização ID={idt}")
    return '<h1 style="color: red;">Fazer a renderização da página com as informações de uma localização e seus residentes (personagens).<h1/>'



#####################################################
####           TRATAMENTO  DE  ERROS             ####
#####################################################

@app.errorhandler(404)
def page_not_found(exeption: Exception) -> tuple[str, int]:
    '''
    Página não encontrada
    status code = 404
    https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
    '''
    print(f"type(exeption)={type(exeption)} ERRO: {str(exeption)}")
    return render_template('erro.html', msg='Página não encontrada!'), 404


@app.errorhandler(Exception)
def handle_exception(exception: Exception) -> tuple[str, int]:
    '''
    Captura as exceções
    https://flask.palletsprojects.com/en/2.3.x/errorhandling/
    '''
    print(f"TYPE: {type(exception)} ERRO: {str(exception)}")
    return render_template("erro.html", msg='Ops! Ocorreu um erro inesperado.'), 500


if __name__ == "__main__":
    # Modo debug reinicia automaticamente o servidor a cada alteração.
    # Development Server:
    # https://flask-fr.readthedocs.io/server/
    app.run(debug=True, port=8888)

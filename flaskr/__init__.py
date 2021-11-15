import json
import urllib.request
import os

from flask import Flask, render_template, request

with urllib.request.urlopen('https://raw.githubusercontent.com/theikkila/postinumerot/master/postcode_map_light.json') as response:
        html = response.read()
postinumerot=json.loads(html)

def find(postitoimipaikka):
    check = postitoimipaikka.upper() in postinumerot.values()
    if check == True:
        lista = ""
        for ptp in postinumerot:
            if (postinumerot[ptp]==postitoimipaikka.upper().replace(" ", "")):
                if lista=="":
                    lista = ptp
                else: 
                    lista = lista + ", " + ptp 
        return 'Postinumerot: ' + lista
    else:
        return 'Postitoimipaikkaa ei löydy'

def nayta_postitoimipaikka(postinumero):
    try:
        return postinumerot[postinumero]
    except:
        return 'Postinumeroa ei ole olemassa'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/postinumerot', methods=["POST", "GET"])
    def postinumerot():
        postinumero = ''
        postitp = ''
        if request.method == 'POST':
            postitp = request.form['postitoimipaikka']
            postinumero = find(postitp)
        return render_template('template.html', values=postinumero, haku=postitp)
    
    @app.route('/postitoimipaikat', methods=["POST", "GET"])
    def postitoimipaikat():
        postinro = ''
        postitp = ''
        if request.method == 'POST':
            postinro = request.form['postinumero']
            postitp = nayta_postitoimipaikka(postinro)
        return render_template('postnotemplate.html', values=postitp, haku=postinro)
    
    return app
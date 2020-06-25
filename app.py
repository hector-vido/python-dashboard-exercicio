#!/usr/bin/python3

import requests
from os import environ

# importar de config health_check e login_required
# importar blueprints

# insanciar Flask na variável app
# criar secret_key, pode ir ao duckduckgo.com e procurar por "password strong 32"
app.url_map.strict_slashes = False
# registrar blueprints

@app.route('/')
# adicionar o decorator login_required de config.py, terá que criá-lo
def index():
  #health = health_check()
  #renderizar "index.html", enviando uma variável chamada health com o valor de health logo acima
  return 'Parece funcionar...' # remover

@app.route('/login')
def get_login():
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def post_login():
  # dados enviados por formulários ficam em request.form['nome']
  # popular as variáveis "usuario" e "senha" com os valores do formulário

  try:
    # conectar-se ao OpenLDAP
    if ldap.bind(): # se o bind funcionar, usuário se autenticou
      session['auth'] = True # cria um indicador de que usuário se autenticou
      return redirect('/')
    else:
      # criar flash message do tipo "error" com a mensagem "Usuário ou senha inválidos"
      return redirect('/login')
  except Exception as e:
    print(e)
    raise e

@app.route('/logoff')
def logoff():
  del session['auth'] # remove o indicador, deslogando o usuário
  return redirect('/')

@app.errorhandler(404)
def page_not_found(error):
  return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
  return render_template('errors/500.html'), 500

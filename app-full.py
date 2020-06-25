#!/usr/bin/python3

import requests
from os import environ
from ldap3 import Server, Connection
from flask import Flask, flash, redirect, render_template, request, session

from config import health_check, login_required
from blueprints.docker_routes import docker_routes
from blueprints.gitea_routes import gitea_routes
from blueprints.jenkins_routes import jenkins_routes

app = Flask(__name__)
app.secret_key = 'TqMYB8^wbe!%cTcx3UbV!qUsZ2*#*XK6B3ZFj*zK'
app.url_map.strict_slashes = False
app.register_blueprint(docker_routes)
app.register_blueprint(gitea_routes)
app.register_blueprint(jenkins_routes)

@app.route('/')
@login_required
def index():
  health = health_check()
  return render_template('index.html', health=health)

@app.route('/login')
def get_login():
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def post_login():
  usuario = request.form['usuario'] or ' '
  senha = request.form['senha'] or ' '

  try:
    server = Server(environ['LDAP_HOST'], use_ssl=False)
    ldap = Connection(server, user='uid={},ou=users,dc=example,dc=com'.format(usuario), password=senha)
    if ldap.bind():
      session['auth'] = True
      return redirect('/')
    else:
      flash('Usuário ou senha inválidos', 'error')
      return redirect('/login')
  except Exception as e:
    print(e)
    raise e

@app.route('/logoff')
@login_required
def logoff():
  del session['auth']
  return redirect('/')

@app.errorhandler(404)
def page_not_found(error):
  return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
  return render_template('errors/500.html'), 500

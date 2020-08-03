#!/usr/bin/python3

import requests, docker
from os import environ
from functools import wraps
from flask import redirect, session

def login_required(f):
    pass

def health_check():

  results = {}

  checks = {
    'Docker' : lambda : 1 / 0, # Dividir por zero força exceção... DockerClient().info()
    'Gitea' : gitea_check,
    'Jenkins' : jenkins_check,
    'OpenLDAP' : openldap_check
  }
  for i in checks:
    try:
      checks[i]() # As checagens são executadas aqui, por isso cada uma é uma função
      results[i.lower()] = {'class' : 'success', 'message' : '{0}'.format(i)} # a classe afeta a cor no painel, verde ou vermelho
    except Exception as ex:
      print(ex) # com este print, podemos ter uma ideia melhor dos erros na saída do terminal
      results[i.lower()] = {'class' : 'error', 'message' : '{0}'.format(i)}

  return results

def gitea_check():
  # consultar /api/v1/user
  # response = requests.get('example.com', timeout=1, allow_redirects=False)
  if response.status_code != 200: # a conexão pode funcionar sem exceções, neste caso forçar uma
    raise Exception('Gitea: {} - {}'.format(response.status_code, response.reason))
  raise Exception('Nada, apagar')

def jenkins_check():
  # consultar /overallLoad/api/json
  # auth é uma tupla com usuário e senha
  # response = requests.get('exemple.com', auth=None, timeout=1)
  if response.status_code != 200: # a conexão pode funcionar sem exceções, neste caso forçar uma
    raise Exception('Jenkins: {} - {}'.format(response.status_code, response.reason))
  raise Exception('Nada, apagar')

def openldap_check():
  # server = Server('example.com', use_ssl=False, connect_timeout=1)
  # conecte-se utilizando autobind
  raise Exception('Nada, apagar')

class LoggerHandler(logging.handlers.HTTPHandler):

  def __init__(self, host, url, auth_host, method='GET', secure=False, credentials=None, context=None):
    # chamar construtor da classe pai
    self.auth_host = auth_host

  def emit(self, record):
    message = {'data' : record.asctime.split(',')[0], 'texto' : record.message}
    # enviar um post para /auth com um json contento "user" e "password"
    # extrair o token
    # enviar o log para /insert com o token no cabeçalho "Authorization: Bearer <token>"

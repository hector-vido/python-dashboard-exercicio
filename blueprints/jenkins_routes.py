#!/usr/bin/python3

import requests
from os import environ
from config import login_required
from flask import Blueprint, render_template, redirect

jenkins_routes = Blueprint('jenkins_routes', __name__)

AUTH = (,) # puxar variáveis do ambiente
JENKINS_HOST = '' # puxar variável do ambiente

@jenkins_routes.route('/jenkins')
# adicionar decorator para verificar a autenticação
def get_jobs():
  # Disparar um GET para /api/json com autenticação, atribuindo a variável "response", isso trará os projetos
  data = response.json() if response.status_code == 200 else {'jobs' : []}
  for job in data['jobs']:
    # disparar um GET para /job/nomedojob/api/json com autenticação, atribuindo a variável "response", isso capturará detalhes do job
    if response.status_code == 200:
      job['info'] = response.json()
      try:
        last_build = job['info']['builds'][0]['number'] # utiliza o último build para capturar os logs
        response = requests.get('{}/job/{}/{}/logText/progressiveText?start=0'.format(JENKINS_HOST, job['name'], last_build), auth=AUTH)
        job['info']['logs'] = response.text
      except:
        job['info']['logs'] = 'Nenhum log encontrado'
  return render_template('jenkins.html', jobs=data['jobs'])

@jenkins_routes.route('/jenkins/build/<job>')
@login_required
def build_job(job):
  # É possível utilizar requests.Session() ao invés dos cookies diretamente
  # disparar um GET para /crumbIssuer/api/json, lembre-se de enviar a autenticação, atribuindo a variável "response"
  data = response.json()
  cookies = response.cookies # Capturar o cookie para enviar na próxima requisição

  # Criar um dicionário utilizando o valor de "crumbRequestField" como chave e "crumb" como valor
  headers = {}
  response = requests.post('{}/job/{}/build'.format(JENKINS_HOST, job), headers=headers, auth=AUTH, cookies=cookies)
  # redirecionar para /jenkins

@jenkins_routes.route('/jenkins/stop/<job>/<n>')
@login_required
def build_stop(job, n):
  # disparar um GET para /crumbIssuer/api/json, lembre-se de enviar a autenticação, atribuindo a variável "response"
  data = response.json()
  cookies = response.cookies

  headers = {data['crumbRequestField'] : data['crumb']}
  # disparar um POST para /job/nomejob/numerojob/stop com os cabeçalhos, autenticação e cookies
  # redirecionar para /jenkins

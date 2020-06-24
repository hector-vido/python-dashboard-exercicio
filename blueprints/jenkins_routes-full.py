#!/usr/bin/python3

import requests
from os import environ
from config import login_required
from flask import Blueprint, render_template, redirect

jenkins_routes = Blueprint('jenkins_routes', __name__)

AUTH = (environ['JENKINS_USER'], environ['JENKINS_PASSWORD'])
JENKINS_HOST = '{}'.format(environ['JENKINS_HOST'])

@jenkins_routes.route('/jenkins')
@login_required
def get_jobs():
  response = requests.get('{}/api/json'.format(JENKINS_HOST), auth=AUTH)
  data = response.json() if response.status_code == 200 else {'jobs' : []}
  for job in data['jobs']:
    response = requests.get('{}/job/{}/api/json'.format(JENKINS_HOST, job['name']), auth=AUTH)
    if response.status_code == 200:
      job['info'] = response.json()
      try:
        last_build = job['info']['builds'][0]['number']
        response = requests.get('{}/job/{}/{}/logText/progressiveText?start=0'.format(JENKINS_HOST, job['name'], last_build), auth=AUTH)
        job['info']['logs'] = response.text
      except:
        job['info']['logs'] = 'Nenhum log encontrado'
  return render_template('jenkins.html', jobs=data['jobs'])

@jenkins_routes.route('/jenkins/build/<job>')
@login_required
def build_job(job):
  # É possível utilizar requests.Session() ao invés dos cookies diretamente
  response = requests.get('{}/crumbIssuer/api/json'.format(JENKINS_HOST), auth=AUTH)
  data = response.json()
  cookies = response.cookies

  headers = {data['crumbRequestField'] : data['crumb']}
  response = requests.post('{}/job/{}/build'.format(JENKINS_HOST, job), headers=headers, auth=AUTH, cookies=cookies)
  return redirect('/jenkins')

@jenkins_routes.route('/jenkins/stop/<job>/<n>')
@login_required
def build_stop(job, n):
  response = requests.get('{}/crumbIssuer/api/json'.format(JENKINS_HOST), auth=AUTH)
  data = response.json()
  cookies = response.cookies

  headers = {data['crumbRequestField'] : data['crumb']}
  response = requests.post('{}/job/{}/{}/stop'.format(JENKINS_HOST, job, n), headers=headers, auth=AUTH, cookies=cookies)
  return redirect('/jenkins')

#!/usr/bin/python3

import requests, docker
from os import environ
from functools import wraps
from ldap3 import Server, Connection
from flask import redirect, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'auth' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def health_check():

  results = {}

  checks = {
    'Docker' : lambda : docker.DockerClient(base_url='unix://var/run/docker.sock').info(),
    'Gitea' : gitea_check,
    'Jenkins' : jenkins_check,
    'OpenLDAP' : openldap_check
  }
  for i in checks:
    try:
      checks[i]()
      results[i.lower()] = {'class' : 'success', 'message' : '{0}'.format(i)}
    except Exception as ex:
      print(ex)
      results[i.lower()] = {'class' : 'error', 'message' : '{0}'.format(i)}

  return results

def gitea_check():
  headers = {'Authorization' : 'token {}'.format(environ['GITEA_TOKEN'])}
  response = requests.get('{}/api/v1/user'.format(environ['GITEA_HOST']), headers=headers, timeout=1, allow_redirects=False)
  if response.status_code != 200:
    raise Exception('Gitea: {} - {}'.format(response.status_code, response.reason))

def jenkins_check():
  AUTH = (environ['JENKINS_USER'], environ['JENKINS_PASSWORD'])
  JENKINS_HOST = '{}'.format(environ['JENKINS_HOST'])
  response = requests.get('{}/overallLoad/api/json'.format(JENKINS_HOST), auth=AUTH, timeout=1)
  if response.status_code != 200:
    raise Exception('Jenkins: {} - {}'.format(response.status_code, response.reason))

def openldap_check():
  server = Server(environ['LDAP_HOST'], use_ssl=False, connect_timeout=1) 
  Connection(server, user=environ['LDAP_ADMIN'], password=environ['LDAP_PASSWORD'], auto_bind=True)

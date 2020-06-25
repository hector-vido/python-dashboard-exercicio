#!/usr/bin/python3

import docker
from config import login_required
from flask import Blueprint, render_template, redirect

# definir blueprint na variavel docker_routes e chamá-lo de docker_rotes

# utilizar um dos métodos do módulo "docker" para se conectar ao docker
# unix socket ou tcp
# atribuindo-o a variável "client"
client = None

@docker_routes.route('/docker')
# adicionar decorator para verificar autenticação
def get_docker():
  conteineres = []
  for c in client.containers.list(all=True):
    pass
    # adicionar o dicionário dentro da lsita "conteineres"
    #{'short_id' : c.short_id, 'name' : c.name, 'image' : c.image.tags[0], 'status' : c.status}
  # enviar os contêineres para render_template
  return render_template('docker.html', var=outravar)

# criar a rota para iniciar os contêineres, ela deve receber o parâmetro "cid"
# adicionar decorator para verificar autenticação
def start_container(cid):
  # procurar o contêiner pelo id, e atribuí-lo a variável "c"
  c = None
  # iniciar o contêiner
  # redirecionar para /docker

@docker_routes.route('/docker/stop/<cid>')
# adicionar decorator para verificar autenticação
def stop_container(cid):
  # procurar o contêiner pelo id, e atribuí-lo a variável "c"
  c = None
  # parar o contêiner
  # redirecionar para /docker

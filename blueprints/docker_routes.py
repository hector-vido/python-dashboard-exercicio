#!/usr/bin/python3

import docker
from config import login_required
from flask import Blueprint, render_template, redirect

docker_routes = Blueprint('docker_routes', __name__)

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

@docker_routes.route('/docker')
@login_required
def get_docker():
  conteineres = []
  for c in client.containers.list(all=True):
    conteineres.append({'short_id' : c.short_id, 'name' : c.name, 'image' : c.image.tags[0], 'status' : c.status})
  return render_template('docker.html', conteineres=conteineres)

@docker_routes.route('/docker/start/<cid>')
@login_required
def start_container(cid):
  c = client.containers.get(cid)
  c.start()
  return redirect('/docker')

@docker_routes.route('/docker/stop/<cid>')
@login_required
def stop_container(cid):
  c = client.containers.get(cid)
  c.stop()
  return redirect('/docker')

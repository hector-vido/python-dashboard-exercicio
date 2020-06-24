#!/usr/bin/python3

import requests
from os import environ
from datetime import datetime
from config import login_required
from flask import Blueprint, flash, render_template, redirect, request, get_flashed_messages

from forms.gitea_user import UserFormCreate, UserFormEdit

gitea_routes = Blueprint('gitea_routes', __name__)

headers = {'Authorization' : 'token {}'.format(environ['GITEA_TOKEN'])}

@gitea_routes.route('/gitea')
@login_required
def get_gitea():
  response = requests.get('{}/api/v1/admin/users'.format(environ['GITEA_HOST']), headers=headers)
  users = response.json() if response.status_code == 200 else []
  for u in users:
    u['last_login'] = datetime.strptime(u['last_login'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y')

  response = requests.get('{}/api/v1/repos/search'.format(environ['GITEA_HOST']), headers=headers)
  repos = response.json() if response.status_code == 200 else []

  return render_template('gitea/index.html', users=users, repos=repos['data'])

@gitea_routes.route('/gitea/usuario')
@gitea_routes.route('/gitea/usuario/<username>')
@login_required
def get_usuario(username = None):
  if username:
    response = requests.get('{}/api/v1/users/{}'.format(environ['GITEA_HOST'], username), headers=headers)
    if response.status_code != 200:
      flash('Usuário <b>{}</b> não encontrado!'.format(username), 'error')
      return redirect('/gitea')
    form = UserFormEdit(data=response.json())
  else:
    form = UserFormCreate()
  return render_template('gitea/editar_usuario.html', form=form)

@gitea_routes.route('/gitea/usuario', methods=['POST'])
@gitea_routes.route('/gitea/usuario/<username>', methods=['POST'])
@login_required
def post_usuario(username = None):

  form = UserFormEdit(request.form) if username else UserFormCreate(request.form)
  if form.validate():
    if not username:
      response_user = requests.post('{}/api/v1/admin/users'.format(environ['GITEA_HOST']), headers=headers, json=form.data)
      if response_user.status_code != 201:
        data = response_user.json()
        flash('Gitea: ' + data['message'], 'error')

    if form.is_admin.data or username:
      response_admin = requests.patch('{}/api/v1/admin/users/{}'.format(environ['GITEA_HOST'], form.username.data), headers=headers, json={'admin' : form.is_admin.data, **form.data})
      if response_admin.status_code != 200:
        data = response_admin.json()
        flash('Gitea: ' + data['message'], 'error')

    if len(get_flashed_messages()) == 0:
      flash('Usuário <b>{}</b> {} com sucesso!'.format(form.email.data, 'atualizado' if username else 'cadastrado'), 'success')
      return redirect('/gitea')

  return render_template('gitea/editar_usuario.html', form=form)

@gitea_routes.route('/gitea/usuario/remover/<username>', methods=['GET'])
@login_required
def confirm_delete_usuario(username):
  response = requests.get('{}/api/v1/users/{}'.format(environ['GITEA_HOST'], username), headers=headers)
  if response.status_code != 200:
    flash('Usuário <b>{}</b> não encontrado!'.format(username), 'error')
    return redirect('/gitea')
  return render_template('gitea/remover_usuario.html', username=username)

@gitea_routes.route('/gitea/usuario/remover/<username>', methods=['POST'])
@login_required
def delete_usuario(username):
  response = requests.get('{}/api/v1/users/{}'.format(environ['GITEA_HOST'], username), headers=headers)
  if response.status_code != 200:
    flash('Usuário <b>{}</b> não encontrado!'.format(username), 'error')
  else:
    response = requests.delete('{}/api/v1/admin/users/{}'.format(environ['GITEA_HOST'], username), headers=headers)
    if response.status_code == 204:
      flash('Usuário <b>{}</b> removido com sucesso!'.format(username), 'success')
    else:
      flash('Problemas ao remover usuário <b>{}</b>!'.format(username), 'error')

  return redirect('/gitea')

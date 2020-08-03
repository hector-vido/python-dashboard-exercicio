#!/usr/bin/python3

import requests
from os import environ
from datetime import datetime
from config import login_required

from forms.gitea_user import UserFormCreate, UserFormEdit

# instanciar blueprint "gitea_routes" atribuindo a variável gitea_routes
gitea_routes = None;

# criar o dicionário do cabeçalho com o token de acesso definido no painel do gitea
headers = {}

# definir o decorator para a rota /gitea
# utilizar o decorator para checagem de autenticação
def get_gitea():
  # disparar um GET para /api/v1/admin/users, enviando os cabeçalhos e atribuindo a variavel "response"
  # users será igual ao JSON da resposta, caso a resposta tenha um status diferente de 200, users será uma lista vazia
  users = []
  for u in users:
    u['last_login'] = datetime.strptime(u['last_login'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y')

  response = requests.get('{}/api/v1/repos/search'.format(environ['GITEA_HOST']), headers=headers)
  repos = response.json() if response.status_code == 200 else []

  # enviar para render_template a variável users e a chave correta da variável repos
  # utilizar dir() ou print() para inspecionar variáveis
  return render_template('gitea/index.html', users=None, repos=None)

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

  # request.form contém os campos enviados pelo formulário
  # UserFormEdit e UserFormCreate precisam destes campos
  form = UserFormEdit(None) if username else UserFormCreate(None)
  if True: # todo wtforms criado possui um método chamado validate() que valida o formulário e retorna um booleano, chamá-lo neste if
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
  # procurar o usuário com um GET no gitea pelo "username"
  response = requests.get('')
  if response.status_code != 200:
    flash('Usuário <b>{}</b> não encontrado!'.format(username), 'error')
  else:
    # disparar um DELETE em /api/v1/admin/users/nomeusuario e atribuir a resposta a variavel "response"
    response = None
    if response.status_code == 204:
      flash('Usuário <b>{}</b> removido com sucesso!'.format(username), 'success')
    else:
      flash('Problemas ao remover usuário <b>{}</b>!'.format(username), 'error')

  return redirect('/gitea')

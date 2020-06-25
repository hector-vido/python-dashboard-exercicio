# Dashboard - Flask

Este é o repositório da aplicação, a infraestrutura utilizada está presente no diretório **docker**.

Para provisionar a aplicação recomendamos a utilização do módulo **venv**:

```bash
mkdir ~/projeto
cd ~/projeto
git clone https://github.com/hector-vido/python-dashboard.git .
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
cp .env-example .env
flask run
```

## Ambiente

Copie e modifique o arquivo de `.env-example` para indicar os usuários, senhas e tokens das demais aplicações:

```bash
cp .env-example .env
vim .env
```

## Dependências

As dependências do **python** são as seguintes:

- docker
- flask
- flask-wtf
- ldap3
- python-dotenv
- requests

## Criar Usuário

Existem várias formas de adicionar um usuário ao OpenLDAP, abaixo há um pequeno script que cria o grupo e o usuário utilizado para se logar ao painel:

```python
#!/usr/bin/env python3

from ldap3.utils.hashed import hashed
from ldap3 import Server, Connection, HASHED_SHA

server = Server('192.168.1.30', use_ssl=False)
ldap = Connection(server, user='cn=admin,dc=example,dc=com', password='4linux')

if not ldap.bind():
  print('Problemas ao se autenticar')
  exit(1)

ldap.add('ou=users,dc=example,dc=com', ['organizationalUnit'], {'ou' : 'users'})

ldif = {
  'cn': 'Developer',
  'sn': 'Desenvolvedor',
  'mail': 'developer@example.com',
  'uidNumber': 10001,
  'gidNumber': 10001,
  'homeDirectory': '/srv/home/developer',
  'uid': 'developer',
  'userPassword' : hashed(HASHED_SHA, '123')
}

object_classes = ['top', 'posixAccount', 'person', 'inetOrgPerson']

ldap.add('uid=developer,ou=users,dc=example,dc=com', object_classes, ldif)
```

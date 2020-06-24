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

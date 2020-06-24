# Provisionar

Para provisionar esta infraestrutura basta executar o seguinte comando a partir do diretório clonado:

```bash
cd docker
docker-compose up
```

Os contêineres utilizam a máscara 192.168.1.0/24.

## OpenLDAP

Para adicionar um usuário de testes no OpenLDAP - apenas para fins didáticos - acesse o contêiner do OpenLDAP:

```bash
docker exec -ti docker_ldap_1 bash
```

E então cadastre o novo usuário através do comando `ldapadd`:

```bash
ldapadd -D cn=admin,dc=example,dc=com -w 4linux <<EOF
dn: uid=developer,dc=example,dc=com
objectClass: top
objectClass: account
objectClass: posixAccount
cn: Desenvolvedor
uid: developer
uidNumber: 10000
gidNumber: 10000
homeDirectory: /srv/home/developer
loginShell: /bin/bash
userPassword: {SSHA}tEALeciuVaFehmWJSTCqGOCJqFcrM6zw
EOF
```

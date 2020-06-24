FROM debian:buster-slim
EXPOSE 80

COPY . /var/www/dashboard
WORKDIR /var/www/dashboard

ENV LDAP_HOST='192.168.1.30' \
  LDAP_ADMIN='cn=<user>,dc=example,dc=com' \
  LDAP_PASSWORD='password' \
  JENKINS_HOST='http://192.168.1.20:8080' \
  JENKINS_USER='user' \
  JENKINS_PASSWORD='password' \
  GITEA_HOST='http://192.168.1.10:3000' \
  GITEA_TOKEN='token'

RUN apt-get update && \
apt-get install -y libapache2-mod-wsgi-py3 apache2 python3-pip && \
apt-get clean
RUN pip3 install -r /var/www/dashboard/requirements.txt

# Possível sem o wtforms
# RUN apt-get update && \
# apt-get install -y libapache2-mod-wsgi-py3 apache2 python3-ldap3 python3-docker python3-flask python3-requests python3-dotenv && \
# apt-get clean

RUN mv /var/www/dashboard/docker/dashboard.conf /etc/apache2/sites-enabled/000-default.conf && \
mv /var/www/dashboard/docker/dashboard.wsgi /var/www/dashboard/ && \
rm -rf /var/www/dashboard/docker && \
sed -ri \
  -e 's!^(\s*CustomLog)\s+\S+!\1 /proc/self/fd/1!g' \
  -e 's!^(\s*ErrorLog)\s+\S+!\1 /proc/self/fd/2!g' \
  -e 's!^(\s*TransferLog)\s+\S+!\1 /proc/self/fd/1!g' \
  /etc/apache2/apache2.conf

CMD apachectl -DFOREGROUND -k start

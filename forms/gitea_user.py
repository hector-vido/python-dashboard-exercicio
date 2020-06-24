import re
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError

def password_check(form, field):
    if not re.search(UserForm.password_regex, field.data):
        raise ValidationError('A senha precisa ser mais forte')

class UserForm(Form):
  class Meta:
    locales = ['pt_BR', 'en_US']

  password_regex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,}$")

  username = StringField('Usuário', [validators.Length(min=4, max=32)], render_kw={"placeholder": "Usuário de login"})
  full_name = StringField('Nome', [validators.Length(min=4, max=32)], render_kw={"placeholder": "Nome completo"})
  email = StringField('E-mail', [validators.Length(min=6, max=255)], render_kw={"placeholder" : "E-mail, utilizado para nome de usuário"})
  password = PasswordField('Senha', [
      validators.DataRequired(),
      validators.Length(min=8),
      validators.EqualTo('confirm', message='As senhas devem ser iguais'),
      password_check
  ], render_kw={"placeholder" : "Senha de no mínimo 6 caracteres"})
  confirm = PasswordField('Repita a Senha', render_kw={"placeholder" : "Repita a senha"})
  is_admin = BooleanField('Este usuário é administrador')

class UserFormCreate(UserForm):
  must_change_password = BooleanField('Mudar a senha no primeiro acesso')

class UserFormEdit(UserForm):
  password = PasswordField('Senha', [
      validators.Optional(),
      validators.Length(min=8),
      validators.EqualTo('confirm', message='As senhas devem ser iguais'),
      password_check
  ], render_kw={"placeholder" : "Senha de no mínimo 6 caracteres"})
  username = StringField('Usuário', [validators.Length(min=4, max=32)], render_kw={"placeholder": "Usuário de login", "readonly" : "readonly"})

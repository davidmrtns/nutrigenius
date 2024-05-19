from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, DecimalField, FieldList
from wtforms.fields.form import FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from .models import Usuario


class FormCriarConta(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(8, 20)])
    confirmacao = PasswordField("Confirmação da senha", validators=[EqualTo("senha")])
    botao_submit_criar_conta = SubmitField("Criar conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Já existe um usuário cadastrado com esse e-mail")


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(8, 20)])
    lembrar_dados = BooleanField("Lembrar meus dados de acesso")
    botao_submit_login = SubmitField("Fazer login")


class FormIngrediente(FlaskForm):
    ingrediente = StringField("Ingrediente")


class FormCriarReceita(FlaskForm):
    ingredientes = FieldList(FormField(FormIngrediente), min_entries=3, max_entries=20)
    calorias = DecimalField("Calorias", validators=[DataRequired(), NumberRange(min=0)])
    botao_submit_criar_receita = SubmitField("Gerar receita")


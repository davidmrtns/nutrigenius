from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user

from .forms import FormCriarConta, FormLogin
from app import database, bcrypt
from .models import Usuario

def init_app(app):
    @app.route("/")
    def inicio():
        return render_template("inicio.html")


    @app.route("/login", methods=['GET', 'POST'])
    def login():
        form_login = FormLogin()

        if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
            usuario = Usuario.query.filter_by(email=form_login.email.data).first()
            if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
                login_user(usuario, remember=form_login.lembrar_dados.data)
                par_proximo = request.args.get('next')
                if par_proximo:
                    return redirect(par_proximo)
                else:
                    return redirect(url_for('dashboard'))
        return render_template("login.html", form_login=form_login)


    @app.route("/criar-conta", methods=['GET', 'POST'])
    def criar_conta():
        form_criar_conta = FormCriarConta()

        if form_criar_conta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
            senha_cript = bcrypt.generate_password_hash(form_criar_conta.senha.data)
            usuario = Usuario(nome=form_criar_conta.nome.data, email=form_criar_conta.email.data,
                              senha=senha_cript)
            database.session.add(usuario)
            database.session.commit()
            return redirect(url_for('login'))
        return render_template("criar_conta.html", form_criar_conta=form_criar_conta)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('inicio'))


    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

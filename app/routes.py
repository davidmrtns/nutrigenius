import openai
from flask import render_template, request, redirect, url_for, session, flash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import FormCriarConta, FormLogin, FormCriarReceita
from app import database, bcrypt
from .models import Usuario, Receita, Ingrediente, ModoPreparo
import json


def init_app(app):
    @app.route("/")
    def inicio():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template("inicio.html")


    @app.route("/login", methods=['GET', 'POST'])
    def login():
        form_login = FormLogin()
        if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
            usuario = Usuario.query.filter_by(email=form_login.email.data).first()
            if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
                login_user(usuario, remember=form_login.lembrar_dados.data)
                par_proximo = request.args.get('next')
                flash(f'Login feito com sucesso para o e-mail {form_login.email.data}', 'alert-success')
                if par_proximo:
                    return redirect(par_proximo)
                else:
                    return redirect(url_for('dashboard'))
            else:
                flash('Falha no login. E-mail ou senha incorretos', 'alert-danger')
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
            flash(f'Conta criada para o e-mail {form_criar_conta.email.data}', 'alert-success')
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
        receitas = Receita.query.filter_by(usuario_id=current_user.id).all()
        return render_template("dashboard.html", receitas=receitas)


    @app.route("/ver-receita/<id_receita>")
    @login_required
    def ver_receita(id_receita):
        receita = Receita.query.filter_by(usuario_id=current_user.id, id=id_receita).first()
        return render_template("ver_receita.html", receita=receita)


    @app.route("/criar-receita", methods=['GET', 'POST'])
    @login_required
    def criar_receita(receita=None):
        form_criar_receita = FormCriarReceita()
        num_entradas = request.args.get('num_entradas', default=3, type=int)
        if num_entradas >= 3:
            if num_entradas > 20:
                num_entradas = 20
                flash('Sua receita não pode ter mais do que 20 ingredientes', 'alert-info')
            form_criar_receita.ingredientes.min_entries = num_entradas
            if len(form_criar_receita.ingredientes.entries) < num_entradas:
                for _ in range(num_entradas - len(form_criar_receita.ingredientes.entries)):
                    form_criar_receita.ingredientes.append_entry()
        else:
            flash('Sua receita deve ter ao menos 3 ingredientes', 'alert-info')
        if not receita and form_criar_receita.validate_on_submit() and 'botao_submit_criar_receita' in request.form:
            itens = [ingrediente.ingrediente.data for ingrediente in form_criar_receita.ingredientes]
            ingredientes = ', '.join(itens)
            messages = [{"role": "system",
                         "content": f"Gere um dicionário Python de uma receita fitness de {form_criar_receita.calorias.data} calorias e usando os seguintes ingredientes: {ingredientes}. Devolva como resultado apenas o dicionário Pyhton, com as chaves 'nome_receita' e 'rendimento' (que deverão ser strings), calorias (que deve ser um número inteiro) e 'ingredientes' e 'modo_preparo' (que deverão ser listas contendo individualmente cada item). Separe tudo apenas por espaços únicos, não use quebras de linha ou indentação e não numere os passos do modo de preparo"}]
            chat = openai.chat.completions.create(
                model='gpt-4o', messages=messages
            )
            reply = chat.choices[0].message.content
            formatado = reply.replace("\'", "\"").replace("\n", "")
            receita = json.loads(formatado)
            receita["ingredientes_og"] = ingredientes
            session["receita"] = receita
            return criar_receita(receita)
        return render_template("criar_receita.html", form_criar_receita=form_criar_receita, receita=receita)

    @app.route("/regerar-receita")
    @login_required
    def regerar_receita():
        receita = session.get("receita")
        if receita:
            messages = [{"role": "system",
                         "content": f"Gere um dicionário Python de uma receita fitness de {receita.get("calorias")} calorias e usando os seguintes ingredientes: {receita.get("ingredientes_og")}. A receita deve ser diferente de {receita.get("nome_receita")} Devolva como resultado apenas o dicionário Pyhton, com as chaves 'nome_receita' e 'rendimento' (que deverão ser strings), calorias (que deve ser um número inteiro) e 'ingredientes' e 'modo_preparo' (que deverão ser listas contendo individualmente cada item). Separe tudo apenas por espaços únicos, não use quebras de linha ou indentação e não numere os passos do modo de preparo"}]
            chat = openai.chat.completions.create(
                model='gpt-4o', messages=messages
            )
            reply = chat.choices[0].message.content
            formatado = reply.replace("\'", "\"").replace("\n", "")
            receita = json.loads(formatado)
            session["receita"] = receita
            return criar_receita(receita)


    @app.route("/salvar-receita")
    @login_required
    def salvar_receita():
        receita = session.get("receita")
        if receita:
            receita_salva = Receita(nome=receita.get("nome_receita"), calorias=receita.get("calorias"), rendimento=receita.get("rendimento"), usuario=current_user)
            database.session.add(receita_salva)
            for ingrediente in receita.get("ingredientes"):
                ingrediente_receita = Ingrediente(nome=ingrediente, receita=receita_salva)
                database.session.add(ingrediente_receita)
            for index, passo in enumerate(receita.get("modo_preparo")):
                pass_modo_preparo = ModoPreparo(passo=passo, ordem=index, receita=receita_salva)
                database.session.add(pass_modo_preparo)
            database.session.commit()
            session.pop('receita', None)
        return redirect(url_for('dashboard'))


    @app.route("/excluir-receita/<id_receita>")
    @login_required
    def excluir_receita(id_receita):
        receita = Receita.query.filter_by(usuario_id=current_user.id, id=id_receita).first()
        if receita:
            database.session.delete(receita)
            database.session.commit()
            flash('A receita foi excluída', 'alert-danger')
        return redirect(url_for('dashboard'))

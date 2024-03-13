from flask import render_template

def init_app(app):
    @app.route("/")
    def inicio():        
        return render_template("inicio.html")
    
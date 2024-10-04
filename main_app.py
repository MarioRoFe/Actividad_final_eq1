from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, session, redirect, url_for
import numpy as np
import os
from dotenv import load_dotenv
from tensorflow.keras.models import load_model

def create_app():
    # Iinicializar la aplicación y las extensiones
    app = Flask(__name__)
    bootstrap = Bootstrap5(app)

    app.config.from_mapping(
        SECRET_KEY= os.getenv("SECRET_KEY")
    )

    model = load_model("./modelo_corto.keras")


    @app.route("/")
    def index():
        return render_template("index.html")


    @app.route("/encuesta", methods=["GET", "POST"])
    def encuesta():
        if request.method == "POST":
            session["reservas"] = request.form.get("reservas")
            session["comida_bebidas"] = request.form.get("comida_bebidas")
            session["asientos"] = request.form.get("asientos")
            session["amenidades"] = request.form.get("amenidades")
            session["servicio_abordo"] = request.form.get("servicio_abordo")
            session["checking"] = request.form.get("checking")
            session["personal"] = request.form.get("personal")
            session["limpieza"] = request.form.get("limpieza")
            return redirect(url_for("resultado"))
        return render_template("encuesta.html")


    @app.route("/resultado", methods=["GET"])
    def resultado():
        reservas = int(session.get("reservas"))
        comida = int(session.get("comida_bebidas"))
        asientos = int(session.get("asientos"))
        amenidades = int(session.get("amenidades"))
        servicio = int(session.get("servicio_abordo"))
        cheking = int(session.get("checking"))
        personal = int(session.get("personal"))
        limpieza = int(session.get("limpieza"))

        entrada = np.array([
            [reservas,
            comida, asientos, 
            amenidades, servicio, 
            cheking, personal, limpieza]])
        
        prediccion = model.predict(entrada)

        if prediccion <= 0.5:
            resultado_cliente = "Insatisfecho"
        else:
            resultado_cliente = "Satisfecho"
        
        return render_template("resultado.html",
                            prediccion = prediccion[0][0],
                            resultado_cliente=resultado_cliente) 
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
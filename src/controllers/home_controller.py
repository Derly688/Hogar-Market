from src.app import app 
from flask import render_template
from flask_controller import FlaskController

class HomeController(FlaskController):
  @app.route('/')
  def index():
      
<<<<<<< HEAD
    return render_template('inicio-de-sesion.html')
  
  @app.route('/inicio-de-sesion.html')
  def inicio_sesion():
      return render_template('inicio-de-sesion.html')
=======
    return render_template('inicio-de-sesion.html')
>>>>>>> 19a1a418060f82a1bd470b87b9e26a74659bebf1

import os
from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
import numpy as np

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)

    def json(self):
        return {'id': self.id, 'title': self.title, 'description': self.description}

with app.app_context():
    db.create_all()
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/home')
def casa():
    return render_template("index.html")

@app.route('/insertar', methods=['POST', 'GET'])
def insertar():
    bandera = ""
    if request.method=='GET':
        bandera = ""
        mostrar = False
        return render_template("inNotas.html", bandera = bandera)

        
    else: 
        
        titulo = request.form['title']
        descripcion = request.form['des']
        temp_nota = Note(title=titulo, description = descripcion)
        db.session.add(temp_nota)
        db.session.commit()
        bandera = "La nota ha sido insertada"
        
        return render_template("inNotas.html", bandera = bandera)
    

@app.route('/eliminar', methods=['POST'])
def eliminar():
    note_id = request.form.get('id')  # Obtiene el ID desde el formulario
    note = Note.query.get(note_id)  # Busca la nota en la base de datos

    if note:
        db.session.delete(note)  # Elimina la nota
        db.session.commit()  
        return render_template("delNotas.html", mensaje="Nota eliminada con éxito")
    else:
        return render_template("delNotas.html", mensaje="Nota no encontrada")

    

@app.route('/actualizar', methods=['POST'])
def actualizar():
    note_id = request.form.get('id')
    note = Note.query.get(note_id)

    if note:
        note.title = request.form.get('title')
        note.description = request.form.get('des')

        db.session.commit()  # Guarda cambios en la base de datos
        return render_template("updNotas.html", mostrar=False, bandera="Actualizado correctamente")
    else:
        return render_template("updNotas.html", mostrar=False, bandera="No encontrado")
    

@app.route('/actualizar', methods=['GET'])
def buscar_act():
    note_id = request.args.get('id')
    note = Note.query.get(note_id)  # Busca por ID

    if note:
        return render_template("updNotas.html", mostrar=True, tit=note.title, desdes=note.description, id=note.id)
    else:
        return render_template("updNotas.html", mostrar=False, bandera="No encontrado")
    
@app.route('/eliminar', methods=['GET'])
def buscar_del():
    note_id = request.args.get('id')
    note = Note.query.get(note_id)  # Busca por ID

    if note:
        return render_template("delNotas.html", mostrar=True, tit=note.title, desdes=note.description, id=note.id)
    else:
        return render_template("delNotas.html", mostrar=False, bandera="No encontrado")

@app.route('/todo')
def todo():
    data = db.session.query(Note).all()
    return render_template("verNotas.html", notas = data)


@app.route('/ver_uno', methods=['POST','GET'])
def ver_uno():
    bandera = ""
    if request.method=='GET':
        bandera = ""
        mostrar = False
        return render_template("unoNotas.html", bandera = bandera,  mostrar = mostrar)

        
    else: 
        id = request.form['id']
        data = db.session.get(Note, id)
        
        tit = data.title
        desdes= data.description
        bandera = "La nota ha sido encontrada"
        mostrar = True
        return render_template("unoNotas.html", bandera = bandera, tit = tit, desdes = desdes,  mostrar = mostrar)
  


@app.route('/test', methods=['POST'])
def test():
    return 0

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

from flask import Flask, render_template, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost:5432/db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Usuarios(db.Model):
    __tablename__ = "usuarios"
    idUsuario = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(255))

    def __init__(self,email, password):
        self.email=email
        self.password=password

class Editorial(db.Model):
    __tablename__="editorial"
    id_editorial = db.Column(db.Integer, primary_key=True)
    nombre_editorial = db.Column(db.String(80))

    def __init__(self, nombre_editorial):
        self.nombre_editorial = nombre_editorial

class Libro(db.Model):
    __tablename__ = "libro"
    id_libro = db.Column(db.Integer, primary_key=True)
    titulo_libro = db.Column(db.String(80))
    fecha_publicacion = db.Column(db.Date)
    numero_paginas = db.Column(db.Integer)
    formato = db.Column(db.String(30))
    volumen = db.Column(db.Integer)

    id_editorial = db.Column(db.Integer, db.ForeignKey("editorial.id_editorial"))
    id_autor = db.Column(db.Integer, db.ForeignKey("autor.id_autor"))
    id_genero = db.Column(db.Integer, db.ForeignKey("genero.id_genero"))

    def __init__(self, titulo_libro, fecha_publicacion, numero_paginas, formato, volumen, id_editorial, id_autor, id_genero):
        self.titulo_libro = titulo_libro
        self.fecha_publicacion = fecha_publicacion
        self.numero_paginas = numero_paginas
        self.formato = formato
        self.volumen = volumen
        self.id_editorial = id_editorial
        self.id_autor = id_autor
        self.id_genero = id_genero

class Autor(db.Model):
    __tablename__="autor"
    id_autor = db.Column(db.Integer, primary_key=True)
    nombre_autor = db.Column(db.String(130))
    fecha_nac = db.Column(db.Date)
    nacionalidad = db.Column(db.String(30))

    def __init__(self,nombre_autor, fecha_nac, nacionalidad):
        self.nombre_autor = nombre_autor
        self.fecha_nac = fecha_nac
        self.nacionalidad = nacionalidad

class Genero (db.Model):
    __tablename__ = "genero"
    id_genero = db.Column(db.Integer, primary_key=True)
    nombre_genero = db.Column(db.String(130))

    def __init__(self, nombre_genero):
        self.nombre_genero = nombre_genero

class Misfavoritos(db.Model):
    __tablename__ = "misfavoritos"
    id_lista_favoritos = db.Column(db.Integer, primary_key=True)

    id_libro = db.Column(db.Integer, db.ForeignKey("libro.id_libro"))
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.idUsuario"))

    def __init__(self, id_libro, id_usuario):
        self.id_libro = id_libro
        self.idUsuario = id_usuario

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/inicio")
def index():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    return render_template("/catalogo.html")

@app.route("/registrar")
def registrar():
    return render_template("registrar.html")

@app.route("/registrar_usuario", methods=['POST'])
def registrar_usuario():
    email = request.form.get("email")
    password = request.form.get("password")
    password_cifrado = bcrypt.generate_password_hash(password)
    print(email)
    print(password)
    print(password_cifrado)

    usuario = Usuarios(email = email, password = password_cifrado)
    db.session.add(usuario)
    db.session.commit()

    return "Registro exitoso"

@app.route("/iniciar")
def iniciar():
    return render_template("index.html")

@app.route("/formulario_editorial")
def formulario_editorial():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    return render_template("formEditorial.html", consulta_editorial=consulta_editorial)

@app.route("/formulario_libro")
def formulario_libro():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    consulta_genero = Genero.query.all()
    print(consulta_genero)
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    return render_template("formLibro.html",consulta_editorial=consulta_editorial,consulta_genero=consulta_genero,consulta_autor=consulta_autor) 

@app.route("/formulario_autor")
def formulario_autor():
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    return render_template("formAutor.html", consulta_autor=consulta_autor)

@app.route("/formulario_genero")
def formulario_genero():
   consulta_genero = Genero.query.all()
   print(consulta_genero)
   return render_template("formGenero.html", consulta_genero=consulta_genero)
    
@app.route("/registrar_libro", methods=['POST'])
def registrar_libro():
    #Todo el codigo para guardar el libro de la base de datos
    titulo_libro = request.form.get("titulo_libro")
    fecha_publicacion = request.form.get("fecha_publicacion")
    numero_paginas = request.form.get("numero_paginas")
    formato = request.form.get("formato")
    id_editorial = request.form.get("editorial")
    id_genero = request.form.get("genero")
    id_autor = request.form.get("autor")
    numero_paginas= int(numero_paginas)
    volumen = request.form.get("volumen")
    volumen = int(volumen)
    

    libro_nuevo = Libro(
        titulo_libro=titulo_libro, 
        fecha_publicacion=fecha_publicacion, 
        formato=formato,
        id_editorial=id_editorial,
        id_genero=id_genero, 
        id_autor=id_autor, 
        numero_paginas=numero_paginas,
        volumen=volumen
    )
    db.session.add(libro_nuevo)
    db.session.commit()
    return redirect("/")

@app.route("/registrar_genero", methods=['POST'])
def registrar_genero():
     #Codigo para guardar generos en la base de datos 
    nombre_genero = request.form.get("nombre_genero")
    genero_nuevo = Genero(nombre_genero=nombre_genero)
    db.session.add(genero_nuevo)
    db.session.commit()
    return redirect("/")

@app.route("/registrar_autor", methods=['POST'])
def registrar_autor():
    #Codigo para guardar el autor en la base de datos
    nombre_autor = request.form.get("nombre_autor")
    fecha_nac = request.form.get("fecha_nac")
    nacionalidad = request.form.get("nacionalidad")

    autor_nuevo = Autor(nombre_autor=nombre_autor, fecha_nac=fecha_nac, nacionalidad=nacionalidad)
    db.session.add(autor_nuevo)
    db.session.commit()
    return redirect("/")

@app.route("/registrar_editorial", methods=['POST'])
def registrar_editorial(): 
    #Codigo para guardar la editorial en la base de datos
    nombre_editorial = request.form.get("nombre_editorial")

    editorial_nueva = Editorial(nombre_editorial=nombre_editorial)
    db.session.add(editorial_nueva)
    db.session.commit()
    return redirect("/")

@app.route("/catalogo")
def catalogo():
    Consulta = Libro.query.join(Genero, Libro.id_genero == Genero.id_genero).join(Autor, Libro.id_autor == Autor.id_autor).join(Editorial, Libro.id_editorial == Editorial.id_editorial).add_columns(Libro.titulo_libro, Autor.nombre_autor, Genero.nombre_genero, Editorial.nombre_editorial, Libro.numero_paginas, Libro.formato, Libro.volumen, Libro.fecha_publicacion, Libro.id_libro)
    return render_template("catalogo.html", libros = Consulta)


@app.route("/modificar_libro", methods=['POST'])
def modificar_libro():
    id_libro = request.form.get('id_libro')
    nuevo_titulo = request.form.get('titulo_libro')
    nueva_fechaP = request.form.get('fecha_publicacion')
    nuevo_numPag = request.form.get('numero_paginas')
    nuevo_formato = request.form.get('formato')
    nuevo_volumen = request.form.get('volumen')
    nuevo_genero = request.form.get('genero')
    nuevo_autor = request.form.get('autor')
    nueva_editorial = request.form.get('editorial')
    libro = Libro.query.filter_by(id_libro=int(id_libro)).first()
    libro.titulo_libro = nuevo_titulo
    libro.fecha_publicacion = nueva_fechaP
    libro.numero_paginas = nuevo_numPag
    libro.formato = nuevo_formato
    libro.volumen = nuevo_volumen
    libro.id_genero = nuevo_genero
    libro.id_autor = nuevo_autor
    libro.id_editorial = nueva_editorial
    db.session.commit()
    return redirect ("/catalogo")

@app.route("/editarLibro/<id>")
def editarLibro(id):
    libro = Libro.query.filter_by(id_libro=int(id)).first()
    consulta_editorial = Editorial.query.all()
    consulta_genero = Genero.query.all()
    consulta_autor = Autor.query.all()
    return render_template("editarLibro.html", libro=libro, consulta_editorial=consulta_editorial, consulta_genero=consulta_genero, consulta_autor=consulta_autor)

@app.route("/eliminarLibro/<id>")
def eliminarLibro(id):
    libro = Libro.query.filter_by(id_libro = int(id)).delete()
    db.session.commit()
    return redirect("/catalogo")

@app.route("/catalogoAutores")
def catalogoAutores():
    consulta_autor = Autor.query.all()
    for autor in consulta_autor:
        nombre_autor = autor.nombre_autor
        fecha_nac = autor.fecha_nac
        nacionalidad = autor.nacionalidad
    return render_template("catalogoAutores.html", consulta_autor=consulta_autor)

@app.route("/editarAutor/<id>")
def editarAutor(id):
    autor = Autor.query.filter_by(id_autor=int(id)).first()
    consulta_nombre = Autor.query.all()
    consulta_fecha_nac = Autor.query.all()
    consulta_nacionalidad = Autor.query.all()
    return render_template("editarAutor.html", autor=autor, consulta_nombre=consulta_nombre, consulta_fecha_nac=consulta_fecha_nac, consulta_nacionalidad=consulta_nacionalidad)

@app.route("/modificarAutor", methods=['POST'])
def modificarAutor():
    id_autor = request.form.get('id_autor')
    nuevo_nombre = request.form.get('nombre_autor')
    nueva_fecha = request.form.get('fecha_nac')
    nueva_nacionalidad = request.form.get('nacionalidad')
    autor = Autor.query.filter_by(id_autor=int(id_autor)).first()
    autor.nombre_autor = nuevo_nombre
    autor.fecha_nac = nueva_fecha
    autor.nacionalidad = nueva_nacionalidad
    db.session.commit()
    return redirect("/catalogoAutores")

@app.route("/eliminarAutor/<id>")
def eliminarAutor(id):
    autor = Autor.query.filter_by(id_autor=int(id)).delete()
    db.session.commit()
    return redirect("/catalogoAutores")

@app.route("/catalogoEditorial")
def catalogoEditorial():
    consulta_editorial = Editorial.query.all()
    for editorial in consulta_editorial:
        nombre_editorial = editorial.nombre_editorial
    return render_template("catalogoEditorial.html", consulta_editorial = consulta_editorial)

@app.route("/editarEditorial/<id>")
def editareditorial(id):
    editorial = Editorial.query.filter_by(id_editorial=int(id)).first()
    return render_template("editarEditorial.html", editorial=editorial)

@app.route("/modificarEditorial", methods=['POST'])
def modificareditorial():
    id_editorial = request.form['id_editorial']
    nuevo_nombre = request.form['nombre_editorial']

    editorial = Editorial.query.filter_by(id_editorial=int(id_editorial)).first()
    editorial.nombre_editorial = nuevo_nombre
    db.session.commit()
    return redirect("/catalogoEditorial")

@app.route("/eliminarEditorial/<id>")
def eliminareditorial(id):
    editorial = Editorial.query.filter_by(id_editorial = int(id)).delete()
    db.session.commit()
    return redirect("/catalogoEditorial")

@app.route("/catalogoGenero")
def catalogoGenero():
    consulta_genero = Genero.query.all()
    for genero in consulta_genero:
        nombre_genero = genero.nombre_genero
    return render_template("catalogoGenero.html", consulta_genero = consulta_genero)

@app.route("/editarGenero/<id>")
def editargenero(id):
    genero = Genero.query.filter_by(id_genero=int(id)).first()
    return render_template("editarGenero.html", genero=genero)

@app.route("/modificarGenero", methods=['POST'])
def modificargenero():
    id_genero = request.form.get('id_genero')
    nuevo_nombre = request.form.get('nombre_genero')

    genero = Genero.query.filter_by(id_genero=int(id_genero)).first()
    genero.nombre_genero = nuevo_nombre
    db.session.commit()
    return redirect("/catalogoGenero")

@app.route("/eliminarGenero/<id>")
def eliminargenero(id):
    genero = Genero.query.filter_by(id_genero=int(id)).delete()
    db.session.commit()
    return redirect("/catalogoGenero")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

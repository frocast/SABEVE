#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# [START app]
""" Comentario"""
import logging
import datetime
import socket
import os

from flask import Flask, render_template, request, redirect, session, url_for
#from flask_talisman import Talisman
# from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import jinja2

#from dbconnect import connection, run_query           

app = Flask(__name__)
#print type(app)
app.secret_key='Clave_secreta'

# csrf = SeaSurf(app)
#Talisman(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:p3nt35t1ng@127.0.0.1/aula_virtual"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#print template_dir
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
    autoescape=False
)

db = SQLAlchemy(app)

class Usuarios(db.Model):
    Nombre = db.Column(db.String(30))
    Apellido = db.Column(db.String(30))
    email = db.Column(db.String(30), primary_key=True)
    knd = db.Column(db.String(20))
    fecha_na = db.Column(db.String(15))
    institucion = db.Column(db.String(200))
    genero = db.Column(db.String(10))
    pasw = db.Column(db.String(20)) 
    id_grupo = db.Column(db.Integer)      

    def __init__(self, nombre, apellido, email, knd, fecha_na, institucion, genero, pasw, id_grupo):
        self.Nombre = nombre
        self.Apellido = apellido   
        self.email = email   
        self.knd = knd   
        self.fecha_na = fecha_na
        self.institucion = institucion   
        self.genero = genero  
        self.pasw = pasw
        self.id_grupo = id_grupo

class Intereses(db.Model):
    id_intereses = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))    
    pais = db.Column(db.String(50))        
    habilidades = db.Column(db.String(1000))        
    nota = db.Column(db.String(1000))        
    institucion = db.Column(db.String(100))        

    def __init__(self, email, pais, habilidades, nota, institucion):                        
        self.email = email                                            
        self.pais = pais
        self.habilidades = habilidades
        self.nota = nota
        self.institucion = institucion

class Biblioteca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    autor = db.Column(db.String(50))
    ISSNISBN = db.Column(db.String(20))    
    tipo = db.Column(db.String(10))
    editorial = db.Column(db.String(100))
    fecha = db.Column(db.Integer)
    idioma = db.Column(db.String(20))
    resena = db.Column(db.String(5000))
    link = db.Column(db.String(500))
    portada = db.Column(db.String(5000))       

    def __init__(self, titulo, autor, ISSNISBN, tipo, editorial, fecha, idioma, resena, link, portada):
        self.titulo = titulo
        self.autor = autor   
        self.ISSNISBN = ISSNISBN   
        self.tipo = tipo
        self.editorial = editorial
        self.fecha = fecha
        self.idioma = idioma
        self.resena = resena  
        self.link = link    
        self.portada = portada

class Podcasts(db.Model):
    id_pod = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(5000))
    email = db.Column(db.String(50))    
    fecha_pu = db.Column(db.DateTime, default=db.func.current_timestamp())
    url = db.Column(db.String(500))
    portada = db.Column(db.String(500))
    tipo = db.Column(db.String(10))

    def __init__(self, titulo, descripcion, email, url, portada, tipo):
        self.titulo = titulo
        self.descripcion = descripcion   
        self.email = email           
        self.url = url
        self.portada = portada
        self.tipo = tipo        

class Foro(db.Model):
    id_tema = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String(50))
    titulo = db.Column(db.String(200))
    mensaje = db.Column(db.String(500))
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())  

    def __init__(self, autor, titulo, mensaje):                        
        self.autor = autor
        self.titulo = titulo 
        self.mensaje = mensaje   

class Mensajes(db.Model):
    id_mensaje = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    id_tema= db.Column(db.Integer)       
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())  
    mensaje = db.Column(db.String(500))

    def __init__(self, email, id_tema, mensaje):                        
        self.email = email
        self.id_tema = id_tema 
        self.mensaje = mensaje               

class Moocs(db.Model):
    id_mooc = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(500))
    titulo = db.Column(db.String(100))
    email = db.Column(db.String(50)) 
    id_grupo = db.Column(db.Integer)   

    def __init__(self, descripcion, titulo, email, id_grupo):                
        self.descripcion = descripcion
        self.titulo = titulo 
        self.email = email
        self.id_grupo = id_grupo

class Contenido_mooc(db.Model):
    id_contenido = db.Column(db.Integer, primary_key=True)
    id_mooc = db.Column(db.Integer)
    titulo = db.Column(db.String(200))
    url = db.Column(db.String(500))
    email = db.Column(db.String(50))    

    def __init__(self, id_mooc, titulo, url, email):                        
        self.id_mooc = id_mooc
        self.titulo = titulo 
        self.url = url
        self.email = email

class Evaluaciones(db.Model):
    id_evaluaciones = db.Column(db.Integer, primary_key=True)
    id_mooc = db.Column(db.Integer)
    pregunta = db.Column(db.String(200))
    respuesta_1 = db.Column(db.String(500))
    respuesta_2 = db.Column(db.String(500))    
    respuesta_3 = db.Column(db.String(500))    

    def __init__(self, id_mooc, pregunta, respuesta_1, respuesta_2, respuesta_3):                        
        self.id_mooc = id_mooc
        self.pregunta = pregunta 
        self.respuesta_1 =respuesta_1
        self.respuesta_2 = respuesta_2        
        self.respuesta_3 = respuesta_3

class Resultados(db.Model):
    id_resultados = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    id_mooc = db.Column(db.Integer)
    calificacion = db.Column(db.String(500))    

    def __init__(self, email, id_mooc, calificacion):                        
        self.email = email
        self.id_mooc = id_mooc
        self.calificacion = calificacion   

class Sitios(db.Model):
    id_sitios = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    titulo = db.Column(db.String(100))
    link = db.Column(db.String(500))    

    def __init__(self, email, titulo, link):                        
        self.email = email
        self.titulo = titulo
        self.link = link
              
class Grupos(db.Model):
    id_grupo = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50)) 
    nombre = db.Column(db.String(100))        

    def __init__(self, email, nombre):                        
        self.email = email                   
        self.nombre = nombre                   

class Temas(db.Model):
    
    id_tema = db.Column(db.Integer, primary_key=True)
    id_grupo = db.Column(db.Integer) 
    tema = db.Column(db.String(100))  
    email = db.Column(db.String(50))        

    def __init__(self, id_grupo, tema, email):                        
        self.id_grupo = id_grupo                   
        self.tema = tema
        self.email = email

class Contenidos_tema(db.Model):
    id_contenido = db.Column(db.Integer, primary_key=True)
    id_tema = db.Column(db.Integer)    
    subtema = db.Column(db.String(100))        
    pdf_link = db.Column(db.String(1000))        
    habilitar = db.Column(db.String(10))        

    def __init__(self, id_tema, subtema, pdf_link, habilitar):                        
        self.id_tema = id_tema                                             
        self.subtema = subtema
        self.pdf_link = pdf_link
        self.habilitar = habilitar
        

def rendering_template(content_rendered = None, head_title = '', head_description = '', main_template = 'starter.html'):
    """ Main template rendering """

    template = JINJA_ENVIRONMENT.get_template(main_template)
    html_content = { 'content':content_rendered, 'head_title':head_title, 'head_description':head_description, 'email':session['email'], 'nombre':session['nombre'], 'tipo':session['kind'], 'fecha_na': session['fecha_na']}
    return template.render(html_content)

@app.route('/create_tables', methods=['GET'])
def create_tables():
    """Return a friendly HTTP greeting."""
    try:
        db.create_all()
        return "Tablas Creadas con exito"
    except e:
        return e


@app.route('/', methods=['GET','POST'])
def inicio():
    """Return a friendly HTTP greeting."""

    if request.method == 'GET':
        if "email" in session:
            com = Usuarios.query.filter_by(id_grupo=session['grupo']).all()
            usuario = Usuarios.query.filter_by(email=session['email']).all()
            interes = Intereses.query.filter_by(email=session['email']).all()
            html_content = { 'usuario':usuario, 'companeros': len(com), 'intereses':interes }
            return rendering_template(JINJA_ENVIRONMENT.get_template('profile.html').render(html_content), 'Perfil de Usuario') #prueba_template.render(valores)#render_template('starter.html', creadores = jinja2.Template.render(render_template('formulario.html')))	
        else:
                return redirect('/login')
    if request.method == 'POST':
        return "Acceso por metodo post"

@app.route('/profile', methods=['GET','POST'])
def profile():
    """Return a friendly HTTP greeting."""

    if request.method == 'GET':       
        email = request.args['u']        
        usuario = Usuarios.query.filter_by(email=email).all()
        interes = Intereses.query.filter_by(email=email).all()
        for dato in usuario:            
            com = Usuarios.query.filter_by(id_grupo=dato.id_grupo).all()            
        html_content = { 'usuario':usuario, 'companeros': len(com), 'intereses':interes  }
        return rendering_template(JINJA_ENVIRONMENT.get_template('profile.html').render(html_content), 'Perfil de Usuario') #prueba_template.render(valores)#render_template('starter.html', creadores = jinja2.Template.render(render_template('formulario.html')))	        
    institucion = request.form['institucion']  
    pais = request.form['pais']  
    nota = request.form['nota']  
    habilidades = request.form['habilidades']  
    
    interes = Intereses.query.filter_by(email=session['email']).first()

    if interes:
        interes = Intereses.query.filter_by(email=session['email']).update(dict(pais=pais))    
        db.session.commit()
        interes = Intereses.query.filter_by(email=session['email']).update(dict(institucion=institucion))    
        db.session.commit()
        interes = Intereses.query.filter_by(email=session['email']).update(dict(nota=nota))    
        db.session.commit()
        interes = Intereses.query.filter_by(email=session['email']).update(dict(habilidades=habilidades))    
        db.session.commit()    
    else:
        intere = Intereses(session['email'],pais,"Python",nota,institucion)
        db.session.add(intere)
        db.session.commit()
    return redirect(url_for('inicio'))
        

@app.route('/login', methods=['GET','POST'])
def login():
    """Return a friendly HTTP greeting."""

    if request.method == 'GET':
        return render_template('/login.html')

    email = request.form['email']
    pasw = request.form['pssw']
    
    usuarios = Usuarios.query.filter_by(email=email).all()
    
    #consulta = 'SELECT email, pasw, Nombre, knd, fecha_na FROM usuarios WHERE email = "%s";' %email
    #result = run_query(consulta)    
        # if result[0][0] == email and result[0][1] == pasw:
        #     session['email'] = email
        #     session['nombre'] = result[0][2]
        #     session['kind'] = result[0][3]
        #     session['fecha_na'] = result[0][4]
    try:
        for usuario in usuarios:
            if usuario.email == email and usuario.pasw == pasw:
                session['email'] = usuario.email
                session['nombre'] = usuario.Nombre
                session['kind'] = usuario.knd
                session['fecha_na'] = usuario.fecha_na
                session['grupo'] = usuario.id_grupo
    except: 
        return "Error en el Servidor"
    return redirect('/')

@app.route('/logout', methods=['GET','POST'])
def logout():
    print len(session)
    session.pop('email',None)
    session.pop('nombre',None)
    session.pop('kind',None)
    session.pop('fecha_na',None)   
    session.pop('grupo',None)   
    print len(session)
    # revisar funcion pop session.pop('apellido',None)
    return redirect('/login')    

@app.route('/register', methods=['GET','POST'])
def register():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return render_template('register.html',errortype=None)
    else:
        name = request.form['name']
        lastName = request.form['lastname']
        email = request.form['email']
        knd = request.form['kind']
        pasw = request.form['pssw']
        paswc = request.form['psswc']
        genero = request.form['gen']
        fecha_na = request.form['fecha_na']
        institucion = request.form['institucion']
        id_grupo = request.form['id_grupo']
        terms = request.form['terms']
        
        # Agregar comprobación de usuario existente
        if name and lastName and email and pasw and paswc and terms and knd and institucion and fecha_na and genero:
            if terms == "True":
                if pasw == paswc:
                    usuario = Usuarios(name, lastName, email, knd, fecha_na, institucion, genero, pasw, id_grupo)
                    db.session.add(usuario)
                    db.session.commit()
                    #query = 'INSERT INTO usuarios (Nombre, Apellido, email, knd, fecha_na, institucion, genero, pasw) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' %(name, lastName, email, knd, fecha_na, institucion, genero, pasw)
                    #print run_query(query)
                    session['email'] = email
                    session['nombre'] = name
                    session['kind'] = knd
                    session['fecha_na'] = fecha_na
                    session['grupo'] = id_grupo
                    return redirect('/')
                else:
                    return render_template('/register.html', errortype=2)
            else:
                return render_template('/register.html',errortype=1)
        else:
            return render_template('/register.html', errortype=0)

# Biblioteca -----------------------------------------------------------
# Consulta cambiar libro nuevo_registro
@app.route('/libros', methods=['GET','POST'])
def consulta():
    """Return a friendly HTTP greeting."""
    # if session['kind'] == "Admin" or session['kind'] == "Profesor":
    #     print session['kind']
    # else:
    #     print session['kind']

    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('libros.html').render(), 'Material Bibliografico', 'Consulte los materiales almaceados en la base de datos')

    pa_clave = request.form['pa_clave']
    idioma = request.form['idioma'] 
    rango = request.form['rango']

    #consulta = 'SELECT * FROM biblioteca WHERE titulo = "%s" OR autor = "%s" OR ISSNISBN = "%s" OR idioma = "%s" OR (fecha BETWEEN %d AND %d);' %(pa_clave, pa_clave, pa_clave, idioma, int(rango.split()[2][6:10]), int(rango.split()[2][6:]))
    #run_query(consulta)
    #print resultados    
    libros = Biblioteca.query.filter((Biblioteca.titulo==pa_clave) | (Biblioteca.autor==pa_clave) | (Biblioteca.ISSNISBN==pa_clave) | (Biblioteca.idioma==idioma) | (Biblioteca.fecha.between(int(rango[6:10]), int(rango[19:23])))).all()
    
    html_content = { 'libros': libros}
    return rendering_template(JINJA_ENVIRONMENT.get_template('resultadoliar.html').render(html_content), 'Resultados')

@app.route('/Resultadoliar', methods=['GET','POST'])
def resultados():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('resultadoliar.html').render(), 'Consulta', 'Elementos encontrados')
    nombre = request.form['idioma']
    return nombre

@app.route('/nuevoRegistro', methods=['GET','POST'])
def nuevo_registro():
    """Return a friendly HTTP greeting."""
    
    #Comprobar que el acceso se realiza desde un perfil de maestro
    if session['kind'] == "Alumno":
        return redirect('/')

    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('articulos.html').render(), 'Material Bibliografico', 'Registre nuevos contenidos')
    idioma = request.form['idioma']
    fecha = int(request.form['fecha'])
    titulo = request.form['titulo']
    autor = request.form['autor']
    tipo = request.form['tipo']
    ISSN_ISBN = request.form['isbn-issn']
    editorial = request.form['editorial']
    resena = request.form['resena']
    link = request.form['link']
    portada = request.form['portada']
    #query = 'INSERT INTO biblioteca (titulo, autor, ISSNISBN, tipo, editorial, fecha, idioma, resena, link, portada) VALUES ("%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s");' %(titulo, autor, ISSN_ISBN, tipo, editorial, fecha, idioma, resena, link, portada)
    #run_query(query)
    nuevoLibro = Biblioteca(titulo=titulo, autor=autor, ISSNISBN=ISSN_ISBN, tipo=tipo, editorial=editorial, fecha=fecha, idioma=idioma, resena=resena, link=link, portada=portada)
    db.session.add(nuevoLibro)
    db.session.commit()
    html_content = { 'ruta': 'nuevoRegistro', 'd_ruta':'Nuevo Registro'}
    return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), 'Consulta', 'Elementos encontrados') 


@app.route('/crear_grupo', methods=['GET','POST'])
def crear_grupo():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':        
        return rendering_template(JINJA_ENVIRONMENT.get_template('crear_grupo.html').render(), 'Crear Grupos', 'Crear grupos de estudio')
    nombre_de_grupo =  request.form['nombre_de_grupo']
    grupo = Grupos(session['email'], nombre_de_grupo)    
    db.session.add(grupo)
    db.session.commit()
    return redirect(url_for('crear_grupo'))

@app.route('/agregar_alumnos', methods=['GET','POST'])
def agregar_alumnos():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':     
        grupos = Grupos.query.filter_by(email=session['email']).all()
        html_content = { 'grupos': grupos }
        return rendering_template(JINJA_ENVIRONMENT.get_template('agregar_grupo.html').render(html_content), 'Agregar Alumno', 'Agregar un alumno a un grupo')
    id_grupo =  request.form['id_grupo']
    corre_alu =  request.form['corre_alu']
    alumno = Usuarios.query.filter_by(email=corre_alu).update(dict(id_grupo=id_grupo))
    db.session.commit()
    return redirect(url_for('inicio'))

# Clases -----------------------------------------------------------------------------
# clase_registro(profe), clase_material(ambos), clase_habilitar(prof) pdf, ppt
@app.route('/clase_registro', methods=['GET','POST'])
def clase_registro():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':        
        grupos = Grupos.query.filter_by(email=session['email']).all()
        html_content = { 'grupos': grupos }        
        return rendering_template(JINJA_ENVIRONMENT.get_template('registro_tema_clase.html').render(html_content), 'Material', 'Consulte el material disponible')
    tema = request.form['tema']
    id_grupo = request.form['id_grupo']
    tema = Temas(id_grupo, tema, session['email'])
    db.session.add(tema)
    db.session.commit()
    return redirect('/agregar_contenido')

@app.route('/agregar_contenido', methods=['GET','POST'])
def agregar_contenido():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        temas = Temas.query.filter_by(email=session['email']).all()
        html_content = { 'temas': temas }
        return rendering_template(JINJA_ENVIRONMENT.get_template('contenido_registro.html').render(html_content), 'Material', 'Consulte el material disponible')
    id_tema = request.form['id_tema']
    subtema = request.form['subtema']
    pdf_link = request.form['pdf_link']
    habilitar = request.form['habilitar']
    contenido = Contenidos_tema(id_tema,subtema, pdf_link, habilitar)
    db.session.add(contenido)
    db.session.commit()
    return redirect('clase_registro')

@app.route('/clase_habilitar', methods=['GET','POST'])
def clase_habilitar():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':    
        temas = Temas.query.filter_by(email=session['email']).all()
        html_content = { 'temas': temas }
        return rendering_template(JINJA_ENVIRONMENT.get_template('tema_selec.html').render(html_content), 'Material', 'Consulte el material disponible')
    habilitar = request.form['hab']
    return redirect(url_for('material_tema'))

@app.route('/subtema_habilitar', methods=['GET','POST'])
def subtema_habilitar():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':   
        id_tema = request.args['id_tema'] 
        contenidos = Contenidos_tema.query.filter_by(id_tema=id_tema).all()
        html_content = { 'contenidos': contenidos }
        return rendering_template(JINJA_ENVIRONMENT.get_template('material_habilitar.html').render(html_content), 'Material', 'Consulte el material disponible')
    id_contenido = request.form['id_contenido']
    habilitar = request.form['hab']
    contenido = Contenidos_tema.query.filter_by(id_contenido=id_contenido).update(dict(habilitar=habilitar))
    db.session.commit()
    return redirect(url_for('clase_material'))

@app.route('/clase_material', methods=['GET'])
def clase_material():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':        
        temas = Temas.query.filter_by(id_grupo=session['grupo']).all()
        html_content = { 'temas': temas }
        return rendering_template(JINJA_ENVIRONMENT.get_template('material_clases.html').render(html_content), 'Material', 'Consulte el material disponible')

@app.route('/material_tema', methods=['GET','POST'])
def material_tema():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':        
        id_tema = request.args['id_tema']
        contenidos = Contenidos_tema.query.filter_by(id_tema=id_tema).all()
        html_content = { 'contenidos': contenidos }
        return rendering_template(JINJA_ENVIRONMENT.get_template('material_temas.html').render(html_content), 'Material', 'Consulte el material disponible')
    nombre = request.form['idioma']
    return nombre

# Render del pdf
@app.route('/render_pdf', methods=['GET','POST'])
def pdf_render():
    """Return a friendly HTTP greeting."""
    if request.method == 'GET':
        link = request.args['link']
        titulo = request.args['titulo']
        return rendering_template(JINJA_ENVIRONMENT.get_template('pdf.html').render({ 'link':link }), titulo, " ")
    
    return "post"

# Podcast ------------------------------------------------------
# registro_podcast(prof) consula_audio(ambos) consulta_video(ambos) vista_video
@app.route('/registro_podcast', methods=['GET','POST'])
def registro_podcast():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('registro_podcast.html').render(), "Registrar  Nuevo Contenido", 'Vea a espertos hablar de un tema')
    titulo = request.form['titulo']
    url = request.form['url']
    tipo = request.form['tipo']
    descrip = request.form['descrip']
    portada = request.form['portada']
    podcast = Podcasts(titulo, descrip, session['email'], url, portada, tipo)
    db.session.add(podcast)
    db.session.commit()
    #run_query('INSERT INTO podcasts (titulo, descripcion, email, fecha_pu, url, portada, tipo) VALUES ("%s", "%s", "%s", NOW(), "%s", "%s", "%s");' %(titulo, descrip, session['email'], url, portada, tipo))
    html_content = { 'ruta': 'podcast_'+tipo, 'd_ruta':'Podcast '+tipo}
    return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), "Podcast", 'Tema creado exitosamente')

@app.route('/podcast_video', methods=['GET','POST'])
def podcast_video():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        #consulta = 'SELECT * FROM podcasts WHERE tipo = "video";'
        podcasts_video =  Podcasts.query.filter_by(tipo='video')
        html_content = { 'info_video': podcasts_video} #podvideo.html
        return rendering_template(JINJA_ENVIRONMENT.get_template('miniatura.html').render(html_content), "Podcast en Video", 'Ve a espertos hablar de un tema')
    
    return "post"

@app.route('/vista_podcast', methods=['GET','POST'])
def vista_podcast():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        link = request.args['link']
        titulo = request.args['titulo']

        html_content = { 'link': link }
        return rendering_template(JINJA_ENVIRONMENT.get_template('vista_podcast.html').render(html_content), titulo, 'Ve a espertos hablar de un tema')
    
    return "post"

@app.route('/podcast_audio', methods=['GET','POST'])
def podcast_audio():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        
        #consulta = 'SELECT * FROM podcasts WHERE tipo = "audio";'
        podcasts_audio = Podcasts.query.filter_by(tipo="audio") #run_query(consulta)
        html_content = { 'info_audio': podcasts_audio}
        return rendering_template(JINJA_ENVIRONMENT.get_template('podaudio.html').render(html_content), "Podcast en Audio", 'Escuche a espertos hablar de un tema')
    return "post"

#MOOC'S ---------------------------------------------------------
# registro_tema_mooc(prfe, admin), registro_mooc(profe, admin), consulta_mooc(usuarios consula_mooc.html), vista_mooc(evalucion mooc.html) 

@app.route('/moocs', methods=['GET','POST'])
def moocs():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('moocs.html').render(), "Contenidos Complementarios", 'Aprenda de forma sencilla')
    nombre = request.form['idioma']
    return nombre  

@app.route('/registro_tema_mooc', methods=['GET','POST'])
def registro_tema_mooc():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        grupos = Grupos.query.filter_by(email=session['email']).all()
        html_content = { 'grupos': grupos }
        return rendering_template(JINJA_ENVIRONMENT.get_template('registro_tema_mooc.html').render(html_content), "Registro de Nuevo Tema", 'Aprender de forma sencilla')
    titulo = request.form['titulo']
    descrip = request.form['descrip']
    id_grupo = request.form['id_grupo']
    
    #run_query('INSERT INTO moocs (descripcion, titulo, email) VALUES ("%s", "%s", "%s");' %(descrip, titulo, session['email']))
    tema_mooc = Moocs(descrip, titulo, session['email'], id_grupo)
    db.session.add(tema_mooc)
    db.session.commit()
    html_content = {'ruta':'moocs', 'd_ruta':'Regresar a Moocs'}
    return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), "Registro de Nuevo Tema", 'Aprender de forma sencilla')

@app.route('/registro_mooc', methods=['GET','POST'])
def registro_mooc():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        #consulta = 'SELECT * FROM moocs WHERE email = "%s";' %(session['email'])        
        temas = Moocs.query.filter_by(email=session['email']) #run_query(consulta)
        html_content = { 'temas':temas }
        return rendering_template(JINJA_ENVIRONMENT.get_template('registro_mooc.html').render(html_content), "Registro de Nuevo Contenido", 'Aprender de forma sencilla')

    id_mooc = request.form['id_mooc']
    titulo_video = request.form['titulo_video']
    link = request.form['link']
    
    pregunta = request.form['pregunta']
    r1 = request.form['r1']
    r2 = request.form['r2']
    r3 = request.form['r3']
    
    #run_query('INSERT INTO contenido_mooc (id_mooc, titulo, url, email) VALUES ("%s", "%s", "%s", "%s");' %(id_mooc, titulo_video, link, session['email']))
    #run_query('INSERT INTO evaluaciones (id_mooc, pregunta, respuesta_1, respuesta_2, respuesta_3) VALUES ("%s", "%s", "%s", "%s", "%s");' %(id_mooc, pregunta, r1, r2, r3))
    try:
        contenido_mooc = Contenido_mooc(id_mooc, titulo_video, link, session['email'])
        db.session.commit() 
        db.session.add(contenido_mooc) 
            
        id_con = Contenido_mooc.query.filter_by(id_mooc=id_mooc, titulo=titulo_video, url=link, email=session['email']).first() 
        evaluacion = Evaluaciones(id_con.id_contenido, pregunta, r1, r2, r3)       
        db.session.add(evaluacion)
        db.session.commit() 
        html_content = {'ruta':'consulta_tema_mooc', 'd_ruta':'Regresar a Moocs'}
        return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), "Registro de Nuevo Contenido", 'Aprender de forma sencilla')
    except :
        return "Error"

@app.route('/consulta_tema_mooc', methods=['GET','POST'])
def consulta_tema_mooc():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        if session['kind'] == 'Admin' or session['kind'] == 'Profesor':
            temas_mooc = Moocs.query.filter_by(email=session['email']).all() 
            html_content = { 'info_mooc':temas_mooc }
            return rendering_template(JINJA_ENVIRONMENT.get_template('consulta_tema_mooc.html').render(html_content), "Contenidos Complementarios", 'Aprender de forma sencilla')    
        #consulta = 'SELECT * FROM moocs WHERE email = "%s";' %(session['email']) # CAMBIAR POR ID DEL GRUPO
        temas_mooc = Moocs.query.filter_by(id_grupo=session['grupo']).all() 
        html_content = { 'info_mooc':temas_mooc }
        return rendering_template(JINJA_ENVIRONMENT.get_template('consulta_tema_mooc.html').render(html_content), "Contenidos Complementarios", 'Aprender de forma sencilla')

    return "post"

@app.route('/consulta_mooc', methods=['GET','POST'])
def consulta_mooc():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        id_mooc = request.args['id']
        titulo = request.args['t']
        descrip = request.args['d']
        email = request.args['a']
        
        #consulta = 'SELECT * FROM contenido_mooc WHERE id_mooc = "%s";' %(id_mooc) # CAMBIAR POR ID DEL GRUPO
        contenidos_mooc = Contenido_mooc.query.filter_by(id_mooc=id_mooc).all() #run_query(consulta)     
        html_content = {'info_contenido':contenidos_mooc }
        return rendering_template(JINJA_ENVIRONMENT.get_template('consulta_mooc.html').render(html_content), "Contenidos Complementarios", 'Aprender de forma sencilla')

    return "post"

@app.route('/vista_mooc', methods=['GET','POST'])
def vista_mooc():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        id_mooc = request.args['id']
        titulo = request.args['t']
        url = request.args['u']
        email = request.args['a']
        #consulta = 'SELECT * FROM contenido_mooc WHERE id_mooc = "%s";' %(id_mooc)
        #resultados = run_query(consulta)
        html_content = {'id':id_mooc, 't':titulo, 'u':url, 'a':email }
        return rendering_template(JINJA_ENVIRONMENT.get_template('moocs.html').render(html_content), titulo, 'Aprender de forma sencilla')

    return "post"

@app.route('/evaluacion', methods=['GET','POST'])
def evaluacion():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        id_contenido = request.args['id']
        #titulo = request.args['t']
        #url = request.args['u']
        #email = request.args['a']
        #consulta = 'SELECT * FROM evaluaciones WHERE id_mooc = "%s";' %(id_mooc)
        resultados = Evaluaciones.query.filter_by(id_mooc=id_contenido) #run_query(consulta)
        html_content = {'info_evaluacion':resultados }        
        return rendering_template(JINJA_ENVIRONMENT.get_template('evaluacion.html').render(html_content), "Evaluar", 'Aprender de forma sencilla')
    respuesta = request.form['respuesta']
    id_mooc = request.form['id']
    #query = 'INSERT INTO resultados (email, id_mooc, calificacion) VALUES ("%s", "%s", "%s");' %(session['email'],id_mooc, respuesta)
    #run_query(query)
    try:
        resultado = Resultados(session['email'], int(id_mooc), respuesta)
        db.session.add(resultado)
        db.session.commit()
        html_content = {'ruta':'consulta_tema_mooc', 'd_ruta':'Regresar a Contenidos'}
        return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), "Evaluacion Exitosa", 'Aprender de forma sencilla')
    except Exception as inst:
        return type(inst)

# inicio de logica para foro -------------------------------------------

@app.route('/foro', methods=['GET','POST'])
def foro():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        # PARA MODIFICAR EL TEMA consulta = 'SELECT * FROM foro WHERE autor = "%s";' %session['email']
        #consulta = 'SELECT * FROM foro;'
        resultados = Foro.query.all() #run_query(consulta)

        if resultados:
            template = JINJA_ENVIRONMENT.get_template('foro_temas.html')
            html_content = { 'resultado':resultados}
            #print html_content
            return rendering_template(template.render(html_content),"Foros de discusion","Resulva cualquier duda")
            #return "pass" #rendering_template(JINJA_ENVIRONMENT.get_template('foro_temas.html').render(), "Foros de discusion", 'Resulva cualquier duda')
        else:
            template = JINJA_ENVIRONMENT.get_template('foro_temas.html')
            html_content = { 'resultado': False}
            return rendering_template(template.render(html_content),"Foros de discusion","Resulva cualquier duda")
            
    #nombre = request.form['idioma']
    return redirect("/")

@app.route('/foro/nuevo', methods=['GET','POST'])
def foro_nuevo():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('form_nu_foro.html').render(), "Foros de discusion", 'Crear nuevo tema')
    tema = request.form['subject']
    mensaje = request.form['message']
    #fecha = time.strftime("%x")
    #if True: #run_query('INSERT INTO foro (autor, titulo, mensaje, fecha) VALUES ("%s", "%s", "%s", NOW());' %(session['email'], tema, mensaje)):
    tema_nuevo = Foro(session['email'], tema, mensaje)
    db.session.add(tema_nuevo)
    db.session.commit()
    return redirect("/foro")
    #return rendering_template(JINJA_ENVIRONMENT.get_template('form_nu_foro.html').render(), "Foros de discusion", 'Resulva cualquier duda')
    #html_content = { 'ruta': 'foro', 'd_ruta':'Foro'}
    #return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), "Foros de discusion", 'Tema creado exitosamente')

@app.route('/foro/mensajes', methods=['GET','POST'])
def foro_contenido():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        tema_id = request.args['id_tema']        
        info_tema = Foro.query.filter_by(id_tema=tema_id).all() #run_query('SELECT * FROM foro WHERE id_tema = "%s";' %tema_id)
        info_mensajes = Mensajes.query.filter_by(id_tema=tema_id).all() #run_query('SELECT * FROM mensajes WHERE id_tema = "%s";' %tema_id)
        comentarios = len(info_mensajes)        
        if info_tema:            
            return rendering_template(JINJA_ENVIRONMENT.get_template('mensajes_foro.html').render({'info_tema':info_tema,'info_mensajes':info_mensajes, 'comentarios':comentarios}), info_tema[0].titulo, info_tema[0].mensaje)
        else:            
            return rendering_template(JINJA_ENVIRONMENT.get_template('mensajes_foro.html').render(), "Sin Temas", "Por favor Cree un tema")    
    return "metodo post" 

@app.route('/foro/messagesave', methods=['POST'])
def messasgesave():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'POST':
        id_tema = request.form['tema_id']        
        mensaje = request.form['mensaje']
        #print mensaje
        #run_query('INSERT INTO mensajes (email, id_tema, fecha, mensaje) VALUES ("%s", "%s", NOW(), "%s");' %(session['email'], id_tema, mensaje))
        mensaje = Mensajes(session['email'], id_tema, mensaje)
        db.session.add(mensaje)
        db.session.commit()
        url = '/foro/mensajes?id_tema=%s' %(id_tema)
        return redirect(url) 
    return "metodo post" 

@app.route('/foro/modificar', methods=['GET','POST'])
def foro_modificar():
    """Return a friendly HTTP greeting."""
        
    if request.method == 'GET':
        consulta = 'SELECT * FROM foro WHERE autor = "%s";' %session['email']
        resultados = [] #run_query(consulta)
        if resultados:
            template = JINJA_ENVIRONMENT.get_template('foro_temas.html')
            html_content = { 'resultado':resultados}
            #print html_content
            return rendering_template(template.render(html_content),"Foros de Discusion","Actualice la informacion o elimine")
            #return "pass" #rendering_template(JINJA_ENVIRONMENT.get_template('foro_temas.html').render(), "Foros de discusion", 'Resulva cualquier duda')
        else:
            template = JINJA_ENVIRONMENT.get_template('foro_temas.html')
            html_content = { 'resultado': False}
            return rendering_template(template.render(html_content),"Foros de Discusion"," ")
            
    #nombre = request.form['idioma']
    return redirect("/")

# Fin de logica para foro
# inicio de logica para cendario

@app.route('/calendar', methods=['GET','POST'])
def calendar():
    """Return a friendly HTTP greeting."""

    if request.method == 'GET':
        #return rendering_template()
        #return render_template('starter.html')
        return rendering_template(JINJA_ENVIRONMENT.get_template('calendar.html').render(), 'Calendario', 'Administre su tiempo') #prueba_template.render(valores)#render_template('starter.html', creadores = jinja2.Template.render(render_template('formulario.html')))	
    return "Acceso por metodo post"

@app.route('/sitios', methods=['GET','POST'])
def sitios():
    """Return a friendly HTTP greeting."""

    if request.method == 'GET':
        #return rendering_template()
        #return render_template('starter.html')
        sitios = Sitios.query.all()
        html_content = {'sitios':sitios}
        return rendering_template(JINJA_ENVIRONMENT.get_template('sitios.html').render(html_content), 'sitios de Interes', '') #prueba_template.render(valores)#render_template('starter.html', creadores = jinja2.Template.render(render_template('formulario.html')))	
    return "Acceso por metodo post"

@app.route('/nuevoSitio', methods=['GET','POST'])
def nuevoSitio():
    """Return a friendly HTTP greeting."""

    if request.method == 'GET':
        #return rendering_template()
        #return render_template('starter.html')
        return rendering_template(JINJA_ENVIRONMENT.get_template('nuevoSitio.html').render(), 'sitios de Interes', '') #prueba_template.render(valores)#render_template('starter.html', creadores = jinja2.Template.render(render_template('formulario.html')))	
    titulo = request.form['titulo']
    link = request.form['link']
    sitio = Sitios(session['email'], titulo, link)
    db.session.add(sitio)
    db.session.commit()
    return redirect("/sitios")

@app.route('/menuAdmin', methods=['GET','POST'])
def menuAdmin():
    """Return a friendly HTTP greeting."""

    if request.method == 'GET':    
        usuarios = Usuarios.query.all()
        clases = Temas.query.all()
        html_content = {'usuarios':usuarios, 'clases': clases }    
        return rendering_template(JINJA_ENVIRONMENT.get_template('menuAdmin.html').render(html_content), 'Menu de Administracion', '') #prueba_template.render(valores)#render_template('starter.html', creadores = jinja2.Template.render(render_template('formulario.html')))	

    return redirect(url_for('inicio'))

@app.errorhandler(404)
def page_not_found(e):
    return rendering_template(JINJA_ENVIRONMENT.get_template('404.html').render(), '404', 'Error de Pagina'), 404

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    #print __name__
    app.run(host='0.0.0.0', port=8080, debug=True)
# [END app]


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
from flask_talisman import Talisman
# from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import jinja2

#from dbconnect import connection, run_query           

app = Flask(__name__)
app.secret_key='Clave_secreta'
# csrf = SeaSurf(app)
Talisman(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
print template_dir
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

    def __init__(self, nombre="", apellido="", email="", knd="", fecha_na="", institucion="", genero="", pasw=""):
        self.Nombre = nombre
        self.Apellido = apellido   
        self.email = email   
        self.knd = knd   
        self.fecha_na = fecha_na
        self.institucion = institucion   
        self.genero = genero  
        self.pasw = pasw

def rendering_template(content_rendered = None, head_title = '', head_description = '', main_template = 'starter.html'):
    """ Main template rendering """

    template = JINJA_ENVIRONMENT.get_template(main_template)
    html_content = { 'content':content_rendered, 'head_title':head_title, 'head_description':head_description, 'email':session['email'], 'nombre':session['nombre'], 'tipo':session['kind'], 'fecha_na': session['fecha_na']}
    return template.render(html_content)

@app.route('/', methods=['GET','POST'])
def inicio():
    """Return a friendly HTTP greeting."""

    if request.method == 'GET':
        if "email" in session:
            return rendering_template(JINJA_ENVIRONMENT.get_template('profile.html').render(), 'Perfil de Usuario') #prueba_template.render(valores)#render_template('starter.html', creadores = jinja2.Template.render(render_template('formulario.html')))	
        else:
                return redirect('/login')
    if request.method == 'POST':
        return "Acceso por metodo post"

@app.route('/login', methods=['GET','POST'])
def login():
    """Return a friendly HTTP greeting."""

    if request.method == 'GET':
        return render_template('/login.html')

    email = request.form['email']
    pasw = request.form['pssw']

    usuarios = Usuarios()
    actuales = Usuarios.query.filter_by(email=email).all()
    
    #consulta = 'SELECT email, pasw, Nombre, knd, fecha_na FROM usuarios WHERE email = "%s";' %email
    #result = run_query(consulta)    
        # if result[0][0] == email and result[0][1] == pasw:
        #     session['email'] = email
        #     session['nombre'] = result[0][2]
        #     session['kind'] = result[0][3]
        #     session['fecha_na'] = result[0][4]
    try:
        for usuario in actuales:
            if usuario.email == email and usuario.pasw == pasw:
                session['email'] = usuario.email
                session['nombre'] = usuario.Nombre
                session['kind'] = usuario.knd
                session['fecha_na'] = usuario.fecha_na
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
        terms = request.form['terms']

        
        
        # Agregar comprobación de usuario existente
        if name and lastName and email and pasw and paswc and terms and knd and institucion and fecha_na and genero:
            if terms == "True":
                if pasw == paswc:
                    usuario = Usuarios(name, lastName, email, knd, fecha_na, institucion, genero, pasw)
                    db.session.add(usuario)
                    db.session.commit()
                    #query = 'INSERT INTO usuarios (Nombre, Apellido, email, knd, fecha_na, institucion, genero, pasw) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' %(name, lastName, email, knd, fecha_na, institucion, genero, pasw)
                    #print run_query(query)
                    session['email'] = email
                    session['nombre'] = name
                    session['kind'] = knd
                    session['fecha_na'] = fecha_na
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
    if session['kind'] == "Admin" or session['kind'] == "Profesor":
        print session['kind']
    else:
        print session['kind']

    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('libros.html').render(), 'Material Bibliografico', 'Consulte los materiales almaceados en la base de datos')

    pa_clave = request.form['pa_clave']
    idioma = request.form['idioma'] 
    rango = request.form['rango']

    consulta = 'SELECT * FROM biblioteca WHERE titulo = "%s" OR autor = "%s" OR ISSNISBN = "%s" OR idioma = "%s" OR (fecha BETWEEN %d AND %d);' %(pa_clave, pa_clave, pa_clave, idioma, int(rango.split()[2][6:10]), int(rango.split()[2][6:]))
    resultados = [] #run_query(consulta)
    print resultados
    html_content = { 'resultados': resultados}
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
    query = 'INSERT INTO biblioteca (titulo, autor, ISSNISBN, tipo, editorial, fecha, idioma, resena, link, portada) VALUES ("%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s");' %(titulo, autor, ISSN_ISBN, tipo, editorial, fecha, idioma, resena, link, portada)
    #run_query(query)
    html_content = { 'ruta': 'nuevoRegistro', 'd_ruta':'Nuevo Registro'}
    return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), 'Consulta', 'Elementos encontrados') 

# Clases -----------------------------------------------------------------------------
# clase_registro(profe), clase_material(ambos), clase_habilitar(prof) pdf, ppt
@app.route('/clase_registro', methods=['GET','POST'])
def clase_registro():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('material_clases.html').render(), 'Material', 'Consulte el material disponible')
    nombre = request.form['idioma']
    return nombre 

@app.route('/clase_habilitar', methods=['GET','POST'])
def clase_habilitar():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('material_clases.html').render(), 'Material', 'Consulte el material disponible')
    nombre = request.form['idioma']
    return nombre 

@app.route('/clase_material', methods=['GET','POST'])
def clase_material():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('material_clases.html').render(), 'Material', 'Consulte el material disponible')
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
    #run_query('INSERT INTO podcasts (titulo, descripcion, email, fecha_pu, url, portada, tipo) VALUES ("%s", "%s", "%s", NOW(), "%s", "%s", "%s");' %(titulo, descrip, session['email'], url, portada, tipo))
    html_content = { 'ruta': 'podcast_'+tipo, 'd_ruta':'Podcast '+tipo}
    return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), "Podcast", 'Tema creado exitosamente')

@app.route('/podcast_video', methods=['GET','POST'])
def podcast_video():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        consulta = 'SELECT * FROM podcasts WHERE tipo = "video";'
        resultados = [] #run_query(consulta)
        html_content = { 'info_video': resultados} #podvideo.html
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
        
        consulta = 'SELECT * FROM podcasts WHERE tipo = "audio";'
        resultados = [] #run_query(consulta)
        html_content = { 'info_audio': resultados}
        return rendering_template(JINJA_ENVIRONMENT.get_template('podaudio.html').render(html_content), "Podcast en Audio", 'Escuche a espertos hablar de un tema')
    return "post"

#MOOC'S ---------------------------------------------------------
# registro_tema_mooc(prfe, admin), registro_mooc(profe, admin), consulta_mooc(usuarios consula_mooc.html), vista_mooc(evalucion mooc.html) 

@app.route('/moocs', methods=['GET','POST'])
def moocs():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('moocs.html').render(), "Mooc's", 'Aprenda de forma sencilla')
    nombre = request.form['idioma']
    return nombre  

@app.route('/registro_tema_mooc', methods=['GET','POST'])
def registro_tema_mooc():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('registro_tema_mooc.html').render(), "Registro de Nuevo tema para MOOC", 'Aprender de forma sencilla')
    titulo = request.form['titulo']
    descrip = request.form['descrip']
    
    #run_query('INSERT INTO moocs (descripcion, titulo, email) VALUES ("%s", "%s", "%s");' %(descrip, titulo, session['email']))
    html_content = {'ruta':'moocs', 'd_ruta':'Regresar a Moocs'}
    return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), "Registro de Nuevo tema para MOOC", 'Aprender de forma sencilla')

@app.route('/registro_mooc', methods=['GET','POST'])
def registro_mooc():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        consulta = 'SELECT * FROM moocs WHERE email = "%s";' %(session['email'])
        resultados = [] #run_query(consulta)
        html_content = {'resultados':resultados }
        return rendering_template(JINJA_ENVIRONMENT.get_template('registro_mooc.html').render(html_content), "Registro de Nuevo tema para MOOC", 'Aprender de forma sencilla')

    id_mooc = request.form['id_mooc']
    titulo_video = request.form['titulo_video']
    link = request.form['link']
    
    pregunta = request.form['pregunta']
    r1 = request.form['r1']
    r2 = request.form['r2']
    r3 = request.form['r3']
    
    #run_query('INSERT INTO contenido_mooc (id_mooc, titulo, url, email) VALUES ("%s", "%s", "%s", "%s");' %(id_mooc, titulo_video, link, session['email']))
    #run_query('INSERT INTO evaluaciones (id_mooc, pregunta, respuesta_1, respuesta_2, respuesta_3) VALUES ("%s", "%s", "%s", "%s", "%s");' %(id_mooc, pregunta, r1, r2, r3))

    html_content = {'ruta':'consulta_tema_mooc', 'd_ruta':'Regresar a Moocs'}
    return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), "Registro de Nuevo tema para MOOC", 'Aprender de forma sencilla')

@app.route('/consulta_tema_mooc', methods=['GET','POST'])
def consulta_tema_mooc():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        consulta = 'SELECT * FROM moocs WHERE email = "%s";' %(session['email']) # CAMBIAR POR ID DEL GRUPO
        resultados = [] #run_query(consulta)     
        html_content = {'info_mooc':resultados }
        return rendering_template(JINJA_ENVIRONMENT.get_template('consulta_tema_mooc.html').render(html_content), "Temas de MOOC", 'Aprender de forma sencilla')

    return "post"

@app.route('/consulta_mooc', methods=['GET','POST'])
def consulta_mooc():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        id_mooc = request.args['id']
        titulo = request.args['t']
        descrip = request.args['d']
        email = request.args['a']
        
        consulta = 'SELECT * FROM contenido_mooc WHERE id_mooc = "%s";' %(id_mooc) # CAMBIAR POR ID DEL GRUPO
        resultados = [] #run_query(consulta)     
        html_content = {'info_contenido':resultados }
        return rendering_template(JINJA_ENVIRONMENT.get_template('consulta_mooc.html').render(html_content), "Temas de MOOC", 'Aprender de forma sencilla')

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
        id_mooc = request.args['id']
        #titulo = request.args['t']
        #url = request.args['u']
        #email = request.args['a']
        consulta = 'SELECT * FROM evaluaciones WHERE id_mooc = "%s";' %(id_mooc)
        resultados = [] #run_query(consulta)
        html_content = {'info_evaluacion':resultados }        
        return rendering_template(JINJA_ENVIRONMENT.get_template('evaluacion.html').render(html_content), "Evaluacion", 'Aprender de forma sencilla')
    respuesta = request.form['respuesta']
    id_mooc = request.form['id']
    query = 'INSERT INTO resultados (email, id_mooc, calificacion) VALUES ("%s", "%s", "%s");' %(session['email'],id_mooc, respuesta)
    #run_query(query)
    html_content = {'ruta':'consulta_tema_mooc', 'd_ruta':'Regresar a Mooc'}
    return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), "Evaluacion Exitosa", 'Aprender de forma sencilla')

# inicio de logica para foro -------------------------------------------

@app.route('/foro', methods=['GET','POST'])
def foro():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        # PARA MODIFICAR EL TEMA consulta = 'SELECT * FROM foro WHERE autor = "%s";' %session['email']
        consulta = 'SELECT * FROM foro;'
        resultados = [] #run_query(consulta)
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
    fecha = time.strftime("%x")
    if True: #run_query('INSERT INTO foro (autor, titulo, mensaje, fecha) VALUES ("%s", "%s", "%s", NOW());' %(session['email'], tema, mensaje)):
        return rendering_template(JINJA_ENVIRONMENT.get_template('form_nu_foro.html').render(), "Foros de discusion", 'Resulva cualquier duda')
    html_content = { 'ruta': 'foro', 'd_ruta':'Foro'}
    return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), "Foros de discusion", 'Tema creado exitosamente')

@app.route('/foro/mensajes', methods=['GET','POST'])
def foro_contenido():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        tema_id = request.args['id_tema']        
        info_tema = [] #run_query('SELECT * FROM foro WHERE id_tema = "%s";' %tema_id)
        info_mensajes = [] #run_query('SELECT * FROM mensajes WHERE id_tema = "%s";' %tema_id)
        if info_tema:            
            return rendering_template(JINJA_ENVIRONMENT.get_template('mensajes_foro.html').render({'info_tema':info_tema,'info_mensajes':info_mensajes}), info_tema[0][2], info_tema[0][3])
        else:            
            return rendering_template(JINJA_ENVIRONMENT.get_template('mensajes_foro.html').render(), "Sin Temas", "Por favor Cree un tema")    
    return "metodo post" 

@app.route('/foro/messagesave', methods=['POST'])
def messasgesave():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'POST':
        id_tema = request.form['tema_id']
        print id_tema
        mensaje = request.form['mensaje']
        print mensaje
        #run_query('INSERT INTO mensajes (email, id_tema, fecha, mensaje) VALUES ("%s", "%s", NOW(), "%s");' %(session['email'], id_tema, mensaje))
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
        return rendering_template(JINJA_ENVIRONMENT.get_template('sitios.html').render(), 'sitios de Interes', '') #prueba_template.render(valores)#render_template('starter.html', creadores = jinja2.Template.render(render_template('formulario.html')))	
    return "Acceso por metodo post"
####### Version anterior
@app.route('/inicioBiblioteca', methods=["GET", "POST"])
def inicioBiblioteca():

    if request.method == "GET":
        return render_template('inicioB.html', creadores = creadores)

    try:
        #c, conn = connection()
        #query = 'INSERT INTO cuerpo (ojo, boca) VALUES ("%s", "%s")' %(ojo, boca)
        #query = 'UPDATE cuerpo SET boca = "de Sandra" WHERE ojo = "azul" '
        query = 'SELECT Autor FROM Libros WHERE ISSN = "2530-1039" '
        #run_query(query)
        return("Operacion exitosa")
    except Exception as e:
        return(str(e))

@app.route('/busqueda', methods=["GET", "POST"])
def busqueda():
    if request.method == "GET":
        return render_template("Consulta_Libro.html")
    query = request.form['Busqueda']
    radio = request.form['radio1']
    return 'SELECT (Titulo, ano) FROM Libros WHERE %s = "%s" '%(radio, query)

@app.route('/registrarLibro', methods=["GET", "POST"])
def registrarLibro():

    if request.method == "GET":
        #return render_template('base.html', contenido = render_template('formulario.html'), creadores=creadores)
       # return render_template('formulario.html')
    #return render_template('Consulta_Libro.html')  
        return render_template("Registro_Libro.html")
    query = request.form['Registro']
    return render_template("Consulta_Libro.html")

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
    app.run(host='0.0.0.0', port=8080, debug=True)
# [END app]


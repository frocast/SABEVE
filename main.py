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

import jinja2, os, time

from flask import Flask, render_template, request, redirect, session
from dbconnect import connection, run_query           

app = Flask(__name__)
app.secret_key='Clave_secreta'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
print template_dir
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
    autoescape=False
)

def rendering_template(content_rendered = None, head_title = '', head_description = '', main_template = 'starter.html'):
    """ Main template rendering """

    template = JINJA_ENVIRONMENT.get_template(main_template)
    html_content = { 'content':content_rendered, 'head_title':head_title, 'head_description':head_description, 'email':session['email'], 'nombre':session['nombre'], 'tipo':session['kind'] }
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
    
    consulta = 'SELECT email, pasw, Nombre, knd FROM usuarios WHERE email = "%s";' %email
    result = run_query(consulta)
    if result:
        if result[0][0] == email and result[0][1] == pasw:
            session['email'] = email
            session['nombre'] = result[0][2]
            session['kind'] = result[0][3]
    return redirect('/')

@app.route('/logout', methods=['GET','POST'])
def logout():
    print len(session)
    session.pop('email',None)
    session.pop('nombre',None)
    session.pop('kind',None)   
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
        terms = request.form['terms']
        # Agregar comprobación de usuario existente
        if name and lastName and email and pasw and paswc and terms and knd:
            if terms == "True":
                if pasw == paswc:
                    query = 'INSERT INTO usuarios (Nombre, Apellido, email, knd, pasw) VALUES ("%s", "%s", "%s", "%s", "%s");' %(name, lastName, email, knd, pasw)
                    print run_query(query)
                    session['email'] = email
                    session['nombre'] = name
                    session['kind'] = knd
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
    if session['kind'] == "Admin" or session['kind'] == "Maestro":
        print session['kind']
    else:
        print session['kind']

    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('libros.html').render(), 'Libros', 'Consulte los materiales almaceados en la base de datos')

    pa_clave = request.form['pa_clave']
    idioma = request.form['idioma'] 
    rango = request.form['rango']

    consulta = 'SELECT * FROM biblioteca WHERE titulo = "%s" OR autor = "%s" OR ISSNISBN = "%s" OR idioma = "%s" OR (fecha BETWEEN %d AND %d);' %(pa_clave, pa_clave, pa_clave, idioma, int(rango.split()[2][6:10]), int(rango.split()[2][6:]))
    resultados = run_query(consulta)
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
        return rendering_template(JINJA_ENVIRONMENT.get_template('articulos.html').render(), 'Articulos', 'Consulte los materiales almacenados en la base de datos')
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
    print run_query(query)
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
    link = "link"
    if request.method == 'GET':
        link = request.args['link']
        titulo = request.args['titulo']
        return rendering_template(JINJA_ENVIRONMENT.get_template('pdf.html').render({ 'link':link }), titulo, " ")
    nombre = request.form['idioma']
    return link

# Podcast ------------------------------------------------------
# registro_podcast(prof) consula_audio(ambos) consulta_video(ambos) vista_video
@app.route('/podcast_video', methods=['GET','POST'])
def podcast_video():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('miniatura.html').render(), "Podcast en Video", 'Vea a espertos hablar de un tema')
    nombre = request.form['idioma']
    return nombre 

@app.route('/podcast_audio', methods=['GET','POST'])
def podcast_audio():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('podaudio.html').render(), "Podcast en Audio", 'Escuche a espertos hablar de un tema')
    nombre = request.form['idioma']
    return nombre 

#MOOC'S ---------------------------------------------------------
# registro_tema_mooc(prfe, admin), registro_mooc(profe, admin), consulta_mooc(usuarios consula_mooc.html), vista_mooc(evalucion mooc.html) 

@app.route('/moocs', methods=['GET','POST'])
def moocs():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        return rendering_template(JINJA_ENVIRONMENT.get_template('moocs.html').render(), "Mooc's", 'Aprenda de forma sencilla')
    nombre = request.form['idioma']
    return nombre  

# inicio de logica para foro -------------------------------------------

@app.route('/foro', methods=['GET','POST'])
def foro():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        # PARA MODIFICAR EL TEMA consulta = 'SELECT * FROM foro WHERE autor = "%s";' %session['email']
        consulta = 'SELECT * FROM foro;'
        resultados = run_query(consulta)
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
    if run_query('INSERT INTO foro (autor, titulo, mensaje, fecha) VALUES ("%s", "%s", "%s", NOW());' %(session['email'], tema, mensaje)):
        return rendering_template(JINJA_ENVIRONMENT.get_template('form_nu_foro.html').render(), "Foros de discusion", 'Resulva cualquier duda')
    html_content = { 'ruta': 'foro', 'd_ruta':'Foro'}
    return rendering_template(JINJA_ENVIRONMENT.get_template('success.html').render(html_content), "Foros de discusion", 'Tema creado exitosamente')

@app.route('/foro/mensajes:<tema_id><user>', methods=['GET','POST'])
def foro_contenido(tema_id, user):
    """Return a friendly HTTP greeting."""
    
    if request.method == 'GET':
        info_tema = run_query('SELECT * FROM foro WHERE id_tema = "%s";' %tema_id)
        info_mensajes = run_query('SELECT * FROM mensajes WHERE id_tema = "%s";' %tema_id)
        if info_tema:            
            return rendering_template(JINJA_ENVIRONMENT.get_template('mensajes_foro.html').render({'info_tema':info_tema,'info_mensajes':info_mensajes}), " ", " ")
        else:            
            return rendering_template(JINJA_ENVIRONMENT.get_template('mensajes_foro.html').render(), "", "")    
    return "metodo post" 

@app.route('/foro/messagesave', methods=['POST'])
def messasgesave():
    """Return a friendly HTTP greeting."""
    
    if request.method == 'POST':
        id_tema = request.form['tema_id']
        print id_tema
        mensaje = request.form['mensaje']
        print mensaje
        run_query('INSERT INTO mensajes (email, id_tema, fecha, mensaje) VALUES ("%s", "%s", NOW(), "%s");' %(session['email'], id_tema, mensaje))
        url = '/foro/mensajes:%s%s' %(id_tema, session['email'])
        return redirect(url) 
    return "metodo post" 

@app.route('/foro/modificar', methods=['GET','POST'])
def foro_modificar():
    """Return a friendly HTTP greeting."""
        
    if request.method == 'GET':
        consulta = 'SELECT * FROM foro WHERE autor = "%s";' %session['email']
        resultados = run_query(consulta)
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
        print run_query(query)
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


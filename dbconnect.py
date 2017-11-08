# #_# coding:utf-8 #_#
# #import MySQLdb

# def connection(host = "2001:4860:4864:1:53f2:a8e3:2b0e:801e", 
#                user = "root", 
#                passwd = "p3nt35t1ng", 
#                db = "aula_virtual"):                 # Valores por defecto para la conexion

#     try:                                                     
#         conn = MySQLdb.connect(host, user, passwd, db)   # Se realiza la conexion a la base de datos 
#         cursor = conn.cursor()                           # se crea el cursor que tiene acceso a las tablas y columnas           
#         return cursor, conn    
#     except Exception as e:
#         return(str(e))                                   # Imprime el error que se crea si existiera algun problema 

# def run_query(query = ''): 
    
#     cursor, conn = connection()    # se hace uso de la funcion connection para acceso a la base de datos
#     cursor.execute(query)          # Ejecutar una consulta 
 
#     if query.upper().startswith('SELECT'): 
#         data = cursor.fetchall()   # Traer los resultados de un select 
#     else: 
#         conn.commit()              # Hacer efectiva la escritura de datos 
#         data = False 
    
#     cursor.close()                 # Cerrar el cursor 
#     conn.close()                   # Cerrar la conexión 
    
#     return data
    

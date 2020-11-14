from flask import Flask, render_template, request,redirect,url_for, flash
import os
import psycopg2

app= Flask(__name__)

#base de datos
PSQL_HOST ="ec2-34-230-149-169.compute-1.amazonaws.com"
PSQL_PORT = "5432"
PSQL_USER = "aziehlocgovzyx"
PSQL_PASS = "38bbce6333948d60d560ca5d402f61dc0e7cfcf8f2392c8e555f570d6b43e44d"
PSQL_DB = "d80epcddpdinu8"
connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
conn = psycopg2.connect(connstr)
cursor = conn.cursor()
app.secret_key='mysecretkey'

#landing page
@app.route('/')
def init():
    return render_template('page.html')

#principal
@app.route('/index')
def index():
    estudiantes = select_info()
    return render_template('introduce.html', data = get_gender(), estudiantes= estudiantes)

#boton cancelar
@app.route('/cancel')    
def cancel():
    return redirect(url_for('index'))

#obtener genero
def get_gender():
    return {
        'MASCULINO':'MASCULINO',
        'FEMENINO':'FEMENINO',
        'OTROS':'OTROS',
    }

#agregar registro
@app.route('/add_info',methods=['POST'])
def add_info():
    try:
        if request.method =='POST':
            documento=request.form['documento']
            nombre=request.form['nombre']
            fecha=request.form['fecha']
            genero=request.form['genero']
            conn = psycopg2.connect(connstr)
            cursor= conn.cursor()        
            cursor.execute('INSERT INTO estudiante (doc,nombre,genero,fecha) values (%s,%s,%s,%s)',
            (documento,nombre,genero,fecha))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Registro Agregado') 
            return redirect(url_for('index')) 
    except Exception as err:
        flash('La cedula ya existe')
        return redirect(url_for('index'))

#traer informacion        
def select_info():
    conn = psycopg2.connect(connstr)
    cursor= conn.cursor()
    cursor.execute('SELECT * FROM estudiante')
    data = cursor.fetchall()
    cursor.close()     
    return data 
      
#actualizar registros
@app.route('/update_info/<string:id>', methods=['POST','GET'])
def update_info(id):
    conn = psycopg2.connect(connstr)
    cursor= conn.cursor()
    try:
        if request.method == 'GET':
            cursor.execute('select * from estudiante where id ={}'.format(id)) 
            data = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()  
            datos = data[0]
            return render_template('update.html',estudiante=datos,data=get_gender())
        else:
            documento=request.form['documento']
            nombre=request.form['nombre']
            fecha=request.form['fecha']
            genero=request.form['genero']    
            cursor.execute(""" 
                UPDATE estudiante 
                SET doc=%s,
                nombre=%s, 
                genero=%s,
                fecha=%s
                WHERE id=%s """, (documento,nombre,genero,fecha,id))
            conn.commit()
            cursor.close()
            conn.close()  
            flash('Registro Actualizado') 
            return redirect(url_for('index'))
    except Exception as err:
        flash('El registro de la cedula ya existe')
        return redirect(url_for('update_info'))         

#eliminar informacion
@app.route('/delete_info/<string:id>')
def delete_info(id):
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM estudiante WHERE id={}'.format(id))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Registro Eliminado') 
    return redirect(url_for('index')) 

#ejecucion de la aplicacion
if __name__ == '__main__':
    app.run(port=3000, debug=True)    
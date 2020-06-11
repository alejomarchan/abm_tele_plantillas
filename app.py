from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'abl_telefonica'
conn = MySQL(app)

#Sesion activa desde el navegador
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = conn.connection.cursor()
    cur.execute('select * from abl_telefonica.abl_telefonica')
    registros = cur.fetchall()
    print(registros)
    return render_template('index.html', registros_for_html = registros)

@app.route('/add_process', methods=['POST'])
def add_process():
    if request.method=='POST':
        proceso_form = request.form['proceso_form']
        predecesor_form = request.form['predecesor_form']
        tabla_form = request.form['tabla_form']
        print(proceso_form)
        cur = conn.connection.cursor()
        cur.execute('insert into abl_telefonica.abl_telefonica (proceso, predecesor,tabla) values (%s, %s, %s)',
        (proceso_form, predecesor_form, tabla_form))
        conn.connection.commit()
        flash('Registro almacenado correctamente')
    return redirect(url_for('index'))

@app.route('/edit_process/<string:proceso_html>')
def edit_process(proceso_html):
    cur = conn.connection.cursor()
    cur.execute('select * from abl_telefonica.abl_telefonica where proceso = %s', [proceso_html])
    registro = cur.fetchall()
    print(registro[0])
    return  render_template('edit_process.html', registro_for_html = registro[0])

@app.route('/update_process/<string:proceso_html>', methods=['POST'])
def update_process(proceso_html):
    if request.method=='POST':
        proceso_from_html = request.form['proceso_form']
        predecesor_from_html = request.form['predecesor_form']
        tabla_from_html = request.form['tabla_form']
        cur = conn.connection.cursor()
        cur.execute("""update abl_telefonica.abl_telefonica
                    set proceso = %s,
                        predecesor = %s,
                        tabla = %s
                    where proceso = %s""", (proceso_from_html,predecesor_from_html,tabla_from_html,proceso_html))
        conn.connection.commit()    
        flash('Registro actualizado correctamente')
        return redirect(url_for('index'))

@app.route('/delete_process/<string:proceso_html>')
def delete_process(proceso_html):
    print(proceso_html)
    cur = conn.connection.cursor()
    cur.execute('delete from abl_telefonica.abl_telefonica where proceso = %s', [proceso_html])
    cur.connection.commit()
    flash('Registro borrado correctamente')
    return redirect(url_for('index'))    

if __name__ == '__main__':
    app.run(port = 3000, debug = True)


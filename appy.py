#app.py

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"

DB_HOST = "localhost"
DB_NAME = "uni_luanda"
DB_USER = "postgres"
DB_PASS = "zb17"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route("/")
def index():
    curso = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #curso.execute("SELECT c.id, cc.nome, c.titulo, c.imagem FROM curso c inner join categoria_curso cc on c.categoria_id = cc.id ") # Execute the SQL
    #list_curso = curso.fetchall()
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

"""@app.route("/inscrever")
def inscrever():
    if session.get('logged_in'):
        return render_template('inscrever.html', list_user = data))
    else:
        return render_template('index.html', message="Hello!")"""
    
@app.route("/ver_Blog01")
def ver_Blog01():
    return render_template('ver_Blog01.html')

@app.route("/blog")
def blog():
    publicacao = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #publicacao.execute("SELECT c.id, cc.nome, c.titulo, c.descricao, c.imagem FROM publicacao c inner join categoria_publicacao cc on c.categoria_id = cc.id ") # Execute the SQL
    list_publicacao = publicacao.fetchall()
    return render_template('blog.html', list_publicacao = list_publicacao)    
    


@app.route("/contactos")
def contactos():
    return render_template('contactos.html')

@app.route('/inscrever')
def inscrever():
     curso = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     #curso.execute("SELECT c.id,  cc.nome, c.titulo FROM curso c inner join categoria_curso cc on c.categoria_id = cc.id") # Execute the SQL
     list_curso = curso.fetchall()
     return render_template('inscrever.html', list_curso = list_curso)


@app.route("/add_inscricao", methods=['POST'])
def add_inscricao():
    inscricao = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        dt_Nasc = request.form['dt_Nasc']
        curso = request.form['curso']
        #inscricao.execute("INSERT INTO inscricao (nome, email,data_nascimento, curso_id) VALUES (%s,%s,%s, %s)", (nome, email,dt_Nasc, curso))
        conn.commit()
        flash('Inscrição realizada com sucesso')
        return redirect(url_for('inscrever'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
     if request.method == 'GET':
        return render_template('login.html')
     else:
        user = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        email = request.form['email']
        palavra_passe = request.form['palavra_passe']
        #user.execute("SELECT email, palavra_passe FROM utilizador WHERE email = %s and palavra_passe = %s", (email, palavra_passe))
        data = user.fetchall()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return render_template('admin.html')
        

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

@app.route("/registrar")
def registrar():
    return render_template('registrar.html')    

@app.route("/add_registrar", methods=['POST'])
def add_registrar():
    user = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        palavra_passe = request.form['palavra_passe']
        user.execute("INSERT INTO utilizador (nome, email,palavra_passe) VALUES (%s,%s,%s)", (nome, email,palavra_passe))
        conn.commit()
        flash('Utilizador adicionado com sucesso')
        return redirect(url_for('registrar'))

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route("/users")
def users():
    #user = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #s = "SELECT * FROM utilizador"
    #user.execute(s) # Execute the SQL
    #list_users = user.fetchall()
    return render_template('users/users.html')

@app.route('/estudantes')
def estudantes():
     #estudantes = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     #estudantes.execute("SELECT ins.id, ins.nome, cc.nome, c.titulo FROM inscricao ins inner join curso c on ins.curso_id = c.id inner join categoria_curso cc on c.categoria_id = cc.id ") # Execute the SQL
     #list_estudantes = estudantes.fetchall()
     return render_template('estudantes/estudantes.html')            

@app.route("/cursos")
def cursos():
    #curso = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #curso.execute("SELECT c.id, cc.nome, c.titulo, c.descricao FROM curso c inner join categoria_curso cc on c.categoria_id = cc.id ") # Execute the SQL
    #list_curso = curso.fetchall()
    return render_template('cursos/cursos.html')   

@app.route('/cursos/ver_Curso/<id>')
def ver_Curso(id):
    curso = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    curso.execute("SELECT c.id, cc.nome, c.titulo, c.descricao FROM curso c inner join categoria_curso cc on c.categoria_id = cc.id order by c.id desc limit 6") # Execute the SQL
    list_curso = curso.fetchall()

    curso.execute('SELECT * FROM curso c inner join categoria_curso cc on c.categoria_id = cc.id  WHERE c.id = %s', (id))
    data = curso.fetchall()
    curso.close()
    print(data[0])
    return render_template('cursos/ver_Curso.html', curso = data[0], list_curso = list_curso)

@app.route("/create_curso")
def create_curso():
    #form = UploadForm()
    #curso = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #curso.execute("SELECT * FROM categoria_curso") # Execute the SQL
    #list_curso = curso.fetchall()
    return render_template('cursos/create.html')

class UploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])

@app.route("/add_curso", methods=['POST'])
def add_curso():
    form = UploadForm()

    #curso = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        categoria = request.form['categoria']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        filename = form.file.data.filename
        form.file.data.save(f'static/images/cursos/{filename}')

        curso.execute("INSERT INTO curso (categoria_id, titulo,descricao,imagem ) VALUES (%s,%s,%s, %s)", (categoria, titulo,descricao, filename))
        conn.commit()
        flash('Curso adicionado com sucesso')
        return redirect(url_for('create_curso'))

@app.route('/cursos/edit/<id>')
def get_curso(id):
    form = UploadForm()

    curso = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    curso.execute("SELECT * FROM categoria_curso") # Execute the SQL
    list_curso = curso.fetchall()

    curso.execute('SELECT c.id, cc.nome, c.titulo, c.descricao FROM curso c inner join categoria_curso cc on c.categoria_id = cc.id  WHERE c.id = %s', (id))
    data = curso.fetchall()
    curso.close()
    print(data[0])
    return render_template('cursos/edit.html', curso = data[0], list_curso = list_curso, form=form)

@app.route("/update_curso/<id>", methods=['POST'])
def update_curso(id):
    form = UploadForm()

    curso = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        categoria = request.form['categoria']
        titulo = request.form['titulo']                                            
        
        descricao = request.form['descricao']
        filename = form.file.data.filename
        form.file.data.save(f'static/images/cursos/{filename}')

        curso.execute("""UPDATE curso set categoria_id = %s, titulo = %s, descricao = %s ,imagem = %s where id = %s""", (categoria, titulo,descricao, filename, id )) 
        conn.commit()
        flash('Curso atualizado com sucesso')
        return redirect(url_for('create_curso'))

@app.route('/cursos/delete/<string:id>', methods = ['POST','GET'])
def delete_curso(id):
    curso = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    curso.execute('DELETE FROM curso WHERE id = {0}'.format(id))
    conn.commit()
    flash('Curso Removido com sucesso')
    return redirect(url_for('cursos'))

@app.route("/publicacoes")
def publicacoes():
    publicacao = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    publicacao.execute("SELECT c.id, cc.nome, c.titulo, c.descricao FROM publicacao c inner join categoria_publicacao cc on c.categoria_id = cc.id ") # Execute the SQL
    list_publicacao = publicacao.fetchall()
    return render_template('publicacoes/publicacoes.html', list_publicacao = list_publicacao)    

@app.route('/publicacoes/ver_Blog/<id>')
def ver_Blog(id):
    publicacao = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    publicacao.execute("SELECT c.id, cc.nome, c.titulo, c.descricao FROM publicacao c inner join categoria_publicacao cc on c.categoria_id = cc.id order by c.id desc limit 6") # Execute the SQL
    list_publicacao = publicacao.fetchall()

    publicacao.execute('SELECT * FROM publicacao c inner join categoria_publicacao cc on c.categoria_id = cc.id  WHERE c.id = %s', (id))
    data = publicacao.fetchall()
    publicacao.close()
    print(data[0])
    return render_template('publicacoes/ver_Blog.html', publicacao = data[0], list_publicacao = list_publicacao)


@app.route("/create_publicacoes")
def create_publicacoes():
    form = UploadForm()
    publicacoes = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    publicacoes.execute("SELECT * FROM categoria_publicacao") # Execute the SQL
    list_publicacoes = publicacoes.fetchall()
    return render_template('publicacoes/create.html', list_publicacoes = list_publicacoes, form=form)

@app.route("/add_publicacoes", methods=['POST'])
def add_publicacoes():
    form = UploadForm()

    publicacoes = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        categoria = request.form['categoria']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data = request.form['data']
        filename = form.file.data.filename
        form.file.data.save(f'static/images/blog/{filename}')

        publicacoes.execute("INSERT INTO publicacao (categoria_id, titulo,descricao,imagem, data ) VALUES (%s,%s,%s, %s, %s)", (categoria, titulo,descricao, filename, data ))
        conn.commit()
        flash('publicação adicionada com sucesso')
        return redirect(url_for('create_publicacoes'))

@app.route('/publicacao/edit/<id>')
def get_publicacao(id):
    form = UploadForm()

    publicacao = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    publicacao.execute("SELECT * FROM categoria_publicacao") # Execute the SQL
    list_publicacao = publicacao.fetchall()

    publicacao.execute('SELECT c.id, cc.nome, c.titulo, c.descricao FROM publicacao c inner join categoria_publicacao cc on c.categoria_id = cc.id  WHERE c.id = %s', (id))
    data = publicacao.fetchall()
    publicacao.close()
    print(data[0])
    return render_template('publicacoes/edit.html', publicacao = data[0], list_publicacao = list_publicacao, form=form)

@app.route("/update_publicacao/<id>", methods=['POST'])
def update_publicacao(id):
    form = UploadForm()

    publicacao = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        categoria = request.form['categoria']
       
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data = request.form['data']
        filename = form.file.data.filename
        form.file.data.save(f'static/images/blog/{filename}')

        publicacao.execute("UPDATE publicacao set categoria_id = %s, titulo = %s, descricao = %s ,imagem = %s, data = %s where id = %s", (categoria, titulo,descricao, filename, data, id))
        conn.commit()
        flash('Publicação atualizado com sucesso')
        return redirect(url_for('publicacoes'))


@app.route('/publicacao/delete/<string:id>', methods = ['POST','GET'])
def delete_publicacao(id):
    publicacao = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    publicacao.execute('DELETE FROM publicacao WHERE id = {0}'.format(id))
    conn.commit()
    flash('publicacao Removido com sucesso')
    return redirect(url_for('publicacoes'))



@app.route("/conexao")
def conexao():
    print(conn)
    return "conexao bem sucedida"


if __name__ == "__main__":
    app.run(debug=True)


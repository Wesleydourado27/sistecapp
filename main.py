from flask import Flask, render_template, request, redirect, url_for, jsonify
# -------------------------------------
# Definir o Modelo (Model) para o Banco de Dados:
from flask_sqlalchemy import SQLAlchemy
# -------------------------------------
# -------------------------------------
app = Flask(__name__)

# Definir o Modelo (Model) para o Banco de Dados:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Obra.db'
db = SQLAlchemy(app)

class Obra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    tipo_literatura = db.Column(db.String(100))
    editora = db.Column(db.String(100))
    ano = db.Column(db.Integer)
    isbn = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(255), nullable=False)
# -------------------------------------
# -------------------------------------
# Rota para mostrar todos os registros
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
@app.route('/mostrar_obras', methods=['GET', 'POST'])
def mostrar_obras():
    # Verifica se há um pedido de ordenação
    ordenar_por = request.form.get('ordenar')

    if ordenar_por == 'titulo':
        obras = Obra.query.order_by(Obra.titulo).all()
    elif ordenar_por == 'autor':
        obras = Obra.query.order_by(Obra.autor).all()
    else:
        obras = Obra.query.all()

    return render_template('mostrar_obras.html', obras=obras)
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# Rota para a página inicial
@app.route("/")
def homepage():
    return render_template("homepage.html")
# -------------------------------------
# Dados do usuário (username: password)
usuarios_cadastrados = {
    'w': 'w',
}
# -------------------------------------
# Fazer login para site de cadastros
@app.route('/login')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']

        if usuario in usuarios_cadastrados and usuarios_cadastrados[usuario] == senha:
            # Credenciais corretas, redirecionar para a página desejada
            return redirect(url_for('cadastrar_obra'))
        else:
            # Credenciais inválidas, exibir mensagem de erro
            return render_template('login.html', error='Usuário ou senha inválida')
# -------------------------------------
# Rota para a site de Cadastros
@app.route("/site_de_cadastro")
def site_de_cadastro():
    return render_template("site_de_cadastro.html")
# -------------------------------------
# Rota para a página de BUSCA DE LIVROS
@app.route("/busca_livros")
def busca_livros():
    return render_template("busca_livros.html")
# -------------------------------------
# Rota para a página de BUSCA DE LIVROS
@app.route("/desenvolvedores")
def desenvolvedores():
    return render_template("desenvolvedores.html")
# -----------------------------------------------------------
# Criar as Rotas para Cadastro e Pesquisa:
# ...
# -----------------------------------------------------------
@app.route('/cadastrar_obra', methods=['GET', 'POST'])
def cadastrar_obra():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        tipo_literatura = request.form['tipo_literatura']
        editora = request.form['editora']
        ano = request.form['ano']
        codigo = request.form['codigo']
        isbn = request.form['isbn']

        nova_obra = Obra(
            titulo=titulo,
            autor=autor,
            tipo_literatura=tipo_literatura,
            editora=editora,
            ano=ano,
            codigo=codigo,
            isbn=isbn
        )

        db.session.add(nova_obra)
        db.session.commit()

    return render_template('cadastrar_obra.html')

# ...

# -----------------------------------------------------------

# -----------------------------------------------------------
# pesquisar obras
@app.route('/pesquisar_obras', methods=['GET', 'POST'])
def pesquisar_obras():
    if request.method == 'POST':
        titulo_pesquisa = request.form['titulo_pesquisa']
        autor_pesquisa = request.form['autor_pesquisa']

        obras = Obra.query.filter(Obra.autor.ilike(f'%{autor_pesquisa}%'), Obra.titulo.ilike(f'%{titulo_pesquisa}%')).all()
        return render_template('resultado_pesquisa.html', obras=obras)

    return render_template('pesquisar_obras.html')


# -------------------------------------
# -------------------------------------
# Rota para buscar e excluir obras
# ...
@app.route('/excluir_obra', methods=['GET', 'POST'])
def excluir_obra():
    if request.method == 'POST':
        # Verifique se os dados do formulário estão presentes antes de acessá-los
        autor_pesquisa = request.form.get('autor_pesquisa', '')
        titulo_pesquisa = request.form.get('titulo_pesquisa', '')

        # Realize a busca no banco de dados
        obras = Obra.query.filter(Obra.autor.ilike(f'%{autor_pesquisa}%'), Obra.titulo.ilike(f'%{titulo_pesquisa}%')).all()

        return render_template('excluir_obra.html', obras=obras)

    return render_template('excluir_obra.html')


# -----------------------------------------------------------
@app.route('/excluir_obras/<int:obra_id>', methods=['POST'])
def excluir_obras(obra_id):
    obra_a_excluir = Obra.query.get_or_404(obra_id)
    db.session.delete(obra_a_excluir)
    db.session.commit()

    return redirect(url_for('excluir_obra'))


# -------------------------------------
# -------------------------------------
# Colocar no ar
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
from database import conectar

app = Flask(__name__)

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")

# ==========================================
# CADASTRAR ALUNO
# ==========================================

@app.route("/cadastro", methods=["GET", "POST"])

def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        nascimento = request.form["nascimento"]
        naturalidade = request.form["naturalidade"]
        sexo = request.form["sexo"]
        rg = request.form["rg"]
        cpf = request.form["cpf"]

        rua = request.form["rua"]
        numero = request.form["numero"]
        bairro = request.form["bairro"]
        cidade = request.form["cidade"]
        cep = request.form["cep"]

        responsavel = request.form["responsavel"]
        telefone1 = request.form["telefone1"]
        telefone2 = request.form["telefone2"]
        parentesco = request.form["parentesco"]

        alergias = request.form["alergias"]
        tipo_sanguineo = request.form["tipo_sanguineo"]
        observacoes = request.form["observacoes"]

        matricula = request.form["matricula"]
        turma = request.form["turma"]
        serie = request.form["serie"]
        ano_letivo = request.form["ano_letivo"]

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO alunos (

            nome_completo,
            data_nascimento,
            naturalidade,
            sexo,
            rg,
            cpf,

            rua,
            numero,
            bairro,
            cidade,
            cep,

            responsavel,
            telefone1,
            telefone2,
            parentesco,

            alergias,
            tipo_sanguineo,
            observacoes_importantes,

            numero_matricula,
            turma,
            serie,
            ano_letivo

        )

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        """

        valores = (

            nome,
            nascimento,
            naturalidade,
            sexo,
            rg,
            cpf,

            rua,
            numero,
            bairro,
            cidade,
            cep,

            responsavel,
            telefone1,
            telefone2,
            parentesco,

            alergias,
            tipo_sanguineo,
            observacoes,

            matricula,
            turma,
            serie,
            ano_letivo

        )

        cursor.execute(sql, valores)

        conexao.commit()
        conexao.close()

        return redirect("/alunos")

    return render_template("cadastro.html")

# ==========================================
# LISTAR ALUNOS
# ==========================================

@app.route("/alunos")

def alunos():

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM alunos")

    lista_alunos = cursor.fetchall()

    conexao.close()

    return render_template(
        "alunos.html",
        alunos=lista_alunos
    )

# ==========================================
# PESQUISA
# ==========================================

@app.route("/pesquisa")

def pesquisa():

    nome = request.args.get("nome")

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
    SELECT * FROM alunos
    WHERE nome_completo LIKE %s
    """

    valor = (f"%{nome}%",)

    cursor.execute(sql, valor)

    resultado = cursor.fetchall()

    conexao.close()

    return render_template(
        "alunos.html",
        alunos=resultado
    )

# ==========================================
# DELETAR ALUNO
# ==========================================

@app.route("/deletar/<int:id>")

def deletar(id):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM alunos WHERE id = %s"

    cursor.execute(sql, (id,))

    conexao.commit()
    conexao.close()

    return redirect("/alunos")

# ==========================================
# VISUALIZAR DETALHES DO ALUNO
# ==========================================

@app.route("/visualizar/<int:id>")

def visualizar(id):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = "SELECT * FROM alunos WHERE id = %s"

    cursor.execute(sql, (id,))

    aluno = cursor.fetchone()

    conexao.close()

    return render_template(
        "visualizar.html",
        aluno=aluno
    )

# ==========================================
# EDITAR ALUNO
# ==========================================

@app.route("/editar/<int:id>", methods=["GET", "POST"])

def editar(id):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    if request.method == "POST":

        nome = request.form["nome"]
        nascimento = request.form["nascimento"]
        naturalidade = request.form["naturalidade"]
        sexo = request.form["sexo"]
        rg = request.form["rg"]
        cpf = request.form["cpf"]

        rua = request.form["rua"]
        numero = request.form["numero"]
        bairro = request.form["bairro"]
        cidade = request.form["cidade"]
        cep = request.form["cep"]

        responsavel = request.form["responsavel"]
        telefone1 = request.form["telefone1"]
        telefone2 = request.form["telefone2"]
        parentesco = request.form["parentesco"]

        alergias = request.form["alergias"]
        tipo_sanguineo = request.form["tipo_sanguineo"]
        observacoes = request.form["observacoes"]

        matricula = request.form["matricula"]
        turma = request.form["turma"]
        serie = request.form["serie"]
        ano_letivo = request.form["ano_letivo"]

        sql = """

        UPDATE alunos SET

        nome_completo = %s,
        data_nascimento = %s,
        naturalidade = %s,
        sexo = %s,
        rg = %s,
        cpf = %s,

        rua = %s,
        numero = %s,
        bairro = %s,
        cidade = %s,
        cep = %s,

        responsavel = %s,
        telefone1 = %s,
        telefone2 = %s,
        parentesco = %s,

        alergias = %s,
        tipo_sanguineo = %s,
        observacoes_importantes = %s,

        numero_matricula = %s,
        turma = %s,
        serie = %s,
        ano_letivo = %s

        WHERE id = %s

        """

        valores = (
            nome,
            nascimento,
            naturalidade,
            sexo,
            rg,
            cpf,

            rua,
            numero,
            bairro,
            cidade,
            cep,

            responsavel,
            telefone1,
            telefone2,
            parentesco,

            alergias,
            tipo_sanguineo,
            observacoes,

            matricula,
            turma,
            serie,
            ano_letivo,
            id
        )

        cursor.execute(sql, valores)

        conexao.commit()
        conexao.close()

        return redirect("/alunos")

    sql = "SELECT * FROM alunos WHERE id = %s"

    cursor.execute(sql, (id,))

    aluno = cursor.fetchone()

    conexao.close()

    return render_template(
        "editar.html",
        aluno=aluno
    )

# ==========================================

app.run(debug=True)
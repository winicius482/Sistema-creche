from flask import Flask, render_template, request, redirect
from database import conectar

app = Flask(__name__)


def obter_aluno_com_responsavel(aluno_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
    SELECT
        a.*,
        r.id AS responsavel_id,
        r.nome_responsavel,
        r.parentesco,
        r.telefone_1,
        r.telefone_2,
        r.endereco_completo,
        r.rg AS responsavel_rg,
        r.cpf AS responsavel_cpf
    FROM alunos a
    LEFT JOIN aluno_responsavel ar ON a.id = ar.id_aluno
    LEFT JOIN responsaveis r ON ar.id_responsavel = r.id
    WHERE a.id = %s
    """
    cursor.execute(sql, (aluno_id,))
    aluno = cursor.fetchone()
    conexao.close()
    return aluno

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
        try:
            # Capturar todos os dados do formulário
            nome = request.form.get("nome", "").strip()
            nascimento = request.form.get("nascimento", "").strip()
            naturalidade = request.form.get("naturalidade", "").strip()
            sexo = request.form.get("sexo", "").strip()
            rg = request.form.get("rg", "").strip()
            cpf = request.form.get("cpf", "").strip()
            certidao_nascimento = request.form.get("certidao_nascimento", "").strip()
            rua = request.form.get("rua", "").strip()
            numero = request.form.get("numero", "").strip()
            bairro = request.form.get("bairro", "").strip()
            cidade = request.form.get("cidade", "").strip()
            cep = request.form.get("cep", "").strip()
            tipo_sanguineo = request.form.get("tipo_sanguineo", "").strip()
            alergias = request.form.get("alergias", "").strip()
            doencas_cronicas = request.form.get("doencas_cronicas", "").strip()
            observacoes = request.form.get("observacoes", "").strip()
            numero_matricula = request.form.get("matricula", "").strip()
            turma = request.form.get("turma", "").strip()
            serie = request.form.get("serie", "").strip()
            ano_letivo = request.form.get("ano_letivo", "").strip()
            relatorio_descritivo = request.form.get("relatorio_descritivo", "").strip()
            necessidades_especiais = request.form.get("necessidades_especiais", "").strip()
            comportamento = request.form.get("comportamento", "").strip()
            foto = request.form.get("foto", "").strip()
            
            nome_responsavel = request.form.get("nome_responsavel", "").strip()
            telefone_1 = request.form.get("telefone_1", "").strip()
            telefone_2 = request.form.get("telefone_2", "").strip()
            parentesco = request.form.get("parentesco", "").strip()
            endereco_completo = request.form.get("endereco_completo", "").strip()
            responsavel_rg = request.form.get("responsavel_rg", "").strip()
            responsavel_cpf = request.form.get("responsavel_cpf", "").strip()

            conexao = conectar()
            cursor = conexao.cursor()

            # INSERT na tabela alunos com 24 colunas = 24 %s (CORRIGIDO: adicionado %s faltante)
            sql = """
            INSERT INTO alunos (
                nome_completo,
                foto,
                data_nascimento,
                naturalidade,
                sexo,
                rg,
                cpf,
                certidao_nascimento,
                rua,
                numero,
                bairro,
                cidade,
                cep,
                tipo_sanguineo,
                alergias,
                doencas_cronicas,
                observacoes_importantes,
                numero_matricula,
                turma,
                serie,
                ano_letivo,
                relatorio_descritivo,
                necessidades_especiais,
                comportamento
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            valores = (
                nome,
                foto,
                nascimento,
                naturalidade,
                sexo,
                rg,
                cpf,
                certidao_nascimento,
                rua,
                numero,
                bairro,
                cidade,
                cep,
                tipo_sanguineo,
                alergias,
                doencas_cronicas,
                observacoes,
                numero_matricula,
                turma,
                serie,
                ano_letivo,
                relatorio_descritivo,
                necessidades_especiais,
                comportamento
            )

            cursor.execute(sql, valores)
            aluno_id = cursor.lastrowid

            # Cadastrar responsável se houver dados
            if nome_responsavel or telefone_1 or telefone_2 or parentesco or endereco_completo or responsavel_rg or responsavel_cpf:
                sql_resp = """
                INSERT INTO responsaveis (
                    nome_responsavel,
                    parentesco,
                    telefone_1,
                    telefone_2,
                    endereco_completo,
                    rg,
                    cpf
                ) VALUES (%s,%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(sql_resp, (
                    nome_responsavel,
                    parentesco,
                    telefone_1,
                    telefone_2,
                    endereco_completo,
                    responsavel_rg,
                    responsavel_cpf
                ))
                responsavel_id = cursor.lastrowid
                
                # Criar vínculo na tabela aluno_responsavel
                cursor.execute(
                    "INSERT INTO aluno_responsavel (id_aluno, id_responsavel) VALUES (%s, %s)",
                    (aluno_id, responsavel_id)
                )

            conexao.commit()
            conexao.close()

            return redirect("/alunos")

        except Exception as e:
            print(f"Erro ao cadastrar aluno: {e}")
            try:
                conexao.close()
            except:
                pass
            return redirect("/cadastro")

    return render_template("cadastro.html")

# ==========================================
# LISTAR ALUNOS
# ==========================================

@app.route("/alunos")
def alunos():
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM alunos")
        lista_alunos = cursor.fetchall()
        conexao.close()

        return render_template("alunos.html", alunos=lista_alunos)

    except Exception as e:
        print(f"Erro ao listar alunos: {e}")
        return render_template("alunos.html", alunos=[])

# ==========================================
# PESQUISA
# ==========================================

@app.route("/pesquisa")
def pesquisa():
    try:
        nome = request.args.get("nome", "").strip()

        if not nome:
            return redirect("/alunos")

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM alunos WHERE nome_completo LIKE %s"
        cursor.execute(sql, (f"%{nome}%",))
        resultado = cursor.fetchall()
        conexao.close()

        return render_template("alunos.html", alunos=resultado)

    except Exception as e:
        print(f"Erro na pesquisa: {e}")
        return redirect("/alunos")

# ==========================================
# DELETAR ALUNO
# ==========================================

@app.route("/deletar/<int:id>")
def deletar(id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Buscar responsáveis vinculados
        cursor.execute(
            "SELECT id_responsavel FROM aluno_responsavel WHERE id_aluno = %s",
            (id,)
        )
        responsaveis_ids = [row[0] for row in cursor.fetchall()]

        # Deletar vínculos na tabela aluno_responsavel
        cursor.execute(
            "DELETE FROM aluno_responsavel WHERE id_aluno = %s",
            (id,)
        )

        # Deletar responsáveis que não possuem mais vínculos
        for responsavel_id in responsaveis_ids:
            cursor.execute(
                "SELECT COUNT(*) FROM aluno_responsavel WHERE id_responsavel = %s",
                (responsavel_id,)
            )
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.execute(
                    "DELETE FROM responsaveis WHERE id = %s",
                    (responsavel_id,)
                )

        # Deletar aluno
        cursor.execute("DELETE FROM alunos WHERE id = %s", (id,))

        conexao.commit()
        conexao.close()

        return redirect("/alunos")

    except Exception as e:
        print(f"Erro ao deletar aluno: {e}")
        return redirect("/alunos")

# ==========================================
# VISUALIZAR DETALHES DO ALUNO
# ==========================================

@app.route("/visualizar/<int:id>")
def visualizar(id):
    try:
        aluno = obter_aluno_com_responsavel(id)

        if aluno is None:
            return redirect("/alunos")

        return render_template("visualizar.html", aluno=aluno)

    except Exception as e:
        print(f"Erro ao visualizar aluno: {e}")
        return redirect("/alunos")

# ==========================================
# EDITAR ALUNO
# ==========================================

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    try:
        aluno = obter_aluno_com_responsavel(id)

        if aluno is None:
            return redirect("/alunos")

        if request.method == "POST":
            # Capturar todos os dados do formulário
            nome = request.form.get("nome", "").strip()
            nascimento = request.form.get("nascimento", "").strip()
            naturalidade = request.form.get("naturalidade", "").strip()
            sexo = request.form.get("sexo", "").strip()
            rg = request.form.get("rg", "").strip()
            cpf = request.form.get("cpf", "").strip()
            certidao_nascimento = request.form.get("certidao_nascimento", "").strip()
            rua = request.form.get("rua", "").strip()
            numero = request.form.get("numero", "").strip()
            bairro = request.form.get("bairro", "").strip()
            cidade = request.form.get("cidade", "").strip()
            cep = request.form.get("cep", "").strip()
            tipo_sanguineo = request.form.get("tipo_sanguineo", "").strip()
            alergias = request.form.get("alergias", "").strip()
            doencas_cronicas = request.form.get("doencas_cronicas", "").strip()
            observacoes = request.form.get("observacoes", "").strip()
            numero_matricula = request.form.get("matricula", "").strip()
            turma = request.form.get("turma", "").strip()
            serie = request.form.get("serie", "").strip()
            ano_letivo = request.form.get("ano_letivo", "").strip()
            relatorio_descritivo = request.form.get("relatorio_descritivo", "").strip()
            necessidades_especiais = request.form.get("necessidades_especiais", "").strip()
            comportamento = request.form.get("comportamento", "").strip()
            foto = request.form.get("foto", "").strip()
            
            nome_responsavel = request.form.get("nome_responsavel", "").strip()
            telefone_1 = request.form.get("telefone_1", "").strip()
            telefone_2 = request.form.get("telefone_2", "").strip()
            parentesco = request.form.get("parentesco", "").strip()
            endereco_completo = request.form.get("endereco_completo", "").strip()
            responsavel_rg = request.form.get("responsavel_rg", "").strip()
            responsavel_cpf = request.form.get("responsavel_cpf", "").strip()
            responsavel_id = request.form.get("responsavel_id")

            conexao = conectar()
            cursor = conexao.cursor()

            # UPDATE na tabela alunos com 24 colunas = 24 %s + 1 para WHERE id
            sql = """
            UPDATE alunos SET
                nome_completo = %s,
                foto = %s,
                data_nascimento = %s,
                naturalidade = %s,
                sexo = %s,
                rg = %s,
                cpf = %s,
                certidao_nascimento = %s,
                rua = %s,
                numero = %s,
                bairro = %s,
                cidade = %s,
                cep = %s,
                tipo_sanguineo = %s,
                alergias = %s,
                doencas_cronicas = %s,
                observacoes_importantes = %s,
                numero_matricula = %s,
                turma = %s,
                serie = %s,
                ano_letivo = %s,
                relatorio_descritivo = %s,
                necessidades_especiais = %s,
                comportamento = %s
            WHERE id = %s
            """

            valores = (
                nome,
                foto,
                nascimento,
                naturalidade,
                sexo,
                rg,
                cpf,
                certidao_nascimento,
                rua,
                numero,
                bairro,
                cidade,
                cep,
                tipo_sanguineo,
                alergias,
                doencas_cronicas,
                observacoes,
                numero_matricula,
                turma,
                serie,
                ano_letivo,
                relatorio_descritivo,
                necessidades_especiais,
                comportamento,
                id
            )

            cursor.execute(sql, valores)

            # Atualizar responsável se existir
            if responsavel_id and responsavel_id != "None" and responsavel_id != "":
                sql_resp = """
                UPDATE responsaveis SET
                    nome_responsavel = %s,
                    parentesco = %s,
                    telefone_1 = %s,
                    telefone_2 = %s,
                    endereco_completo = %s,
                    rg = %s,
                    cpf = %s
                WHERE id = %s
                """
                cursor.execute(sql_resp, (
                    nome_responsavel,
                    parentesco,
                    telefone_1,
                    telefone_2,
                    endereco_completo,
                    responsavel_rg,
                    responsavel_cpf,
                    responsavel_id
                ))
            elif nome_responsavel or telefone_1 or telefone_2 or parentesco or endereco_completo or responsavel_rg or responsavel_cpf:
                # Inserir novo responsável se não existe
                sql_resp = """
                INSERT INTO responsaveis (
                    nome_responsavel,
                    parentesco,
                    telefone_1,
                    telefone_2,
                    endereco_completo,
                    rg,
                    cpf
                ) VALUES (%s,%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(sql_resp, (
                    nome_responsavel,
                    parentesco,
                    telefone_1,
                    telefone_2,
                    endereco_completo,
                    responsavel_rg,
                    responsavel_cpf
                ))
                novo_responsavel_id = cursor.lastrowid
                
                # Verificar se já existe vínculo
                cursor.execute(
                    "SELECT COUNT(*) FROM aluno_responsavel WHERE id_aluno = %s",
                    (id,)
                )
                if cursor.fetchone()[0] == 0:
                    cursor.execute(
                        "INSERT INTO aluno_responsavel (id_aluno, id_responsavel) VALUES (%s, %s)",
                        (id, novo_responsavel_id)
                    )
                else:
                    # Atualizar vínculo existente
                    cursor.execute(
                        "UPDATE aluno_responsavel SET id_responsavel = %s WHERE id_aluno = %s",
                        (novo_responsavel_id, id)
                    )

            conexao.commit()
            conexao.close()

            return redirect("/alunos")

        return render_template("editar.html", aluno=aluno)

    except Exception as e:
        print(f"Erro ao editar aluno: {e}")
        return redirect("/alunos")

# ==========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
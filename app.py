import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from funcoes import *

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database", "projeto_viagens.db")

def get_db():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

@app.route('/')
def index():
    conexao = get_db()
    cursor = conexao.cursor()

    viagens_futuras = proxima_viagem(cursor)
    motoristas_cadastrados = listar_motoristas(cursor)
    veiculos_cadastrados = listar_veiculos(cursor)
    hospitais_cadastrados = listar_hospitais(cursor)

    conexao.close()

    return render_template('index.html', 
                           viagens=viagens_futuras, 
                           motoristas=motoristas_cadastrados, 
                           veiculos=veiculos_cadastrados,
                           hospitais=hospitais_cadastrados)

@app.route('/limpar-historico', methods=['POST'])
def rota_limpar_historico():
    conexao = get_db()
    cursor = conexao.cursor()
    
    cursor.execute("DELETE FROM viagens WHERE (data || ' ' || hora_saida) < datetime('now', 'localtime')")
    
    conexao.commit()
    conexao.close()
    return redirect(url_for('historico'))

@app.route('/historico')
def historico():
    conexao = get_db()
    cursor = conexao.cursor()

    viagens_concluidas = historico_viagens(cursor)

    conexao.close()

    return render_template('historico_viagens.html', viagens=viagens_concluidas)

@app.route('/cadastrar-viagem', methods=['GET', 'POST'])
def cadastrar_viagem():
    conexao = get_db()
    cursor = conexao.cursor()
    mensagem = None

    if request.method == 'POST':
        data = request.form.get('data')
        hora_saida = request.form.get('hora_saida')
        ponto = request.form.get('ponto')
        hospital_id = request.form.get('hospital')
        destino = request.form.get('destino')
        observacao = request.form.get('observacao')
        motorista_id = request.form.get('motorista')
        veiculo_id = request.form.get('veiculo')

        try:
            cursor.execute("""
                INSERT INTO viagens (data, hora_saida, ponto, hospital_id, destino, observacao, motorista_id, veiculo_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (data, hora_saida, ponto, hospital_id, destino, observacao, motorista_id, veiculo_id))
            
            conexao.commit()
            mensagem = "Viagem agendada com sucesso!"
        except Exception as e:
            conexao.rollback()
            mensagem = f"Erro ao agendar viagem: {e}"

    cursor.execute("SELECT id, nome, cidade FROM hospitais WHERE ativo = 1 ORDER BY nome")
    hospitais = cursor.fetchall()

    cursor.execute("SELECT id, nome FROM motoristas WHERE ativo = 1 ORDER BY nome")
    motoristas = cursor.fetchall()

    cursor.execute("SELECT id, tipo, placa FROM veiculos WHERE ativo = 1 ORDER BY tipo, placa")
    veiculos = cursor.fetchall()

    conexao.close()

    return render_template('cadastrar_viagem.html', 
                           mensagem=mensagem, 
                           hospitais=hospitais, 
                           motoristas=motoristas, 
                           veiculos=veiculos)

@app.route('/cadastrar-motorista', methods=['GET', 'POST'])
def rota_cadastrar_motorista():
    mensagem = None

    if request.method == 'POST':
        nome = request.form['nome']
        cnh = request.form['cnh']
        categoria = request.form['categoria']
        telefone = request.form['telefone']

        conexao = get_db()
        cursor = conexao.cursor()

        mensagem = cadastro_motorista(conexao, cursor, nome, cnh, categoria, telefone)

        conexao.close()

    return render_template('cadastrar_motorista.html', mensagem=mensagem)

@app.route('/cadastrar-veiculo', methods=['GET', 'POST'])
def rota_cadastrar_veiculo():
    mensagem = None

    if request.method == 'POST':
        tipo = request.form['tipo']
        ano = request.form['ano']
        placa = request.form['placa']
        capacidade = request.form['capacidade']

        conexao = get_db()
        cursor = conexao.cursor()

        mensagem = cadastro_veiculo(conexao, cursor, tipo, ano, placa, capacidade)

        conexao.close()

    return render_template('cadastrar_veiculo.html', mensagem=mensagem)

@app.route('/cadastrar-hospital', methods=['GET', 'POST'])
def rota_cadastrar_hospital():
    mensagem = None

    if request.method == 'POST':
        codigo = request.form['codigo']
        nome = request.form['nome']
        cidade = request.form['cidade']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        tipo = request.form['tipo']

        conexao = get_db()
        cursor = conexao.cursor()

        mensagem = cadastro_hospital(conexao, cursor, codigo, nome, cidade, telefone, endereco, tipo)

        conexao.close()

    return render_template('cadastrar_hospital.html', mensagem=mensagem)

@app.route('/imprimir-viagens')
def imprimir_viagens():
    conn = get_db()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            v.id, v.data, v.hora_saida, v.ponto, v.destino, v.observacao,
            m.nome AS nome, ve.placa AS placa,
            h.nome AS hospital, 
            h.endereco AS hospital_endereco, 
            h.cidade AS hospital_cidade
        FROM viagens v
        LEFT JOIN motoristas m ON v.motorista_id = m.id
        LEFT JOIN veiculos ve ON v.veiculo_id = ve.id
        LEFT JOIN hospitais h ON v.hospital_id = h.id
        WHERE (v.data || ' ' || v.hora_saida) >= datetime('now', 'localtime')
        ORDER BY v.data ASC, v.hora_saida ASC
    """
    cursor.execute(query)
    viagens = cursor.fetchall()
    conn.close()
    
    hoje = datetime.now().strftime('%d/%m/%Y')
    return render_template('imprimir_viagens.html', viagens=viagens, hoje=hoje)

@app.route('/deletar-viagem/<int:id>')
def rota_deletar_viagem(id):
    conexao = get_db()
    cursor = conexao.cursor()
    deletar_viagem(conexao, cursor, id)
    conexao.commit()
    conexao.close()
    return redirect(url_for('index'))

@app.route('/deletar-motorista/<int:id>')
def rota_deletar_motorista(id):
    conexao = get_db()
    cursor = conexao.cursor()
    deletar_motorista(conexao, cursor, id)
    conexao.commit()
    conexao.close()
    return redirect(url_for('index'))

@app.route('/deletar-veiculo/<int:id>')
def rota_deletar_veiculo(id):
    conexao = get_db()
    cursor = conexao.cursor()
    deletar_veiculo(conexao, cursor, id)
    conexao.commit()
    conexao.close()
    return redirect(url_for('index'))

@app.route('/deletar-hospital/<int:id>')
def rota_deletar_hospital(id):
    conexao = get_db()
    cursor = conexao.cursor()
    deletar_hospital(conexao, cursor, id)
    conexao.commit()
    conexao.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
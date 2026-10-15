import sqlite3
from datetime import datetime

def listar_motoristas(cursor):
    cursor.execute("SELECT * FROM motoristas WHERE ativo = 1 ORDER BY nome")
    return cursor.fetchall()

def listar_veiculos(cursor):
    cursor.execute("SELECT * FROM veiculos WHERE ativo = 1 ORDER BY tipo, placa")
    return cursor.fetchall()

def proxima_viagem(cursor):
    query = """
        SELECT 
            v.id,
            v.data,
            v.hora_saida,
            v.ponto,
            v.destino,
            v.observacao,
            m.nome AS motorista,
            m.nome AS nome,
            ve.placa AS placa,
            CASE 
                WHEN ve.tipo IS NOT NULL AND ve.placa IS NOT NULL THEN ve.tipo || ' (' || ve.placa || ')'
                ELSE ve.placa 
            END AS veiculo,
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
    return cursor.fetchall()

def historico_viagens(cursor):
    query = """
        SELECT 
            v.id,
            v.data,
            v.hora_saida,
            v.ponto,
            v.destino,
            v.observacao,
            m.nome AS motorista,
            m.nome AS nome,
            CASE 
                WHEN ve.tipo IS NOT NULL AND ve.placa IS NOT NULL THEN ve.tipo || ' (' || ve.placa || ')'
                ELSE ve.placa 
            END AS veiculo,
            ve.placa AS placa,
            h.nome AS hospital,
            h.endereco AS hospital_endereco,
            h.cidade AS hospital_cidade
        FROM viagens v
        LEFT JOIN motoristas m ON v.motorista_id = m.id
        LEFT JOIN veiculos ve ON v.veiculo_id = ve.id
        LEFT JOIN hospitais h ON v.hospital_id = h.id
        WHERE (v.data || ' ' || v.hora_saida) < datetime('now', 'localtime')
        ORDER BY v.data DESC, v.hora_saida DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

def cadastrar_viagem(conexao, cursor, data, hora_saida, ponto, destino, motorista, veiculo, hospital, observacao=None):
    motorista_id = int(motorista) if str(motorista).isdigit() else None
    veiculo_id = int(veiculo) if str(veiculo).isdigit() else None
    hospital_id = int(hospital) if str(hospital).isdigit() else None

    cursor.execute("""
        INSERT INTO viagens (data, hora_saida, ponto, destino, motorista_id, veiculo_id, hospital_id, observacao) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (data, hora_saida, ponto, destino, motorista_id, veiculo_id, hospital_id, observacao))

    conexao.commit()
    return "Viagem cadastrada com sucesso!"

def cadastro_motorista(conexao, cursor, nome, cnh, categoria_cnh, telefone):
    try:
        query = """
            INSERT INTO motoristas (nome, cnh, categoria_cnh, telefone, ativo)
            VALUES (?, ?, ?, ?, 1)
        """
        cursor.execute(query, (nome, str(cnh), str(categoria_cnh), str(telefone)))
        conexao.commit()
        return "Motorista cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        conexao.rollback()
        return "Erro ao cadastrar: Já existe um motorista cadastrado com este número de CNH."
    except Exception as e:
        conexao.rollback()
        return f"Erro ao cadastrar motorista: {e}"

def cadastro_veiculo(conexao, cursor, tipo, ano, placa, capacidade_passageiros):
    if not str(ano).isdigit():
        return "Erro: No campo 'Ano' só pode números!"

    if not str(capacidade_passageiros).isdigit():
        return "Erro: A capacidade só pode conter números!"

    placa = placa.strip().upper().replace("-", "")
    if len(placa) != 7:
        return "Erro: A placa precisa ter exatamente 7 caracteres!"

    cursor.execute("""SELECT id FROM veiculos WHERE placa = ?""", (placa,))

    if cursor.fetchone():
        return "Erro: Essa placa já está cadastrada!"

    cursor.execute("""INSERT INTO veiculos (tipo, ano, placa, capacidade_passageiros, ativo) VALUES (?, ?, ?, ?, 1) """, 
                   (tipo, int(ano), placa, int(capacidade_passageiros)))
    conexao.commit()
    return "Veículo cadastrado com sucesso!"

def cadastro_hospital(conexao, cursor, codigo, nome, cidade, telefone, endereco, tipo):
    tel_limpo = str(telefone).replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+", "")
    
    if not tel_limpo.isdigit():
        return "Erro: O campo 'Telefone' deve conter apenas números!"

    try:
        query = """
            INSERT INTO hospitais (codigo, nome, cidade, telefone, endereco, tipo, ativo)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """
        cursor.execute(query, (codigo, nome, cidade, telefone, endereco, tipo))
        conexao.commit()
        return "Hospital cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        conexao.rollback()
        return "Erro ao cadastrar: Já existe um hospital/clínica com este código ou nome cadastrado."
    except Exception as e:
        conexao.rollback()
        return f"Erro ao cadastrar hospital: {e}"

def deletar_viagem(conexao, cursor, id_viagem):
    try:
        cursor.execute("DELETE FROM viagens WHERE id = ?", (id_viagem,))
        conexao.commit()
        return "Viagem removida com sucesso!"
    except Exception as e:
        conexao.rollback()
        return f"Erro ao remover viagem: {e}"

def deletar_motorista(conexao, cursor, id_motorista):
    try:
        cursor.execute("UPDATE motoristas SET ativo = 0 WHERE id = ?", (id_motorista,))
        conexao.commit()
        return "Motorista arquivado com sucesso!"
    except Exception as e:
        conexao.rollback()
        return f"Erro ao arquivar motorista: {e}"

def deletar_veiculo(conexao, cursor, id_veiculo):
    try:
        cursor.execute("UPDATE veiculos SET ativo = 0 WHERE id = ?", (id_veiculo,))
        conexao.commit()
        return "Veículo arquivado com sucesso!"
    except Exception as e:
        conexao.rollback()
        return f"Erro ao arquivar veículo: {e}"

def listar_hospitais(cursor):
    cursor.execute("SELECT * FROM hospitais WHERE ativo = 1 ORDER BY nome")
    return cursor.fetchall()

def deletar_hospital(conexao, cursor, id_hospital):
    try:
        cursor.execute("UPDATE hospitais SET ativo = 0 WHERE id = ?", (id_hospital,))
        conexao.commit()
        return "Hospital arquivado com sucesso!"
    except Exception as e:
        conexao.rollback()
        return f"Erro ao arquivar hospital: {e}"
import mysql.connector
import json

def bd_config():

    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='32481024',
        database='csj'
    )
    return mydb


def inserir_funcionario(cpf,nome,tell,senha):
    mydb = bd_config()
    cursor = mydb.cursor()
    
   # Verificar se o CPF já existe
    cursor.execute("SELECT * FROM funcionario WHERE cpf = %s", (cpf,))
    #cursor.fetchall é uma fução que vai retornar todas as tuplas do sql
    resultado = cursor.fetchall()
    
    if resultado:
        cursor.close()
        mydb.close()
        return('CPF JÁ EXISTE')
    # a variável sql com query em string evita o ataque ao banco de dados
    sql = "INSERT INTO funcionario (cpf, nome, tell, senha) VALUES (%s, %s, %s, %s)"
    val = (cpf, nome, tell, senha)
    # cursor.execute vai executar o 1 arg como query sql e o segundo os argumentos de consulta
    cursor.execute(sql, val)
    mydb.commit() # o commit serve para atualizar o banco de dados
    cursor.close() # cursor.close() vai encerrar a manipulação do bd com o py
    mydb.close() # mydb.close() vai encerrar a conexão com o banco de dados
    
    return 'FUNCIONARIO INSERIDO COM SUCESSO!'


def delete_funcionario(cpf):
    mydb = bd_config()
    cursor = mydb.cursor()
    # cursor.execute é uma função que podemos colocar a query e parâmetro
    cursor.execute("SELECT * FROM funcionario WHERE cpf = %s",(cpf,))
    resultado = cursor.fetchall()
    
    if resultado: #se o resultado existir
        cursor.execute("DELETE FROM funcionario WHERE cpf=%s", (cpf,))
        mydb.commit()
        cursor.close()
        mydb.close()
        return 'DELETADO COM SUCESSO'
    else:
       return ' CPF NÃO EXISTE'



def avaliador_login(cpf):
    mydb = bd_config()  # Configura a conexão com o banco de dados
    cursor = mydb.cursor(dictionary=True)  # Retorna resultados como dicionários
    resultado = None  # Inicializa resultado como None para o caso de nenhum usuário ser encontrado
    
    try:
        # Utilizando parâmetro cpf na consulta SQL
        sql = "SELECT cpf, nome, tell, senha FROM funcionario WHERE cpf = %s"
        cursor.execute(sql, (cpf,))
        # cursor.fetchone vai retornar uma tupla(linha) do banco de dados
        resultado = cursor.fetchone()
        print(f"Resultado da consulta para CPF {cpf}: {resultado}")
    
    except mysql.connector.Error as e:
        print(f"Erro ao consultar o banco de dados: {e}")
    
    finally:
        # Sempre feche o cursor e a conexão, independentemente de ter ocorrido um erro ou não
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()

    return resultado

def inserir_usuario(cpf, nome, tell, email):
    mydb = bd_config()
    cursor = mydb.cursor()

    # Verificando se o usuário existe
    cursor.execute("SELECT * FROM usuario WHERE cpf = %s",(cpf,))
   # cursor.fetchall vai retornar todas as tuplas do banco de dados
    resultado = cursor.fetchone()
    if resultado:
        
        mydb.commit()
        cursor.close()
        mydb.close()
        
        return "CPF já existe"
    
    sql = "INSERT INTO usuario (cpf,nome,tell,email) VALUES(%s, %s, %s, %s);"
    val = (cpf, nome, tell, email)
    cursor.execute(sql,(val))
    
    # mydb.commit, faz o commit para o banco dedos ou seja, atualiza.
    mydb.commit()
    # encerra a execução da query
    cursor.close()
    # encerra a conexão com o banco de dados
    mydb.close()
    return "Usuário inserido com Sucesso."

def inserir_processo(num_processo,orgao,unidade,tipo_processo,cpf):
    mydb = bd_config()
    cursor = mydb.cursor()

    # Verificando se o processo existe
    cursor.execute("SELECT * FROM processo WHERE numero_processo = %s",(num_processo,))
   # cursor.fetchall vai retornar todas as tuplas do banco de dados
    resultado = cursor.fetchall()
    if resultado:
        cursor.close()
        mydb.close()
        return "Processo já Existe."
    
    sql = ''' INSERT INTO processo (numero_processo, orgao_julgador, unidade, tipo_processo, fk_cpf_usuario) 
        VALUES(%s, %s, %s, %s, %s);'''
    
    val = (num_processo,orgao, unidade, tipo_processo, cpf)
    cursor.execute(sql,(val))

    # mydb.commit, faz o commit para o banco dedos ou seja, atualiza.
    mydb.commit()
    # encerra a execução da query
    cursor.close()
    # encerra a conexão com o banco de dados
    mydb.close()
    return "Processo inserido com sucesso"


def consultar_dados(cpf):
    mydb = bd_config()
    cursor = mydb.cursor(dictionary=True)
    try:
        if not cpf:
            raise ValueError("CPF não fornecido")

        sql = ''' SELECT usuario.*, processo.numero_processo, processo.orgao_julgador, processo.unidade, processo.tipo_processo 
        FROM usuario 
        INNER JOIN processo 
        ON usuario.cpf = processo.fk_cpf_usuario 
        WHERE cpf = %s
        '''
        
        cursor.execute(sql, (cpf,))
        resultado = cursor.fetchall()
        
        #atualizando o banco de dados
        mydb.commit()
        
        if resultado:
            return resultado
        else:
            return {"erro": "Usuário não encontrado"}
    
    except Exception as e:
        return {"erro": "Erro ao consultar dados"}
    
    finally:
        cursor.close()
        mydb.close()


def atualizar_dados(cpf, telefone, email):
    # configurações do banco de dados
    mydb = bd_config()
    # puxando as funções do cursor retornando dados em dicionário  
    cursor = mydb.cursor(dictionary=True)
    # comando DML para manipulação de dados no BANCO DE DADOS
    sql = ''' UPDATE usuario SET tell = %s, email = %s WHERE cpf = %s '''
    val = (telefone, email, cpf)  # Parâmetros na ordem correta
    
    cursor.execute(sql, val)  # Executando a atualização
    mydb.commit()  # Commitando as alterações no banco de dados
    cursor.close() # vai encerrar a execução
    mydb.close() # vai encerrar a integração com o banco de dados
    return 'Usuario atualizado com Sucesso!'
        
def atualizar_processo(num_processo,orgao_julgador,unidade):
    # configurações do banco de dados
    mydb = bd_config()
    # puxando as funções do cursor retornando dados em dicionário  
    cursor = mydb.cursor(dictionary=True)
  
    sql = ''' UPDATE processo SET orgao_julgador = %s, unidade = %s WHERE numero_processo = %s '''
    val = (orgao_julgador, unidade, num_processo)  # Parâmetros na ordem correta
    cursor.execute(sql, val)  # Executando a atualização
    mydb.commit()  # Commitando as alterações no banco de dados
    cursor.close() # vai encerrar a execução
    mydb.close() # vai encerrar a integração com o banco de dados
    return 'Processo Atualizado com Sucesso!'

def deletar_usuario(cpf):
    # Configurações do banco de dados
    mydb = bd_config()
    cursor = mydb.cursor(dictionary=True)
    
    # Verificando se o usuário existe
    sql = "SELECT * FROM usuario WHERE cpf = %s"
    cursor.execute(sql, (cpf,))
    resultado = cursor.fetchone()
    
    if not resultado:
        cursor.close()
        mydb.close()
        return 'Usuário não existe!'
    
    # Deletando o usuário
    sql = "DELETE FROM usuario WHERE cpf = %s"
    cursor.execute(sql, (cpf,))
    mydb.commit()
    cursor.close()
    mydb.close()
    
    return 'Usuário deletado com sucesso!'

def deletar_processo(numero_processo):
    # Configurações do banco de dados
    mydb = bd_config()
    cursor = mydb.cursor(dictionary=True)
    
    # Verificando se o processo existe
    sql = "SELECT * FROM processo WHERE numero_processo = %s"
    cursor.execute(sql, (numero_processo,))
    resultado = cursor.fetchone()
    
    if not resultado:
        cursor.close()
        mydb.close()
        return 'Processo não existe!'
    
    # Deletando o processo
    sql = "DELETE FROM processo WHERE numero_processo = %s"
    cursor.execute(sql, (numero_processo,))
    mydb.commit()
    cursor.close()
    mydb.close()
    
    return 'Processo deletado com sucesso!'

from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify,json
from banco.database import bd_config, inserir_funcionario, avaliador_login
from banco.database import inserir_usuario, inserir_processo, consultar_dados, atualizar_dados, atualizar_processo
from banco.database import deletar_usuario, deletar_processo
from werkzeug.security import generate_password_hash, check_password_hash


# configurações para o servidor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = "beababebibobu"

# Configuração e integração com o banco de dados
mydb = bd_config()

@app.route('/')
@app.route('/home')
def index():
    if 'fun_name' not in session:
        # o redirecionamento está no javascript
        pass
    return render_template('assets/html/index.html', fun_name=session.get('fun_name'))

@app.route('/inserir', methods = ['GET','POST'])
def inserir():
    if request.method == 'POST':
        action = request.form.get('action')  # campo oculto no formulário para distinguir a ação

        if action == 'inserir_usuario':
            nome = request.form.get('nome')
            cpf = request.form.get('cpf')
            email = request.form.get('email')
            telefone = request.form.get('tell')
           
            # Inserindo o usuário no banco de dados
            dados_usuario = inserir_usuario(cpf, nome, telefone, email)
            # depuração
            print(f'Resultado para CPF: {dados_usuario}')
            if dados_usuario == "CPF já existe":
               flash('Não é possível Cadastrar, Cpf já existe!', 'alert') 
            elif dados_usuario:
                flash('Usuário inserido com sucesso!', 'usuario')
            else:
                flash('Erro ao inserir usuário.', 'usuario')
        
        elif action == 'inserir_processo':
            cpf = request.form.get('cpf')
            numero_processo = request.form.get('numprocesso')
            orgao = request.form.get('orgao')
            unidade = request.form.get('unidade')
            tipo_processo = request.form.get('tipo')

            # Inserindo o processo no banco de dados
            dados_processo = inserir_processo(numero_processo,orgao,unidade,tipo_processo,cpf)
            # depuração
            print(f'Resultado para o numero de processe{dados_processo}')
            
            if dados_processo == "Processo já Existe.":
                flash('Processo já existe!', 'alert') 
            elif dados_processo:
                flash('Processo inserido com sucesso!', 'processo')
            else:
                flash('Erro ao inserir processo.', 'processo')
        return redirect(url_for('inserir'))
          
    return render_template('assets/html/inserir.html')

@app.route('/atualizar', methods = ['GET', 'POST'])
def atualizar():
    if request.method == 'POST':
        
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        email = request.form['email']
        numero_processo =  request.form['numero_processo']
        orgao_julgador = request.form['orgao']      
        unidade = request.form['unidade']

        dados_usuario = atualizar_dados(cpf,telefone,email)
        dados_processo = atualizar_processo(numero_processo,orgao_julgador,unidade)


        print(f'Resultado para: {dados_usuario} e {dados_processo}')
        
        if dados_usuario or dados_processo:
            flash("Dados Atualizados com Sucesso!", 'dados')
        else:
            flash("Não foi possível a Atualização dos Dados!")
    
    return render_template('assets/html/atualizar.html')

@app.route('/deletar', methods = ['GET','POST'])
def deletar():
    if request.method == 'POST':
        action = request.form['action']
        
        if action == "deletar_usuario":
            cpf = request.form['cpf']
            deletado = deletar_usuario(cpf)
        
            if deletado == 'Usuário Deletado com Sucesso':
                flash("Usuario Deletado com Sucesso!", 'usuario')
                return render_template('assets/html/deletar.html')
            else:
                flash('Usuário não existe!', 'usuario')
                return redirect(url_for('deletar')) 
        
        if action == "deletar_processo":
            numero_processo = request.form['numero_processo']
            deletado = deletar_processo(numero_processo)

            if deletado == 'Processo deletado com sucesso!':
                flash('Processo deletado com Sucesso!','processo')
                return render_template('assets/html/deletar.html')
            else:
                flash('Processo não existe!', 'processo')
                return render_template('assets/html/deletar.html')

    return render_template('assets/html/deletar.html')

from flask import flash, jsonify, render_template, request, redirect, url_for

@app.route('/consultar', methods=['GET', 'POST'])
def consulta():
    if request.method == 'POST':
        cpf = request.form['cpf']
        
        # Simulação de função para consultar dados
        # Replace this with your actual data retrieval logic
        resultado = consultar_dados(cpf)
        
        # Adicionando uma impressão para depuração
        print(f"Resultado da consulta: {resultado}")
        
        # Verifica se o resultado indica que o usuário não foi encontrado
        if 'erro' in resultado and resultado['erro'] == 'Usuário não encontrado':
            flash("Usuário não encontrado!", 'alert')
            return render_template('assets/html/search.html')
        
        # Se o resultado foi encontrado com sucesso, retorna para o template
        return render_template('assets/html/search.html', resposta=resultado)

    # Caso seja uma requisição GET (primeiro carregamento da página)
    return render_template('assets/html/search.html')

@app.route('/signup', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['tell']
        senha = request.form['senha']
        confirm_senha = request.form['confirmsenha']
        
        if senha != confirm_senha:
            return redirect(url_for('cadastro'))    
        
        senha_hash = generate_password_hash(senha)
        insert = inserir_funcionario(cpf, nome, telefone, senha_hash)

        if insert == 'FUNCIONARIO INSERIDO COM SUCESSO!':
            return redirect(url_for('login'))
    
    return render_template('assets/html/signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        cpf = request.form['cpf']
        senha = request.form['senha']
        
        #variável que irá armazenar a função de avaliar
        funcionario = avaliador_login(cpf)

        if funcionario:
            senha_hash_banco = funcionario['senha']
            if check_password_hash(senha_hash_banco, senha):
                
                #passando validador de senha e dados, vamos armazenar o nome da pessoa dentro de uma sessão específica
                session['fun_name'] = funcionario['nome']
                
                return redirect(url_for('index'))
        
        return render_template('assets/html/signin.html')

    return render_template('assets/html/signin.html')

@app.route('/session-user')
def session_user():
    if 'fun_name' in session:
        return jsonify({
            "logged_in": True,
            "fun_name": session.get('fun_name')
        })
    return jsonify({"logged_in": False})

@app.route('/logout', methods=['POST'])
def logout():
    # ao sair da página, vai remover o nome da session e redirecionar para tela de login
    session.pop('fun_name', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

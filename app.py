import os
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
# Pega a chave secreta das variáveis de ambiente (Render) ou usa uma padrão para desenvolvimento
app.secret_key = os.environ.get('SECRET_KEY 4989665ffe0b342831dd366ae12894d38fc57e59c369dc5c652ef61d5f5744fd', 'chave_para_desenvolvimento_local')

# Simulando banco de dados em memória (não persistente)
contatos = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/custo-por-km-carro', methods=['GET', 'POST'])
def custo_por_km():
    resultado = None
    if request.method == 'POST':
        try:
            preco_combustivel = float(request.form['preco_combustivel'])
            consumo_medio = float(request.form['consumo_medio'])
            
            custo_km = preco_combustivel / consumo_medio
            
            resultado = {
                'custo_km': round(custo_km, 3),
                'preco': preco_combustivel,
                'consumo': consumo_medio
            }
        except ValueError:
            flash('Por favor, insira valores numéricos válidos', 'error')
        except KeyError:
            flash('Todos os campos são obrigatórios', 'error')
    
    return render_template('custo_por_km.html', resultado=resultado)

@app.route('/gasto-mensal-combustivel', methods=['GET', 'POST'])
def gasto_mensal():
    resultado = None
    if request.method == 'POST':
        try:
            km_mensal = float(request.form['km_mensal'])
            consumo_medio = float(request.form['consumo_medio'])
            preco_combustivel = float(request.form['preco_combustivel'])
            
            litros_necessarios = km_mensal / consumo_medio
            gasto_total = litros_necessarios * preco_combustivel
            
            resultado = {
                'gasto_total': round(gasto_total, 2),
                'litros': round(litros_necessarios, 2),
                'km_mensal': km_mensal
            }
        except ValueError:
            flash('Por favor, insira valores numéricos válidos', 'error')
        except KeyError:
            flash('Todos os campos são obrigatórios', 'error')
    
    return render_template('gasto_mensal.html', resultado=resultado)

@app.route('/etanol-ou-gasolina-calculadora', methods=['GET', 'POST'])
def etanol_gasolina():
    resultado = None
    if request.method == 'POST':
        try:
            preco_etanol = float(request.form['preco_etanol'])
            preco_gasolina = float(request.form['preco_gasolina'])
            
            if preco_gasolina <= 0:
                flash('O preço da gasolina deve ser maior que zero', 'error')
                return render_template('etanol_gasolina.html', resultado=resultado)
            
            relacao = preco_etanol / preco_gasolina
            
            if relacao <= 0.7:
                recomendacao = "etanol"
                economia = "mais econômico"
            else:
                recomendacao = "gasolina"
                economia = "mais econômico"
            
            resultado = {
                'relacao': round(relacao * 100, 1),
                'recomendacao': recomendacao,
                'economia': economia,
                'preco_etanol': preco_etanol,
                'preco_gasolina': preco_gasolina
            }
        except ValueError:
            flash('Por favor, insira valores numéricos válidos', 'error')
        except ZeroDivisionError:
            flash('O preço da gasolina não pode ser zero', 'error')
        except KeyError:
            flash('Todos os campos são obrigatórios', 'error')
    
    return render_template('etanol_gasolina.html', resultado=resultado)

@app.route('/custo-viagem-carro', methods=['GET', 'POST'])
def custo_viagem():
    resultado = None
    if request.method == 'POST':
        try:
            distancia = float(request.form['distancia'])
            consumo_medio = float(request.form['consumo_medio'])
            preco_combustivel = float(request.form['preco_combustivel'])
            pedagios = float(request.form.get('pedagios', 0))
            
            if consumo_medio <= 0:
                flash('O consumo médio deve ser maior que zero', 'error')
                return render_template('custo_viagem.html', resultado=resultado)
            
            litros_necessarios = distancia / consumo_medio
            custo_combustivel = litros_necessarios * preco_combustivel
            custo_total = custo_combustivel + pedagios
            
            resultado = {
                'custo_total': round(custo_total, 2),
                'custo_combustivel': round(custo_combustivel, 2),
                'litros': round(litros_necessarios, 2),
                'pedagios': pedagios,
                'distancia': distancia
            }
        except ValueError:
            flash('Por favor, insira valores numéricos válidos', 'error')
        except ZeroDivisionError:
            flash('O consumo médio não pode ser zero', 'error')
        except KeyError:
            flash('Todos os campos são obrigatórios', 'error')
    
    return render_template('custo_viagem.html', resultado=resultado)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            email = request.form['email']
            mensagem = request.form['mensagem']
            
            # Validação básica
            if not nome or not email or not mensagem:
                flash('Todos os campos são obrigatórios', 'error')
                return render_template('contato.html')
            
            # Simulando envio de contato
            contatos.append({
                'nome': nome,
                'email': email,
                'mensagem': mensagem
            })
            
            flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
        except KeyError:
            flash('Erro ao processar o formulário', 'error')
        
        return redirect(url_for('contato'))
    
    return render_template('contato.html')

@app.route('/politica-de-privacidade')
def politica_privacidade():
    return render_template('politica_privacidade.html')

@app.route('/ads.txt')
def ads_txt():
    # Substitua pelo código exato que o Google forneceu
    return "google.com, pub-2580999860510639, DIRECT, f08c47fec0942fa0"

# Esta parte só executa se rodar diretamente (não no Render)
if __name__ == '__main__':
    # Em produção, o gunicorn vai gerenciar isso
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
import os
from flask import Flask

app = Flask(__name__)
app.secret_key = 'qualquer-coisa-aqui'

@app.route('/')
def index():
    return "Funcionou!"

@app.route('/ads.txt')
def ads_txt():
    return "google.com, pub-SEU_CODIGO_AQUI, DIRECT, f08c47fec0942fa0"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
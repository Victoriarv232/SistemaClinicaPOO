from abc import ABC, abstractmethod
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
import logging

pymysql.install_as_MySQLdb()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/senhas_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

try:
    with app.app_context():
         db.create_all()
    logger.info("Banco de dados conectado e tabelas criadas com sucesso.")
except Exception as e:
    logger.critical(f"Falha crítica ao conectar ou criar tabelas no banco de dados: {e}")

# BANCO DE DADOS
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setor = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(10), nullable=False)
    preferencial = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{self.senha} ({'Preferencial' if self.preferencial else 'Normal'}) - {self.setor}"

# CONSULTÓRIOS E GERADORES
class GeradorSenha(ABC):
    @abstractmethod
    def gerar_senha(self, preferencial=False):
        pass

    @abstractmethod
    def resetar(self):
        pass
class GeradorSenhaUnico(GeradorSenha):
    def __init__(self, sigla, limite):
        self.sigla = sigla
        self.limite = limite
        self.contador = 1
        logger.debug(f"Gerador criado para {sigla} com limite {limite}")


    def gerar_senha(self, preferencial=False):
        if self.contador > self.limite:
            logger.warning(f"Limite de senhas atingido para {self.sigla}")
            return None
        prefixo = f"{self.sigla}P" if preferencial else self.sigla
        senha = f"{prefixo}{self.contador:02d}"
        self.contador += 1
        logger.info(f"Senha gerada: {senha} (Preferencial: {preferencial})")
        return senha

    def resetar(self):
        self.contador = 1

consultorios = {
    'CG - Clínica Geral': {'sigla': 'CG', 'limite': 60},
    'GIN - Ginecologia': {'sigla': 'GIN', 'limite': 40},
    'PED - Pediatria': {'sigla': 'PED', 'limite': 40},
    'GER - Geriatria': {'sigla': 'GER', 'limite': 40},
    'ORT - Ortopedia': {'sigla': 'ORT', 'limite': 40},
}
geradores = {nome: GeradorSenhaUnico(
    info['sigla'], info['limite']) for nome, info in consultorios.items()}

# ROTAS

@app.route('/', methods=['GET', 'POST'])
def index():
    mensagem = None
    if request.method == 'POST':
        setor = request.form['setor']
        preferencial = request.form['preferencial'] == '1'

        total_senhas = Paciente.query.filter_by(setor=setor).count()
        if total_senhas >= consultorios[setor]['limite']:
            mensagem = f" Limite de senhas atingido para {setor}."
            logger.warning(mensagem)
        else:
            senha = geradores[setor].gerar_senha(preferencial)
            if senha is None:
                mensagem = f" Não foi possível gerar nova senha para {setor}"
                logger.error(mensagem)
            else:
                novo_paciente = Paciente(
                    setor=setor, senha=senha, preferencial=preferencial)
                db.session.add(novo_paciente)
                db.session.commit()
                mensagem = f"Senha gerada: {senha}. Aguarde ser chamado."

    return render_template('index.html', consultorios=consultorios, mensagem=mensagem)


@app.route('/painel')
def painel():
    def proximo_paciente():
        preferencial = Paciente.query.filter_by(preferencial=True).first()
        if preferencial:
            logger.info(f"Chamando paciente preferencial: {preferencial}")
            db.session.delete(preferencial)
            db.session.commit()
            return preferencial
        normal = Paciente.query.filter_by(preferencial=False).first()
        if normal:
            logger.info(f"Chamando paciente normal: {normal}")
            db.session.delete(normal)
            db.session.commit()
            return normal
        logger.info("Nenhum paciente na fila para chamar")
        return None

    guiche1 = proximo_paciente()
    guiche2 = proximo_paciente()
    

    fila_espera = Paciente.query.order_by(
        Paciente.preferencial.desc(),  # Preferenciais primeiro (True > False)
        Paciente.id.asc()              # Ordem de chegada (id crescente)
    ).all()

    logger.debug(f"Fila de espera atual: {fila_espera}")

    return render_template('painel.html', guiche1=guiche1, guiche2=guiche2, fila_espera=fila_espera)

@app.route('/resetar')
def resetar():
    # Apaga todas as senhas do banco
    Paciente.query.delete()
    db.session.commit()

    # Reseta os contadores dos geradores
    for g in geradores.values():
        g.resetar()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

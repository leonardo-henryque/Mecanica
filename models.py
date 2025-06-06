from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import  sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import configparser

# Configurar Banco Vercel
# Ler variáveis de ambiente
load_dotenv()

# Carrega a configuração do Banco de Dados
url_ = os.environ.get('DATABASE_URL')
print(f'modo1:{url_}')

# Carregueo arquivo de configuração
config = configparser.ConfigParser()
config.read('config.ini')


engine = create_engine('sqlite:///mecanica.sqlite3')
banco_session = sessionmaker(bind=engine)
Base = declarative_base()
# Base.query = db_session.query_property()

class Ordem_de_servicos(Base):
    __tablename__ = 'ordem_de_servicos'
    id = Column(Integer, primary_key=True)
    veiculo_associados = Column(Integer, nullable=False, index=True)
    data_de_abertura = Column(String, nullable=False, index=True)
    descricao_do_servicos = Column(String, nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True)
    valor_estimado = Column(Float, nullable=False, index=True)

    def __repr__(self):
        return '<Ordens {},{},{},{},{}>'.format(self.id, self.veiculo_associados, self.data_de_abertura, self.descricao_do_servicos, self.status, self.valor_estimado)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e

    # def delete(self, db_session):
    #     db_session.delete(self)
    #     db_session.commit()

    def get_servicos(self):
        dados_servicos = {
            'id': self.id,
            'veiculo_associados': self.veiculo_associados,
            'data_de_abertura': self.data_de_abertura,
            'descricaco_do_servicos': self.descricao_do_servicos,
            'status': self.status,
            'valor_estimado': self.valor_estimado,
        }
        return dados_servicos

class Clientes(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    CPF = Column(Integer, nullable=False, index=True)
    telefone = Column(Integer, nullable=False, index=True)
    endereco = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)

    def __repr__(self):
        return '<Clientes {},{},{},{},{}>' .format(self.nome, self.CPF, self.telefone, self.endereco, self.email)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e

    # def delete_usuario(self, db_session):
    #     db_session.delete(self)
    #     db_session.commit()

    def get_usuario(self):
        dados_usuarios = {
            'id': self.id,
            'nome': self.nome,
            'CPF': self.CPF,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'email': self.email,
        }
        return dados_usuarios

class Veiculos(Base):
    __tablename__ = 'veiculos'
    id = Column(Integer, primary_key=True, index=True)
    cliente_associados = Column(Integer, nullable=False , index=True)
    marca = Column(String, nullable=False, index=True)
    modelo = Column(String, nullable=False, index=True)
    placa = Column(Integer, index=True, nullable=False)
    ano_de_fabricacao = Column(String, nullable=True, index=True)


    def __repr__(self):
        return '<veiculo {},{},{},{},{}'. format(self.cliente_associados, self.marca, self.modelo, self.placa, self.ano_de_fabricacao)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e


    # def delete_emprestimo(self, db_session):
    #     db_session.delete(self)
    #     db_session.commit()

    # Coloca os dados na Tabela
    def get_emprestimo(self):
        dados_emprestimos = {
            'id': self.id,
            'clientes_associados': self.cliente_associados,
            'marca': self.marca,
            'modelo': self.modelo,
            'placa': self.placa,
            'ano_de_fabricacao': self.ano_de_fabricacao,
        }
        return dados_emprestimos


def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()
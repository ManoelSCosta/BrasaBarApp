# app/database/db_connection.py
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'brasa_bar_db'),
    'user': os.getenv('DB_USER', 'mscosta'),
    'password': os.getenv('DB_PASSWORD', 'mscosta')
}

# String de conexão formatada
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Cria a engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    echo=True  # Mantenha True para ver queries no console durante desenvolvimento
)

# Fábrica de sessões
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Sessão thread-safe para uso em aplicações multi-threaded
ScopedSession = scoped_session(SessionLocal)

# Base para modelos declarativos (forma correta para SQLAlchemy 2.x)
Base = declarative_base()


def get_db():
    """Fornece uma nova sessão de banco de dados"""
    db = ScopedSession()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    import app.shared.models  # Importa todos os modelos para registro
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados inicializado com sucesso!")


def test_connection():
    """Testa a conexão com o banco de dados"""
    try:
        with engine.connect() as conn:
            # Testar a versão do PostgreSQL
            result = conn.execute(text("SELECT version()"))
            db_version = result.scalar()
            print(f"✅ Conexão bem-sucedida com PostgreSQL {db_version}")

            # Verificar se o esquema público existe
            result = conn.execute(
                text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'brasa_bar'"))
            if not result.fetchone():
                print("⚠️ Esquema 'brasa_bar' não encontrado!")
                return False

            # Verificar tabelas existentes
            result = conn.execute(text("""
                                       SELECT table_name
                                       FROM information_schema.tables
                                       WHERE table_schema = 'brasa_bar'
                                       """))
            tables = [row[0] for row in result.fetchall()]
            print(f"📊 Tabelas existentes: {', '.join(tables) or 'Nenhuma'}")

            return True
    except Exception as e:
        print(f"❌ Falha na conexão com o banco de dados: {e}")
        print("Verifique suas configurações:")
        print(DB_CONFIG)
        return False


# Teste de conexão ao executar o arquivo
if __name__ == "__main__":
    print("=" * 50)
    print("TESTE DE CONEXÃO COM O BANCO DE DADOS")
    print("=" * 50)
    print(f"Configuração usada:")
    for key, value in DB_CONFIG.items():
        print(f"  {key.upper()}: {value}")

    if test_connection():
        if "--init" in sys.argv:
            init_db()
            print("✨ Tabelas criadas com sucesso!")
    else:
        print("\nDica: Verifique se:")
        print("- O PostgreSQL está rodando")
        print("- As credenciais estão corretas")
        print("- O usuário tem permissões no banco")
        print("- O firewall permite conexões na porta 5432")
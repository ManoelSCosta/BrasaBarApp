# app/database/db_connection.py

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do banco
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'brasa_bar_db'),
    'user': os.getenv('DB_USER', 'mscosta'),
    'password': os.getenv('DB_PASSWORD', 'mscosta'),
    'schema': os.getenv('DB_SCHEMA', 'brasa_bar')
}

# Monta a DATABASE_URL com search_path via options
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    f"?options=-csearch_path%3D{DB_CONFIG['schema']}"
)

# Criação do engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    echo=True
)

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
ScopedSession = scoped_session(SessionLocal)

# Base declarativa
Base = declarative_base()
Base.metadata.schema = DB_CONFIG['schema']


# Dependency injection
def get_db():
    db = ScopedSession()
    try:
        yield db
    finally:
        db.close()


# Cria o schema no banco, se não existir
def create_schema():
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {DB_CONFIG['schema']}"))
        conn.commit()


# Inicializa o banco
def init_db():
    create_schema()
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados inicializado com sucesso!")


# Testa conexão e retorna True/False
def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            db_version = result.scalar()
            print(f"✅ Conexão bem-sucedida com PostgreSQL {db_version}")

            schema = DB_CONFIG['schema']
            result = conn.execute(
                text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema"),
                {"schema": schema}
            )
            if not result.fetchone():
                print(f"⚠️ Esquema '{schema}' não encontrado!")
                return False

            result = conn.execute(text(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = :schema
            """), {"schema": schema})
            tables = [row[0] for row in result.fetchall()]
            print(f"📊 Tabelas existentes: {', '.join(tables) or 'Nenhuma'}")

            return True

    except Exception as e:
        print(f"❌ Falha na conexão: {e}")
        print(f"🧪 Configuração usada:")
        for k, v in DB_CONFIG.items():
            print(f"  {k.upper()}: {v}")
        return False


# Execução direta
if __name__ == "__main__":
    print("=" * 50)
    print("TESTE DE CONEXÃO COM O BANCO DE DADOS")
    print("=" * 50)
    if test_connection():
        if "--init" in sys.argv:
            init_db()
            print("✨ Tabelas criadas com sucesso!")
    else:
        print("\n🔧 Dicas de verificação:")
        print("- Verifique se o PostgreSQL está rodando")
        print("- Confirme usuário, senha e banco no .env")
        print("- Confirme se o schema existe ou se tem permissão CREATE")

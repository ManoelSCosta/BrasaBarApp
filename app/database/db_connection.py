import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'brasa_bar_db'),
    'user': os.getenv('DB_USER', 'mscosta'),
    'password': os.getenv('DB_PASSWORD', 'mscosta'),
    'schema': os.getenv('DB_SCHEMA', 'brasa_bar')  # Novo
}

# String de conexão com schema
DATABASE_URL = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/"
    f"{DB_CONFIG['database']}?options=-csearch_path%3D{DB_CONFIG['schema']}"
)

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    echo=True
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
ScopedSession = scoped_session(SessionLocal)

Base = declarative_base()
Base.metadata.schema = DB_CONFIG['schema']  # Define o schema para todos os modelos


def get_db():
    db = ScopedSession()
    try:
        yield db
    finally:
        db.close()


def create_schema():
    """Cria o schema se não existir"""
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {DB_CONFIG['schema']}"))
        conn.commit()


def init_db():
    """Inicializa o banco criando schema e tabelas"""
    create_schema()
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados inicializado com sucesso!")


def test_connection():
    try:
        with engine.connect() as conn:
            # Testar versão do PostgreSQL
            result = conn.execute(text("SELECT version()"))
            db_version = result.scalar()
            print(f"✅ Conexão bem-sucedida com PostgreSQL {db_version}")

            # Verificar schema
            schema = DB_CONFIG['schema']
            result = conn.execute(
                text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema"),
                {"schema": schema}
            )
            if not result.fetchone():
                print(f"⚠️ Esquema '{schema}' não encontrado!")
                return False

            # Verificar tabelas
            result = conn.execute(text(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = '{schema}'
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"📊 Tabelas existentes: {', '.join(tables) or 'Nenhuma'}")

            return True
    except Exception as e:
        print(f"❌ Falha na conexão: {e}")
        print(f"Configuração: {DB_CONFIG}")
        return False


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
        print("- O schema existe ou tem permissões")
        print("- O usuário tem privilégios CREATE no banco")
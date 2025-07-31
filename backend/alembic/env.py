import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from dotenv import load_dotenv
load_dotenv()

# Config Alembic
config = context.config

# 🔁 Injecte l'URL de la base depuis le fichier .env
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL not found in .env file")
config.set_main_option("sqlalchemy.url", database_url)

# Configure le logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🔽 Ajoute ici les métadonnées SQLAlchemy pour l'autogénération
from src.models import users  # ← adapte selon où est ton Base
target_metadata = users.Base.metadata

def run_migrations_offline() -> None:
    """Exécute les migrations en mode offline (génère des SQL bruts)."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Exécute les migrations en mode online (avec une vraie connexion DB)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

# Point d'entrée
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

# Import your Base class from your database module
from src.database.db import Base

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target_metadata to your Base's metadata
target_metadata = Base.metadata


def run_migrations_online():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_offline():
    context.configure(
        url=SQLALCHEMY_DATABASE_URL, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

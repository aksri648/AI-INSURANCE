import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from alembic import context
from app.database import Base
from app.models import *
from app.config import settings

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=settings.database_url_sync, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    from sqlalchemy import create_engine
    connectable = create_engine(settings.database_url_sync)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

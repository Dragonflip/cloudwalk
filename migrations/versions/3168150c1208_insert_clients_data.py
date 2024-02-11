"""insert clients data

Revision ID: 3168150c1208
Revises: 397c930c2bfd
Create Date: 2024-02-10 14:06:56.907964

"""
from typing import Sequence, Union
import os
import csv

from alembic import op
from sqlalchemy import create_engine
from  cloudwalk.settings import Settings

# revision identifiers, used by Alembic.
revision: str = '3168150c1208'
down_revision: Union[str, None] = '397c930c2bfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    settings = Settings()    #type: ignore
    dirname = os.getcwd()
    filename = os.path.join(dirname, 'migrations/data/clients.csv')
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        columns = ','.join(header)
        conn = create_engine(settings.DATABASE_URL).raw_connection()
        cursor = conn.cursor()
        cmd = f'COPY clients({columns}) FROM STDIN WITH (FORMAT CSV, HEADER FALSE)'
        cursor.copy_expert(cmd, f)
        conn.commit()

def downgrade() -> None:
    pass

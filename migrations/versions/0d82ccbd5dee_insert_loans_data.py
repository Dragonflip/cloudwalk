"""insert loanss data

Revision ID: 0d82ccbd5dee
Revises: 3168150c1208
Create Date: 2024-02-10 14:07:04.679731

"""
from typing import Sequence, Union
import csv
import os

from alembic import op
from sqlalchemy import create_engine
from  cloudwalk.settings import Settings

# revision identifiers, used by Alembic.
revision: str = '0d82ccbd5dee'
down_revision: Union[str, None] = '3168150c1208'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    settings = Settings()    #type: ignore
    dirname = os.getcwd()
    filename = os.path.join(dirname, 'migrations/data/loans.csv')
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        columns = ','.join(header)
        conn = create_engine(settings.DATABASE_URL).raw_connection()
        cursor = conn.cursor()
        cmd = f'COPY loans({columns}) FROM STDIN WITH (FORMAT CSV, HEADER FALSE)'
        cursor.copy_expert(cmd, f)
        conn.commit()

def downgrade() -> None:
    pass

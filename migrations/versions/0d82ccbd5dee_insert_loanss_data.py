"""insert loanss data

Revision ID: 0d82ccbd5dee
Revises: 3168150c1208
Create Date: 2024-02-10 14:07:04.679731

"""
from typing import Sequence, Union
import csv
import os

from alembic import op
import sqlalchemy as sa
from cloudwalk.settings import Settings
from cloudwalk.db.insert import insert_csv_to_postgres


# revision identifiers, used by Alembic.
revision: str = '0d82ccbd5dee'
down_revision: Union[str, None] = '3168150c1208'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    dirname = os.getcwd()
    filename = os.path.join(dirname, 'migrations/data/loans.csv')
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
    columns = ','.join(header)
    with open(filename, 'r') as f:
        # Construct the COPY command
        copy_sql = f"""
        COPY loans({columns}) FROM stdin WITH CSV HEADER
        {f.read()}
        """
        # Execute the COPY command
        op.execute(copy_sql)

def downgrade() -> None:
    pass

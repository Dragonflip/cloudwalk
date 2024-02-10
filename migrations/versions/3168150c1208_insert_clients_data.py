"""insert clients data

Revision ID: 3168150c1208
Revises: 397c930c2bfd
Create Date: 2024-02-10 14:06:56.907964

"""
from typing import Sequence, Union
import csv
import os

from alembic import op
import sqlalchemy as sa
from cloudwalk.settings import Settings
from cloudwalk.db.insert import insert_csv_to_postgres

# revision identifiers, used by Alembic.
revision: str = '3168150c1208'
down_revision: Union[str, None] = '397c930c2bfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    dirname = os.getcwd()
    filename = os.path.join(dirname, 'migrations/data/clients.csv')
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

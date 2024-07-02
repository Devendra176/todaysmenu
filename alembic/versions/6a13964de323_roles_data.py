"""roles data

Revision ID: 6a13964de323
Revises: 7895b0c22c93
Create Date: 2024-06-13 15:33:43.899681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a13964de323'
down_revision: Union[str, None] = '7895b0c22c93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "INSERT INTO role (role) VALUES ('admin'), ('restaurant'), ('customer')"
    )


def downgrade() -> None:
    pass

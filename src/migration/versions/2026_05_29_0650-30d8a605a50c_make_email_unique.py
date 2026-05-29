"""make email unique

Revision ID: 30d8a605a50c
Revises: 8c4d6d93a8ff
Create Date: 2026-05-29 06:50:19.656758

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "30d8a605a50c"
down_revision: Union[str, Sequence[str], None] = "8c4d6d93a8ff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")

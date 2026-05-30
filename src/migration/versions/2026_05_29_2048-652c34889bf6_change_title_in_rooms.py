"""change title in Rooms

Revision ID: 652c34889bf6
Revises: 30d8a605a50c
Create Date: 2026-05-29 20:48:29.797481

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "652c34889bf6"
down_revision: Union[str, Sequence[str], None] = "30d8a605a50c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "rooms",
        "title",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "rooms",
        "title",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )

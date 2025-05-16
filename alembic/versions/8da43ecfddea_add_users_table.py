"""add users table

Revision ID: 8da43ecfddea
Revises: 8068da51328a
Create Date: 2025-05-15 15:00:43.479223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8da43ecfddea'
down_revision: Union[str, None] = '8068da51328a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.create_table(
        "users",
        sa.Column("id" , sa.Integer() , nullable=False),
        sa.Column("email" , sa.String() , nullable=False),
        sa.Column("password" , sa.String() , nullable=False),
        sa.Column("created_at" , sa.TIMESTAMP(timezone=True) , server_default=sa.text("now()") , nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )

    pass


def downgrade() -> None:
    op.drop_table("users")
    pass

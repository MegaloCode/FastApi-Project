"""add last few columns to posts table

Revision ID: 84abddf13ea5
Revises: 2b044339e4c6
Create Date: 2025-05-15 16:37:47.458027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84abddf13ea5'
down_revision: Union[str, None] = '2b044339e4c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published" , sa.Boolean() , nullable=False , server_default=sa.text("true") ) 
    )

    op.add_column(
        "posts",
        sa.Column("created_at" , sa.TIMESTAMP(timezone=True) , nullable=False , server_default=sa.text("now()"))
    )
    pass


def downgrade() -> None:
    op.drop_column("posts" , "published")
    op.drop_column("posts" , "created_at")
    pass

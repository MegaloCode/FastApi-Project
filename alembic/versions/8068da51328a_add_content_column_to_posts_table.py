"""add content column to posts table

Revision ID: 8068da51328a
Revises: fa3d8c383579
Create Date: 2025-05-15 14:51:08.160240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8068da51328a'
down_revision: Union[str, None] = 'fa3d8c383579'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.add_column(
        "posts" ,
        sa.Column("content" , sa.String() , nullable=False)
        )

    pass


def downgrade() -> None:
    op.drop_column("posts" , "content")
    pass

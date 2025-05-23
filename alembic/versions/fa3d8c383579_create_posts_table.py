"""create_posts_table

Revision ID: fa3d8c383579
Revises: 
Create Date: 2025-05-15 14:05:08.204185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa3d8c383579'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title" , sa.String(), nullable=False )
        )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass

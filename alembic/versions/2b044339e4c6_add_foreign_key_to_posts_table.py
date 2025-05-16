"""add foreign-key to posts table

Revision ID: 2b044339e4c6
Revises: 8da43ecfddea
Create Date: 2025-05-15 16:23:37.220205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b044339e4c6'
down_revision: Union[str, None] = '8da43ecfddea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts" , sa.Column("owner_id" , sa.Integer() , nullable=False))
    op.create_foreign_key("posts_users_fk" , source_table="posts" , referent_table="users" , local_cols=["owner_id"] , remote_cols=["id"] , ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk" , table_name="posts")
    op.drop_column("posts" , "owner_id")
    pass

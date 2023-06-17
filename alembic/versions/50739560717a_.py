"""empty message

Revision ID: 50739560717a
Revises: 261fef2ae4f4
Create Date: 2023-06-13 23:54:19.448017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "50739560717a"
down_revision = "261fef2ae4f4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        None, "residence", "resident", ["resident_id"], ["id"], use_alter=True
    )
    op.add_column("visit", sa.Column("user_id", sa.UUID(), nullable=True))
    op.create_foreign_key(None, "visit", "user", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "visit", type_="foreignkey")
    op.drop_column("visit", "user_id")
    op.drop_constraint(None, "residence", type_="foreignkey")
    # ### end Alembic commands ###

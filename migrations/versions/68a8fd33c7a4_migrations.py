"""migrations

Revision ID: 68a8fd33c7a4
Revises:
Create Date: 2023-07-16 13:41:19.056308

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "68a8fd33c7a4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "guard",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "qr",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("code", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "residence",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("information", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "resident",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "visitor",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "residents_residences",
        sa.Column("resident_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("residence_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["residence_id"],
            ["residence.id"],
        ),
        sa.ForeignKeyConstraint(
            ["resident_id"],
            ["resident.id"],
        ),
    )
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "role",
            postgresql.ENUM("RESIDENT", "GUARD", "ADMIN", name="role"),
            nullable=False,
        ),
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("resident_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("guard_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["guard_id"], ["guard.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["resident_id"], ["resident.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "visit",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column(
            "state",
            postgresql.ENUM(
                "PENDING", "REGISTERED", "CANCELLED", "EXPIRED", name="visitstate"
            ),
            nullable=False,
        ),
        sa.Column("additional_info", sa.JSON(), nullable=True),
        sa.Column("qr_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("visitor_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("guard_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("resident_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["guard_id"], ["guard.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["qr_id"], ["qr.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["resident_id"], ["resident.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["visitor_id"], ["visitor.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("visit")
    op.drop_table("user")
    op.drop_table("residents_residences")
    op.drop_table("visitor")
    op.drop_table("resident")
    op.drop_table("residence")
    op.drop_table("qr")
    op.drop_table("guard")
    # ### end Alembic commands ###
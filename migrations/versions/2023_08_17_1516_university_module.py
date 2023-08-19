"""university_module

Revision ID: c747af1a40d1
Revises: 7f03ada45945
Create Date: 2023-08-17 15:16:51.637262

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c747af1a40d1"
down_revision = "7f03ada45945"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "university",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("address", sa.JSON(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("reg_date", sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "university_tour",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("university_id", sa.Integer(), nullable=False),
        sa.Column("tour_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tour_id"],
            ["tour.id"],
        ),
        sa.ForeignKeyConstraint(
            ["university_id"],
            ["university.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "university_event",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("university_id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["event.id"],
        ),
        sa.ForeignKeyConstraint(
            ["university_id"],
            ["university.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("university_event")
    op.drop_table("university_tour")
    op.drop_table("university")
    # ### end Alembic commands ###

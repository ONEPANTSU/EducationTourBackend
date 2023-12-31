"""tour_address

Revision ID: 7f03ada45945
Revises: 0343741d8967
Create Date: 2023-08-15 18:42:14.409061

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7f03ada45945"
down_revision = "0343741d8967"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("tour", sa.Column("address", sa.JSON(), nullable=True))
    op.drop_column("tour", "city")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tour", sa.Column("city", sa.VARCHAR(), autoincrement=False, nullable=False)
    )
    op.drop_column("tour", "address")
    # ### end Alembic commands ###

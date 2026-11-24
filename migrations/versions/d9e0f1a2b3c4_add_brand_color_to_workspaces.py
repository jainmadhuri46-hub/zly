from alembic import op
import sqlalchemy as sa

revision = "d9e0f1a2b3c4"
down_revision = "c8d9e0f1a2b3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "workspaces",
        sa.Column("brand_color", sa.String(length=7), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("workspaces", "brand_color")

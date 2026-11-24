
"""Add is_superuser column to users table."""

from alembic import op
import sqlalchemy as sa


revision = "b7c9d2e4f610"
down_revision = "39664acc0069"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "is_superuser",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.alter_column(
        "users",
        "is_superuser",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("users", "is_superuser")

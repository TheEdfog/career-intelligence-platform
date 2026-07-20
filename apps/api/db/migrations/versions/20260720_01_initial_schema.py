"""Create the initial application schema.

Revision ID: 20260720_01
Revises:
"""

from alembic import op

from apps.api.db import models  # noqa: F401
from apps.api.db.database import Base

revision = "20260720_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind(), checkfirst=False)


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind(), checkfirst=False)

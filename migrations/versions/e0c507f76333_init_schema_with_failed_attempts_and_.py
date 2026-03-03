"""init schema with failed_attempts and locked_until

Revision ID: e0c507f76333
Revises:
Create Date: 2026-02-23 14:44:17.964471
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e0c507f76333'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ✅ PostgreSQL-safe: solo crea columnas si NO existen

    op.execute("""
        ALTER TABLE usuarios
        ADD COLUMN IF NOT EXISTS failed_attempts INTEGER NOT NULL DEFAULT 0;
    """)

    op.execute("""
        ALTER TABLE usuarios
        ADD COLUMN IF NOT EXISTS locked_until TIMESTAMP;
    """)


def downgrade():
    # 🔙 reversión segura

    op.execute("""
        ALTER TABLE usuarios
        DROP COLUMN IF EXISTS locked_until;
    """)

    op.execute("""
        ALTER TABLE usuarios
        DROP COLUMN IF EXISTS failed_attempts;
    """)
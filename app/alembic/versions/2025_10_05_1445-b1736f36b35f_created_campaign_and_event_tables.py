"""created Campaign and Event tables

Revision ID: b1736f36b35f
Revises:
Create Date: 2025-10-05 14:45:36.216517

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1736f36b35f"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "campaigns",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_campaigns")),
        sa.UniqueConstraint("name", name=op.f("uq_campaigns_name")),
    )
    op.create_table(
        "events",
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("message_id", sa.Integer(), nullable=False),
        sa.Column(
            "status", sa.Enum("PENDING", "COMPLETED", name="statusenum"), nullable=False
        ),
        sa.Column("campaign_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["campaign_id"],
            ["campaigns.id"],
            name=op.f("fk_events_campaign_id_campaigns"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_events")),
        sa.UniqueConstraint(
            "campaign_id", "chat_id", "message_id", name=op.f("uq_events_campaign_id")
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("events")
    op.drop_table("campaigns")

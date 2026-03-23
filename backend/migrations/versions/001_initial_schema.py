"""Initial schema

Revision ID: 001
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None

def upgrade():
    # ── users ──────────────────────────────────────────────
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('NOW()')),
    )

    # ── sources ────────────────────────────────────────────
    op.create_table('sources',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('url', sa.Text, nullable=False, unique=True),
        sa.Column('type', sa.String(50), nullable=False),  # rss | api | scrape
        sa.Column('category', sa.String(100)),              # llm | robotics | cv …
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('last_fetched_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('NOW()')),
    )

    # ── news_items ─────────────────────────────────────────
    op.create_table('news_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('source_id', sa.Integer, sa.ForeignKey('sources.id'), nullable=False),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('url', sa.Text, nullable=False, unique=True),
        sa.Column('content', sa.Text),
        sa.Column('summary', sa.Text),             # AI-generated
        sa.Column('linkedin_caption', sa.Text),    # AI-generated
        sa.Column('email_caption', sa.Text),       # AI-generated
        sa.Column('tags', postgresql.ARRAY(sa.Text)),
        sa.Column('image_url', sa.Text),
        sa.Column('author', sa.String(255)),
        sa.Column('published_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('url_hash', sa.String(64), nullable=False, unique=True),  # SHA256
        sa.Column('embedding', postgresql.ARRAY(sa.Float)),  # for semantic dedup
        sa.Column('ai_processed', sa.Boolean, default=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('NOW()')),
    )
    op.create_index('ix_news_items_published_at', 'news_items', ['published_at'])
    op.create_index('ix_news_items_source_id', 'news_items', ['source_id'])
    op.create_index('ix_news_items_url_hash', 'news_items', ['url_hash'])

    # ── favorites ──────────────────────────────────────────
    op.create_table('favorites',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id'), nullable=False),
        sa.Column('news_item_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('news_items.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('NOW()')),
        sa.UniqueConstraint('user_id', 'news_item_id', name='uq_user_news_favorite'),
    )

    # ── broadcast_logs ─────────────────────────────────────
    op.create_table('broadcast_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id')),
        sa.Column('news_item_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('news_items.id')),
        sa.Column('channel', sa.String(50), nullable=False),  # email | linkedin | whatsapp
        sa.Column('status', sa.String(50), default='sent'),   # sent | failed | queued
        sa.Column('payload', postgresql.JSONB),
        sa.Column('sent_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('NOW()')),
    )


def downgrade():
    op.drop_table('broadcast_logs')
    op.drop_table('favorites')
    op.drop_table('news_items')
    op.drop_table('sources')
    op.drop_table('users')
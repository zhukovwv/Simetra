"""Prevent removal of PostGIS extension

Revision ID: ca02d1d78445
Revises: 
Create Date: 2024-03-27 18:29:27.633929

"""
from typing import Sequence, Union

import geoalchemy2
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ca02d1d78445'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.create_table('GPS',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('location',
                              geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT',
                                                         name='geometry'), nullable=True),
                    sa.Column('speed', sa.Integer(), nullable=True),
                    sa.Column('gps_time', sa.DateTime(), nullable=True),
                    sa.Column('vehicle_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('GPS')

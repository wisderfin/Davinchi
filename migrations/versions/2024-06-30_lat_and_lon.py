"""lat and lon

Revision ID: b6ce4ec0d33e
Revises: 48555a36a959
Create Date: 2024-06-30 11:15:42.288231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text
import requests


# revision identifiers, used by Alembic.
revision: str = 'b6ce4ec0d33e'
down_revision: Union[str, None] = '48555a36a959'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Добавляем новые столбцы
    op.add_column('users', sa.Column('lat', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('users', sa.Column('lon', sa.Float(), nullable=True, server_default='0.0'))

    # Обновляем существующие записи с координатами на основе location
    connection = op.get_bind()
    locations = connection.execute(text("SELECT id, location FROM users"))

    for user in locations:
        id, location = user
       

        try:
            response = requests.get(f"https://nominatim.openstreetmap.org/search?q={location}&format=json")
            data = response.json()
            if data:
                lat = data[0]['lat']
                lon = data[0]['lon']
            else:
                lat = 0.0
                lon = 0.0  # Значения по умолчанию, если координаты не найдены
        except requests.RequestException as e:
            lat = 0.0
            lon = 0.0  # Значения по умолчанию при ошибке запроса

        # Обновляем координаты в таблице
        connection.execute(
            text("UPDATE users SET lat = :lat, lon = :lon WHERE id = :id"),
            {'lat': lat, 'lon': lon, 'id': id}
        )

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'lon')
    op.drop_column('users', 'lat')
    # ### end Alembic commands ###

from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
contact = Table('contact', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('date_created', DATETIME),
    Column('last_edited', DATETIME),
    Column('first_name', VARCHAR(length=64)),
    Column('last_name', VARCHAR(length=64)),
    Column('middle_name', VARCHAR(length=64)),
    Column('email', VARCHAR(length=64)),
    Column('phone', VARCHAR(length=64)),
    Column('street_address_1', VARCHAR(length=64)),
    Column('street_address_2', VARCHAR(length=64)),
    Column('city', VARCHAR(length=64)),
    Column('state', VARCHAR(length=64)),
    Column('zip_code', VARCHAR(length=64)),
    Column('company', VARCHAR(length=64)),
    Column('position', VARCHAR(length=64)),
    Column('tags', VARCHAR(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['contact'].columns['last_edited'].drop()
    pre_meta.tables['contact'].columns['tags'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['contact'].columns['last_edited'].create()
    pre_meta.tables['contact'].columns['tags'].create()

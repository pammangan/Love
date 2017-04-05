from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
contact = Table('contact', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date_created', DateTime),
    Column('last_edited', DateTime),
    Column('first_name', String(length=64)),
    Column('last_name', String(length=64)),
    Column('middle_name', String(length=64)),
    Column('email', String(length=64)),
    Column('phone', String(length=64)),
    Column('street_address_1', String(length=64)),
    Column('street_address_2', String(length=64)),
    Column('city', String(length=64)),
    Column('state', String(length=64)),
    Column('zip_code', String(length=64)),
    Column('company', String(length=64)),
    Column('position', String(length=64)),
    Column('tags', String(length=64)),
)

note = Table('note', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=140)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('contact_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['contact'].create()
    post_meta.tables['note'].columns['contact_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['contact'].drop()
    post_meta.tables['note'].columns['contact_id'].drop()

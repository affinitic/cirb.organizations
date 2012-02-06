import sqlalchemy.types
import sqlalchemy.schema
from zope.interface import implements
from cirb.organizations import ORMBase

class Organization(ORMBase):

    __tablename__="organization"

    organizationId = sqlalchemy.schema.Column(
            sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
            )

    organizationName = sqlalchemy.schema.Column(
            sqlalchemy.types.String(255),
            nullable=False,
            )



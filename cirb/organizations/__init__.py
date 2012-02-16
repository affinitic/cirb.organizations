# -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory

organizationsMessageFactory = MessageFactory('cirb.organizations')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

from sqlalchemy.ext import declarative
ORMBase = declarative.declarative_base()

# -*- coding: utf-8 -*-
from sqlalchemy.ext import declarative
from zope.i18nmessageid import MessageFactory
#from Acquisition import Implicit
organizationsMessageFactory = MessageFactory('cirb.organizations')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


from ExtensionClass import ExtensionClass
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.ext.declarative import _as_declarative, _undefer_column_name, _deferred_relationship, Column, MapperProperty
type = ExtensionClass


class DeclarativeMetaExtensionClass(ExtensionClass):
    """Combination fo ExtensionClass and DeclarativeMeta to prevent type errors

    Example usage:
        >>> from sqlalchemy.ext.declarative import declarative_base
        >>> from collective.tin.declarative import DeclarativeMetaExtensionClass
        >>> Base = declarative_base(metaclass=DeclarativeMetaExtensionClass)
    """
    # cut and paste from sqlalchemy.ext.declarative.DeclarativeMeta @ r5148
    def __init__(cls, classname, bases, dict_):
        if '_decl_class_registry' in cls.__dict__:
            return type.__init__(cls, classname, bases, dict_)
        else:
            _as_declarative(cls, classname, cls.__dict__)
        return type.__init__(cls, classname, bases, dict_)

    def __setattr__(cls, key, value):
        if '__mapper__' in cls.__dict__:
            if isinstance(value, Column):
                _undefer_column_name(key, value)
                cls.__table__.append_column(value)
                cls.__mapper__.add_property(key, value)
            elif isinstance(value, ColumnProperty):
                for col in value.columns:
                    if isinstance(col, Column) and col.table is None:
                        _undefer_column_name(key, col)
                        cls.__table__.append_column(col)
                cls.__mapper__.add_property(key, value)
            elif isinstance(value, MapperProperty):
                cls.__mapper__.add_property(
                                        key,
                                        _deferred_relationship(cls, value)
                                )
            else:
                type.__setattr__(cls, key, value)
        else:
            type.__setattr__(cls, key, value)


#ORMBase = declarative.declarative_base(metaclass=DeclarativeMetaExtensionClass)
ORMBase = declarative.declarative_base()

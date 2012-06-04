from sqlalchemy import (Column, Integer, ForeignKey, String, Sequence,
        DateTime, func, LargeBinary, and_, Boolean)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import AbstractConcreteBase
from z3c.saconfig import Session
from zope.interface import implements
from cirb.organizations import ORMBase
from cirb.organizations.interfaces import IOrganization


class Association(ORMBase):
    __tablename__ = 'association'
    canonical_id = Column(Integer,
                          ForeignKey('organization.organization_id'),
                          primary_key=True)
    translated_id = Column(Integer,
                           ForeignKey('organization.organization_id'),
                           primary_key=True)
    association_type = Column(String(255),
                              Sequence('association_seq'),
                              primary_key=True)


class Organization(ORMBase):
    __tablename__ = 'organization'
    implements(IOrganization)
    # Sequence required by oracle
    organization_id = Column(Integer,
                             Sequence('organization_seq'),
                             primary_key=True, autoincrement=True)
    create_date = Column(DateTime, default=func.now())
    name = Column(String(255), nullable=False,)
    status = Column(String(255))
    status_other = Column(String(255))
    address_id = Column(Integer(), ForeignKey('address.address_id'))
    # TODO test blob file :
    logo = Column(LargeBinary)
    picture = Column(LargeBinary)
    website = Column(String(255))
    language = Column(String(2))
    objectif = Column(String(1024))
    comments = Column(String(1024))

    #used to geolocalisation
    x = Column(String(255))
    y = Column(String(255))

    address = relationship('Address', backref=backref('organization',
                                                      uselist=False, cascade="all, delete-orphan"))
    category = relationship('Category', uselist=False,
                            backref='organization', cascade="all, delete-orphan")
    person_incharge = relationship('InCharge', uselist=False,
                                   backref='organization',
                                   cascade="all, delete-orphan")
    person_contact = relationship('Contact', uselist=False,
                                  backref='organization',
                                  cascade="all, delete-orphan")
    translated_organization = relationship(Association,
                                        primaryjoin=organization_id == Association.canonical_id,
                                        secondaryjoin=and_(organization_id == Association.translated_id, Association.association_type == "lang"),
                                        secondary="association")

    def get_translation(self):
        session = Session()
        trans_orga = session.query(Association).filter(Association.canonical_id == self.organization_id).scalar()
        attr = "translated_id"
        if not trans_orga:
            trans_orga = session.query(Association).filter(Association.translated_id == self.organization_id).scalar()
            attr = "canonical_id"
        if not trans_orga:
            return False

        return session.query(Organization).get(getattr(trans_orga, attr))


class Address(ORMBase):
    __tablename__ = 'address'
    address_id = Column(Integer, Sequence('address_seq'), primary_key=True, autoincrement=True)
    street = Column(String(255))
    num = Column(String(10))
    post_code = Column(String(10))
    municipality = Column(String(255))


class Category(ORMBase):
    __tablename__ = 'category'
    category_id = Column(Integer, Sequence('category_seq'), primary_key=True, autoincrement=True)
    welcome = Column(Boolean, default=False)
    language_training = Column(Boolean, default=False)
    plastic_art = Column(Boolean, default=False)
    scenic_art = Column(Boolean, default=False)
    social_cohesion = Column(Boolean, default=False)
    legal_advice = Column(Boolean, default=False)
    culture = Column(Boolean, default=False)
    danse = Column(Boolean, default=False)
    sustainable_development = Column(Boolean, default=False)
    employment = Column(Boolean, default=False)
    childhood = Column(Boolean, default=False)
    education = Column(Boolean, default=False)
    envrironment = Column(Boolean, default=False)
    body_language = Column(Boolean, default=False)
    familly = Column(Boolean, default=False)
    training = Column(Boolean, default=False)
    handicap = Column(Boolean, default=False)
    information = Column(Boolean, default=False)
    it = Column(Boolean, default=False)
    youth = Column(Boolean, default=False)
    accomodation = Column(Boolean, default=False)
    music = Column(Boolean, default=False)
    social_restaurant = Column(Boolean, default=False)
    mental_health = Column(Boolean, default=False)
    health = Column(Boolean, default=False)
    solidarity = Column(Boolean, default=False)
    tutoring = Column(Boolean, default=False)
    sport = Column(Boolean, default=False)
    third_age = Column(Boolean, default=False)
    other = Column(String(255))
    organization_id = Column(Integer, ForeignKey('organization.organization_id'))


class Person(AbstractConcreteBase, ORMBase):
    title = Column(String(255))
    first_name = Column(String(255))
    second_name = Column(String(255))
    function = Column(String(255))


class InCharge(Person):
    __tablename__ = 'incharge'
    __mapper_args__ = {'polymorphic_identity': 'incharge', 'concrete': True}
    person_id = Column(Integer, Sequence('incharge_seq'), primary_key=True)
    organization_id = Column(Integer, ForeignKey('organization.organization_id'))


class Contact(Person):
    __tablename__ = 'contact'
    __mapper_args__ = {'polymorphic_identity': 'contact',
                       'concrete': True}
    person_id = Column(Integer, Sequence('contact_seq'), primary_key=True)
    phone = Column(String(255))
    fax = Column(String(255))
    email = Column(String(255))
    organization_id = Column(Integer, ForeignKey('organization.organization_id'))
    address_id = Column(Integer(), ForeignKey('address.address_id'))
    address = relationship('Address', backref=backref('contact', uselist=False))

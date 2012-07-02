# -*- coding: utf-8 -*-
import re
import zope.interface
from zope.interface import Interface
from zope import schema
from zope.schema import vocabulary
from plone.namedfile import field

from cirb.organizations import organizationsMessageFactory as _
from z3c.form import interfaces


class IOrganizationsLayer(Interface):
    """A layer specific for this add-on product."""


class ISearch(IOrganizationsLayer):
    search = schema.TextLine(title=_(u'Search'), required=False)


class Terms(vocabulary.SimpleVocabulary):
    zope.interface.implements(interfaces.ITerms)
    def getValue(self, token):
        return self.getTermByToken(token).value

STATUS = Terms([
    Terms.createTerm('asbl', 'asbl', _(u'ASBL')),
    Terms.createTerm('sprl', 'sprl', _(u'SPRL')),
    Terms.createTerm('pouvoirpublique', 'pouvoirpublique', _(u'Pouvoir Publique')),
    Terms.createTerm('other', 'autres', _(u'Autres')),
    ])

LANG = Terms([
    Terms.createTerm('fr', 'fr', _(u'Français')),
    Terms.createTerm('nl', 'nl', _(u'Néerlandais')),
    ])


class IOrganizations(Interface):
    """
    Organizations view interface
    """
    name = schema.TextLine(title=_(u"Organization name"), max_length=255)
    # TODO 
    logo = field.NamedImage(title=_(u"Logo"), required=False)
    picture = field.NamedImage(title=_(u"Picture"), required=False)

    website = schema.TextLine(title=_(u"Website"), required=False, max_length=255)    
    language = schema.Choice(title=_(u"Language"), required=True, vocabulary=LANG) 

    activite_language_fr = schema.Bool(title=_(u"Activité en francais"))
    activite_language_nl = schema.Bool(title=_(u"Activité en neerlandais"))
    activite_language_other = schema.Bool(title=_(u"Activité dans une autre langue"))

    status = schema.Choice(title=_(u"Status"), required=False, vocabulary=STATUS) 
    status_other = schema.TextLine(title=_(u"Other status"), required=False, max_length=255) 
    # auto generate field, it could be hidden for user :
    x = schema.TextLine(title=u"x", required=True)
    y = schema.TextLine(title=u"y", required=True)


class IAddress(Interface):
    street = schema.TextLine(title=_(u"Street"), max_length=255)
    num = schema.TextLine(title=_(u"Number"), max_length=10)
    post_code = schema.TextLine(title=_(u"Post Code"), max_length=10)
    municipality = schema.TextLine(title=_(u"Municipality"), max_length=255)


class ICategory(Interface):
    welcome = schema.Bool(title=_(u"welcome"))
    bibliotheque = schema.Bool(title=_(u"bibliotheque"))
    language_training = schema.Bool(title=_(u"language_training"))
    plastic_art = schema.Bool(title=_(u"plastic_art"))
    scenic_art = schema.Bool(title=_(u"scenic_art"))
    social_cohesion = schema.Bool(title=_(u"social_cohesion"))
    legal_advice = schema.Bool(title=_(u"legal_advice"))
    culture = schema.Bool(title=_(u"culture"))
    danse = schema.Bool(title=_(u"danse"))
    sustainable_development = schema.Bool(title=_(u"sustainable_development"))
    employment = schema.Bool(title=_(u"employment"))
    childhood = schema.Bool(title=_(u"childhood"))
    education = schema.Bool(title=_(u"education"))
    envrironment = schema.Bool(title=_(u"envrironment"))
    body_language = schema.Bool(title=_(u"body_language"))
    familly = schema.Bool(title=_(u"familly"))
    training = schema.Bool(title=_(u"training"))
    handicap = schema.Bool(title=_(u"handicap"))
    information = schema.Bool(title=_(u"information"))
    it = schema.Bool(title=_(u"it"))
    youth = schema.Bool(title=_(u"youth"))
    accomodation = schema.Bool(title=_(u"accomodation"))
    music = schema.Bool(title=_(u"music"))
    social_restaurant = schema.Bool(title=_(u"social_restaurant"))
    mental_health = schema.Bool(title=_(u"mental_health"))
    health = schema.Bool(title=_(u"health"))
    solidarity = schema.Bool(title=_(u"solidarity"))
    tutoring = schema.Bool(title=_(u"tutoring"))
    sport = schema.Bool(title=_(u"sport"))
    third_age = schema.Bool(title=_(u"third_age"))
    other = schema.TextLine(title=_(u"other"), required=False)


class IInCharge(Interface):
    title = schema.TextLine(title=_(u"title"), required=False, max_length=255)
    first_name = schema.TextLine(title=_(u"first_name"), max_length=255)
    second_name = schema.TextLine(title=_(u"second_name"), max_length=255)
    function = schema.TextLine(title=_(u"function"), required=False, max_length=255)


class IContact(Interface):
    title = schema.TextLine(title=_(u"title"), required=False, max_length=255)
    first_name = schema.TextLine(title=_(u"first_name"), max_length=255)
    second_name = schema.TextLine(title=_(u"second_name"), max_length=255)
    function = schema.TextLine(title=_(u"function"), required=False)
    phone = schema.TextLine(title=_(u"phone"), max_length=255)
    fax = schema.TextLine(title=_(u"fax"), max_length=255, required=False)
    email = schema.TextLine(title=_(u"email"), 
                        max_length=255, 
                        constraint=re.compile('^[_.0-9a-z-]+@([0-9a-z][0-9a-z-]+.)+[a-z]{2,6}$', re.IGNORECASE).match)
    # add address 


class IAdditionalInformation(Interface):
    objectif = schema.Text(title=_(u"Objectif"), required=False, max_length=2048) 
    comments = schema.Text(title=_(u"Comments"), required=False, max_length=1024)

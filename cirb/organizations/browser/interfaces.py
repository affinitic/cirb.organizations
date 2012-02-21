from zope.interface import Interface
from zope import schema

from cirb.organizations import organizationsMessageFactory as _
import zope.interface

class IOrganizationsLayer(Interface):
        """A layer specific for this add-on product."""

class IOrganizations(Interface):
    """
    Organizations view interface
    """
    name = schema.TextLine(title=_(u"OrganizationName"))
    status = schema.TextLine(title=_(u"Status")) 
    # TODO 
    logo = schema.Bytes(title=_(u"Logo"), required=False)
    picture = schema.Bytes(title=_(u"Picture"), required=False)

    website = schema.TextLine(title=_(u"Website"), required=False)    
    status = schema.TextLine(title=_(u"Language"), required=False) 
    # auto generate field, it could be hidden for user :
    x = schema.TextLine(title=u"x")
    y = schema.TextLine(title=u"y")

class IAddress(Interface):
    street = schema.TextLine(title=_(u"Street"))
    num = schema.TextLine(title=_(u"Number"))
    post_code = schema.TextLine(title=_(u"Post Code"))
    municipality = schema.TextLine(title=_(u"Municipality"))

class ICategory(Interface):
    welcome = schema.Bool(title=_(u"welcome"))
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
    title = schema.TextLine(title=_(u"title"), required=False)
    first_name = schema.TextLine(title=_(u"first_name"))
    second_name = schema.TextLine(title=_(u"second_name"))
    function = schema.TextLine(title=_(u"function"), required=False)

class IContact(Interface):
    title = schema.TextLine(title=_(u"title"), required=False)
    first_name = schema.TextLine(title=_(u"first_name"))
    second_name = schema.TextLine(title=_(u"second_name"))
    function = schema.TextLine(title=_(u"function"), required=False)
    phone = schema.TextLine(title=_(u"phone"))
    fax = schema.TextLine(title=_(u"fax"))
    email = schema.TextLine(title=_(u"email"))
    # add address 



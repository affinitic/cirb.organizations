from zope import schema
from zope.interface import implements, Interface
from zope.component import provideAdapter
from zope.publisher.interfaces.browser import IBrowserRequest

from z3c.saconfig import Session
from z3c.form import form, field, button
from plone.app.z3cform.layout import wrap_form
from collective.z3cform.wizard import wizard

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile

from cirb.organizations import organizationsMessageFactory as _
from cirb.organizations.content.organization import Organization

from zope.schema.vocabulary import SimpleVocabulary

class IOrganizations(Interface):
    """
    Organizations view interface
    """
    name = schema.TextLine(title=_(u"OrganizationName"))
    status = schema.TextLine(title=_(u"Status")) 
    # TODO 
    logo = schema.Bytes(title=_(u"Logo"), required=False)
    picture = schema.Bytes(title=_(u"Picture"), required=False)

    website = schema.TextLine(title=_(u"Website"))    
    status = schema.TextLine(title=_(u"Language")) 
    # auto generate field :
    x = schema.TextLine()
    y = schema.TextLine()

class IAddress(Interface):
    street = schema.TextLine(title=_(u"Street"))
    num = schema.TextLine(title=_(u"Number"))
    post_code = schema.TextLine(title=_(u"Post Code"))
    municipality = schema.TextLine(title=_(u"Municipality"))

class ICategory(Interface):
    welcom = schema.Bool()

class IInCharge(Interface):
    title = schema.TextLine(title=_(u"title"))

class IContact(Interface):
    phone = schema.TextLine(title=_(u"phone"))


class OrganizationsForm(wizard.Step):
    prefix = "orga"
    fields = field.Fields(IOrganizations)

    def load(self, context):
        data = self.getContent()
        name = data.get('name') # ... or do stuff
        print name
        #self.test = Session.query(Organization).filter(Organization.name.like("%{0}%".format(name))).all()
        #self.status = "Thank you very much!"

    def apply(self, context):
        data = self.getContent()
        print 'Name from orga: {0}'.format(data.get('name'))

class AddressForm(wizard.Step):
    prefix = "addr"
    field = field.Fields(IAddress)

    def load(self, context):                                                                 
        data = self.getContent()
    
    def apply(self, context):
        data = self.getContent()

class Wizard(wizard.Wizard):
    label = _(u"Organization")
    steps = OrganizationsForm, AddressForm 

WizardView = wrap_form(Wizard)


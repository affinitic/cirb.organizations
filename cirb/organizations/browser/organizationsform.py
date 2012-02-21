from zope import schema
from zope.interface import implements, Interface
from zope.component import provideAdapter
from zope.publisher.interfaces.browser import IBrowserRequest

from z3c.saconfig import Session
import transaction
from z3c.form import form, field, button
from plone.app.z3cform.layout import wrap_form
from collective.z3cform.wizard import wizard
from plone.z3cform.fieldsets import group

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile

from cirb.organizations import organizationsMessageFactory as _
from cirb.organizations.content.organization import *
from cirb.organizations.browser.interfaces import *

from zope.schema.vocabulary import SimpleVocabulary

class AddressGroup(group.Group):
    prefix = "addr"
    label = _(u"Address")
    fields = field.Fields(IAddress)

    def load(self, context): 
        data = self.getContent()
    
    def apply(self, context):
        data = self.getContent()


class OrganizationsStep(wizard.GroupStep):
    prefix = "orga"
    label = _(u"Organization Information")
    fields = field.Fields(IOrganizations)
    groups = [AddressGroup]

    def load(self, context):
        data = self.getContent()
        name = data.get('name') # ... or do stuff
        print name
        #self.test = Session.query(Organization).filter(Organization.name.like("%{0}%".format(name))).all()
        #self.status = "Thank you very much!"

    def apply(self, context):
        data = self.getContent()
        print 'Name from orga: {0}'.format(data.get('name'))


class CategoryStep(wizard.Step):
    prefix = "cat"
    label = _(u"Category")
    fields = field.Fields(ICategory)
    
    def load(self, context): 
        data = self.getContent()

    def apply(self, context):
        data = self.getContent()


class InChargeStep(wizard.Step):
    prefix = "incharge"
    label = _(u"Person in charge")
    fields = field.Fields(IInCharge)

    def load(self, context):
        data = self.getContent()

    def apply(self, context):
        data = self.getContent()


class ContactStep(wizard.GroupStep):
    prefix = "contact"
    label = _(u"Person for contact")
    fields = field.Fields(IContact)
    groups = [AddressGroup]

    def load(self, context):                                              
        data = self.getContent()

    def apply(self, context):
        data = self.getContent()


class Wizard(wizard.Wizard):
    label = _(u"Organization")
    steps = OrganizationsStep, CategoryStep, InChargeStep, ContactStep

    def finish(self):
        data = self.session
        sqlalsession = Session()
        orgastep = data.get('orga')
        catstep = data.get('cat')
        inchargestep = data.get('incharge')
        contactstep = data.get('contact')
        
        cat = Category()
        for key, value in catstep.items():
            if key in Category.__dict__.keys():
                setattr(cat, key, value)

        incharge = InCharge()
        for key, value in inchargestep.items():
            if key in InCharge.__dict__.keys():
                setattr(incharge, key, value)

        contact_address = Address()
        contact = Contact()
        for key, value in contactstep.items():
            if key in Contact.__dict__.keys():
                setattr(contact, key, value)
            if key in Address.__dict__.keys():
                setattr(contact_address, key, value)
        setattr(contact, 'address', contact_address)
                
        orga_address = Address()
        orga = Organization()
        for key, value in orgastep.items():
            if key in Organization.__dict__.keys():
                setattr(orga, key, value)
            if key in Address.__dict__.keys():
                setattr(orga_address, key, value)
        setattr(orga, 'address', orga_address)
        setattr(orga, 'person_incharge', incharge)
        setattr(orga, 'person_contact', contact)
        setattr(orga, 'category', cat)
        sqlalsession.add(orga)
        transaction.commit()



WizardView = wrap_form(Wizard)


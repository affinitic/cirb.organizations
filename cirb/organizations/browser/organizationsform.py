# -*- coding: utf-8 -*-
from z3c.form import field
from z3c.saconfig import Session
import transaction
from plone.app.z3cform.layout import wrap_form
from collective.z3cform.wizard import wizard
from plone.z3cform.fieldsets import group

from cirb.organizations import organizationsMessageFactory as _
from cirb.organizations.content.organization import Organization, Category, Address, Contact, InCharge
from cirb.organizations.browser.interfaces import IAddress, ICategory, IContact, IInCharge, IOrganizations


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
        self.wizard.session = check_edit(self.wizard.session, self.request.form)
        edit = self.wizard.session.get('edit')
        if edit:
            orga = Session.query(Organization).get(edit)
            data = init_form(orga)
            self.request.SESSION[self.wizard.sessionKey] = data
            self.request.SESSION[self.wizard.sessionKey]['edit'] = edit
        #self.test = Session.query(Organization).filter(Organization.name.like("%{0}%".format(name))).all()
        #self.status = "Thank you very much!"


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

    def initialize(self):
        print self.onFirstStep
        print self.session
        super(Wizard, self).initialize()
    
    def finish(self):
        data = self.session
        print 'data : {0}'.format(data)
        sqlalsession = Session()
        orgastep = data.get('orga')
        catstep = data.get('cat')
        inchargestep = data.get('incharge')
        contactstep = data.get('contact')
        edition = self.session.get('edit') 
        if edition:
            orga = sqlalsession.query(Organization).get(edition)
            cat = orga.category
            incharge = orga.person_incharge
            contact_address = orga.person_contact.address
            contact = orga.person_contact
            orga_address = orga.address

        else:
            cat = Category()
            incharge = InCharge()
            contact_address = Address()
            contact = Contact()
            orga_address = Address()
            orga = Organization()

        for key, value in catstep.items():
            if key in Category.__dict__.keys():
                setattr(cat, key, value)

        for key, value in inchargestep.items():
            if key in InCharge.__dict__.keys():
                setattr(incharge, key, value)

        for key, value in contactstep.items():
            if key in Contact.__dict__.keys():
                setattr(contact, key, value)
            if key in Address.__dict__.keys():
                setattr(contact_address, key, value)
        setattr(contact, 'address', contact_address)
                
        for key, value in orgastep.items():
            if key in Organization.__dict__.keys():
                setattr(orga, key, value)
            if key in Address.__dict__.keys():
                setattr(orga_address, key, value)
        setattr(orga, 'address', orga_address)
        setattr(orga, 'person_incharge', incharge)
        setattr(orga, 'person_contact', contact)
        setattr(orga, 'category', cat)
        if edition:
            sqlalsession.flush()
        else:
            sqlalsession.add(orga)
        transaction.commit()
        self.request.SESSION.clear()

WizardView = wrap_form(Wizard)

def check_edit(session, form):
    if form.get('edit'):
        session['edit'] = form.get('edit')
    else:
        session['edit'] = 0
    return session

def init_form(orga):
    orga_fields = get_fields_name([OrganizationsStep, AddressGroup])
    cat_fields = get_fields_name([CategoryStep])
    incharge_fields = get_fields_name([InChargeStep])
    contact_fields = get_fields_name([ContactStep, AddressGroup])
    data={}
    tmp={}
    for key in orga_fields:
        if key in orga.__dict__.keys():
            tmp[key] = getattr(orga, key)
        if key in orga.address.__dict__.keys():
            tmp[key] = getattr(orga.address, key)
    data['orga'] = tmp 
    tmp={}
    for key in cat_fields:
        tmp[key] = getattr(orga.category, key)
    data['cat'] = tmp
    tmp={}
    for key in incharge_fields:
        tmp[key] = getattr(orga.person_incharge, key)
    data['incharge'] = tmp 
    tmp={}
    for key in contact_fields:
        if key in orga.person_contact.__dict__.keys():
            tmp[key] = getattr(orga.person_contact, key)
        if key in orga.person_contact.address.__dict__.keys():
            tmp[key] = getattr(orga.person_contact.address, key)
    data['contact'] = tmp 
    return data

def get_fields_name(steps):
    fields_name = []
    for step in steps:
        for key in step.fields.keys():
            fields_name.append(key)
    return fields_name

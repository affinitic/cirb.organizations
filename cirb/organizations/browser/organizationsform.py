# -*- coding: utf-8 -*-
from z3c.form import field
from z3c.saconfig import Session
import transaction
from plone.app.z3cform.layout import FormWrapper
from collective.z3cform.wizard import wizard
from plone.z3cform.fieldsets import group
from plone.namedfile.field import NamedImage
from plone.namedfile import file
#from plone.formwidget.namedfile import NamedFileWidget
from cirb.organizations.traversal import OrganizationWrapper
from cirb.organizations import organizationsMessageFactory as _
from cirb.organizations.content.organization import Organization, Category, Address, Contact, InCharge, AdditionalInformation, Association
from cirb.organizations.browser.interfaces import IAddress, ICategory, IContact, IInCharge, IOrganizations, IAdditionalInformation

from zope.app.pagetemplate import viewpagetemplatefile
import os


class AddressGroup(group.Group):
    prefix = "addr"
    label = _(u"Address")
    fields = field.Fields(IAddress)


class OrganizationsStep(wizard.GroupStep):
    prefix = "orga"
    label = _(u"Organization Information")
    fields = field.Fields(IOrganizations)
    groups = [AddressGroup]
    index = viewpagetemplatefile.ViewPageTemplateFile('templates/orgastep.pt')

    def load(self, context):
        data = self.getContent()
        for field in self.fields:
            if isinstance(self.fields[field].field, NamedImage):
                blob = getattr(context, field, None)
                if blob:
                    data[field] = file.NamedImage(data=blob)
            else:
                data[field] = getattr(context, field, None)
        for group in self.groups:
            for field in group.fields:
                data[field] = getattr(context.address, field, None)

    def apply(self, context):
        data = self.getContent()
        for field in self.fields:
            if isinstance(data[field], file.NamedImage):
                blob = data[field].data
                setattr(self.wizard.session['organization'], field, blob)
            else:
                setattr(self.wizard.session['organization'], field, data[field])
        for group in self.groups:
            for field in group.fields:
                setattr(self.wizard.session['organization'].address, field, data[field])

    def get_gis_service(self):
        gis_url = os.environ.get('GIS_SERVICE')
        if not gis_url:
            gis_url = 'http://service.gis.irisnetlab.be/urbis/'
        return gis_url


class InChargeStep(wizard.Step):
    prefix = "incharge"
    label = _(u"Person in charge")
    fields = field.Fields(IInCharge)

    def load(self, context):
        data = self.getContent()
        for field in self.fields:
            data[field] = getattr(context.person_incharge, field, None)

    def apply(self, context):
        data = self.getContent()
        for field in self.fields:
            setattr(self.wizard.session['organization'].person_incharge, field, data[field])


class ContactStep(wizard.GroupStep):
    prefix = "contact"
    label = _(u"Person for contact")
    fields = field.Fields(IContact)
    groups = [AddressGroup]

    def load(self, context):
        data = self.getContent()
        for field in self.fields:
            data[field] = getattr(context.person_contact, field, None)
        for group in self.groups:
            for field in group.fields:
                data[field] = getattr(context.person_contact.address, field, None)

    def apply(self, context):
        data = self.getContent()
        for field in self.fields:
            setattr(self.wizard.session['organization'].person_contact, field, data[field])
        for group in self.groups:
            for field in group.fields:
                setattr(self.wizard.session['organization'].person_contact.address, field, data[field])


class CategoryStep(wizard.Step):
    prefix = "cat"
    label = _(u"Category")
    fields = field.Fields(ICategory)

    def load(self, context):
        data = self.getContent()
        for field in self.fields:
            data[field] = getattr(context.category, field, None)

    def apply(self, context):
        data = self.getContent()
        for field in self.fields:
            setattr(self.wizard.session['organization'].category, field, data[field])


class AdditionalInformationStep(wizard.Step):
    prefix = "additionalinfo"
    label = _(u"Descritpion and comments")
    fields = field.Fields(IAdditionalInformation)

    def load(self, context):
        data = self.getContent()
        for field in self.fields:
            data[field] = getattr(context.additionalinfo, field, None)

    def apply(self, context):
        data = self.getContent()
        for field in self.fields:
            setattr(self.wizard.session['organization'].additionalinfo, field, data[field])


class Wizard(wizard.Wizard):
    label = _(u"Organization")
    steps = OrganizationsStep, InChargeStep, ContactStep, CategoryStep, AdditionalInformationStep

    def initialize(self):
        if isinstance(self.context, OrganizationWrapper):
            orga = Session().query(Organization).get(self.context.organization_id)
            self.loadSteps(orga)
        else:
            orga = Organization(address=Address(), category=Category(), person_incharge=InCharge(), person_contact=Contact(), additionalinfo=AdditionalInformation())
            orga.person_contact.address = Address()
        self.session['organization'] = orga
        self.session['canonical_id'] = self.request.get('canonical_id')

    def finish(self):
        #super(Wizard, self).finish()
        self.applySteps(self.context)
        sqlalsession = Session()
        sqlalsession.flush()
        organization = self.session['organization']
        canonical_id = self.session['canonical_id']
        if organization.organization_id:
            sqlalsession.merge(organization)
        else:
            sqlalsession.add(organization)
            if canonical_id:
                # flush required for organization.organization_id creation
                sqlalsession.flush()
                assoc = Association(association_type="lang")
                assoc.translated_id = organization.organization_id
                assoc.canonical_id = canonical_id
                sqlalsession.add(assoc)

        transaction.commit()
        self.request.SESSION.clear()

    @property
    def absolute_url(self):
        return self.action
        #return self.context.absolute_url() + '/' + self.__name__

    #def translate_url(self):
    #    from Acquisition import aq_inner
    #    context = aq_inner(self.context)
    #    if context.getLanguage() == 'fr':
    #        view = context.getTranslation('nl')
    #        absolute_url = "{0}/organizations_form?set_language=nl".format(view.absolute_url())
    #    else:
    #        view = context.getTranslation('fr')
    #        absolute_url = "{0}/organizations_form?set_language=fr".format(view.absolute_url())

    #    return absolute_url

class WizardView(FormWrapper):
    form = Wizard

    

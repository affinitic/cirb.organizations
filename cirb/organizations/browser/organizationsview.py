from zope import schema
from zope.interface import implements, Interface
from zope.component import provideAdapter
from zope.publisher.interfaces.browser import IBrowserRequest

from z3c.saconfig import Session
from z3c.form import form, field, button
from plone.app.z3cform.layout import FormWrapper

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile

from cirb.organizations import organizationsMessageFactory as _
from cirb.organizations.content.organization import Organization


class IOrganizations(Interface):
    """
    Organizations view interface
    """
    name = schema.TextLine(title=_(u"OrganizationName"))
    website = schema.TextLine(title=_(u"website"))    


class OrganizationsForm(form.Form):
    fields = field.Fields(IOrganizations)
    ignoreContext = True # don't use context to get widget data

    @button.buttonAndHandler(_(u'Search organization'))
    def handleApply(self, action):
        data, errors = self.extractData()
        name = data.get('name') # ... or do stuff
        self.test = Session.query(Organization).filter(Organization.name.like("%{0}%".format(name))).all()
        print self.test
        self.status = "Thank you very much!"

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page."""


class OrganizationFormWrapper(FormWrapper):
    form = OrganizationsForm
    label = _(u"Add a organization")

    def get_all(self):
        return Session.query(Organization).all()

    def get_search(self):
        import pdb; pdb.set_trace()
        return self.test

    def status(self):
        return self.status

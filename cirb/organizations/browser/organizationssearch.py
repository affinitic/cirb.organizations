from zope import schema
from zope.interface import implements, Interface

from z3c.saconfig import Session
from z3c.form import form, field, button
from plone.app.z3cform.layout import wrap_form
from plone.app.z3cform.layout import FormWrapper

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from cirb.organizations import organizationsMessageFactory as _
from cirb.organizations.content.organization import *
from cirb.organizations.browser.interfaces import *


class ISearch(IOrganizationsLayer):
    search = schema.TextLine(title=_(u'Search'), required=False)

class Search(form.Form):
    label = _(u'Organization search')
    ignoreContext = True
    fields = field.Fields(ISearch)

    template  = ViewPageTemplateFile('templates/search.pt')
    results = []
    def search(self, data):
        session = Session()
        search = data.get('search')
        if not search:
            self.results = session.query(Organization).all()
        else:
            self.results = session.query(Organization).filter(Organization.name.like('%{0}%'.format(search))).all()
        if len(self.results) ==  0:
            self.status = _(u"No organization found.")

    @button.buttonAndHandler(_(u'Search'))
    def handleSubmit(self, action):
        data, errors = self.extractData()
        if not errors:
            self.search(data)

    def get_results(self):
        if len(self.results) ==  0:
            return None    
        return self.results

#SearchView =  wrap_form(Search)

class SearchView(FormWrapper):
    form = Search
from zope.component import provideAdapter
from zope.publisher.interfaces.browser import IBrowserRequest
provideAdapter(adapts=(ISearch, IBrowserRequest), provides=ISearch, factory=SearchView, name="organizations_search")
from z3c.saconfig import Session
from z3c.form import form, field, button
from plone.app.z3cform.layout import FormWrapper
from collective.z3cform.wizard.wizard import WIZARD_SESSION_KEY

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from cirb.organizations import organizationsMessageFactory as _
from cirb.organizations.content.organization import Organization
from cirb.organizations.browser.interfaces import ISearch

import json
import logging

SESSION_SEARCH_IDS = "search_ids"

class Search(form.Form):
    label = _(u'Organization search')
    ignoreContext = True
    fields = field.Fields(ISearch)

    template = ViewPageTemplateFile('templates/search.pt')
    results = []

    def search(self, data):
        session = Session()
        search = data.get('search')
        if not search:
            self.results = session.query(Organization).filter(Organization.language == self.context.Language()).all()
        else:
            self.results = session.query(Organization).filter(Organization.name.like('%{0}%'.format(search))).filter(Organization.language == self.context.Language()).all()

        # add result in a session variable for the GIS Service
        if SESSION_SEARCH_IDS in self.request.SESSION.keys():
            self.request.SESSION.delete(SESSION_SEARCH_IDS)
        self.request.SESSION.set(SESSION_SEARCH_IDS, [orga.organization_id for orga in self.results])

        if len(self.results) == 0:
            self.status = _(u"No organization found.")

    @button.buttonAndHandler(_(u'Search'))
    def handleSubmit(self, action):
        data, errors = self.extractData()
        if not errors:
            self.search(data)

    def get_results(self):
        if len(self.results) == 0:
            return None
        return self.results


class SearchView(FormWrapper):
    form = Search    
    def __call__(self, *args, **kw):
        keys = [k for k in self.request.SESSION.keys() if WIZARD_SESSION_KEY in k]
        for key in keys:
            self.request.SESSION.delete(key)
        return super(SearchView, self).__call__(*args, **kw)

    def get_json(self):
        ids = self.request.SESSION.get(SESSION_SEARCH_IDS)
        self.request.response.setHeader('Content-Type',"application/json")
        return list_to_json(ids)

def list_to_json(ids):
    return json.dumps(ids)
    
 

from zope.component import provideAdapter
from zope.publisher.interfaces.browser import IBrowserRequest
provideAdapter(adapts=(ISearch, IBrowserRequest), provides=ISearch, factory=SearchView, name="organizations_search")

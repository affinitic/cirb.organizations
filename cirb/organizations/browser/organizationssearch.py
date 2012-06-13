from z3c.saconfig import Session
from z3c.form import form, field, button
from plone.app.z3cform.layout import FormWrapper
#from collective.z3cform.wizard.wizard import WIZARD_SESSION_KEY

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from cirb.organizations import organizationsMessageFactory as _
from cirb.organizations.content.organization import Organization, Category
from cirb.organizations.browser.interfaces import ISearch

import json
from sqlalchemy import func 
from plone.namedfile import file
from plone.namedfile.interfaces import IImageScaleTraversable
#import logging

from zope.interface import implements
SESSION_JSON = "search_json"
SESSION_SEARCH = "search_term"


class Search(form.Form):
    implements(IImageScaleTraversable)

    label = _(u'Organization search')
    ignoreContext = True
    fields = field.Fields(ISearch)

    template = ViewPageTemplateFile('templates/search.pt')
    results = []

    def search(self, search):
        session = Session()
        self.results = session.query(Organization).filter(func.lower(Organization.name).like('{0}'.format(search))).filter(Organization.language == self.context.Language()).all()

        # add result in a session variable for the GIS Service
        if 'SESSION' in self.request.keys():
            if SESSION_JSON in self.request.SESSION.keys():
                self.request.SESSION.delete(SESSION_JSON)

            self.request.SESSION.set(SESSION_JSON, [{'orga': {'id':orga.organization_id, 'name':orga.name, 'x': orga.x, 'y':orga.y}} for orga in self.results])
            self.request.SESSION.set(SESSION_SEARCH, search)
    
        if len(self.results) == 0:
            self.status = _(u"No organization found.")

    def get_categories(self):
        categories = [cat for cat in dir(Category) if not cat.startswith("_") and not cat[-3:] == "_id"]
        return categories

    @button.buttonAndHandler(_(u'Search'))
    def handleSubmit(self, action):
        data, errors = self.extractData()
        if not errors:
            input_content = data.get('search')
            if not input_content:
                search_text = "%"
            else:
                search_text = "%{0}%".format(input_content.lower())

            self.search(search_text)
    
    def js(self):
        return """
            $(document).ready(function() {
                $('.letters').click(function () {
                    $('form').submit();
                });
            });
            """

    def get_results(self):
        if len(self.results) == 0:
            return None
        return self.results

    def folder_url(self):
        return self.context.absolute_url()

    def img(self, name, orga_id):
        session = Session()
        orga = session.query(Organization).get(orga_id)
        blob = getattr(orga, name)
        src = ""
        if blob:
            namedimage = file.NamedImage(data=blob) 
            extension = namedimage.contentType.split('/')[-1].lower()
            src = "{0}/org/{1}/@@images/{2}.{3}".format(self.context.absolute_url(), orga.organization_id, name, extension)
        return src

    @button.buttonAndHandler(u'A')
    def handleSubmit(self, action):
        self.search('a%')
    
    @button.buttonAndHandler(u'B')
    def handleSubmit(self, action):
        self.search('b%')
    
    @button.buttonAndHandler(u'C')
    def handleSubmit(self, action):
        self.search('c%')
    
    @button.buttonAndHandler(u'D')
    def handleSubmit(self, action):
        self.search('d%')

    @button.buttonAndHandler(u'E')
    def handleSubmit(self, action):
        self.search('e%')

    @button.buttonAndHandler(u'F')
    def handleSubmit(self, action):
        self.search('f%')

    @button.buttonAndHandler(u'G')
    def handleSubmit(self, action):
        self.search('g%')

    @button.buttonAndHandler(u'H')
    def handleSubmit(self, action):
        self.search('h%')

    @button.buttonAndHandler(u'I')
    def handleSubmit(self, action):
        self.search('i%')

    @button.buttonAndHandler(u'J')
    def handleSubmit(self, action):
        self.search('j%')
    
    @button.buttonAndHandler(u'K')
    def handleSubmit(self, action):
        self.search('k%')

    @button.buttonAndHandler(u'L')
    def handleSubmit(self, action):
        self.search('l%')
    
    @button.buttonAndHandler(u'M')
    def handleSubmit(self, action):
        self.search('m%')

    @button.buttonAndHandler(u'N')
    def handleSubmit(self, action):
        self.search('n%')


class SearchView(FormWrapper):
    form = Search
    
    def __call__(self):
        
        return super(SearchView, self).__call__()

    def json(self):
        ids = self.request.SESSION.get(SESSION_JSON)
        self.request.response.setHeader('Content-Type', "application/json")
        return list_to_json(ids)
    

def list_to_json(ids):
    return json.dumps(ids)

from zope.component import provideAdapter
from zope.publisher.interfaces.browser import IBrowserRequest
provideAdapter(adapts=(ISearch, IBrowserRequest), provides=ISearch, factory=SearchView, name="organizations_search")

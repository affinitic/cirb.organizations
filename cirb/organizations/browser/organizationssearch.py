from z3c.saconfig import Session
from z3c.form import form, field, button
from plone.app.z3cform.layout import FormWrapper

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from cirb.organizations import organizationsMessageFactory as _
from cirb.organizations.content.organization import Organization
from cirb.organizations.browser.interfaces import ISearch


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


from collective.z3cform.wizard.wizard import WIZARD_SESSION_KEY
class SearchView(FormWrapper):
    form = Search    
    #import pdb; pdb.set_trace()
    def __call__(self, *args, **kw):
        self.request.SESSION.clear()
        return super(SearchView, self).__call__(*args, **kw)

from zope.component import provideAdapter
from zope.publisher.interfaces.browser import IBrowserRequest
provideAdapter(adapts=(ISearch, IBrowserRequest), provides=ISearch, factory=SearchView, name="organizations_search")

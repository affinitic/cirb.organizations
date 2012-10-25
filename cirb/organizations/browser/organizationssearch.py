from z3c.saconfig import Session
from z3c.form import form, field, button
from plone.app.z3cform.layout import FormWrapper
#from collective.z3cform.wizard.wizard import WIZARD_SESSION_KEY
from sqlalchemy import or_

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from cirb.organizations import organizationsMessageFactory as _
from cirb.organizations.content.organization import Organization, Category
from cirb.organizations.browser.interfaces import ISearch, IAdvancedSearch

import json
from sqlalchemy import func
from plone.namedfile import file
from plone.namedfile.interfaces import IImageScaleTraversable
#import logging

from zope.interface import implements
SESSION_JSON = "search_json"
SESSION_SEARCH = "search_term"
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


class LetterButton(button.Button):
    pass


class CategoryButton(button.ImageButton):

    def __init__(self, *args, **kwargs):
        super(CategoryButton, self).__init__(*args, **kwargs)

    def update(self):
        super(CategoryButton, self)


def renderCategoryButton(context, name, selected=None):
    if selected:
        render = u'<div class="categorie-inputs">\n<input id="form-buttons-{0}" name="form.buttons.{0}" class="image-widget categorybutton-field selected" src="{1}/++resource++{0}.png" value="{2}" type="image" alt="{2}" title="{2} "/><div class="bottominputcategory">{2}</div>\n</div>\n'.format(name, context.portal_url(), context.translate(name))
    else:
        render = u'<div class="categorie-inputs">\n<input id="form-buttons-{0}" name="form.buttons.{0}" class="image-widget categorybutton-field" src="{1}/++resource++{0}.png" value="{2}" type="image" alt="{2}" title="{2} "/><div class="bottominputcategory">{2}</div></div>\n\n'.format(name, context.portal_url(), context.translate(name))
    return render


class Search(form.Form):
    implements(IImageScaleTraversable)

    label = _(u'Organization search')
    ignoreContext = True
    fields = field.Fields(ISearch)

    cat_search = ''
    template = ViewPageTemplateFile('templates/search.pt')
    results = []

    def __init__(self, context, request):
        super(Search, self).__init__(context, request)
        organisations_serached = request.SESSION.get(SESSION_SEARCH)
        if organisations_serached:
            session = Session()
            self.results = organisations_serached


    def search(self, search):
        session = Session()
        self.results = session.query(Organization).filter(func.lower(Organization.name).like('{0}'.format(search))).filter(Organization.language == self.context.Language()).order_by(Organization.name).all()
        if len(self.results) == 0:
            self.status = _(u"No organization found.")

    def get_categories(self):
        return Category.attributes

    def update(self):
        for letter in ALPHABET:
            letterbutton = LetterButton(letter, unicode(letter))
            self.buttons = button.Buttons(self.buttons, letterbutton)
        self.handlers.addHandler(LetterButton, button.Handler(LetterButton, self.handleLettersButton))
        for cat in self.get_categories():
            categorybutton = CategoryButton(name=str(cat), title=cat,
                                            image=u"{0}.png".format(str(cat)))
            self.buttons = button.Buttons(self.buttons, categorybutton)
        self.handlers.addHandler(CategoryButton, button.Handler(CategoryButton, self.handleCategoriesButton))
        super(Search, self).update()
        for cat in self.get_categories():
            if cat == self.cat_search:
                self.actions[cat].render = renderCategoryButton(self.context, cat, 'selected')
            else:
                self.actions[cat].render = renderCategoryButton(self.context, cat)
    
    def handleLettersButton(self, form, action):
        self.search("{0}%".format(action.value.lower()))

    def handleCategoriesButton(self, form, action):
        session = Session()
        # add selected class
        self.cat_search = action.value
        if action.value == 'enseignement_formation':
            self.results = session.query(Organization).filter(or_(Organization.category.has(getattr(Category, 'tutoring') == True),
                                                   Organization.category.has(getattr(Category, 'training') == True),
                                                   Organization.category.has(getattr(Category, 'education') == True) )).filter(Organization.language == self.context.Language()).all()

        else:
            self.results = session.query(Organization).filter(Organization.category.has(getattr(Category, action.value) == True)).filter(Organization.language == self.context.Language()).all()
        if len(self.results) == 0:
            self.status = _(u"No organization found.")

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

    def get_results(self):
        if not 'SESSION' in self.request.keys():
            return None

        if SESSION_JSON in self.request.SESSION.keys():
            self.request.SESSION.delete(SESSION_JSON)

        if len(self.results) == 0:
            return None

        session = Session()
        json = []
        sa_results = []
        for orga in self.results:
            sa_orga = session.query(Organization).get(orga.organization_id)
            sa_results.append(sa_orga)
            dict_orga = {}
            dict_orga['id'] = sa_orga.organization_id
            dict_orga['name'] = sa_orga.name
            dict_orga['x'] = sa_orga.x
            dict_orga['y'] = sa_orga.y
            dict_orga['street'] = u"{0}, {1}".format(sa_orga.address.num, sa_orga.address.street)
            dict_orga['city'] = u"{0} {1}".format(sa_orga.address.post_code, sa_orga.address.municipality)
            dict_orga['url'] = "{0}/org/{1}/oview".format(self.context.absolute_url(), sa_orga.organization_id)
            dict_orga['icon'] = "{0}/++resource++map_pin.png".format(self.context.portal_url())
            json.append({'orga': dict_orga})

        self.request.SESSION.set(SESSION_JSON, json)
        self.results = sa_results
        return sa_results

    def set_results(self, results):
        self.results = results

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
            src = "{0}/org/{1}/@@images/{2}.{3}".format(
                    self.context.absolute_url(),
                    orga.organization_id,
                    name,
                    extension)
        return src

    def get_advanced_search_url(self):
        suffix = "orga_advanced_search"
        url = "{0}/{1}".format(self.context.absolute_url(), suffix)
        return url


class SearchView(FormWrapper):
    form = Search

    def json(self):
        ids = self.request.SESSION.get(SESSION_JSON)
        self.request.response.setHeader('Content-Type', "application/json")
        return list_to_json(ids)


def list_to_json(ids):
    return json.dumps(ids)


class AdvancedSearch(form.Form):
    implements(IImageScaleTraversable)

    label = _(u'Organization advanced search')
    ignoreContext = True
    fields = field.Fields(IAdvancedSearch)
    template = ViewPageTemplateFile('templates/advanced_search.pt')
    results = []

    @button.buttonAndHandler(_(u'Search'))
    def handleSubmit(self, action):
        data, errors = self.extractData()
        session = Session()
        searched_categories = data.get('categories')
        request = session.query(Organization)
        for categorie in searched_categories:
            request = request.filter(Organization.category.has(getattr(Category, categorie) == True))
        request = request.filter(Organization.language == self.context.Language())
        self.results = request.all()
        if len(self.results) == 0:
            self.status = _(u"No organization found.")
        else: 
            self.request.SESSION.set(SESSION_SEARCH, self.results)
            self.request.response.redirect('organizations_search')

    def get_result(self):
        return self.results


class AdvancedSearchView(FormWrapper):
    form = AdvancedSearch

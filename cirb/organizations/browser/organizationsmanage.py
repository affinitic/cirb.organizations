from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.LinguaPlone.interfaces import ITranslatable

from z3c.saconfig import Session
from cirb.organizations.content.organization import Organization
import transaction
import logging

class ManageView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.session = Session()

    def manage(self):
        results = self.session.query(Organization).filter(Organization.language==self.context.Language()).all()
        return results
 
    def translate_url(self):
        context = aq_inner(self.context)
        if context.getLanguage() == 'fr':
            view = context.getTranslation('nl')
            absolute_url = "{0}/organizations_form?set_language=nl".format(view.absolute_url())
        else:
            view = context.getTranslation('fr')
            absolute_url = "{0}/organizations_form?set_language=fr".format(view.absolute_url())
        return absolute_url

class DeleteView(BrowserView):
    def __init__(self, context, request):
        self.context = context   
        self.request = request   
        self.session = Session() 
        self.logger = logging.getLogger('cirb.organizations.browser.organizationsmanage')

    def delete(self):
        id_del_orga = self.request.form.get('del')
        if not id_del_orga:
            self.logger.info(u'no id fund for delete a organization')
            return self.request.response.redirect(self.context.absolute_url())    
        del_orga = self.session.query(Organization).get(id_del_orga)
        self.session.delete(del_orga)
        transaction.commit()
        # TODO add status message
        return self.request.response.redirect(self.context.absolute_url())



from Acquisition import aq_inner
from Products.Five import BrowserView
#from Products.LinguaPlone.interfaces import ITranslatable
from Products.statusmessages.interfaces import IStatusMessage

from z3c.saconfig import Session
from cirb.organizations.content.organization import Organization
from cirb.organizations import organizationsMessageFactory as _
import transaction
import logging


class ManageView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.session = Session()

    def manage(self):
        results = self.session.query(Organization).filter(Organization.language == self.context.Language()).all()
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
    def __init__(self, context, request, session=''):
        self.context = context
        self.request = request
        self.session = Session()
        self.logger = logging.getLogger('cirb.organizations.browser.organizationsmanage')

    def delete(self):
        id_del_orga = self.request.form.get('del')
        if not delete_orga(self.session, id_del_orga):
            msg = u'no id fund for delete a organization'
            self.logger.info(msg)
            IStatusMessage(self.request).add(msg, type="error")
            return self.request.response.redirect(self.context.absolute_url())
        msg = _(u"The organization {0} is deleted".format(self.session.query(Organization).get(id_del_orga)))
        IStatusMessage(self.request).add(msg, type="info")
        return self.request.response.redirect(self.context.absolute_url())


def delete_orga(session, id):
    del_orga = session.query(Organization).get(id)
    if not del_orga:
        return False
    translated_orga = del_orga.get_translation()
    if translated_orga:
        session.delete(translated_orga)

    session.delete(del_orga)
    transaction.commit()
    # XXX delete Association

    return True

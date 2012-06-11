# -*- coding: utf-8 -*-
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class LanguageSelector(TranslatableLanguageSelector):
    render = ViewPageTemplateFile('templates/languageselector.pt')

    def custom_url(self):
        import pdb; pdb.set_trace()
        return 'lang'

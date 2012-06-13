# -*- coding: utf-8 -*-
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector


class LanguageSelector(TranslatableLanguageSelector):

    def _findpath(self, path, path_info):
        return 'lang'

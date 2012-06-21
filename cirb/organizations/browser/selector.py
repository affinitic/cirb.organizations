from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector

class FormTranslatableLanguageSelector(TranslatableLanguageSelector):

    def languages(self):
        import pdb; pdb.set_trace()
        super(self, FormTranslatableLanguageSelector).languages()

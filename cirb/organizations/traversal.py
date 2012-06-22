# -*- coding: utf-8 -*-
import re
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.interface import implements
from zope.component import adapts
from five import grok
from z3c.saconfig import Session

from collective.shuttle.traversal import Traverser, TraversableItem
from OFS.interfaces import ITraversable
from Acquisition import Implicit
from .browser.interfaces import ISearch
from .interfaces import IOrganization
from cirb.organizations.content.organization import Organization, Category, Address, Contact, InCharge, AdditionalInformation, Association
from plone.namedfile import file
from plone.namedfile.interfaces import IImageScaleTraversable
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from Products.LinguaPlone.interfaces import ITranslatable


def isInt(name):
    m = re.compile(r'^\d+$')
    return bool(m.match(name))


class PloneTraverser(Traverser):
    grok.adapts(ISearch, IHTTPRequest)
    grok.provides(IPublishTraverse)


class OrganizationWrapper(Implicit):
    """ Traversable organization
    """
    implements(IOrganization, IImageScaleTraversable, ITranslatable)
    security = ClassSecurityInfo()

    def __init__(self, organization):
        self._organization = organization
        initlogo = self._organization.logo
        if not initlogo:
            self._logo = file.NamedImage()
        else:
            self._logo = file.NamedImage(data=initlogo)
        initpicture = self._organization.picture
        if not initpicture:
            self._picture = file.NamedImage()
        else:
            self._picture = file.NamedImage(data=initpicture)

    security.declarePublic('logo')
    @property
    def logo(self):
        """ logo """
        return self._logo

    security.declarePublic('picture')
    @property
    def picture(self):
        """ picture """
        return self._picture

    def __getattr__(self, name):
        try:
            return getattr(self._organization, name)
        except AttributeError:
            return Implicit.__getattr__(self, name)

    def getId(self):
        return str(self._organization.organization_id)

    def Title(self):
        return self._organization.name

    def absolute_url(self):
        container = self.aq_parent.aq_parent
        translatedContainer = container.getTranslation(self.language)
        return "/".join((translatedContainer.absolute_url(),
                         'org',
                         self.getId()))

    def getPhysicalPath(self):
        return self.__parent__.getPhysicalPath() + (self.getId(),)

    # ITranslatable

    def Language(self):
        return self._organization.language

    def _wrapOrganization(self, organization):
        parent = self.aq_parent
        return OrganizationWrapper(organization).__of__(parent)

    def getTranslation(self, language):
        """ return id of the transalted organization or None """
        translation = self._organization.get_translation()
        if translation.language == language:
            return self._wrapOrganization(translation)

    def getTranslations(self, include_canonical=True, review_state=True,
                          _is_canonical=None):
        """Returns a dict of {lang : [object, wf_state]}.
          If review_state is False, returns a dict of {lang : object}
        """
        trans = self._organization.get_translation()
        if trans:
            translation = self._wrapOrganization(trans)
            if review_state:
                return {translation.language: [translation, None]}
            else:
                return {translation.language: translation}
        return {self.Language: self}

    def hasTranslation(self, language):
        return bool(self._organization.get_translation())

    def addTranslation(self, language):
        organization = Organization(address=Address(), category=Category(),
                                    person_incharge=InCharge(), person_contact=Contact(),
                                    additionalinfo=AdditionalInformation())
        organization.name = self._organization.name
        organization.language = language
        session = Session()
        session.add(organization)
        session.flush()
        canonical_id = self.getId()
        assoc = Association(association_type="lang")
        assoc.translated_id = organization.organization_id
        assoc.canonical_id = canonical_id
        session.add(assoc)
        session.flush()


from AccessControl.class_init import InitializeClass
InitializeClass(OrganizationWrapper)


class OrganizationTraversable(TraversableItem):
    implements(IHideFromBreadcrumbs)

    def __getitem__(self, key):
        if isInt(key):
            session = Session()
            organization = session.query(Organization).get(int(key))
            if organization is not None:
                wrapper = OrganizationWrapper(organization)
                return  wrapper.__of__(self)
        raise KeyError


@grok.adapter(ISearch, name=u"org")
@grok.implementer(ITraversable)
def getOrganizationsTraversable(context):
    return OrganizationTraversable("org")


from plone.z3cform.traversal import WrapperWidgetTraversal
from Acquisition import aq_base
from cirb.organizations.browser.organizationsform import WizardView

from zope.traversing.interfaces import TraversalError
from zope.interface import noLongerProvides
from zope.interface import alsoProvides

from z3c.form import util
from plone.z3cform.interfaces import IDeferSecurityCheck

from Acquisition import aq_inner


class WizardWidgetTraversal(WrapperWidgetTraversal):
    adapts(WizardView, IBrowserRequest)

    def traverse(self, name, ignored):

        form = self._prepareForm()

        # Since we cannot check security during traversal,
        # we delegate the check to the widget view.
        alsoProvides(self.request, IDeferSecurityCheck)
        form.update()
        noLongerProvides(self.request, IDeferSecurityCheck)

        # If name begins with form.widgets., remove it
        form_widgets_prefix = util.expandPrefix(form.prefix) + util.expandPrefix(form.widgets.prefix)
        if name.startswith(form_widgets_prefix):
            name = name[len(form_widgets_prefix):]

        # Split string up into dotted segments and work through
        target = aq_base(form)
        parts = name.split('.')
        while len(parts) > 0:
            part = parts.pop(0)
            if type(getattr(target, 'widgets', None)) is list:  # i.e. a z3c.form.widget.MultiWidget
                try:
                    # part should be integer index in list, look it up
                    target = target.widgets[int(part)]
                except IndexError:
                    raise TraversalError("'" + part + "' not in range")
                except ValueError:
                    #HACK: part isn't integer. Iterate through widgets to
                    # find matching name. This is required for
                    # DataGridField, which appends 'AA' and 'TT' rows to
                    # it's widget list.
                    full_name = util.expandPrefix(target.prefix) + part
                    filtered = [w for w in target.widgets
                                        if w.name == full_name]
                    if len(filtered) == 1:
                        target = filtered[0]
                    else:
                        raise TraversalError("'" + part + "' not valid index")
            elif hasattr(target, 'widgets'):  # Either base form, or subform
                # Check to see if we can find a "Behaviour.widget"
                new_target = None
                if len(parts) > 0:
                    new_target = self._form_traverse(target, parts[-1])  # HACK bsuttor, before : (target,part+'.'+parts[0])

                if new_target is not None:
                    # Remove widget name from stack too
                    parts.pop(0)
                else:
                    # Find widget in form without behaviour prefix
                    new_target = self._form_traverse(target, part)

                target = new_target
            elif hasattr(target, 'subform'):  # subform-containing widget, only option is to go into subform
                if part == 'widgets':
                    target = target.subform
                else:
                    target = None
            else:
                # HACK bsuttor
                if not target:
                    raise TraversalError('Cannot traverse through ' + target.__repr__())

            # Could not traverse from target to part
            if target is None: raise TraversalError(part)

        # Make the parent of the widget the traversal parent.
        # This is required for security to work in Zope 2.12
        if target is not None:
            target.__parent__ = aq_inner(self.context)
            return target
        raise TraversalError(name)

    def _form_traverse(self, form, name):
        print name
        step = getattr(form, 'currentStep', None)
        if step:
            if name in step.widgets:
                return step.widgets.get(name)

        if name in form.widgets:
            return form.widgets.get(name)
        # If there are no groups, give up now
        if getattr(aq_base(form), 'groups', None) is None:
            return None
        for group in form.groups:
            if group.widgets and name in group.widgets:
                return group.widgets.get(name)

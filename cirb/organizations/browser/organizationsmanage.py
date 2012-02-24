from Products.Five import BrowserView
from z3c.saconfig import Session
from cirb.organizations.content.organization import Organization

class ManageView(BrowserView):
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.session = Session()

    def manage(self):
        results = self.session.query(Organization).filter(Organization.language==self.context.Language()).all()
        return results

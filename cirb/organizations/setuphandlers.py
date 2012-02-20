from sqlalchemy import types, schema
from zope.interface import implements
from cirb.organizations import ORMBase
from cirb.organizations.content.organization import *
from zope import component
from z3c.saconfig.interfaces import IEngineFactory
from z3c.saconfig import Session
import transaction

def setupOrganizations(context):
    logger = context.getLogger("setupOrganization")
    logger.info('start setup organization')
    site = context.getSite()
    portal_workflow = site.portal_workflow
    if context.readDataFile('cirb.organizations.txt') is None:
        return
    
    # TODO check if table exists
    engine = component.getUtility(IEngineFactory, name="gscetterbeek")()
    ORMBase.metadata.create_all(engine)

    session = Session()
    
    addr = Address(street='mystreet', num='007', post_code='1000', municipality='Bruxelles')
    cat = Category(music=True, welcome=True, other="god")
    incharge = InCharge(title="Sir", first_name="Ferguson", second_name="Alex")
    contact_addr = Address(street='contact street', num='7', post_code='1001', municipality='Brux')
    contact = Contact(title="double zero", first_name="Bond", second_name="James", phone="007/11.11.11", fax="00", email="jb@mi6.uk", address=contact_addr)
    # TODO add logo
    orga = Organization(name='orgaTEST1', 
            address=addr, 
            person_incharge=incharge,
            person_contact=contact, 
            category=cat, 
            status="ASBL", 
            language="fr", 
            website="http://www.cirb.irisnet.be",
            x="5.253",
            y="152.35")

    orga2 = Organization(name='orgaistation 2', 
            address=addr, 
            person_incharge=incharge,
            person_contact=contact, 
            category=cat, 
            status="SPRL", 
            language="nl", 
            website="http://www.cibg.irisnet.be",
            x="5.253",
            y="152.35")

    session.add(orga)
    session.add(orga2)
    transaction.commit()
    
    logger.info('end setup organization')

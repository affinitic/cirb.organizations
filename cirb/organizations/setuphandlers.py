def setupOrganizations(context):
    logger = context.getLogger("setupOrganization")
    logger.info('start setup organization')
    if context.readDataFile('cirb.organizations.txt') is None:
        return

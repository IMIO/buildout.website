import transaction
from Products.CMFCore.utils import getToolByName
def test(self):
  catalog = getToolByName(self, 'portal_catalog', None)
  brains = catalog.searchResults({'portal_type': 'GeoLocation'})
  strPath = ''
  for brain in brains:
    geoloc = brain.getObject()
    geoloc.portal_type = 'Folder'
    strPath = strPath + "<br/>" + "<a href= "+geoloc.absolute_url()+">" + geoloc.absolute_url() + "</a>"
    transaction.commit()
  return strPath


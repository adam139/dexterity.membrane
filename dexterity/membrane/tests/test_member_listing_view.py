#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from dexterity.membrane.testing import FUNCTIONAL_TESTING 

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest
from plone.namedfile.file import NamedImage
import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        import datetime
#        import pdb
#        pdb.set_trace()
        start = datetime.datetime.today()
        end = start + datetime.timedelta(7)
        portal.invokeFactory('dexterity.membrane.memberfolder', 'memberfolder1')
        
        portal['memberfolder1'].invokeFactory('dexterity.membrane.member', 'member1',
                             email="12@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             bonus = 10,
                             description="I am member1")     
        portal['memberfolder1'].invokeFactory('dexterity.membrane.member', 'member2',
                             email="13@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             bonus = 300,
                             description="I am member1")   
        
        portal['memberfolder1'].invokeFactory('dexterity.membrane.member', 'member3',
                             email="12@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             bonus = 300,
                             description="I am member1")   
        
        portal['memberfolder1'].invokeFactory('dexterity.membrane.member', 'member4',
                             email="12@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             bonus = 300,
                             description="I am member1")   
        
        portal['memberfolder1'].invokeFactory('dexterity.membrane.member', 'member5',
                             email="15@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             bonus = 300,
                             description="I am member1")                                
          
 
        data = getFile('image.jpg').read()
        item = portal['memberfolder1']['member1']
        item.photo = NamedImage(data, 'image/jpg', u'image.jpg')
           
        self.portal = portal
    
    def test_member_listing_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['memberfolder1'].absolute_url() + '/@@admin_view'        

        browser.open(obj)
 
        outstr = "qq.com"        
        self.assertTrue(outstr in browser.contents)          
        
   
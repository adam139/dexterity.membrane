# -*- coding: utf-8 -*-
from dexterity.membrane import _
from dexterity.membrane.membrane_helpers import validate_unique_email
from plone.directives import form
from plone.directives import dexterity
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid, invariant
import re
from plone.namedfile.field import NamedBlobImage

from my315ok.socialorgnization.registrysource import RegistrySource, DynamicVocabulary,FirstDynamicVocabulary
from my315ok.socialorgnization.content.orgnization import IOrgnization

def is_email(value):
    """Is this an email address?

    We only do very basic validation, as the docs say we should just
    check if there is an '@' sign in the address.

    >>> is_email('joe@example.org')
    True
    >>> is_email('joe')
    Traceback (most recent call last):
    ...
    Invalid: Not an email address
    >>> is_email('')
    Traceback (most recent call last):
    ...
    Invalid: Not an email address
    >>> is_email(None)
    Traceback (most recent call last):
    ...
    Invalid: Not an email address
    >>> is_email(object())
    Traceback (most recent call last):
    ...
    Invalid: Not an email address

    """
    if not isinstance(value, basestring) or not '@' in value:
        raise Invalid(_(u"Not an email address"))
    return True


def is_url(value):
    """Is this a URL?

    >>> is_url("http://google.com/")
    True
    >>> is_url("https://google.com")
    True
    >>> is_url("http://example.org/folder/somepage")
    True
    >>> is_url("ssh://google.com")
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url("nothing")
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url("")
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url(None)
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url(object())
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link

    """
    if isinstance(value, basestring):
        pattern = re.compile(r"^https?://[^\s\r\n]+")
        if pattern.search(value.strip()):
            return True
    raise Invalid(_(u"Not a valid link"))


class IEmail(form.Schema):
    """Email address schema.

    If you have this field, we can make you a member.  To authenticate
    you also need a password though.
    """

    email = schema.TextLine(
        # String with validation in place looking for @, required.
        # Note that a person's email address will be their username.
        title=_(u"E-mail Address"),
        required=True,
        constraint=is_email,
        )

    @invariant
    def email_unique(data):
        """The email must be unique, as it is the login name (user name).

        The tricky thing is to make sure editing a user and keeping
        his email the same actually works.
        """
        user = data.__context__
        if user is not None:
            if hasattr(user, 'email') and user.email == data.email:
                # No change, fine.
                return
        error = validate_unique_email(data.email)
        if error:
            raise Invalid(error)


class IMember(IEmail):
    """
    Member
    """
    title = schema.TextLine(title=_(u"Full name"),
            required=True)


    description = schema.Text(
        title=_(u"Short Bio"),
        description=_(u"Tell us more about yourself"),
        required=False,
    )    

    first_name = schema.TextLine(
        title=_(u"First Name"),
        required=True,
        )

    last_name = schema.TextLine(
        title=_(u"Last Name"),
        required=True,
        )

    homepage = schema.TextLine(
        # url format
        title=_(u"External Homepage"),
        required=False,
        constraint=is_url,
        )

    form.widget(bio="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    bio = schema.Text(
        title=_(u"Biography"),
        required=False,
        )
    
    photo = NamedBlobImage(
        title=_(u"Photo"),
        description=_(u"Your photo or avatar. Recommended size is 150x195"),
        required=False
    )    
### organization membe
inlist = ["市民政局","市科协","市社科联","市文联","市工商联"]
class IOrganizationMember(IMember):
    """
    Organization Member
    """    

#    inlist = ["市民政局","市科协","市社科联","市文联","市工商联"]
#     orgname = schema.Choice(
#             title=_(u"organization name"),
#             source=FirstDynamicVocabulary("my315ok.socialorgnization.content.orgnization",
#                                      "IOrgnization",inlist,
#                                      orgnization_belondtoArea="xiangtanshi")
#                         )  
### organization sponsor member
class ISponsorMember(IMember):
    """
    Government department Member
    """
    

#     orgname = schema.Choice(
#             title=_(u"Government department"),
#             source=DynamicVocabulary("my315ok.socialorgnization.content.governmentdepartment", "IOrgnization")
#                         )     
        
### wechat member    
class IWechatMember(IMember):
    """
    Wechat Member
    """
    
    phone = schema.TextLine(
        title=_(u"Phone number"),
        required=True
    )
    organization = schema.Text(
        title=_(u"organization"),
        required=False,
    )
    sector = schema.Choice(
        title=_(u"Sector"),
        required=True,
        vocabulary="dexterity.membrane.vocabulary.sector"
        )
    address = schema.TextLine(
        title=_(u"personal address"),       
        required=False,
        ) 
    qq_number = schema.Int(
        # url format
        title=_(u"QQ Number"),
        required=False,

        )      
          
    
### conference member
class IConferenceMember(IMember):
    """
    Conference Member
    """
 
    
    phone = schema.TextLine(
        title=_(u"Phone number"),
        required=True
    )
    
   
    organization = schema.TextLine(
        title=_(u"Organization / Company"),
        required=True,
    )
    
    sector = schema.Choice(
        title=_(u"Sector"),
        required=True,
        vocabulary="dexterity.membrane.vocabulary.sector"
        )        

    position = schema.TextLine(
        title=_(u"Position / Role in Organization"),
        required=True,
    )     
        
    research_domain = schema.TextLine(

        title=_(u"research domain"),
        required=False,

        )
    
    country = schema.Choice(
        title=_(u"Country"),
        description=_(u"Where you are from"),
        required=False,
        default='China',
        vocabulary="collective.conference.vocabulary.countries"
    )

    province = schema.Choice(
        title=_(u"the province of your company"),
        vocabulary="dexterity.membrane.vocabulary.province",        
        required=True,
        ) 

    address = schema.TextLine(
        title=_(u"personal address"),       
        required=False,
        ) 
    
#    dexterity.write_permission(bonus='cmf.ReviewPortalContent')            
    bonus = schema.Int(
        # url format
        title=_(u"bonus"),
        description=_(u"user's bonus,user permission was controlled by this"),        
        required=False,
        default=0,
#        constraint=is_url,
        )    
    
    qq_number = schema.Int(
        # url format
        title=_(u"QQ Number"),
        required=False,

        )          
    



#    form.fieldset('sponsorship',
#            label=_(u"Funding"),
#            fields=['need_sponsorship', 'roomshare', 'tshirt_size','is_vegetarian','comment']
#    )

    need_sponsorship = schema.Bool(
            title=_(u"Need funding"),
            description=_(u"Check this option if you need funding to attend."), required=False)

    roomshare = schema.Bool(
            title=_(u"Roomshare"),
            description=_(u"If you want or need a room, check this option"),
            required=False)

    comment = schema.Text(
        title=_(u"Comments"),
        description=_(u"Fill in this field with things you need the organizers to know.\
        If you are roomsharing and already have a roommate, please mention your roommate's name here"),
        required=False
    )
    is_vegetarian = schema.Bool(
        title=_(u"Vegetarian?"),
        required=False
    )

    tshirt_size = schema.Choice(
        title=_(u"T-shirt size"),
        vocabulary="collective.conference.vocabulary.tshirtsize",
        required=False
    )
    

    form.widget(color="collective.z3cform.colorpicker.colorpickeralpha.ColorpickerAlphaFieldWidget")
    color = schema.TextLine(
        title=_(u"Person Color Tag"),
        default=u'cccccc',
        required=False
    )

    
    form.omitted('bonus')   


@form.validator(field=IMember['photo'])
def maxPhotoSize(value):
    if value is not None:
        if value.getSize()/1024 > 512:
            raise schema.ValidationError(_(u"Please upload image smaller than 512KB"))

@implementer(IMember)
class member(dexterity.Item):
    pass     
from core import register_element, AgentBase, decode


@register_element
class Actor(AgentBase):
    """
    Model representation of a person that can perform tasks and do things, perhaps even own assets.
    """

    type_name = 'actor'

    def __init__(self, internal_id, name, email, phone_number):
        super(Actor, self).__init__(internal_id=internal_id)
        self.name = name
        self.email = email
        self.phone_number = phone_number

    def serialize(self):
        retdict = super(Actor, self).serialize()
        retdict['kwargs']['name'] = self.name
        retdict['kwargs']['email'] = self.email
        retdict['kwargs']['phone_number'] = self.phone_number
        return retdict

    @classmethod
    def decode(cls, internal_id, kwargs):
        retobj = super(Actor, cls).decode(internal_id, kwargs)
        retobj.name = kwargs['name']
        retobj.email = kwargs['email']
        retobj.phone_number = kwargs['phone_number']
        return retobj


@register_element
class Asset(AgentBase):
    """
    This model represents things, like cars or coolers or anything else that needs to be tracked.s
    """

    type_name = 'asset'

    def __init__(self, internal_id, name, owner, description):
        """
        Constructor method for the `Asset` class.

        :param internal_id: string of the internal ID of this object
        :param name: string of the name of this `Asset`
        :param owner: either a Logis `Actor` object, or `None`.
        :param description: A string that briefly describes this asset
        """
        super(Asset, self).__init__(internal_id)
        self.name = name
        if not (owner is None or isinstance(owner, Actor)):
            raise ValueError("The owner must be either None or an instance of Actor. We got {}".format(owner))
        self.owner = owner
        self.description = description

    def serialize(self):
        retdict = super(Asset, self).serialize()
        retdict['kwargs']['name'] = self.name
        try:
            retdict['kwargs']['owner'] = self.owner.serialize()
        except AttributeError:
            retdict['kwargs']['owner'] = self.owner  # This only happens in the case self.owner is None
        retdict['kwargs']['description'] = self.description

    @classmethod
    def decode(cls, internal_id, kwargs):
        retobj = super(Asset, cls).decode(internal_id, kwargs)
        retobj.name = kwargs['name']
        if kwargs['owner'] is None:
            retobj.owner = None
        else:
            retobj.owner = decode(kwargs['owner'])
        retobj.description = kwargs['description']
        return retobj

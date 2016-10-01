from core import register_element, PhysicalObjectBase


@register_element
class Actor(PhysicalObjectBase):
    """
    Model representation of a person that can perform tasks and do things, perhaps even own assets.
    """

    name = 'actor'

    def __init__(self, internal_id, name, email, phone_number):
        super(Actor, self).__init__(internal_id=internal_id)
        self.name = name
        self.email = email
        self.phone_number = phone_number

from core import register_element, AgentBase


class IncompatibleTaskError(Exception):
    pass


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

    def assign_to(self, task):
        if not self.is_busy(task.start_time, task.stop_time):
            self.tasks_assigned_to.append(task)
            self.tasks_assigned_to.sort(key=lambda _task: _task.start_time)
        else:
            raise IncompatibleTaskError("This task conflicts with tasks already assigned to this actor")

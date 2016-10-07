from core import decode, register_element, BaseLogisObject
from actors import Asset
import utils


@register_element
class Task(BaseLogisObject):
    type_name = 'task'

    def __init__(self, internal_id, start_time, stop_time, actors, description):
        """
        The base constructor for a Task object.

        :param internal_id: internal ID to be used for serialization/uniqueness tracking
        :param start_time: a datetime tuple/object indicating when the task begins
        :param stop_time: a datetime tuple/object indicating when the task ends
        :param actors: A list of `Actor` objects, indicating who is involved on this task
        :param description: A list that contains strings and Asset objects. Assets are
                            meant to be embedded into description strings, and so the order of
                            the list should be as it would be rendered on the webpage. Something
                            like:
                            ["Drive ", <Asset: Steve's Van>, " to the airport"]
        """
        super(Task, self).__init__(internal_id=internal_id)

        # Now, for the actors and assets, make sure that we don't conflict.
        assets = [item for item in description if isinstance(item, Asset)]

        for agent in actors + assets:
            if agent.is_busy(start_time, stop_time):
                raise ValueError("The actor {} already has a task assigned for this time")

        self.start_time = start_time
        self.stop_time = stop_time
        self.actors = actors
        self.description = description

    def serialize(self):
        retdict = super(Task, self).serialize()

        retdict['kwargs']['start_time'] = utils.serialize_datetime_obj(self.start_time)
        retdict['kwargs']['stop_time'] = utils.serialize_datetime_obj(self.stop_time)

        actor_list = [actor.serialize() for actor in self.actors]
        retdict['kwargs']['actors'] = actor_list
        description = [item.serialize() if isinstance(item, Asset) else item for item in self.description]
        retdict['kwargs']['description'] = description

        return retdict

    @classmethod
    def decode(cls, internal_id, kwargs):
        start_time = utils.decode_datetime_obj(kwargs['start_time'])
        stop_time = utils.decode_datetime_obj(kwargs['stop_time'])
        actors = [decode(actor) for actor in kwargs['actors']]
        description = [decode(item) if isinstance(item, dict) else item for item in kwargs['description']]

        retobj = cls(internal_id, start_time, stop_time, actors, description)
        return retobj

"""
This module contains the base definitions for the models that are to be implemented by Logis, as well as the decoding
mechanism by which Logis objects will be reconstructed from stored values on the database.

The way serialization/decoding works is thus: all LogisObjects must store their constructors in the `ELEMENTS`
dictionary defined in this module, keyed by an class-level property called `type_name`. When you define a new
model/element that must be storable/fetchable from the database, you must decorate your class with the
`register_element` decorator. This will tell Logis how it should interpret your object.

With this `register_element` decorator, the following code:

..code-block::python

    import core

    class NewObject(core.BaseLogisObject):
        type_name = 'some_generic_object'

    core.ELEMENTS[NewObject.type_name] = NewObject

Becomes this:

..code-block::python

    import core

    @core.register_element
    class NewObject(core.BaseLogisObject):
        type_name = 'some_generic_object'

And this is the preferred way of creating and registering new elements.
"""

ELEMENTS = {}


class IncompatibleTaskError(Exception):
    pass


def register_element(elem):
    """
    This allows you to make an element available for serialization/decoding. If a class with the type_name you are
    trying to register already exists, it will complain.

    :param elem:
    :return:
    """
    if elem.type_name in ELEMENTS.keys():
        raise ValueError("An element with the name {} already exists".format(elem.type_name))
    ELEMENTS[elem.type_name] = elem
    return elem


def decode(serialization):
    """
    This function returns the decoded LogisObject for the given dictionary

    :param serialization:
    :return: Logis object
    """
    type_name = serialization['type_name']
    kwargs = serialization['kwargs']
    return ELEMENTS[type_name].decode(internal_id=serialization['internal_id'],
                                      kwargs=kwargs)


@register_element
class BaseLogisObject(object):
    """
    This is the base Logis object, that all other Logis models ought to be derived from. The only special thing about
    this is that it adds an internal id, which should be unique to every object.

    :param internal_id: string indicating uniqueness of element

    In addition to the constructor, there should be a class-level definition of `type_name`. This will help us in
    decoding Logis objects from database storage.
    """

    type_name = 'base_object'

    def __init__(self, internal_id):
        self._internal_id = internal_id

    def __eq__(self, other):
        return self.internal_id == other.internal_id

    @property
    def internal_id(self):
        """
        MongoDB has a way of assigning internal IDs to objects automatically
        to preserve uniqueness.
        """
        return self._internal_id

    def serialize(self):
        """
        This should convert this object into a dictionary that can then be reconstructed via the from_dict method.

        The format of this dictionary should be:
        {
            "type": self.name
            "kwargs": the arguments you supply to the constructor to uniquely reconstruct this object
        }

        :return:
        """
        return dict(type_name=self.type_name,
                    internal_id=self.internal_id,
                    kwargs={})

    @classmethod
    def decode(cls, internal_id, kwargs):
        return cls(internal_id=internal_id)


@register_element
class AgentBase(BaseLogisObject):
    """
    This base class is used to help define Actors and Assets, since with both, you need to make sure that whenever
    they're assigned to a task, that they don't conflict with what they're already assigned to.
    """

    type_name = 'physical_object_base'

    def __init__(self, internal_id):
        super(AgentBase, self).__init__(internal_id)
        # Upon invocation of the constructor method, the Agent should not already have tasks assigned to it. That is
        # what the decoding method is for.
        self.tasks_assigned_to = []

    def tasks_during(self, start_time, stop_time):
        """
        This method should return the tasks that we are assigned to during this time interval

        :param start_time: a datetime indicating when the task begins
        :param stop_time: a datetime indicating when the task ends
        :return:
        """
        retlist = []
        for task in self.tasks_assigned_to:
            max_start = max(task.start_time, start_time)
            min_end = min(task.stop_time, stop_time)

            if max_start < min_end:
                retlist.append(task)
        return retlist

    def is_busy(self, start_time, stop_time):
        """
        Lets you know if this agent is busy during this time. Basically, tells you if
        `len(self.tasks_during(start_time, stop_time)) == 0`
        """
        return len(self.tasks_during(start_time, stop_time)) != 0

    def serialize(self):
        retdict = super(AgentBase, self).serialize()
        # The tasks_assigned_to is a list of LogisObjects, so we need to invoke their serializations as well.
        serialized_list = [logis_task.serialize() for logis_task in self.tasks_assigned_to]
        retdict['kwargs']['tasks_assigned_to'] = serialized_list
        return retdict

    @classmethod
    def decode(cls, internal_id, kwargs):
        task_list = kwargs['tasks_assigned_to']
        task_list = [decode(task) for task in task_list]

        retobj = cls.__new__(cls)
        retobj._internal_id = internal_id
        retobj.tasks_assigned_to = task_list

        return retobj

    def assign_to(self, task):
        if not self.is_busy(task.start_time, task.stop_time):
            self.tasks_assigned_to.append(task)
            self.tasks_assigned_to.sort(key=lambda _task: _task.start_time)
        else:
            raise IncompatibleTaskError("This task conflicts with tasks already assigned to this actor")

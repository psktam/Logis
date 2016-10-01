ELEMENTS = {}


def register_element(elem):
    """
    This allows you to make an element available for serialization/decoding
    :param elem:
    :return:
    """
    if elem.name in ELEMENTS.keys():
        raise ValueError("An element with the name {} already exists".format(elem.name))
    ELEMENTS[elem.name] = elem
    return elem


def decode(serialization):
    """
    This function returns the decoded LogisObject for the given dictionary

    :param serialization:
    :return: Logis object
    """
    type_name = serialization['type']
    kwargs = serialization['kwargs']
    return ELEMENTS[type_name].decode(kwargs)


@register_element
class BaseLogisObject(object):
    """
    This is the base Logis object, that all other Logis models ought to be derived from. The only special thing about
    this is that it adds an internal id, which should be unique to every object.

    :param internal_id: string indicating uniqueness of element
    """

    name = 'base_object'

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
        return dict(type=self.name,
                    kwargs=dict(internal_id=self.internal_id))

    @classmethod
    def decode(cls, kwargs):
        return cls(internal_id=kwargs['internal_id'])


@register_element
class PhysicalObjectBase(BaseLogisObject):
    """
    This base class is used to help define Actors and Assets, since with both, you need to make sure that whenever
    they're assigned to a task, that they don't conflict with what they're already assigned to.
    """

    name = 'physical_object_base'

    def __init__(self, internal_id, tasks_assigned_to):
        super(PhysicalObjectBase, self).__init__(internal_id)
        self.tasks_assigned_to = tasks_assigned_to  # Should be an internal list of tasks already assigned to

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

            if min_end < max_start:
                retlist.append(task)
        return retlist

    def is_busy(self, start_time, stop_time):
        """
        Lets you know if this agent is busy during this time. Basically, tells you if
        `len(self.tasks_during(start_time, stop_time)) == 0`
        """
        return len(self.tasks_during(start_time, stop_time)) != 0

    def serialize(self):
        retdict = super(PhysicalObjectBase, self).serialize()
        # The tasks_assigned_to is a list of LogisObjects, so we need to invoke their serializations as well.
        serialized_list = [logis_task.serialize() for logis_task in self.tasks_assigned_to]
        retdict['kwargs'] = dict(internal_id=self.internal_id, tasks_assigned_to=serialized_list)
        return retdict

    @classmethod
    def decode(cls, kwargs):
        id = kwargs['internal_id']
        task_list = kwargs['tasks_assigned_to']
        task_list = [decode(task) for task in task_list]

        return cls(id, task_list)

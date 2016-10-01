from core import BaseLogisObject


class Task(BaseLogisObject):

    def __init__(self, internal_id, start_time, stop_time, actors, assets, description):
        """
        The base constructor for a Task object.

        :param internal_id: internal ID to be used for serialization/uniqueness tracking
        :param start_time: a datetime tuple/object indicating when the task begins
        :param stop_time: a datetime tuple/object indicating when the task ends
        :param actors: A list of `Actor` objects, indicating who is involved on this task
        :param assets: A list of `Asset` objects, indicating what is involved in this task
        :param description: A string that describes the task. The format of this string should be tied to the contents
                            of `assets`. Whenever you see a pattern like `{{<id>}}`, `id` should correspond to an object
                            in `assets`, and all objects in `assets` must correspond to an `id`, and only one `id`, in
                            `description`. Because of this, in the online form, you should make sure that the user
                            cannot type in `{{}}`.
        """
        super(Task, self).__init__(internal_id=internal_id)

        # Do some argument checking
        if start_time is None and stop_time is None:
            raise ValueError("Both start_time and stop_time cannot be None. One of them must be a datetime object")

        # Now, for the actors and assets, make sure that we don't conflict.
        for actor in actors:
            if actor.conflicts_with(start_time, stop_time):
                raise ValueError("The actor {} already has a task assigned for ")

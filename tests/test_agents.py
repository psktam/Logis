from unittest import TestCase
from datetime import datetime

import nose.tools as nt
import mock

from logis.core import decode
from logis.actors import Actor, IncompatibleTaskError


class TestActor(TestCase):

    def setUp(self):
        self.test_actor = Actor('12345', 'Steve Winston', 'steve.winston@email.com', '123-456-7890')

    def test_serialization(self):
        real_dict = dict(internal_id='12345',
                         type_name='actor',
                         kwargs=dict(name='Steve Winston',
                                     email='steve.winston@email.com',
                                     phone_number='123-456-7890',
                                     tasks_assigned_to=[]))
        serialization = self.test_actor.serialize()
        self.assertDictEqual(real_dict, serialization)

    def test_decoding(self):
        test_serialization = dict(internal_id='12345',
                                  type_name='actor',
                                  kwargs=dict(name='Steve Winston',
                                              email='steve.winston@email.com',
                                              phone_number='123-456-7890',
                                              tasks_assigned_to=[]))
        reconstructed = decode(test_serialization)
        self.assertIsInstance(reconstructed, Actor)
        self.assertEqual('12345', reconstructed.internal_id)
        self.assertEqual('Steve Winston', reconstructed.name)
        self.assertEqual('steve.winston@email.com', reconstructed.email)
        self.assertEqual('123-456-7890', reconstructed.phone_number)
        self.assertListEqual([], reconstructed.tasks_assigned_to)

    def test_can_assign_valid_task(self):
        """
        Make sure that you can assign to a task that does not conflict with any tasks this actor is currently assigned
        to.

        :return:
        """
        task_1 = mock.Mock()
        task_1.start_time = datetime(year=2016, month=1, day=1, hour=1, minute=0, second=0)
        task_1.stop_time = datetime(year=2016, month=1, day=1, hour=1, minute=0, second=10)

        self.test_actor.assign_to(task_1)

        task_2 = mock.Mock()
        task_2.start_time = datetime(year=2016, month=1, day=1, hour=1, minute=0, second=10)
        task_2.stop_time = datetime(year=2016, month=1, day=1, hour=1, minute=0, second=20)

        self.test_actor.assign_to(task_2)

    @nt.raises(IncompatibleTaskError)
    def test_cannot_assign_invalid_task(self):
        """Make sure that we are not allowed to assign to a task that conflicts with currently assigned tasks"""
        task_1 = mock.Mock()
        task_1.start_time = datetime(year=2016, month=1, day=1, hour=1, minute=0, second=0)
        task_1.stop_time = datetime(year=2016, month=1, day=1, hour=1, minute=0, second=10)

        self.test_actor.assign_to(task_1)

        task_2 = mock.Mock()
        task_2.start_time = datetime(year=2016, month=1, day=1, hour=1, minute=0, second=5)
        task_2.stop_time = datetime(year=2016, month=1, day=1, hour=1, minute=0, second=20)

        self.test_actor.assign_to(task_2)
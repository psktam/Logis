from unittest import TestCase

from logis.core import decode
from logis.actors import Actor


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

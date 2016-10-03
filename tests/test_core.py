from unittest import TestCase
from datetime import datetime

import mock
from nose.tools import raises

from logis import core


class TestBaseObject(TestCase):

    def setUp(self):
        self.base_obj = core.BaseLogisObject(internal_id='12345')

    def test_serialization(self):
        serialized = self.base_obj.serialize()
        real_dict = dict(type_name='base_object', internal_id='12345',
                         kwargs={})
        self.assertDictEqual(serialized, real_dict)

    def test_reconstruction(self):
        test_serialization = dict(type_name='base_object',
                                  internal_id='12345',
                                  kwargs={})
        reconstructed_obj = core.decode(test_serialization)
        self.assertEqual(self.base_obj, reconstructed_obj)

    @raises(ValueError)
    def test_cant_register_redundant_elements(self):
        """
        This makes sure that we can't register multiple elements that have the same type name.
        :return:
        """
        test_class_type = 'object_1'

        class Elem1(object):
            type_name = test_class_type

        class Elem2(object):
            type_name = test_class_type

        try:
            # Before registering these elements, make sure that test_class_type doesn't already exist
            self.assertTrue(test_class_type not in core.ELEMENTS.keys(), "The dummy class '{}' already exists. "
                                                                         "Change the name of the test class"
                                                                         "".format(test_class_type))
            core.register_element(Elem1)
            core.register_element(Elem2)

        finally:
            if test_class_type in core.ELEMENTS.keys():
                core.ELEMENTS.pop(test_class_type)


class TestAgentBase(TestCase):

    def setUp(self):
        self.internal_id = '12345'
        self.base_agent = core.AgentBase(internal_id=self.internal_id)

    def test_busy_method(self):
        """
        Make sure that you show that you're busy when you're supposed to be busy.
        """
        mock_task = mock.Mock()
        mock_task.start_time = datetime(year=2016, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        mock_task.stop_time = datetime(year=2016, month=1, day=1, hour=0, minute=0, second=10, microsecond=0)

        self.base_agent.tasks_assigned_to.append(mock_task)

        test_start = datetime(year=2016, month=1, day=1, hour=0, minute=0, second=2, microsecond=0)
        test_stop = datetime(year=2016, month=1, day=1, hour=0, minute=0, second=8, microsecond=0)
        self.assertTrue(self.base_agent.is_busy(test_start, test_stop))

    def test_free_when_not_busy(self):
        """Make sure that the is_busy method does say we're busy when we are free"""
        mock_task = mock.Mock()
        mock_task.start_time = datetime(year=2016, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        mock_task.stop_time = datetime(year=2016, month=1, day=1, hour=0, minute=0, second=10, microsecond=0)

        self.base_agent.tasks_assigned_to.append(mock_task)

        test_start = datetime(year=2016, month=2, day=1, hour=0, minute=0, second=0, microsecond=0)
        test_stop = datetime(year=2016, month=2, day=1, hour=1, minute=0, second=0, microsecond=0)

        self.assertFalse(self.base_agent.is_busy(test_start, test_stop))

    def test_serialization(self):
        """Sanity checking to make sure the serialization method outputs what we expect"""
        serial_output = self.base_agent.serialize()
        real_dict = dict(internal_id=self.internal_id,
                         type_name='physical_object_base',
                         kwargs=dict(tasks_assigned_to=[]))
        self.assertDictEqual(real_dict, serial_output)

    def test_decoding(self):
        test_serial = dict(internal_id=self.internal_id,
                           type_name='physical_object_base',
                           kwargs=dict(tasks_assigned_to=[]))
        reconstructed = core.decode(test_serial)
        self.assertIsInstance(reconstructed, core.AgentBase)
        self.assertEqual(reconstructed.internal_id, self.internal_id)
        self.assertEqual(reconstructed.tasks_assigned_to, [])

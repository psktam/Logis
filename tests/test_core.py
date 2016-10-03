from unittest import TestCase

import mock
from nose.tools import raises

from logis import core


class TestBaseObject(TestCase):

    def setUp(self):
        self.base_obj = core.BaseLogisObject(internal_id='12345')

    def test_serialization(self):
        serialized = self.base_obj.serialize()
        real_dict = dict(type='base_object', kwargs=dict(internal_id='12345'))
        self.assertDictEqual(serialized, real_dict)

    def test_reconstruction(self):
        reconstructed_obj = core.decode(dict(type='base_object', kwargs=dict(internal_id='12345')))
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

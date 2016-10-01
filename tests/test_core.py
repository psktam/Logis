from unittest import TestCase
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


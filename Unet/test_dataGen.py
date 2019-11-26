import os
from unittest import TestCase
from ex1 import DataGen


class DataGenMock(TestCase):
    def setUp(self):
        self.dataGen = DataGen(['0a7d30b252359a10fd298b638b90cb9ada3acced4e0c0e5a3692013f432ee4e9'],
                               'data-science-bowl-2018/stage1_train/')


class TestDataGen(DataGenMock):
    def test_on_epoch_end(self):
        self.assertTrue(True)

    def test_init_batch_size(self):
        # self.fail()
        self.assertEqual(self.dataGen.batch_size, 8)

    def test_init_image_size(self):
        # self.fail()
        self.assertEqual(self.dataGen.image_size, 128)

    def test_check_valid_path(self):
        # self.fail()
        image_path = os.path.join(self.dataGen.path, self.dataGen.ids[0], "images",  self.dataGen.ids[0] + ".png")
        exists = os.path.isfile(image_path)
        self.assertTrue(exists)

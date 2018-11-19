import unittest

from support_methods import storeData, deletedata, editdata, searchdata


class MYTEST(unittest.TestCase):
    '''functionality testing'''

    def test1(self):
        '''if inserted successfully'''
        self.assertEqual(store({"name":"Ashish", "email":"ashish@artifacia.com", "number":"9090932321"}), True)

    def test2(self):
        '''if duplicate'''
        self.assertEqual(store({"name":"Dinesh", "email":"ashish@artifacia.com", "number":"9090992321"}), False)

    def test3(self):
        '''if deleted successfully'''
        self.assertEqual(deletedata({"numner":"8988383838"}), True)

    def test4(self):
        '''if not found when try to delete'''
        self.assertEqual(deletedata({"number":"8838383838"}), False)

    def test5(self):
        '''if edited successfully'''
        self.assertEqual(editdata({"number":999999999,"data_tobe_updated":{"name":"Dinesh"}}), True)

    def test6(self):
        '''if not edited successfully'''
        self.assertEqual(editdata({"number":9999999,"data_tobe_updated":{"name":"Dinesh"}}), False)

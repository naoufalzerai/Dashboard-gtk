from unittest import TestCase

from DAL.UOW import BaseModel


class Test(TestCase):
    def test_load(self):
        self.assert_(1 == 1)


class Test(TestCase):
    def test_get_attrs(self):
        from Helper.Crud import get_attrs
        # arrange
        attributes = get_attrs(BaseModel)
        self.assert_(attributes[1][0][0]=='id')

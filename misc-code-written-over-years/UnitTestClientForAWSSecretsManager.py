import unittest
from aws_secrets import AWSSecrets
from botocore.exceptions import ClientError


class test_aws_secrets_manager(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Set up class")
        cls.secret = AWSSecrets()
        
    
    def test_Secret(self):
        
        self.assertEqual(self.secret.get_secret('TEST_API_KEY'),'abc123')
    
    def test_Secret_failure(self):
        
        self.assertNotEqual(self.secret.get_secret('TEST_API_KEY'),'abc123')
        
    # def test_Exception(self):
        
    #     self.assertRaises(ClientError,self.secret.get_secret('TESTX_API_KEY'))
        
    @classmethod
    def tearDownClass(cls):
        cls.secret = None
    
if __name__ == "__main__":
    unittest.main()
    
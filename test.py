import unittest
from recipe import RecipeSearch


class RecipeSearchTest(unittest.TestCase):

    # should exit when 1 is entered
    print('--> should exit when 1 is entered \n')
    def test_user_input_1(self):
        result = RecipeSearch().validate_ingredients('1')
        self.assertEqual(result, None)

    # should not allow numbers as ingredients
    print('--> should not allow numbers as ingredients \n')
    def test_user_input_numbers(self):
        test_data = ['3', '2', '123', '24541']
        for i in test_data:
            result = RecipeSearch().validate_ingredients(i)
            self.assertEqual(result, "Note: Only Alphabets Allowed!")



if __name__ == "__main__":
    unittest.main()
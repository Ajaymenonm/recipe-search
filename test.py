import unittest
from recipe import RecipeSearch


class RecipeSearchTest(unittest.TestCase):

    # should exit when 1 is entered
    def test_user_input_1(self):
        print('--> should exit when 1 is entered \n')
        result = RecipeSearch().validate_ingredients('1')
        self.assertEqual(result, None)

    # should not allow numbers as ingredients
    def test_user_input_numbers(self):
        print('--> should not allow numbers as ingredients \n')
        test_data = ['3', '2', '123', '24541']
        for i in test_data:
            result = RecipeSearch().validate_ingredients(i)
            self.assertEqual(result, "Note: Only Alphabets Allowed!")

    # should not allow whitespaces
    def test_user_input_whitespace(self):
        print('--> should not allow numbers as ingredients \n')
        test_data = [' ', '  ']
        for i in test_data:
            result = RecipeSearch().validate_ingredients(i)
            self.assertEqual(result, "No Ingredient Entered \n")

    # should not allow special characters
    def test_user_input_special_char(self):
        print('--> should not allow special characters\n')
        test_data = ['@', '$#%', '*&^%$#']
        for i in test_data:
            result = RecipeSearch().validate_ingredients(i)
            self.assertEqual(result, "Note: Only Alphabets Allowed!")

    # should convert plural ingredients to singular
    def test_user_input_plural_to_singular(self):
        print('--> should convert plural ingredients to singular\n')
        test_data = ['eggs', 'onions', 'loaves', 'potatoes']
        expected_result = ['egg', 'onion', 'loaf', 'potato']
        for i, x in zip(test_data, expected_result):
            result = RecipeSearch().validate_ingredients(i)
            self.assertEqual(result, "You Have: {}".format(x))


if __name__ == "__main__":
    unittest.main()
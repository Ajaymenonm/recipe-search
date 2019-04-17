import json
import unittest
from recipe import RecipeSearch


class FakeInput(RecipeSearch):

    def __init__(self):
        super(FakeInput, self).__init__()  # Do RecipeSearch's __init__
        self.ingredients_with_user = []  # Allow over riding the instance variable

    # New method saves fake ingredients
    def set_fake_ingredients_with_user(self, ing_input):
        self.ingredients_with_user.append(ing_input)

    # return length of ingredient list entered by user
    def ingredient_list_size(self):
        return len(self.ingredients_with_user)


class RecipeSearchTest(unittest.TestCase):

    # should exit when 1 is entered
    def test_user_input_1(self):
        print('--> should exit when 1 is entered \n')
        result = RecipeSearch().validate_ingredients('1')
        self.assertIsNone(result)

    # should not allow numbers as ingredients
    def test_user_input_numbers(self):
        print('--> should not allow numbers as ingredients \n')
        test_data = ['3', '2', '123', '24541']
        for i in test_data:
            result = RecipeSearch().validate_ingredients(i)
            self.assertEqual(result, "Note: Only Alphabets Allowed!")

    # should not allow whitespaces
    def test_user_input_whitespace(self):
        print('--> should not allow whitespaces as ingredients \n')
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

    # should trim whitespaces from ingredient
    def test_user_input_trim_whitespace(self):
        print('--> should trim whitespaces from ingredient\n')
        test_data = ['  eggs', 'onions   ', 'loa  ves', ' p o t a t o e s ']
        expected_result = ['egg', 'onion', 'loaf', 'potato']
        for i, x in zip(test_data, expected_result):
            result = RecipeSearch().validate_ingredients(i)
            self.assertEqual(result, "You Have: {}".format(x))

    # should not include duplicate ingredients
    def test_user_input_discard_duplicates(self):
        print('--> should not include duplicate ingredients\n')
        test_data = ['eggs', 'egg', 'Apple', 'apples', 'apple']
        recipe = FakeInput()
        for i in test_data:
            recipe.validate_ingredients(i)
        self.assertEqual(recipe.ingredient_list_size(), 2)

    # should return if no recipes found for ingredients
    def test_for_no_recipe_found(self):
        print('--> should return if no recipes found for ingredients\n')
        recipe = FakeInput()
        recipe.set_fake_ingredients_with_user("kjhdliduilhig")
        self.assertEqual(recipe.search_all_popular_recipes(), "\n No recipes found for ingredients: kjhdliduilhig \n\n")

    # should return recipe and missing ingredients
    def test_if_correct_recipe_returned(self):
        print('--> should return recipe and missing ingredients\n')
        data = load_test_data_from_file('test1.json')
        test_data = ['bread', 'egg', 'milk']
        recipe = FakeInput()
        for x in test_data:
            recipe.set_fake_ingredients_with_user(x)
        a = recipe.search_individual_recipe(data)
        self.assertEqual(a[0]['recipe_id'], "35499")
        self.assertEqual(a[0]['source_url'], "http://www.closetcooking.com/2009/11/pumpkin-pie-french-toast.html")
        self.assertEqual(len(a[1]), recipe.ingredient_list_size())


def load_test_data_from_file(fixture_file):
    with open(fixture_file) as f:
        data = json.load(f)
        return data


if __name__ == "__main__":
    unittest.main()

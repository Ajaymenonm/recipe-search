import os
import yaml
import inflect
import requests
from logging import getLogger
logger = getLogger('error')
p = inflect.engine()


class RecipeSearch:

    def __init__(self):
        self.ingredients_with_user = []
        config = self.__load_secrets()
        self.api_key = os.environ['KEY'] or config['KEY']
        self.sort_by = config['SORT_TYPE']
        self.bulk_recipe_url = config['RECIPE_URL']
        self.specific_recipe_url = config['INGREDIENT_URL']
        self.table = {}

    def get_ingredients(self):
        try:
            self.__clear_data()
            while True:

                generic_instruction = '\n\n    Instructions: \n **Enter 1 to exit.** '
                print(generic_instruction if len(self.ingredients_with_user) == 0 else generic_instruction + '\n **Enter 2 to search for recipe.**')

                # get ingredients from user
                user_input = input('Please Enter Ingredient No.{0} \n'.format(len(self.ingredients_with_user) + 1))
                user_input = user_input.replace(' ', '').lower()

                if len(user_input) == 0:
                    print('No Ingredient Entered \n')

                if user_input == '1':
                    return
                elif user_input == '2' and len(self.ingredients_with_user) >= 1:
                    self.search_popular_recipes()
                    return

                """
                Entered Ingredients Acceptance Criteria:
                1. Only alphabets
                2. No whitespaces
                3. No special characters
                4. Ingredients entered one at a time
                """
                if user_input.isalpha():
                    a = p.singular_noun(user_input)
                    if a:
                        user_input = a
                    self.ingredients_with_user.append(user_input)
                    self.ingredients_with_user = list(set(self.ingredients_with_user))
                    print('You Have: ', ", ".join(reversed(self.ingredients_with_user)))
                else:
                    print('Note: Only Alphabets Allowed!')
        except Exception:
            logger.error('Exception Raised: ', exc_info=True)
        except KeyboardInterrupt:
            print('Goodbye!')

    def search_popular_recipes(self):
        try:
            ingredients = ','.join(self.ingredients_with_user)
            query_params = {
                'key': self.api_key,
                'sort': self.sort_by,
                'q': ingredients
            }

            # api request to get matching recipe list
            api_request = requests.get(self.bulk_recipe_url, params=query_params)
            data = api_request.json()

            if data['count'] == 0:
                print('\n No recipes found for ingredients {0} \n\n'.format(ingredients))

            else:
                full_ingredients = []
                already_available_ingredients = set()
                missing_ingredients = set()
                matching_ingredients = set()
                current_recipe = []

                for item in range(data['count']):

                    length_with_user = len(self.ingredients_with_user)
                    length_available = len(already_available_ingredients)

                    """
                    Return Missing Ingredients 
                    from the Most Popular Recipe
                    """
                    if length_available == length_with_user:
                        display_result(current_recipe, already_available_ingredients, missing_ingredients)
                        return

                    recipe_id = data['recipes'][item]['recipe_id']
                    query_params = {
                        'key': self.api_key,
                        'rId': recipe_id
                    }

                    # api request to get individual recipe ingredients
                    api_request = requests.get(self.specific_recipe_url, params=query_params)

                    # clear data from previous iteration
                    full_ingredients.clear()
                    already_available_ingredients.clear()
                    missing_ingredients.clear()
                    matching_ingredients.clear()

                    # parse api response
                    api_data = api_request.json()
                    current_recipe = api_data['recipe']
                    full_ingredients = api_data['recipe']['ingredients']
                    full_ingredients = [x.lower() for x in full_ingredients]
                    full_ingredients = set(full_ingredients)

                    # search missing ingredient
                    for x in self.ingredients_with_user:
                        for y in full_ingredients:
                            if x in y:
                                already_available_ingredients.add(x)
                                matching_ingredients.add(y)
                            else:
                                missing_ingredients.add(y)
                    missing_ingredients = full_ingredients - matching_ingredients

                    # for ingredient in full_ingredients:
                    #     # print(s.lower() in ingredient for s in self.ingredients_with_user)
                    #     if any(s.lower() in ingredient for s in self.ingredients_with_user):
                    #
                    #         already_available_ingredients.append(ingredient)
                    #
                    #     else:
                    #         missing_ingredients.append(ingredient)

                    self.table[recipe_id] = {}
                    self.table[recipe_id]['available_ingredients'] = already_available_ingredients
                    self.table[recipe_id]['missing_ingredients'] = missing_ingredients
                    self.table[recipe_id]['full_recipe'] = current_recipe

                """
                If not all of the ingredients entered by User found in the recipe (all individual recipes),
                return the most popular / rated with highest matching ingredient.
                """
                for item in list(self.table):
                    display_result(self.table[item]['full_recipe'], self.table[item]['available_ingredients'], self.table[item]['missing_ingredients'])
                    break
            return
            # self.get_ingredients()

        except Exception:
            logger.error('Exception Raised: ', exc_info=True)

    def __clear_data(self):
        self.ingredients_with_user.clear()
        self.table.clear()

    @staticmethod
    def __load_secrets():
        with open("secrets.yml", 'r') as ymlfile:
            config = yaml.load(ymlfile)
        return config['API_VARIABLES']


# utility method to display result
def display_result(current_recipe, already_available_ingredients, missing_ingredients):
    print('\n######################################################################')
    print('\n**{0} is the Most Popular Recipe I could find for the ingredients you have.**'.format(
        current_recipe['title']))
    print('Title: {0}\nAvailable Ingredients: {1}'.format(current_recipe['title'],
                                                          ', '.join(already_available_ingredients)))
    print('\nMissing Ingredients:')
    print('\n'.join(missing_ingredients))
    print('\nFor Cooking Instructions, Visit: {0}'.format(current_recipe['source_url']))
    print('\n######################################################################')


rs = RecipeSearch()
rs.get_ingredients()

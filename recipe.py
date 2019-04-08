import os
import yaml
import requests
from logging import getLogger
logger = getLogger('error')


class RecipeSearch:

    def __init__(self):
        self.ingredients_with_user = []
        config = self.__load_secrets()
        # self.api_key = os.environ['KEY'] or config['KEY']
        # TODO add env
        self.api_key = config['KEY']
        self.bulk_recipe_url = config['RECIPE_URL']
        self.specific_recipe_url = config['INGREDIENT_URL']
        self.table = {}

    def get_ingredients(self):
        try:
            self.__clear_data()
            while True:

                generic_instruction = '\n\n    Instructions: \n **Enter 1 to exit.** '
                print(generic_instruction if len(self.ingredients_with_user) == 0 else generic_instruction + '\n **Enter 2 to search for recipe.**')

                user_input = input('Please Enter Ingredient No.{0} \n'.format(len(self.ingredients_with_user) + 1))
                user_input = user_input.replace(' ', '').lower()

                if len(user_input) == 0:
                    print('No Ingredient Entered \n')

                if user_input == '1':
                    return
                elif user_input == '2' and len(self.ingredients_with_user) >= 1:
                    self.search_popular_recipes()
                    return

                if user_input.isalpha():
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
                'sort': 'r',
                'q': ingredients
            }

            api_request = requests.get(self.bulk_recipe_url, params=query_params)
            data = api_request.json()

            if data['count'] == 0:
                print('\n No recipes found for ingredients {0} \n\n'.format(ingredients))

            else:
                full_ingredients = []
                already_available_ingredients = set()
                missing_ingredients = set()
                matching_ingredients = set()

                for item in range(data['count']):

                    length_with_user = len(self.ingredients_with_user)
                    length_available = len(already_available_ingredients)

                    # print('length of available ==========', length_available)
                    # print('length of ing with user ==========', length_with_user)

                    '''
                    Return Missing Ingredients 
                    from the Most Popular Recipe
                    '''
                    if length_available == length_with_user:
                        print('\nMissing Ingredients:')
                        print("\n".join(missing_ingredients))
                        return

                    recipe_id = data['recipes'][item]['recipe_id']

                    query_params = {
                        'key': self.api_key,
                        'rId': recipe_id
                    }

                    api_request = requests.get(self.specific_recipe_url, params=query_params)
                    # print(api_request.json())

                    # clear data from previous iteration
                    full_ingredients.clear()
                    already_available_ingredients.clear()
                    missing_ingredients.clear()
                    matching_ingredients.clear()

                    api_data = api_request.json()
                    full_ingredients = api_data['recipe']['ingredients']

                    # self.searchIndividualRecipeIngredients(recipe_id)
                    full_ingredients = [x.lower() for x in full_ingredients]
                    full_ingredients = set(full_ingredients)
                    # for ingredient in self.ingredients_with_user:
                    # TODO: Refactor this block
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
                    self.table[recipe_id]['available_length'] = len(already_available_ingredients)
                    self.table[recipe_id]['available_ingredients'] = already_available_ingredients
                    self.table[recipe_id]['missing_ingredients'] = missing_ingredients

                    print('available  ======= {0}'.format(already_available_ingredients))
                    print('available items from recipe  ======= {0}'.format(matching_ingredients))
                    print('missing ========= {0}'.format(missing_ingredients))
                    print('table ========== {0}'.format(self.table))
                    # self.getIngredients()

                # returns highest matching one
                print('Missing Ingredients: \n')
                for item in list(self.table):
                    print('\n'.join(self.table[item]['missing_ingredients']))
                    break

            self.get_ingredients()
        # return
        except Exception:
            logger.error('Exception Raised: ', exc_info=True)

    # def searchIndividualRecipeIngredients(self, recipe_id):
    #
    #     self.full_ingredients = map(lambda x:x.lower(), self.full_ingredients)
    #     for ingredient in self.full_ingredients:
    #         # print(ingredient)
    #         if any(s.lower() in ingredient for s in self.ingredients_with_user):
    #             self.available.append(ingredient)
    #         else:
    #             self.missing_ingredients.append(ingredient)
    #
    #     self.table[recipe_id] = {}
    #     self.table[recipe_id]['available_length'] = len(self.available)
    #     self.table[recipe_id]['available_ingredients'] = self.available
    #     self.table[recipe_id]['missing_ingredients'] = self.missing_ingredients
    #
    #     print('available {0}'.format(self.available))
    #     print('missing {0}'.format(self.missing_ingredients))
    #     print('table {0}'.format(self.table))
    #     return

    def __clear_data(self):
        self.ingredients_with_user.clear()
        self.table.clear()

    def __load_secrets(self):
        with open("secrets.yml", 'r') as ymlfile:
            config = yaml.load(ymlfile)
        return config['API_VARIABLES']


rs = RecipeSearch()
rs.get_ingredients()

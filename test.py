import os
import recipe
import unittest
from unittest import mock
from unittest import TestCase
from unittest.mock import patch
import unittest.mock
from nose.tools import *
import io
# import mock
# from httmock import urlmatch, HTTMock



class RecipeSearchTest(unittest.TestCase):

    def test_handler_no_env(self):
        original_input = mock.builtins.input
        mock.builtins.input = lambda _: "yes"
        assert_equal(recipe.RecipeSearch.get_ingredients(), "you entered yes")
        mock.builtins.input = original_input



if __name__ == '__main__':
    unittest.main()
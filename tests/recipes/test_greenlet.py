import unittest
from unittest.mock import patch

from tests.recipes.recipe_ctx import RecipeCtx


class TestGreenletRecipe(RecipeCtx, unittest.TestCase):

    recipe_name = "greenlet"

    def test_get_recipe_env_sets_target_cxx_shared_linker(self):
        parent_env = {
            'CXX': (
                '/ndk/bin/aarch64-linux-android24-clang++ '
                '--target=aarch64-linux-android24'
            ),
            'LDCXXSHARED': 'clang++ -bundle -undefined dynamic_lookup',
            'CFLAGS': '-DANDROID',
        }

        with patch(
            'pythonforandroid.recipe.PyProjectRecipe.get_recipe_env',
            return_value=parent_env,
        ) as get_recipe_env:
            env = self.recipe.get_recipe_env(self.arch)

        get_recipe_env.assert_called_once_with(self.arch)
        self.assertEqual(
            env['LDCXXSHARED'],
            parent_env['CXX'] + ' -shared',
        )
        self.assertEqual(env['CFLAGS'], '-DANDROID')

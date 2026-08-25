from pythonforandroid.recipe import PyProjectRecipe


class GreenletRecipe(PyProjectRecipe):
    version = '3.5.1'
    url = 'https://pypi.python.org/packages/source/g/greenlet/greenlet-{version}.tar.gz'
    depends = ['setuptools']
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)
        env['LDCXXSHARED'] = env['CXX'] + ' -shared'
        return env


recipe = GreenletRecipe()

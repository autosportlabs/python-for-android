from pythonforandroid.recipe import PyProjectRecipe, Recipe
from os.path import exists, join


class FFPyPlayerRecipe(PyProjectRecipe):
    version = 'v4.5.1'
    url = 'https://github.com/matham/ffpyplayer/archive/{version}.zip'
    depends = ['python3', 'sdl2', 'ffmpeg']
    patches = ["setup.py.patch"]
    opt_depends = ['openssl', 'ffpyplayer_codecs']

    def get_recipe_env(self, arch, with_flags_in_cc=True):
        env = super().get_recipe_env(arch)

        build_dir = Recipe.get_recipe('ffmpeg', self.ctx).get_build_dir(arch.arch)
        env["FFMPEG_INCLUDE_DIR"] = join(build_dir, "include")
        env["FFMPEG_LIB_DIR"] = join(build_dir, "lib")

        env["SDL_INCLUDE_DIR"] = join(self.ctx.bootstrap.build_dir, 'jni', 'SDL', 'include')
        env["SDL_LIB_DIR"] = join(self.ctx.bootstrap.build_dir, 'libs', arch.arch)

        env["USE_SDL2_MIXER"] = '1'

        # ffpyplayer does not allow to pass more than one include dir for sdl2_mixer (and ATM is
        # not needed), so we only pass the first one.
        sdl2_mixer_recipe = self.get_recipe('sdl2_mixer', self.ctx)
        env["SDL2_MIXER_INCLUDE_DIR"] = sdl2_mixer_recipe.get_include_dirs(arch)[0]

        # NDKPLATFORM and LIBLINK are our switches for detecting Android platform, so can't be empty
        # FIXME: We may want to introduce a cleaner approach to this?
        env['NDKPLATFORM'] = "NOTNONE"
        env['LIBLINK'] = 'NOTNONE'

        # ffpyplayer can use libpostproc when ffmpeg provides it, but codec
        # builds do not always install the postproc header/library.
        postproc_header = join(build_dir, "include", "libpostproc", "postprocess.h")
        postproc_lib = join(build_dir, "lib", "libpostproc.so")
        if not exists(postproc_header) or not exists(postproc_lib):
            env["CONFIG_POSTPROC"] = '0'

        return env


recipe = FFPyPlayerRecipe()

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models


class FlavorPlugin(CMSPluginBase):
    model = models.Flavor
    render_template = 'plugin-flavor.html'

plugin_pool.register_plugin(FlavorPlugin)


class SundeaPlugin(CMSPluginBase):
    model = models.Sundea
    render_template = 'plugin-sundea.html'

plugin_pool.register_plugin(SundeaPlugin)


class PicturePlugin(CMSPluginBase):
    model = models.Picture
    render_template = 'plugin-picture.html'

plugin_pool.register_plugin(PicturePlugin)

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import (
    PluginModelWithFKFromModel,
    PluginModelWithM2MToModel,
    FKPluginModel,
    M2MTargetPluginModel,
    PluginModelWithFKFromPlugin,
    PluginModelWithM2MToPlugin,
)


class PluginWithFKFromModel(CMSPluginBase):
    model = PluginModelWithFKFromModel
    render_template = "cms_plugin.html"

plugin_pool.register_plugin(PluginWithFKFromModel)


class PluginWithM2MToModel(CMSPluginBase):
    model = PluginModelWithM2MToModel
    render_template = "cms_plugin.html"

plugin_pool.register_plugin(PluginWithM2MToModel)


class FKPlugin(CMSPluginBase):
    model = FKPluginModel
    render_template = "cms_plugin.html"

plugin_pool.register_plugin(FKPlugin)


class M2MTargetPlugin(CMSPluginBase):
    model = M2MTargetPluginModel
    render_template = "cms_plugin.html"

plugin_pool.register_plugin(M2MTargetPlugin)


class PluginWithFKFromPlugin(CMSPluginBase):
    model = PluginModelWithFKFromPlugin
    render_template = "cms_plugin.html"

plugin_pool.register_plugin(PluginWithFKFromPlugin)


class PluginWithM2MToPlugin(CMSPluginBase):
    model = PluginModelWithM2MToPlugin
    render_template = "cms_plugin.html"

plugin_pool.register_plugin(PluginWithM2MToPlugin)

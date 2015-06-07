from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import (
    FKModel,
    FKPluginModel,
    M2MTargetModel,
    PluginModelWithM2MToModel,
    M2MTargetPluginModel,
    PluginModelWithM2MToPlugin,
    SimplePluginModel
)


class SimplePlugin(CMSPluginBase):
    model = SimplePluginModel
    render_template = "cms_plugin.html"

plugin_pool.register_plugin(SimplePlugin)


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


class PluginWithM2MToPlugin(CMSPluginBase):
    model = PluginModelWithM2MToPlugin
    render_template = "cms_plugin.html"

plugin_pool.register_plugin(PluginWithM2MToPlugin)

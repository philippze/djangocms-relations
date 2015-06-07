import unittest

from cms import api

from .base import BaseRelationsTest

from testapp.models import (
    FKModel,
    FKPluginModel,
    M2MTargetModel,
    PluginModelWithM2MToModel,
    M2MTargetPluginModel,
    PluginModelWithM2MToPlugin,
    SimplePluginModel
)


class ClassCreation(BaseRelationsTest):
    

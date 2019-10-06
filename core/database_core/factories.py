from schematics.models import Model
from schematics.types import (IntType, StringType, ListType, ModelType)

from .database.schema import Repo as AlchemyRepo


class SQLAlchemyMixin:
    def to_alchemy(self):
        return self.alchemy_model(**self.to_native())

    @classmethod
    def from_alchemy(cls, alchemy_object):
        return cls(alchemy_object.to_dict())


class Base(Model):
    def __repr__(self):
        def filter_properties(obj):
            # this function decides which properties should be exposed through repr
            properties = obj.to_native().keys()
            for prop in properties:
                yield (prop, str(getattr(obj, prop)))
            return

        prop_tuples = filter_properties(self)
        prop_string_tuples = (": ".join(prop) for prop in prop_tuples)
        prop_output_string = " | ".join(prop_string_tuples)
        cls_name = self.__module__ + "." + self.__class__.__name__

        return "<%s('%s')>" % (cls_name, prop_output_string)


class Repo(Base, SQLAlchemyMixin):
    alchemy_model = AlchemyRepo

    id = IntType(required=True)
    name = StringType(required=True)
    stars = IntType()
    forked = IntType()
    repo_url = StringType(required=True)
    deps = ListType(ModelType('Repo'))

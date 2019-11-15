# coding=utf-8

from sqlalchemy import (Column, Integer, DateTime, Numeric, ForeignKey, Table,
                        String, DDL, FetchedValue, func, Date,
                        UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy_utils import JSONType
from sqlalchemy.orm import relationship, backref

from .utils import on_table_create


class Base(object):
    """
    a base class for all of our models, this defines:
    1) the table name to be the lower-cased version of the class name
    2) generic __init__ and __repr__ functions
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __init__(self, **kwargs):
        for key in kwargs:
            if key not in self.attr_accessor:
                raise Exception(f'Invalid Prop: {key}')
            setattr(self, key, kwargs[key])

    def to_dict(self):
        # for k, v in self.__dict__.items():
        #     print(k, v, type(v), type(v).__name__)
        #     if type(
        #             v
        #     ).__name__ == 'InstrumentedList':
        #         print('aaaaaaaaaa')
        return {
            k: v if type(v).__name__ != 'InstrumentedList' else None
            for k, v in self.__dict__.items() if not k.startswith('_')
        }

    def __repr__(self):
        def filter_properties(obj):
            # this function decides which properties should be exposed through repr
            properties = obj.__dict__.keys()
            for prop in properties:
                if prop[0] != "_" and not callable(prop):
                    yield (prop, str(getattr(obj, prop)))
            return

        prop_tuples = filter_properties(self)
        prop_string_tuples = (": ".join(prop) for prop in prop_tuples)
        prop_output_string = " | ".join(prop_string_tuples)
        cls_name = self.__module__ + "." + self.__class__.__name__

        return "<%s('%s')>" % (cls_name, prop_output_string)


Base = declarative_base(cls=Base)

dependents = Table(
    'dependencies', Base.metadata,
    Column('repo_dependent_id',
           Integer,
           ForeignKey('repo.id'),
           primary_key=True),
    Column('repo_dependency_id',
           Integer,
           ForeignKey('repo.id'),
           primary_key=True))


class Repo(Base):
    __tablename__ = 'repo'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    repo_url = Column(String, unique=True)
    stars = Column(Integer)
    forked = Column(Integer)

    # this relationship is used for persistence
    deps = relationship("Repo",
                        secondary=dependents,
                        lazy='joined',
                        primaryjoin=id == dependents.c.repo_dependent_id,
                        secondaryjoin=id == dependents.c.repo_dependency_id,
                        backref=backref('dependencies', lazy='joined'))

    def __repr__(self):
        return "Repo(%r)" % self.name

import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import ClauseElement

engine = create_engine(os.environ['DATABASE_URL'],
                       echo=True,
                       convert_unicode=True,
                       pool_size=200,
                       pool_recycle=170,
                       isolation_level="READ COMMITTED")
Session = sessionmaker(bind=engine, autoflush=False)


class DBGateway(object):
    # IMP: Keep the lifecycle of the session (and usually the transaction) *separate and external*
    @staticmethod
    @contextmanager
    def session_scope():
        """Provide a transactional scope around a series of operations."""
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_or_create(session, model, defaults=None, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.items()
                          if not isinstance(v, ClauseElement))
            params.update(defaults or {})
            instance = model(**params)
            session.add(instance)
            return instance, True

    @staticmethod
    def update_or_create(session, model, defaults=None, **kwargs):
        instance = session.query(model).filter_by(
            **kwargs).with_for_update().first()
        if instance:
            for k, v in defaults.items():
                setattr(instance, k, v)
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.items()
                          if not isinstance(v, ClauseElement))
            params.update(defaults or {})
            instance = model(**params)
            session.add(instance)
            return instance, True

    @staticmethod
    def get_for_update_or_create(session, model, defaults=None, **kwargs):
        instance = session.query(model).filter_by(
            **kwargs).with_for_update().first()
        if instance:
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.items()
                          if not isinstance(v, ClauseElement))
            params.update(defaults or {})
            instance = model(**params)
            session.add(instance)
            return instance, True

    @staticmethod
    def get_by_id(session, model, ident):
        instance = session.query(model).get(ident)
        return instance

    @staticmethod
    def get(session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        return instance

    @staticmethod
    def filter(session, model, **kwargs):
        instances = session.query(model).filter_by(**kwargs).all()
        return instances

    @staticmethod
    def filter_for_update(session, model, **kwargs):
        import pdb
        pdb.set_trace()
        instances = session.query(model).filter_by(
            **kwargs).with_for_update().all()
        return instances

    @staticmethod
    def update(session, model, ident, **kwargs):
        obj = DBGateway.get_by_id(session, model, ident)
        params = dict((k, v) for k, v in kwargs.items()
                      if not isinstance(v, ClauseElement))
        for k, v in params.items():
            setattr(obj, k, v)

    @staticmethod
    def update_all(session, model, criterion, **kwargs):
        objs = session.query(model).filter_by(**criterion).update(
            kwargs, 'fetch')
        return objs

    @staticmethod
    def get_all(session, model):
        objs = session.query(model).all()
        return objs

    @staticmethod
    def create(session, model, **kwargs):
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        session.refresh(instance)
        return instance

    @staticmethod
    def call_db_function(session, model, func_name, **params):
        raise NotImplementedError("TODO: to be implemented")

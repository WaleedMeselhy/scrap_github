import datetime
from datetime import timedelta
from database_core.factories import Repo
from decimal import Decimal
from sqlalchemy import or_, and_, desc, func
from sqlalchemy.orm import aliased
# from .database.gateway import session_scope

# from sqlalchemy.orm import with_expression
# from sqlalchemy.types.Comparator import overlaps


class DefaultRepository(object):
    model = None
    model_id_field = None

    def __init__(self, model=None, model_id_field=None):
        if model:
            self.model = model
        if model_id_field:
            self.model_id_field = model_id_field

    def get_or_create(self, gateway, defaults=None, **kwargs):
        with gateway.session_scope() as session:
            obj, created = gateway.get_or_create(session,
                                                 self.model.alchemy_model,
                                                 defaults=defaults,
                                                 **kwargs)
            obj = self.model.from_alchemy(obj) if obj else None
        return obj, created

    def get_by_id(self, gateway, ident):
        with gateway.session_scope() as session:
            obj = gateway.get_by_id(session,
                                    self.model.alchemy_model,
                                    ident=ident)
            obj = self.model.from_alchemy(obj) if obj else None
        return obj

    def get(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            obj = gateway.get(session, self.model.alchemy_model, **kwargs)
            obj = self.model.from_alchemy(obj) if obj else None
        return obj

    def filter(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            objs = gateway.filter(session, self.model.alchemy_model, **kwargs)
            objs = list(map(lambda obj: self.model.from_alchemy(obj), objs))
        return objs

    def get_all(self, gateway):
        with gateway.session_scope() as session:
            objs = gateway.get_all(session, self.model.alchemy_model)
            objs = list(map(lambda obj: self.model.from_alchemy(obj), objs))
        return objs

    def update(self, gateway, obj, **kwargs):
        with gateway.session_scope() as session:
            obj = gateway.update(session, self.model.alchemy_model,
                                 getattr(obj, self.model_id_field), **kwargs)
            obj = self.model.from_alchemy(obj) if obj else None
        return obj

    def update_all(self, gateway, criterion, **kwargs):
        with gateway.session_scope() as session:
            ids = gateway.update_all(session, self.model.alchemy_model,
                                     criterion, **kwargs)
            # objs = list(map(lambda obj: self.model.from_alchemy(obj), objs))
        return ids

    def create(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            obj = gateway.create(session, self.model.alchemy_model, **kwargs)
            obj = self.model.from_alchemy(obj)
        return obj


class RepoRepository(DefaultRepository):
    model = Repo
    model_id_field = 'id'

    def create(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            kwargs.pop('deps', None)
            repo = gateway.create(session, self.model.alchemy_model, **kwargs)
            session.refresh(repo)
            obj = self.model.from_alchemy(repo)
        return obj

    # def get_or_create(self, gateway, defaults=None, **kwargs):
    #     raise NotImplementedError("TODO: to be implemented")

    def add_dependant(self, gateway, repo_id, dep):
        with gateway.session_scope() as session:
            repo = gateway.get_by_id(session, self.model.alchemy_model,
                                     repo_id)
            dep_repo = gateway.get(session,
                                   self.model.alchemy_model,
                                   name=dep['name'])
            if dep_repo is None:
                dep.pop('deps', None)
                dep_repo = gateway.create(session, self.model.alchemy_model,
                                          **dep)
            dep_repo.deps.append(repo)

    def get_repos_depends_on_repos(self,
                                   gateway,
                                   repos_names,
                                   stars=0,
                                   forked=0):
        repo_model = self.model.alchemy_model
        repoalias = aliased(repo_model)
        with gateway.session_scope() as session:
            repos = session.query(repo_model).join(
                repoalias, repo_model.deps).filter(
                    repoalias.name.in_(repos_names)).group_by(
                        repo_model.id).having(
                            func.count(repo_model.id) > (
                                len(repos_names) - 1)).distinct(
                                    repo_model.name).filter(
                                        repo_model.stars >= stars,
                                        repo_model.forked >= forked).all()
            repos = [self.model.from_alchemy(repo) for repo in repos]
            return repos

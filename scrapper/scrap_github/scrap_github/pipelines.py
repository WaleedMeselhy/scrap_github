from database_core.database.gateway import DBGateway
from database_core.factories import Repo
from database_core.repositories import RepoRepository
from datetime import datetime
from schematics.exceptions import ValidationError, DataError
from sqlalchemy.exc import IntegrityError
import logging
from contextlib import suppress

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapGithubPipeline(object):
    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.repo_repository = RepoRepository()
        self.repo, created = self.repo_repository.get_or_create(DBGateway,
                                                                defaults=None,
                                                                name=repo_name)
        if created:
            # to get id
            self.repo = self.repo_repository.get_or_create(DBGateway,
                                                           defaults=None,
                                                           name=repo_name)[0]

    @classmethod
    def from_crawler(cls, crawler):
        repo_name = getattr(crawler.spider, 'repo_name')
        return cls(repo_name)

    def process_item(self, item, spider):
        dependant_repo = Repo(item)
        with suppress(IntegrityError):
            self.repo_repository.add_dependant(DBGateway,
                                               repo_id=self.repo.id,
                                               dep=dependant_repo.to_native())

        return item

from database_core.database.gateway import DBGateway
from database_core.factories import Repo
from database_core.repositories import RepoRepository
from datetime import datetime
from schematics.exceptions import ValidationError, DataError
from sqlalchemy.exc import IntegrityError
import logging
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapGithubPipeline(object):
    def __init__(self):
        self.repo_repository = RepoRepository()

    def process_item(self, item, spider):
        logging.log(logging.WARNING, "aa")
        logging.log(logging.WARNING, str(type(item)))
        logging.log(logging.WARNING, str(item))
        repo = Repo(item)
        self.repo_repository.create(DBGateway, **repo.to_native())

        return item

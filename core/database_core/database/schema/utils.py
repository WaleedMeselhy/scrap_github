from functools import partial

from sqlalchemy import Table
from sqlalchemy.event import listen

# from sqlalchemy.ext.compiler import compiles
# from sqlalchemy.sql import ClauseElement
# from sqlalchemy.sql.expression import _literal_as_binds, _CompareMixin
# from sqlalchemy.types import NullType


def on_table_create(class_, ddl):
    def listener(tablename, ddl, table, bind, **kw):
        if table.name == tablename:
            ddl(table, bind, **kw)

    listen(Table, 'after_create', partial(listener, class_.__table__.name,
                                          ddl))


# class TupleClause(ClauseElement, _CompareMixin):
#     def __init__(self, *columns):
#         self.columns = [_literal_as_binds(col) for col in columns]
#         self.type = NullType()
#
#
# @compiles(TupleClause)
# def compile_tupleclause(element, compiler, **kw):
#     return "(%s)" % ", ".join(compiler.process(col) for col in
#                               element.columns)
#
#
# # Usage:
# def overlaps(a_pair, b_pair):
#     return TupleClause(*a_pair).op('OVERLAPS')(TupleClause(*b_pair))

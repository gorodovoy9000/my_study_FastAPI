from pydantic import BaseModel
from sqlalchemy import delete, insert, Table


def add_bulk_to_table(table: Table, bulk_data: list[BaseModel]):
    stmt = insert(table).values([schema.model_dump() for schema in bulk_data])
    return stmt


def delete_bulk_to_table(table: Table, *filters):
    stmt = delete(table).filter(*filters)
    return stmt

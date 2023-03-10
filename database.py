from franz.openrdf.repository import Repository
from franz.openrdf.sail import AllegroGraphServer
from fastapi import UploadFile
from typing import Optional
import settings

server = AllegroGraphServer(
    host=settings.HOST, port=settings.PORT,
    user=settings.USER, password=settings.PASSWORD
)

catalog = server.openCatalog(settings.CATALOG_NAME)

repository = catalog.getRepository(settings.REPOSITORY_NAME, Repository.ACCESS)


def add_file_to_rep(filename: str):
    with repository.getConnection() as connection:
        connection.addFile(settings.OWL_FILES_STORAGE + filename)


async def write_file(file: Optional[UploadFile]) -> bool:
    if file is None:
        return False

    with open(settings.OWL_FILES_STORAGE + file.filename, "wb") as created_file:
        content = await file.read()
        created_file.write(content)
        created_file.close()
        add_file_to_rep(file.filename)

    return True


def execute_get_query(subject="?s", relation="?r", object="?o"):
    """select query for get endpoints"""
    query_string = "SELECT ?s ?r ?o WHERE {%s %s %s}" % (subject, relation, object)
    result_list = []

    with repository.getConnection() as connection:
        result = connection.executeTupleQuery(
            query=query_string
        )

        with result:
            for bindung_set in result:
                result_list.append(
                    {
                        "subject": bindung_set.getValue('s').__str__(),
                        "relation": bindung_set.getValue('r').__str__(),
                        "object": bindung_set.getValue('o').__str__()
                    }
                )

    return result_list


def execute_post_query(subject, relation, object):
    string_query = "INSERT DATA { %s %s %s}" % (subject, relation, object)

    with repository.getConnection() as connection:
        return connection.executeUpdate(
            query=string_query
        )


def execute_delete_query(subject, predicate, object):
    string_query = "DELETE DATA { %s %s %s }" % (subject, predicate, object)

    with repository.getConnection() as connection:
        return connection.executeUpdate(
            query=string_query
        )



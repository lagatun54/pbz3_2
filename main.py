import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from starlette import status
from typing import Optional
import database

app = FastAPI()


@app.post("/file/upload/")
async def root(file: Optional[UploadFile] = File(...)):
    await database.write_file(file)

    return JSONResponse(
        content={"filename": file.filename},
        status_code=status.HTTP_200_OK
    )


@app.get("/class/")
async def get_classes():
    content = []

    query_result = database.execute_get_query(
        relation="rdf:type", object="owl:Class"
    )

    for item in query_result:
        content.append(item["subject"])

    return JSONResponse(
        content={"data": content},
        status_code=status.HTTP_200_OK
    )


@app.get("/subclasses/")
async def get_subclasses():
    content = []

    query_result = database.execute_get_query(
        relation="rdfs:subClassOf"
    )

    for item in query_result:
        content.append(
            {
                "subclass": item["subject"],
                "parent": item["object"]
            }
        )

    return JSONResponse(
        content=content,
        status_code=status.HTTP_200_OK
    )


@app.get("/object_property/")
async def get_object_property():
    content = []

    query_result = database.execute_get_query(
        relation="rdf:type", object="owl:ObjectProperty"
    )

    for item in query_result:
        content.append(item['subject'])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content
    )


@app.get("/data_property/")
async def get_data_properties():
    content = []

    query_result = database.execute_get_query(
        relation="rdf:type", object="owl:DatatypeProperty"
    )

    for item in query_result:
        content.append(item['subject'])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content
    )


@app.post("/data_property/create/")
async def create_data_property(data_property):
    """create a data property"""
    if database.execute_post_query(f"<{data_property}>", "rdf:type", "owl:DatatypeProperty"):
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={}
        )

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={})


@app.post("/data_property/connect/")
async def add_data_property_to_class(subject, data_property, object_class):
    """connect data property with class"""
    if database.execute_post_query(f"<{subject}>", f"<{data_property}>", f"<{object_class}>"):
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={}
        )

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={})


@app.post("/object_property/create/")
async def create_object_property(object_property):
    """create a object property"""
    if database.execute_post_query(f"<{object_property}>", "rdf:type", "owl:ObjectProperty"):
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={}
        )

    return JSONResponse(content={}, status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/subclass/create/")
async def create_subclass(classname, parent):
    """create a subclass"""
    if database.execute_post_query(f"<{classname}>", "rdfs:subClassOf", f"<{parent}>"):
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={}
        )

    return JSONResponse(content={}, status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/classes/create/")
async def create_class(classname):
    """create a class"""
    if database.execute_post_query(f"<{classname}>", "rdf:type", "owl:Class"):
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={}
        )

    return JSONResponse(content={}, status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/instance/create/")
async def create_instance(instance_name, instance_type):
    """create instance"""
    if database.execute_post_query(f"<{instance_name}>", "rdf:type", "owl:NamedIndividual"):
        database.execute_post_query(f"<{instance_name}>", "rdf:type", f"owl:{instance_type}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={}
        )

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={})


@app.delete("/data_property/delete/")
async def delete_data_property(object_property):
    database.execute_delete_query(f":{object_property}", "rdf:type", "owl:ObjectProperty")

    return JSONResponse(
        content={"result": "property was deleted"},
        status_code=status.HTTP_204_NO_CONTENT
    )


@app.delete("/class/delete")
async def delete_class(subject_class):
    """delete class"""
    if database.execute_delete_query(f"<{subject_class}>", "rdf:type", "owl:Class"):
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={}
        )

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={})


@app.delete("/subclasses/delete")
async def delete_subclass(subclass_name, parent):
    """delete class"""
    if database.execute_delete_query(f"<{subclass_name}>", "rdfs:subClassOf", f"<{parent}>"):
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={}
        )

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={})


@app.post("/class/rename/")
async def rename_class(classname, new_name):
    database.execute_delete_query(f"<{classname}>", "rdf:type", "owl:Class")
    database.execute_post_query(f"<{new_name}>", "rdf:type", "owl:Class")

    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@app.post("/instance/rename")
async def rename_instance(instance_name, new_name):
    database.execute_delete_query(f"<{instance_name}>", "rdf:type", "owl:NamedIndividual")
    database.execute_post_query(f"<{new_name}>", "rdf:type", "owl:NamedIndividual")

    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@app.delete("/object_property/delete/")
async def delete_object_property(object_property):
    """delete object property"""
    if database.execute_delete_query(f":{object_property}", "rdf:type", "owl:ObjectProperty"):
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={}
        )

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={})


def runserver(host="localhost", port=8888):
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        lifespan="on",
    )


if __name__ == "__main__":
    runserver()

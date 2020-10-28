from starlette.applications import Starlette
from starlette.responses import Response, PlainTextResponse, StreamingResponse, FileResponse
from starlette.routing import Route
from tempfile import NamedTemporaryFile
import time
import databases
import sqlalchemy


def create_test_database(DATABASE_URL):
    engine = sqlalchemy.create_engine(DATABASE_URL)
    engine.execute("DROP TABLE IF EXISTS notes;")
    metadata = sqlalchemy.MetaData()
    sqlalchemy.Table(
        "notes",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("text", sqlalchemy.String),
        sqlalchemy.Column("completed", sqlalchemy.Boolean),
    )
    metadata.create_all(engine)


DATABASE_URL = "sqlite:///test.db"
create_test_database(DATABASE_URL)

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata = sqlalchemy.MetaData(bind=engine, reflect=True)
notes_table = metadata.tables["notes"]


async def homepage(request):
    if "sleep" in request.query_params and request.query_params["sleep"]:
        time.sleep(3)
    response = "Success"
    return PlainTextResponse(response)


async def success(request):
    response = "Success"
    return PlainTextResponse(response)


async def create(request):
    response = "Created"
    return Response(response, status_code=201, headers=None, media_type=None)


async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Server error")


async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    response = "Server error"
    return PlainTextResponse(response)


def stream_response():
    yield b"streaming"


async def stream(request):
    return StreamingResponse(stream_response())


async def file(request):
    with NamedTemporaryFile(delete=False) as fp:
        fp.write(b"Datadog says hello!")
        fp.flush()
        return FileResponse(fp.name)


async def get_tables(request):
    response = engine.table_names()
    return PlainTextResponse(str(response))


async def list_notes(request):
    query = "SELECT * FROM NOTES"
    with engine.connect() as connection:
        result = connection.execute(query)
        d, a = {}, []
        for rowproxy in result:
            for column, value in rowproxy.items():
                d = {**d, **{column: value}}
            a.append(d)
    response = str(a)
    return PlainTextResponse(response)


async def add_note(request):
    request_json = await request.json()
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(notes_table.select())
            connection.execute(notes_table.insert(), request_json)
    response = "Success"
    return PlainTextResponse(response)


def get_app():
    routes = [
        Route("/", endpoint=homepage, name="homepage", methods=["GET"]),
        Route("/200", endpoint=success, name="200", methods=["GET"]),
        Route("/201", endpoint=create, name="201", methods=["POST"]),
        Route("/500", endpoint=error, name="500", methods=["GET"]),
        Route("/stream", endpoint=stream, name="stream", methods=["GET"]),
        Route("/file", endpoint=file, name="file", methods=["GET"]),
        Route("/users/{userid:int}", endpoint=success, name="path_params", methods=["GET"]),
        Route("/users/{userid:int}/info", endpoint=success, name="multi_path_params", methods=["GET"]),
        Route("/users/{userid:int}/{attribute:str}", endpoint=success, name="multi_path_params", methods=["GET"]),
        Route("/tables", endpoint=get_tables, name="tables", methods=["GET"]),
        Route("/notes", endpoint=list_notes, methods=["GET"]),
        Route("/notes", endpoint=add_note, methods=["POST"]),
    ]
    app = Starlette(routes=routes, on_startup=[database.connect], on_shutdown=[database.disconnect])
    return app

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from src import api
from src.core import config, db
# from src.core.extensions import configure_extensions
from src.core.logging import logger
from src.middlewares.exception import ExceptionMiddleware
from src.middlewares.time import TimeMiddleware
from src.services.auth import flows as auth_flows

if os.name != "nt":
    import uvloop  # noqa

    uvloop.install()

# configure_extensions()


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with db.async_session_maker() as session:
        await auth_flows.create_first_superuser(session)
    logger.info("Application... Online!")
    yield


async def not_found(request: Request, _: Exception):
    return ORJSONResponse(status_code=404, content={"detail": [{"msg": "Not Found"}]})


exception_handlers = {404: not_found}


app = FastAPI(
    openapi_url="",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    debug=config.app.debug,
    exception_handlers=exception_handlers,
)
app.add_middleware(ExceptionMiddleware)
# app.add_middleware(SentryAsgiMiddleware)
app.add_middleware(TimeMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)

api_app = FastAPI(
    title="DudeDuck CRM Backend",
    root_path="/api/v1",
    debug=config.app.debug,
    default_response_class=ORJSONResponse,
    exception_handlers=exception_handlers,
)
api_app.add_middleware(ExceptionMiddleware)
api_app.include_router(api.router)


@api_app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return ORJSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "msg": jsonable_encoder(exc.errors(), exclude={"url", "type", "ctx"}),
                    "code": "unprocessable_entity",
                }
            ]
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.app.cors_origins if config.app.cors_origins else ["http://localhost", "http://localhost:3000", "http://192.168.1.88:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
)


if config.app.use_correlation_id:
    from src.middlewares.correlation import CorrelationMiddleware

    app.add_middleware(CorrelationMiddleware)

app.mount("/api/v1", app=api_app)

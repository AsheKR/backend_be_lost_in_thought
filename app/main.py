import os

import click
import uvicorn
from core.config import Env, EnvironmentKey, get_config


@click.command()
@click.option(
    "--env",
    type=click.Choice([Env.local, Env.development, Env.production], case_sensitive=False),
)
@click.option(
    "--debug",
    type=click.BOOL,
)
def main(env: str | None, debug: bool | None) -> None:
    if env is not None:
        os.environ[EnvironmentKey.env] = env

    if debug is not None:
        os.environ[EnvironmentKey.debug] = str(debug)

    config = get_config()
    uvicorn.run(
        app="api.server:fast_api",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != Env.production else False,
        workers=1,
    )


if __name__ == "__main__":
    main()

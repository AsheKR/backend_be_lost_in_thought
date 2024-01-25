import os

import click
import uvicorn

from core.config import Env, EnvironmentKey, get_config


@click.command()
@click.option(
    "--env",
    type=click.Choice([Env.local, Env.development, Env.production], case_sensitive=False),
    default="local",
)
@click.option(
    "--debug",
    type=click.BOOL,
    default=False,
)
def main(env: str, debug: bool):
    os.environ[EnvironmentKey.env] = env
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

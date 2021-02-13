#! /usr/bin/env python3

import argparse

from abc import abstractmethod
from pathlib import Path

from jinja2 import Template

# ------------------------------------------------------------------------------

REPO_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------

EnvLike = dict[str, str]


class Env:

    def __init__(self, env: EnvLike) -> None:
        self._env = env

    @staticmethod
    def from_file(path: Path) -> "Env":
        env: EnvLike = {}

        with open(path, "r") as f:
            for line in f:
                # Empty line
                if not line.strip():
                    continue

                # Comment
                if line.lstrip().startswith("#"):
                    continue

                key, value = line.rstrip().split("=", maxsplit=1)
                env[key] = value

        return Env(env)

    # Bracket operator: `env[key]`
    def __getitem__(self, key) -> str:
        if key not in self._env:
            self._env[key] = input(f"Enter value for ${key}: ")

        return self._env[key]


# ------------------------------------------------------------------------------


def _render_template(src: Path, dst: Path, ctx: EnvLike) -> None:
    with open(src, "r") as f:
        template = Template(f.read())
    rendered = template.render(ctx)
    with open(dst, "w") as f:
        f.write(rendered)


class Service:

    def __init__(self, env: Env) -> None:
        self._env = env

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def generate_config(self) -> None:
        pass


class NginxService(Service):

    def name(self) -> str:
        return "nginx"

    def generate_config(self) -> None:
        ctx = {
            "historian_port": self._env["HISTORIAN_PORT"],
        }
        _render_template(
            src=REPO_DIR / "nginx" / "templates" / "nginx.conf",
            dst=REPO_DIR / "nginx" / "generated" / "nginx.conf",
            ctx=ctx,
        )


# ------------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate services configs")

    parser.add_argument(
        "service",
        help="Name of service to generate config for",
        metavar="SERVICE",
        type=str,
        nargs="+",
    )
    parser.add_argument(
        "--env-file",
        help="Path to env file",
        dest="env_file_path",
        default=REPO_DIR / ".env",
        type=str,
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    env = Env.from_file(args.env_file_path)

    services = [
        NginxService(env),
    ]

    for service in services:
        print(f"Generating config for `{service.name()}` ...", end=" ")
        service.generate_config()
        print("done")


if __name__ == "__main__":
    main()

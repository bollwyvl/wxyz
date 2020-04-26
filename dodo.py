""" wxyz top-level automation
"""
from doit.tools import result_dep

from _scripts import _paths as P
from _scripts import _util as U

PY_LINT_CMDS = [
    ["isort", "-rc"],
    ["black", "--quiet"],
    ["flake8", "--max-line-length", "88"],
    ["pylint"],
]

DOIT_CONFIG = {
    "backend": "sqlite3",
}


def task_setup():
    """ make all the setups
    """
    yield dict(
        name="ts",
        file_dep=[*P.TS_PACKAGE, P.ROOT_PACKAGE],
        targets=[P.YARN_INTEGRITY, P.YARN_LOCK],
        actions=[["jlpm", "--prefer-offline"], ["jlpm", "lerna", "bootstrap"]],
    )

    if P.RUNNING_IN_CI:
        yield dict(
            name="py_wheels",
            file_dep=P.WHEELS,
            actions=[[P.PY, "-m", "pip", "install", *P.WHEELS]],
        )
    else:
        for i, setup_py in enumerate(P.PY_SETUP):
            pkg = setup_py.parent

            uptodate = {}

            if i:
                uptodate["uptodate"] = [
                    result_dep(f"setup:py_{P.PY_SETUP[i-1].parent.name}")
                ]

            yield dict(
                name=f"py_{pkg.name}",
                file_dep=[setup_py, pkg / "setup.cfg"],
                targets=[P.SITE_PKGS / f"{pkg.name}.egg-link".replace("_", "-")],
                actions=[
                    [
                        P.PY,
                        "-m",
                        "pip",
                        "install",
                        "-e",
                        str(pkg),
                        "--ignore-installed",
                        "--no-deps",
                    ]
                ],
                **uptodate,
            )


def task_lint():
    """ make all the linters
    """
    uptodate = dict(uptodate=[result_dep("setup")])
    yield dict(
        name="prettier",
        file_dep=P.ALL_PRETTIER,
        actions=[["jlpm", "lint"]],
        **uptodate,
    )

    groups = {
        i.parent.name: [i, *sorted((i.parent / "src").rglob("*.py"))]
        for i in P.PY_SETUP
    }

    groups["misc"] = [P.DODO, *P.SCRIPTS.glob("*.py")]

    for label, files in groups.items():
        actions = [cmd + files for cmd in PY_LINT_CMDS]
        yield dict(name=label, file_dep=files, actions=actions, **uptodate)


def _one_pydist(pkg, file_dep, output):
    """ build a single task so we can run in the cwd
    """
    name = f"{output}_{pkg.name}"
    args = [P.PY, "setup.py", output, "--dist-dir", P.DIST / output]
    actions = [lambda: U.call(args, cwd=pkg) == 0]
    return dict(name=name, file_dep=file_dep, actions=actions)


def task_pydist():
    """ build python release artifacts
    """
    for setup_py in P.PY_SETUP:
        pkg = setup_py.parent
        file_dep = [
            setup_py,
            pkg / "setup.cfg",
            *sorted((pkg / "src").rglob("*.py")),
        ]
        for output in ["sdist", "bdist_wheel"]:
            yield _one_pydist(pkg, file_dep, output)


def task_ts():
    """ build typescript components
    """
    return dict(
        file_dep=[P.YARN_LOCK, *P.TS_PACKAGE],
        targets=[*P.TS_TARBALLS],
        actions=[["jlpm", "build"]],
        uptodate=[result_dep("lint:prettier")],
    )


def task_nbtest():
    """ smoke test all notebooks with nbconvert
    """
    return dict(
        file_dep=[*P.ALL_SRC_PY, *P.ALL_IPYNB],
        actions=[
            lambda: U.call(
                [P.PY, "-m", "pytest", "-vv"], cwd=P.PY_SRC / "wxyz_notebooks"
            )
            == 0
        ],
        uptodate=[result_dep("lint:prettier")],
    )


def task_lab():
    """ set up local jupyterlab
    """
    jpy = [P.PY, "-m", "jupyter"]
    app_dir = ["--debug", "--app-dir", P.LAB]

    yield dict(
        name="extensions",
        file_dep=[*P.TS_PACKAGE],
        actions=[
            [
                *jpy,
                "labextension",
                "install",
                *P.ALL_LABEXTENSIONS,
                "--no-build",
                *app_dir,
            ]
        ],
        uptodate=[result_dep("ts")],
    )

    yield dict(
        name="build",
        actions=[
            [*jpy, "lab", "build", "--dev-build=False", "--minimize=True", *app_dir]
        ],
        uptodate=[result_dep("lab:extensions")],
    )

    yield dict(
        name="list", actions=[[*jpy, "labextension", "list", *app_dir]],
    )


def task_robot():
    """ test in browser with robot framework
    """
    atest = [P.PY, "-m", "_scripts._atest"]

    yield dict(
        name="dryrun",
        file_dep=[*P.ALL_ROBOT, *P.ALL_SRC_PY, *P.ALL_TS],
        uptodate=[result_dep("lab:build")],
        actions=[[*atest, "--dryrun"]],
    )

    yield dict(
        name="firefox",
        file_dep=[*P.ALL_ROBOT, *P.ALL_SRC_PY, *P.ALL_TS],
        uptodate=[result_dep("robot:dryrun")],
        actions=[[*atest]],
    )

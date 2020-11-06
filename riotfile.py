from riot import Suite, Case

global_deps = [
    "mock",
    "pytest<4",
    "opentracing",
]

global_env = [("PYTEST_ADDOPTS", "--color=yes")]

suites = [
    Suite(
        name="black",
        command="black --check .",
        cases=[
            Case(
                pys=[3.8],
                pkgs=[
                    ("black", ["==20.8b1"]),
                ],
            ),
        ],
    ),
    Suite(
        name="flake8",
        command="flake8 ddtrace/ tests/",
        cases=[
            Case(
                pys=[3.8],
                pkgs=[
                    ("flake8", [">=3.8,<3.9"]),
                    ("flake8-blind-except", [""]),
                    ("flake8-builtins", [""]),
                    ("flake8-docstrings", [""]),
                    ("flake8-logging-format", [""]),
                    ("flake8-rst-docstrings", [""]),
                    ("pygments", [""]),
                ],
            ),
        ],
    ),
    Suite(
        name="tracer",
        command="pytest tests/tracer/",
        cases=[
            Case(
                pys=[
                    2.7,
                    3.5,
                    3.6,
                    3.7,
                    3.8,
                    3.9,
                ],
                pkgs=[("msgpack", [""])],
            ),
        ],
    ),
    Suite(
        name="pymongo",
        command="pytest tests/contrib/pymongo",
        cases=[
            Case(
                pys=[
                    2.7,
                    3.5,
                    3.6,
                    3.7,
                ],
                pkgs=[
                    (
                        "pymongo",
                        [
                            ">=3.0,<3.1",
                            ">=3.1,<3.2",
                            ">=3.2,<3.3",
                            ">=3.3,<3.4",
                            ">=3.4,<3.5",
                            ">=3.5,<3.6",
                            ">=3.6,<3.7",
                            ">=3.7,<3.8",
                            ">=3.8,<3.9",
                            ">=3.9,<3.10",
                            ">=3.10,<3.11",
                            "",
                        ],
                    ),
                    ("mongoengine", [""]),
                ],
            ),
            Case(
                pys=[
                    3.8,
                    3.9,
                ],
                pkgs=[
                    (
                        "pymongo",
                        [
                            ">=3.0,<3.1",
                            ">=3.1,<3.2",
                            ">=3.2,<3.3",
                            ">=3.3,<3.4",
                            ">=3.5,<3.6",
                            ">=3.6,<3.7",
                            ">=3.7,<3.8",
                            ">=3.8,<3.9",
                            ">=3.9,<3.10",
                            ">=3.10,<3.11",
                            "",
                        ],
                    ),
                    ("mongoengine", [""]),
                ],
            ),
        ],
    ),
    Suite(
        name="requests",
        command="pytest tests/contrib/requests",
        cases=[
            Case(
                pys=[2.7, 3.5, 3.6, 3.7, 3.8, 3.9,],
                pkgs=[
                    ("requests-mock", [">=1.4"]),
                    (
                        "requests",
                        [
                            ">=2.8,<2.9",
                            ">=2.10,<2.11",
                            ">=2.12,<2.13",
                            ">=2.14,<2.15",
                            ">=2.16,<2.17",
                            ">=2.18,<2.19",
                            ">=2.20,<2.21",
                            "",
                        ],
                    ),
                ],
            ),
        ],
    ),
    Suite(
        name="requests_gevent",
        command="pytest tests/contrib/requests/test_requests_gevent.py",
        cases=[
            Case(
                env=[("TEST_GEVENT", "1")],
                pys=[3.6],
                pkgs=[
                    ("requests-mock", [">=1.4"]),
                    (
                        "requests",
                        [
                            ">=2.8,<2.9",
                            ">=2.10,<2.11",
                            ">=2.12,<2.13",
                            ">=2.14,<2.15",
                            ">=2.16,<2.17",
                            ">=2.18,<2.19",
                            ">=2.20,<2.21",
                            "",
                        ],
                    ),
                    ("gevent", [">=1.2,<1.3", ">=1.3,<1.4"]),
                ],
            ),
            Case(
                env=[("TEST_GEVENT", "1")],
                pys=[3.7, 3.8],
                pkgs=[
                    ("requests-mock", [">=1.4"]),
                    (
                        "requests",
                        [
                            ">=2.8,<2.9",
                            ">=2.10,<2.11",
                            ">=2.12,<2.13",
                            ">=2.14,<2.15",
                            ">=2.16,<2.17",
                            ">=2.18,<2.19",
                            ">=2.20,<2.21",
                            "",
                        ],
                    ),
                    ("gevent", [">=1.3,<1.4"]),
                ],
            ),
        ],
    ),
    Suite(
        name="requests_autopatch",
        command="pytest tests/contrib/requests",
        cases=[
            Case(
                pys=[2.7, 3.5, 3.6, 3.7, 3.8, 3.9],
                pkgs=[("tornado", [">=4.4,<4.5", ">=4.5,<4.6"])],
            ),
        ],
    ),
]

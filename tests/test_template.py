import subprocess
import sys

import pytest
from cookiecutter.exceptions import CookiecutterException
from cookiecutter.main import cookiecutter


def sanity_check_project(proj_path):
    """Sanity-check a generated project (linters, tests, doc generation)."""
    try:
        subprocess.check_output(
            "poetry install --with docs".split(), cwd=proj_path, stderr=subprocess.PIPE
        )
        subprocess.check_output(
            "poetry run poe lint --all-files".split(),
            cwd=proj_path,
            stderr=subprocess.PIPE,
        )
        subprocess.check_output(
            "poetry run poe test".split(), cwd=proj_path, stderr=subprocess.PIPE
        )
        subprocess.check_output(
            "poetry run poe docs".split(), cwd=proj_path, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        print("exit code: {}".format(e.returncode))
        print("stderr: {}".format(e.stderr.decode(sys.getfilesystemencoding())))


@pytest.fixture
def gen(tmp_path_factory):
    """Fixture to generate a project and return resulting directory.

    Project is generated in a tempdir and cleaned up after completing the tests.

    Any passed kwargs are passed through to cookiecutter (e.g. a config).
    """

    def gen_project(**cc_args):
        out_dir = tmp_path_factory.mktemp("gen_proj")
        out_dir_raw = tmp_path_factory.mktemp("gen_proj_raw")

        # NOTE: once 2.1.2 is out with keep_project_on_failure,
        # this can be simplified
        # instantiate without hooks (for debugging)
        cookiecutter(
            template="./",
            no_input=True,
            output_dir=out_dir_raw,
            accept_hooks=False,
            **cc_args,
        )

        # actual project generation (with hooks)
        try:
            cookiecutter(template="./", no_input=True, output_dir=out_dir, **cc_args)
        except CookiecutterException as e:
            print(f"DEBUG DIR (without hook evaluation): {out_dir_raw}")
            raise e

        # should be unique directory
        paths = list(out_dir.iterdir())
        assert len(paths) == 1
        proj_path = paths[0]
        assert proj_path.is_dir()

        # return path e.g. for extra tests on generated project
        return proj_path

    return gen_project


def test_cookiecutter(gen):
    DEMO_PROJ_SLUG = "metador_my_extension_name"

    # generate with default values
    dir = gen()
    sanity_check_project(dir)
    # should NOT have the demo code files
    assert not (dir / f"src/{DEMO_PROJ_SLUG}api.py").is_file()
    assert not (dir / f"src/{DEMO_PROJ_SLUG}/cli.py").is_file()
    assert not (dir / "tests/test_api.py").is_file()
    assert not (dir / "tests/test_cli.py").is_file()
    # should have schema
    assert (dir / f"src/{DEMO_PROJ_SLUG}/schemas.py").is_file()

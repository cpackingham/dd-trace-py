import os
import subprocess
import sys

import pytest

from tests import TracerTestCase


@pytest.mark.skipif("TEST_GEVENT" not in os.environ, reason="Only relevant with gevent installed")
class TestRequestsGevent(TracerTestCase):
    def test_patch(self):
        # Since this test depends on import ordering it is run in a separate
        # process with a fresh interpreter.
        p = subprocess.Popen(
            [sys.executable, "tests/contrib/requests/run_test.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        p.wait()

        assert p.stdout.read() == b"Test succeeded\n", p.stderr.read()

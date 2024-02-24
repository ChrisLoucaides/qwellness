import os
import django
from django.conf import settings
from django.test.utils import get_runner

os.environ['DJANGO_SETTINGS_MODULE'] = 'qwellness.settings'
django.setup()


def run_tests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    apps = ['user_management']
    failures = test_runner.run_tests(apps)
    return failures


if __name__ == "__main__":
    failures = run_tests()
    if failures:
        print("Some tests failed!")
    else:
        print("All tests passed!")

import os
import django
from django.conf import settings
from django.test.utils import get_runner
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

os.environ['DJANGO_SETTINGS_MODULE'] = 'qwellness.settings'
django.setup()


def run_tests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    apps = ['user_management', 'task_management', 'meeting_management']
    failures = test_runner.run_tests(apps)
    return failures


if __name__ == "__main__":
    passed = """
 █████╗ ██╗     ██╗         ████████╗███████╗███████╗████████╗███████╗    ██████╗  █████╗ ███████╗███████╗███████╗██████╗ ██╗
██╔══██╗██║     ██║         ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝    ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗██║
███████║██║     ██║            ██║   █████╗  ███████╗   ██║   ███████╗    ██████╔╝███████║███████╗███████╗█████╗  ██║  ██║██║
██╔══██║██║     ██║            ██║   ██╔══╝  ╚════██║   ██║   ╚════██║    ██╔═══╝ ██╔══██║╚════██║╚════██║██╔══╝  ██║  ██║╚═╝
██║  ██║███████╗███████╗       ██║   ███████╗███████║   ██║   ███████║    ██║     ██║  ██║███████║███████║███████╗██████╔╝██╗
╚═╝  ╚═╝╚══════╝╚══════╝       ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝    ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═════╝ ╚═╝
"""
    failed = """
████████╗███████╗███████╗████████╗ ██╗███████╗██╗         ███████╗ █████╗ ██╗██╗     ███████╗██████╗ 
╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔╝██╔════╝╚██╗        ██╔════╝██╔══██╗██║██║     ██╔════╝██╔══██╗
   ██║   █████╗  ███████╗   ██║   ██║ ███████╗ ██║        █████╗  ███████║██║██║     █████╗  ██║  ██║
   ██║   ██╔══╝  ╚════██║   ██║   ██║ ╚════██║ ██║        ██╔══╝  ██╔══██║██║██║     ██╔══╝  ██║  ██║
   ██║   ███████╗███████║   ██║   ╚██╗███████║██╔╝        ██║     ██║  ██║██║███████╗███████╗██████╔╝
   ╚═╝   ╚══════╝╚══════╝   ╚═╝    ╚═╝╚══════╝╚═╝         ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝ 
    """
    colorama_init()
    failures = run_tests()
    if failures:
        print(f"{Fore.RED}{failed}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}{passed}{Style.RESET_ALL}")

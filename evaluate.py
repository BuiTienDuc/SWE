"""Run a patch on a temporary copy. Requires Python 3.10+ and Git."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--patch', choices=['baseline', 'regression', 'partial', 'fixed'], default='baseline')
parser.add_argument('--expanded', action='store_true')
a = parser.parse_args()
root = Path(__file__).resolve().parent
if a.patch != 'baseline' and shutil.which('git') is None:
    parser.error('Git is required to apply .diff files. Install Git for Windows or git in Ubuntu.')
with tempfile.TemporaryDirectory(prefix='seminar_demo_') as tmp:
    work = Path(tmp)
    shutil.copy(root/'calculator.py', work/'calculator.py')
    shutil.copytree(root/'tests', work/'tests', ignore=shutil.ignore_patterns('__pycache__'))
    if a.patch != 'baseline':
        patch = root/'patches'/f'{a.patch}.diff'
        for extra in (['--check'], []):
            result = subprocess.run(['git', 'apply', *extra, str(patch)], cwd=work, capture_output=True, text=True)
            if result.returncode:
                print('PATCH APPLICATION FAILED\n'+result.stderr)
                sys.exit(2)
    groups = [('FAIL_TO_PASS', 'tests.test_issue'), ('PASS_TO_PASS', 'tests.test_regression')]
    if a.expanded:
        groups.append(('EXTRA_TESTS', 'tests.test_extra'))
    all_pass = True
    print(f'Patch={a.patch}  suite={"expanded" if a.expanded else "original"}', flush=True)
    for label, module in groups:
        result = subprocess.run([sys.executable, '-m', 'unittest', '-v', module], cwd=work, capture_output=True, text=True)
        print(result.stdout+result.stderr, end='')
        ok = result.returncode == 0
        print(f'{label}: {"PASS" if ok else "FAIL"}\n', flush=True)
        all_pass = all_pass and ok
    print('RESULT: '+('RESOLVED (demo criteria)' if all_pass else 'NOT RESOLVED'), flush=True)
    sys.exit(0 if all_pass else 1)

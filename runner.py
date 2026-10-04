"""Execute real patches and tests on a private temporary repository copy."""
from pathlib import Path
import shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parent
PATCHES=('baseline','regression','partial','fixed')
def run_steps(patch, expanded=False):
    if patch not in PATCHES: raise ValueError('Patch không hợp lệ')
    with tempfile.TemporaryDirectory(prefix='swe_seminar_') as tmp:
        work=Path(tmp)
        shutil.copy(ROOT/'calculator.py',work/'calculator.py')
        shutil.copytree(ROOT/'tests',work/'tests',ignore=shutil.ignore_patterns('__pycache__'))
        yield {'title':'1. Chuẩn bị repository','ok':True,'log':'Code và tests được sao chép vào thư mục tạm.'}
        diff='Code ban đầu: không áp dụng patch.'
        if patch!='baseline':
            if not shutil.which('git'): raise RuntimeError('Thiếu Git. Trên Cloud, thêm git vào packages.txt.')
            file=ROOT/'patches'/f'{patch}.diff';diff=file.read_text(encoding='utf-8')
            for flags in (['--check'],[]):
                r=subprocess.run(['git','apply',*flags,str(file)],cwd=work,capture_output=True,text=True,timeout=15)
                if r.returncode: raise RuntimeError('Không áp dụng được patch: '+r.stderr)
        yield {'title':'2. Áp dụng patch','ok':True,'log':diff,'code':(work/'calculator.py').read_text(encoding='utf-8')}
        groups=[('FAIL_TO_PASS','tests.test_issue'),('PASS_TO_PASS','tests.test_regression')]
        if expanded: groups.append(('TEST BỔ SUNG','tests.test_extra'))
        for title,module in groups:
            r=subprocess.run([sys.executable,'-m','unittest','-v',module],cwd=work,capture_output=True,text=True,timeout=15)
            yield {'title':title,'ok':r.returncode==0,'log':r.stdout+r.stderr}

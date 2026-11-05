"""Shared helpers: config loading, browser launch, paths."""
import json, os, shutil, copy

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def chromium_path():
    for c in [os.environ.get('CHROMIUM'), '/usr/bin/chromium', '/usr/bin/chromium-browser', shutil.which('chromium') or '', shutil.which('google-chrome') or '']:
        if c and os.path.exists(c): return c
    return None  # fall back to Playwright's bundled browser

def launch_browser(p, gl=False, extra=None):
    args = ['--allow-file-access-from-files']
    if gl: args += ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
    args += extra or []
    exe = chromium_path()
    return p.chromium.launch(executable_path=exe, args=args) if exe else p.chromium.launch(args=args)

def deep_merge(a, b):
    out = copy.deepcopy(a)
    for k, v in (b or {}).items():
        out[k] = deep_merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else copy.deepcopy(v)
    return out

def load_job(job_path):
    """defaults.json  <-  job.json 'config' overrides. Paths in the job are relative to the job file."""
    d = json.load(open(os.path.join(SKILL, 'config', 'defaults.json'), encoding='utf8'))
    job = json.load(open(job_path, encoding='utf8'))
    cfg = deep_merge(d, job.get('config', {}))
    root = os.path.dirname(os.path.abspath(job_path))
    def P(x): return x if (x is None or os.path.isabs(x) or '://' in x) else os.path.join(root, x)
    job['_root'] = root; job['_cfg'] = cfg; job['_P'] = P
    job.setdefault('workdir', '.')
    job['_work'] = P(job['workdir'])
    for sub in ['src', 'assets', 'build', 'video', 'out']: os.makedirs(os.path.join(job['_work'], sub), exist_ok=True)
    return job

def W(job, *parts): return os.path.join(job['_work'], *parts)

import os, shutil, sys
from pathlib import Path

SAFE_ENV_VARS = ("COMSPEC","PATH","PYTHONPATH","SHELL","USER","USERNAME","VIRTUAL_ENV")
DEVELOPER_TOOLS = ("git","pip","pytest","python")

def check_python():
    return {"name":"python","version":".".join(map(str,sys.version_info[:3])),
            "executable":sys.executable,"ok":True}

def check_disk(path=None):
    target=Path(path or Path.cwd()).expanduser().resolve()
    if not target.exists() or not target.is_dir():
        return {"name":"disk","path":str(target),"free_gb":None,"ok":False,
                "error":"configuration path does not exist or is not a directory"}
    usage=shutil.disk_usage(target)
    return {"name":"disk","path":str(target),
            "free_gb":round(usage.free/(1024**3),2),"ok":usage.free>0}

def check_environment():
    values={k:os.environ[k] for k in SAFE_ENV_VARS if k in os.environ}
    return {"name":"environment","variables":dict(sorted(values.items())),"ok":True}

def check_tools():
    tools={name: shutil.which(name) is not None for name in DEVELOPER_TOOLS}
    return {"name":"developer_tools","tools":dict(sorted(tools.items())),
            "ok":all(tools.values())}

def run_diagnostics(path=None):
    checks=[check_python(),check_disk(path),check_environment(),check_tools()]
    return {"tool":"cli-diagnostics","version":"1.1.0","checks":checks,
            "status":"PASS" if all(c["ok"] for c in checks) else "FAIL"}

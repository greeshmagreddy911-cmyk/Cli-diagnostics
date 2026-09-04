from cli_diagnostics.diagnostics import check_disk, check_python, check_tools, run_diagnostics

def test_successful_diagnostics():
    r=run_diagnostics(".")
    assert r["tool"]=="cli-diagnostics"
    assert len(r["checks"])==4
    assert check_python()["ok"] is True

def test_missing_dependency(monkeypatch):
    import cli_diagnostics.diagnostics as d
    original=d.shutil.which
    monkeypatch.setattr(d.shutil,"which",lambda n: None if n=="pytest" else original(n))
    r=check_tools()
    assert r["tools"]["pytest"] is False
    assert r["ok"] is False

def test_malformed_configuration_path():
    r=check_disk("this/path/should/not/exist/for-cli-diagnostics")
    assert r["ok"] is False
    assert "error" in r

def test_deterministic_tool_order(monkeypatch):
    import cli_diagnostics.diagnostics as d
    monkeypatch.setattr(d.shutil,"which",lambda n:"/usr/bin/"+n)
    assert check_tools()==check_tools()
    assert list(check_tools()["tools"])==["git","pip","pytest","python"]

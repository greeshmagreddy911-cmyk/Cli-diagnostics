import argparse, json
from .diagnostics import run_diagnostics

def build_parser():
    p=argparse.ArgumentParser(prog="cli-diagnostics",
        description="Inspect a developer machine and produce a deterministic report.")
    p.add_argument("--json",action="store_true",help="print deterministic JSON")
    p.add_argument("--path",default=None,help="directory for disk-space check")
    return p

def human_report(report):
    lines=["CLI Diagnostics Report","======================"]
    for c in report["checks"]:
        title=c["name"].replace("_"," ").title()
        lines.append(f"{title}: {'PASS' if c['ok'] else 'FAIL'}")
        if c["name"]=="python": lines.append(f"  Version: {c['version']}")
        elif c["name"]=="disk":
            if c["free_gb"] is not None: lines.append(f"  Free space (GB): {c['free_gb']}")
            if "error" in c: lines.append(f"  Error: {c['error']}")
        elif c["name"]=="developer_tools":
            for t,a in c["tools"].items(): lines.append(f"  {t}: {'available' if a else 'missing'}")
        elif c["name"]=="environment": lines.append(f"  Variables found: {len(c['variables'])}")
    lines.append(f"Overall status: {report['status']}")
    return "\n".join(lines)

def main():
    args=build_parser().parse_args()
    report=run_diagnostics(args.path)
    print(json.dumps(report,indent=2,sort_keys=True) if args.json else human_report(report))
    if args.path is not None and not next(c for c in report["checks"] if c["name"]=="disk")["ok"]: return 2
    return 0 if report["status"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())

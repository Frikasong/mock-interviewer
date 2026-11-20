"""mock-interviewer: one command for everything in this repository.

    mock-interviewer                      open the practice room in your browser
    mock-interviewer skill [agents…]      install the skill into AI agents on this computer
    mock-interviewer prompt               save the one-file version to paste into any chat AI
    mock-interviewer folder EMPLOYER ROLE start a prep folder from the templates
    mock-interviewer check BANK.md        check a question bank before practising
    mock-interviewer debrief DEBRIEF.md   read the numbers out of a debrief
    mock-interviewer mcp                  run the MCP server (for MCP clients)

Run any command with --help for its options. Add --zh (or --en) to choose the language.
"""
from __future__ import annotations

import argparse
import http.server
import pathlib
import shutil
import socket
import sys
import threading
import webbrowser

HERE = pathlib.Path(__file__).resolve().parent
VERSION = "1.2.0"

# agent, folder it reads skills from, folder whose existence means it is installed
AGENTS = [
    ("claude", "~/.claude/skills", "~/.claude"),
    ("codex", "~/.codex/skills", "~/.codex"),
    ("gemini", "~/.gemini/skills", "~/.gemini"),
    ("copilot", "~/.copilot/skills", "~/.copilot"),
    ("cursor", "~/.cursor/skills", "~/.cursor"),
    ("opencode", "~/.config/opencode/skills", "~/.config/opencode"),
    ("goose", "~/.config/goose/skills", "~/.config/goose"),
    ("amp", "~/.config/agents/skills", "~/.config/agents"),
    ("windsurf", "~/.codeium/windsurf/skills", "~/.codeium/windsurf"),
]


def _find(rel: str) -> pathlib.Path:
    """A bundled file: inside the installed package, or in the repository when run from source."""
    for base in (HERE, HERE.parent):
        p = base / rel
        if p.exists():
            return p
    sys.exit(f"Cannot find {rel}. Reinstall, or run from the repository root.")


def _lang(a) -> str:
    return "zh" if getattr(a, "zh", False) else "en"


def _skill_name(lang: str) -> str:
    return "interview-prep-zh" if lang == "zh" else "interview-prep"


# ------------------------------------------------------------------- practice room
def cmd_practice(a) -> None:
    page = _find("interviewer/index.html").read_bytes()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.split("?")[0] not in ("/", "/index.html"):
                self.send_response(404); self.end_headers(); return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)

        def log_message(self, *args):  # keep the terminal quiet
            pass

    port = a.port
    try:
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError:
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)  # port taken: any free one
    url = f"http://localhost:{srv.server_address[1]}/"
    zh = _lang(a) == "zh"
    print(("模拟面试器已启动：" if zh else "Mock Interviewer is running at ") + url)
    print("只在这台电脑上运行；用 Chrome 或 Edge 打开才有实时转录。按 Ctrl+C 停止。" if zh else
          "It runs on this computer only. Use Chrome or Edge for the live transcript. Press Ctrl+C to stop.")
    if not a.no_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n" + ("已停止。" if zh else "Stopped."))
    finally:
        srv.server_close()


# ------------------------------------------------------------------------ skill
def cmd_skill(a) -> None:
    lang = _lang(a)
    name, other = _skill_name(lang), _skill_name("en" if lang == "zh" else "zh")
    src = _find(f"skills/{name}")
    if a.list:
        for n, d, _ in AGENTS:
            print(f"{n:<10} {pathlib.Path(d).expanduser()}")
        return
    targets = []
    if a.dir:
        targets.append(("custom", pathlib.Path(a.dir).expanduser()))
    elif a.agents:
        known = {n: d for n, d, _ in AGENTS}
        for w in a.agents:
            if w not in known:
                sys.exit(f"Unknown agent: {w}. See: mock-interviewer skill --list")
            targets.append((w, pathlib.Path(known[w]).expanduser()))
    else:
        targets = [(n, pathlib.Path(d).expanduser()) for n, d, home in AGENTS if pathlib.Path(home).expanduser().is_dir()]
        if not targets:
            sys.exit("No supported AI agent found. Name one (mock-interviewer skill codex), give a folder "
                     "(--dir PATH), or use the one-file version: mock-interviewer prompt")

    def ask(q: str) -> bool:
        if a.yes:
            return True
        if not sys.stdin.isatty():
            return False
        return input(q + " [y/N] ").strip().lower() in ("y", "yes")

    done = []
    for agent, dest in targets:
        dest.mkdir(parents=True, exist_ok=True)
        if (dest / other).exists():
            if ask(f"[{agent}] {other} is installed too and will compete with {name}. Remove it?"):
                shutil.rmtree(dest / other)
            else:
                print(f"[{agent}] note: {other} is still installed and answers the same requests; keep only one.")
        if (dest / name).exists():
            if not ask(f"[{agent}] {name} is already installed. Replace it?"):
                print(f"[{agent}] skipped (use --yes to replace)")
                continue
            shutil.rmtree(dest / name)
        shutil.copytree(src, dest / name, ignore=shutil.ignore_patterns(".*", "__pycache__"))
        done.append(f"  {agent} → {dest / name}")
    if not done:
        print("Nothing installed.")
        return
    print(f"Installed {name}:\n" + "\n".join(done))
    print("\nRestart the agent, then describe your situation, e.g. "
          "\"I'm interviewing at <employer> for <role> next Thursday, here's the posting.\"")


# ----------------------------------------------------------------------- prompt
def cmd_prompt(a) -> None:
    src = _find(f"portable/{_skill_name(_lang(a))}.md")
    if a.print:
        sys.stdout.write(src.read_text(encoding="utf-8"))
        return
    out = pathlib.Path(a.out or src.name)
    if out.exists() and not a.yes:
        sys.exit(f"{out} already exists. Use --yes to overwrite, or --out another name.")
    shutil.copyfile(src, out)
    print(f"Saved {out.resolve()}")
    print("Paste the whole file into any AI chat as your first message, then describe your situation."
          if _lang(a) == "en" else "把整个文件作为第一条消息粘贴给任何 AI，然后直接说你的情况。")


# --------------------------------------------------------- helpers from the server
def cmd_folder(a) -> None:
    from .server import create_prep_folder
    print(create_prep_folder(a.employer, a.role, str(pathlib.Path(a.dir).expanduser().resolve()), _lang(a)))


def _read_arg(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    p = pathlib.Path(path).expanduser()
    if not p.is_file():
        sys.exit(f"No such file: {p}")
    return p.read_text(encoding="utf-8")


def cmd_check(a) -> None:
    from .server import check_question_bank
    print(check_question_bank(_read_arg(a.file)))


def cmd_debrief(a) -> None:
    from .server import read_debrief
    print(read_debrief(_read_arg(a.file)))


def cmd_mcp(a) -> None:
    from .server import main as serve
    sys.argv = [sys.argv[0]]
    serve()


# ------------------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> None:
    lang = argparse.ArgumentParser(add_help=False)
    g = lang.add_mutually_exclusive_group()
    g.add_argument("--zh", action="store_true", help="中文")
    g.add_argument("--en", action="store_true", help="English (default)")
    # Subcommands accept --zh too; SUPPRESS keeps "mock-interviewer --zh skill" from being reset.
    sublang = argparse.ArgumentParser(add_help=False, argument_default=argparse.SUPPRESS)
    g = sublang.add_mutually_exclusive_group()
    g.add_argument("--zh", action="store_true", help="中文")
    g.add_argument("--en", action="store_true", help="English (default)")

    p = argparse.ArgumentParser(prog="mock-interviewer", parents=[lang],
                                description="Interview prep in three steps, for any AI. With no command, opens the practice room.",
                                formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__.split("\n\n", 1)[1])
    p.add_argument("--version", action="version", version=f"mock-interviewer {VERSION}")
    p.add_argument("--port", type=int, default=5757, help=argparse.SUPPRESS)
    p.add_argument("--no-browser", action="store_true", help=argparse.SUPPRESS)
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("practice", parents=[sublang], help="open the practice room in your browser (the default)")
    s.add_argument("--port", type=int, default=5757, help="port to use on this computer (default 5757)")
    s.add_argument("--no-browser", action="store_true", help="print the address instead of opening a browser")
    s.set_defaults(fn=cmd_practice)

    s = sub.add_parser("skill", parents=[sublang], help="install the skill into AI agents on this computer")
    s.add_argument("agents", nargs="*", help="claude codex gemini copilot cursor opencode goose amp windsurf (default: every one found)")
    s.add_argument("--dir", help="install into this skills folder instead")
    s.add_argument("--list", action="store_true", help="show supported agents and their folders")
    s.add_argument("-y", "--yes", action="store_true", help="replace without asking")
    s.set_defaults(fn=cmd_skill)

    s = sub.add_parser("prompt", parents=[sublang], help="save the one-file version to paste into any chat AI")
    s.add_argument("--out", help="file name to save as")
    s.add_argument("--print", action="store_true", help="print it instead of saving")
    s.add_argument("-y", "--yes", action="store_true", help="overwrite an existing file")
    s.set_defaults(fn=cmd_prompt)

    s = sub.add_parser("folder", parents=[sublang], help="start a prep folder from the templates")
    s.add_argument("employer"); s.add_argument("role")
    s.add_argument("--dir", default=".", help="where to create it (default: here)")
    s.set_defaults(fn=cmd_folder)

    s = sub.add_parser("check", help="check a question bank before practising")
    s.add_argument("file", help="question-bank.md, or - for standard input")
    s.set_defaults(fn=cmd_check)

    s = sub.add_parser("debrief", help="read times, budgets and self-marks out of a debrief")
    s.add_argument("file", help="the debrief .md downloaded from the practice room, or -")
    s.set_defaults(fn=cmd_debrief)

    s = sub.add_parser("mcp", help="run the MCP server over stdio (for MCP clients)")
    s.set_defaults(fn=cmd_mcp)

    a = p.parse_args(argv)
    if not a.cmd:
        a.fn = cmd_practice
    try:
        a.fn(a)
    except BrokenPipeError:  # output piped into head, less, …
        sys.stderr.close()


if __name__ == "__main__":
    main()

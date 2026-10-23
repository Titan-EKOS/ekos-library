"""Tests for the EKOS Library server. Each test runs on a throwaway copy of the library.

    cd D:\\EKOS\\Library\\09_Server
    .venv\\Scripts\\python -m pytest -q
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SERVER_DIR = Path(__file__).resolve().parents[1]
REPO = SERVER_DIR.parent
sys.path.insert(0, str(SERVER_DIR))

from library_server.core import Library, LibraryError  # noqa: E402

TOOLS = {"list_skills", "get_skill", "list_agents", "get_agent", "add_card", "log_lesson",
         "get_qc_rules"}

SKILL = """---
name: pchydro-test
description: Run PC-Hydro for a test basin.
version: 1.0.0
status: active
function: hydrology
jurisdiction: Pima County
tools_versions: PC-Hydro 7.4
owner: JCO
---
# PC-Hydro test skill
Use the program Tc, 5-min minimum.
"""
AGENT = """---
name: qc-test
description: Independent QC reviewer.
version: 1.0.0
status: active
jurisdiction: all
tools_versions: ""
owner: JCO
skills: [pchydro-test]
---
# QC test agent
Review independently.
"""
RULE = """
## QC-0001 Tc label
```yaml
id: QC-0001
rule: Never call time to peak Tc.
scope: [hydrology, pima]
function: hydrology
jurisdiction: Pima County
source_redline: 7TEST0001 markup p.4 comment 2
```
"""
CARD = {
    "id": "7TEST0001-001", "title": "PC-Hydro Tc minimum", "type": "skill",
    "function": "hydrology", "trigger": "Small basins", "steps": ["Use program Tc"],
    "gotchas": ["Tc below 5 min gets reset"], "jurisdiction": "Pima County",
    "tools_versions": "PC-Hydro 7.4", "evidence": [r"D:\Projects\Acme Homes\99_Working\pk6"],
    "hours_lost": 2, "recurrence": 3, "confidence": "high",
}


def git(root, *args, env=None):
    env = env or dict(os.environ, LIBRARY_PYTHON=sys.executable)
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, env=env,
                          stdin=subprocess.DEVNULL)


@pytest.fixture()
def lib_root(tmp_path):
    root = tmp_path / "Library"
    root.mkdir()
    shutil.copy(REPO / "library.yaml", root)
    shutil.copy(REPO / ".gitattributes", root)
    shutil.copy(REPO / ".gitignore", root)
    shutil.copytree(REPO / ".githooks", root / ".githooks")
    shutil.copytree(REPO / "09_Server", root / "09_Server",
                    ignore=shutil.ignore_patterns(".venv", "__pycache__", ".pytest_cache", "tests"))
    (root / "08_Platform_Builds").mkdir()
    shutil.copy(REPO / "08_Platform_Builds" / "build.py", root / "08_Platform_Builds")
    for d in ("03_Skills/pchydro-test", "04_Agents/qc-test", "05_QC_Rules", "07_Inbox",
              "00_Inventory/_local"):
        (root / d).mkdir(parents=True, exist_ok=True)
    (root / "03_Skills/pchydro-test/SKILL.md").write_text(SKILL, encoding="utf-8")
    (root / "04_Agents/qc-test/AGENT.md").write_text(AGENT, encoding="utf-8")
    (root / "05_QC_Rules/rules.md").write_text("# QC Rules\n" + RULE, encoding="utf-8")
    (root / "00_Inventory/_local/path_aliases.csv").write_text("Acme Homes,7TEST0001\n",
                                                                 encoding="utf-8")
    (root / "00_Inventory/_local/client_terms.txt").write_text("Acme\n", encoding="utf-8")
    (root / "07_Inbox/.gitkeep").write_text("")
    git(root, "init", "-q")
    git(root, "config", "user.name", "test")
    git(root, "config", "user.email", "test@ekos.local")
    git(root, "config", "commit.gpgsign", "false")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "init")
    return root


def commits(root) -> int:
    return int(git(root, "rev-list", "--count", "HEAD").stdout.strip())


# ------------------------------------------------------------------ read tools
def test_list_and_get_skill(lib_root):
    lib = Library(lib_root)
    assert [s["name"] for s in lib.list_skills()] == ["pchydro-test"]
    assert lib.list_skills("jurisdiction=pima")[0]["version"] == "1.0.0"
    assert lib.list_skills("jurisdiction=placer") == []
    s = lib.get_skill("pchydro-test")
    assert "5-min minimum" in s["content"]
    (lib_root / "03_Skills/pchydro-test/addons").mkdir()
    (lib_root / "03_Skills/pchydro-test/addons/pima.md").write_text("Pima add-on", encoding="utf-8")
    assert lib.get_skill("pchydro-test", "addons/pima.md")["content"] == "Pima add-on"
    with pytest.raises(LibraryError):
        lib.get_skill("pchydro-test", "../../library.yaml")
    with pytest.raises(LibraryError):
        lib.get_skill("nope")


def test_list_and_get_agent(lib_root):
    lib = Library(lib_root)
    agents = lib.list_agents()
    assert agents[0]["name"] == "qc-test" and agents[0]["skills"] == ["pchydro-test"]
    assert "Review independently" in lib.get_agent("qc-test")["content"]


def test_get_qc_rules(lib_root):
    lib = Library(lib_root)
    assert len(lib.get_qc_rules("all")) == 1
    assert lib.get_qc_rules("pima")[0]["source_redline"].startswith("7TEST0001")
    assert lib.get_qc_rules("exhibits") == []


# ----------------------------------------------------------------- write tools
def test_add_card_append_only_one_commit_each(lib_root):
    lib = Library(lib_root)
    n0 = commits(lib_root)
    r1 = lib.add_card(dict(CARD), "claude", "7TEST0001")
    with pytest.raises(LibraryError, match="Duplicate"):        # identical resubmit refused
        lib.add_card(dict(CARD), "codex", "7TEST0001")
    r2 = lib.add_card(dict(CARD, gotchas=["new gotcha"]), "codex", "7TEST0001")  # same id, new content: new file
    assert r1["path"] != r2["path"]
    assert r1["path"].startswith("07_Inbox/7TEST0001/JCO_")
    assert commits(lib_root) == n0 + 2
    text = (lib_root / r1["path"]).read_text(encoding="utf-8")
    assert "source_ai: claude" in text and "timestamp:" in text and "project: 7TEST0001" in text
    # path alias swapped the client name for the job number
    assert "Acme" not in text and "7TEST0001\\99_Working" in text
    assert git(lib_root, "status", "--porcelain").stdout.strip() == ""


def test_log_lesson_commits(lib_root):
    lib = Library(lib_root)
    n0 = commits(lib_root)
    r = lib.log_lesson("7TEST0001", "HY-8 export needs Word open first.",
                       [r"D:\Projects\7TEST0001\99_Working\hy8"], "local:laguna-s-2.1")
    assert commits(lib_root) == n0 + 1
    assert "type: lesson" in (lib_root / r["path"]).read_text(encoding="utf-8")


@pytest.mark.parametrize("field,value,expect", [
    ("trigger", "email jane@client.com for the plans", "email"),
    ("trigger", "Call 520-555-1234 for access", "phone"),
    ("trigger", "Parcel 123-45-678A", "apn_or_ssn"),
    ("trigger", "Site at 1234 N Main St drains west", "street_address"),
    ("title", "Acme wants a bigger basin", "client term"),
    ("trigger", "x" * 5000, "chars"),
], ids=["email", "phone", "apn", "address", "client-term", "too-long"])
def test_data_guard_rejects(lib_root, field, value, expect):
    lib = Library(lib_root)
    n0 = commits(lib_root)
    card = dict(CARD, **{field: value})
    with pytest.raises(LibraryError) as e:
        lib.add_card(card, "claude", "7TEST0001")
    assert expect in str(e.value)
    assert commits(lib_root) == n0
    assert not list((lib_root / "07_Inbox").rglob("JCO_*"))


def test_validation(lib_root):
    lib = Library(lib_root)
    with pytest.raises(LibraryError, match="source_ai"):
        lib.add_card(dict(CARD), "", "7TEST0001")
    with pytest.raises(LibraryError, match="source_ai"):
        lib.add_card(dict(CARD), "bard", "7TEST0001")
    with pytest.raises(LibraryError, match="type"):
        lib.add_card(dict(CARD, type="procedure"), "claude", "7TEST0001")
    with pytest.raises(LibraryError, match="Missing"):
        lib.add_card({k: v for k, v in CARD.items() if k != "evidence"}, "claude", "7TEST0001")


def test_no_write_outside_inbox(lib_root):
    lib = Library(lib_root)
    before = (lib_root / "03_Skills/pchydro-test/SKILL.md").read_text(encoding="utf-8")
    r = lib.add_card(dict(CARD), "claude", "../03_Skills/pchydro-test")
    assert r["path"].startswith("07_Inbox/")
    with pytest.raises(LibraryError, match="outside 07_Inbox"):
        lib._write_new(lib_root / "03_Skills" / "evil.md", "x", "m", "claude")
    assert (lib_root / "03_Skills/pchydro-test/SKILL.md").read_text(encoding="utf-8") == before
    public = {n for n in dir(Library) if not n.startswith("_")}
    writers = {n for n in public if any(w in n for w in ("edit", "update", "delete", "write", "set_"))}
    assert writers == set()


# --------------------------------------------------------- MCP end to end
def test_mcp_stdio_every_tool(lib_root):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def run():
        params = StdioServerParameters(
            command=sys.executable,
            args=[str(lib_root / "09_Server/run_server.py"), "--root", str(lib_root)])
        async with stdio_client(params) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                names = {t.name for t in (await s.list_tools()).tools}
                assert names == TOOLS            # exactly these 7, nothing that edits masters

                async def call(_tool, **args):
                    res = await s.call_tool(_tool, args)
                    assert not res.isError, res
                    txt = "".join(c.text for c in res.content if hasattr(c, "text"))
                    try:
                        return json.loads(txt)
                    except json.JSONDecodeError:
                        return txt

                assert "pchydro-test" in json.dumps(await call("list_skills", filter="hydrology"))
                assert "5-min" in json.dumps(await call("get_skill", name="pchydro-test"))
                assert "qc-test" in json.dumps(await call("list_agents"))
                assert "Review" in json.dumps(await call("get_agent", name="qc-test"))
                assert "QC-0001" in json.dumps(await call("get_qc_rules", scope="pima"))
                r = await call("add_card", card=dict(CARD), source_ai="claude", project="7TEST0001")
                assert r["status"] == "accepted", r
                r = await call("log_lesson", project="7TEST0001", text="Lesson text.",
                               evidence=["D:\\x"], source_ai="gemini")
                assert r["status"] == "accepted", r
                r = await call("add_card", card=dict(CARD, trigger="a@b.com"),
                               source_ai="claude", project="7TEST0001")
                assert r["status"] == "error" and "email" in r["error"]
                return True

    assert asyncio.run(run())
    files = list((lib_root / "07_Inbox/7TEST0001").glob("JCO_*.md"))
    assert len(files) == 2
    assert "client_reported" in files[0].read_text(encoding="utf-8") + files[1].read_text(encoding="utf-8")


# ------------------------------------------------------- build + hook
def test_build_check_detects_hand_edit(lib_root):
    b = [sys.executable, str(lib_root / "08_Platform_Builds/build.py")]
    assert subprocess.run(b, cwd=lib_root).returncode == 0
    out = lib_root / "08_Platform_Builds/out"
    for f in ("claude/pchydro-test/SKILL.md", "AGENTS.md", "GEMINI.md", "local/_library.txt",
              "local/qc-test.txt"):
        assert (out / f).exists(), f
    skill = (out / "claude/pchydro-test/SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\nname: pchydro-test\ndescription:") and "version:" not in skill.split("---")[1]
    assert "pchydro-test" in (out / "AGENTS.md").read_text(encoding="utf-8")
    assert subprocess.run(b + ["--check"], cwd=lib_root).returncode == 0
    with open(out / "AGENTS.md", "a", encoding="utf-8") as fh:
        fh.write("hand edit\n")
    assert subprocess.run(b + ["--check"], cwd=lib_root, capture_output=True).returncode == 1


def test_hook_blocks_inbox_edit(lib_root):
    subprocess.run([sys.executable, str(lib_root / "08_Platform_Builds/build.py")], cwd=lib_root)
    git(lib_root, "config", "core.hooksPath", ".githooks")
    git(lib_root, "add", "-A")
    assert git(lib_root, "commit", "-q", "-m", "build").returncode == 0
    lib = Library(lib_root)
    r = lib.add_card(dict(CARD), "claude", "7TEST0001")       # server commit passes the hook
    p = lib_root / r["path"]
    p.write_text(p.read_text(encoding="utf-8") + "tampered: true\n", encoding="utf-8")
    git(lib_root, "add", "-A")
    res = git(lib_root, "commit", "-q", "-m", "tamper")
    assert res.returncode != 0 and "append-only" in res.stderr

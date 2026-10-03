#!/usr/bin/env python3
"""
build.py — 一条命令产出所有发布物。

    python3 build.py                     # GitHub 发布物
    python3 build.py --repo you/repo     # 顺便把 README 里的占位符换成真实仓库
    python3 build.py --redskill          # 额外产出 RED Skill 上传包

产出（全部在 dist/，dist/ 不进 git）：

  dist/interview-prep.skill          GitHub Release 附件 / Claude.ai 上传
  dist/interview-prep-zh.skill
加 --redskill 时还会产出（RED Skill 需要粉丝 >= 1000，够了再说）：

  dist/redskill/interview-prep-zh/            文件夹上传：整个拖进去
  dist/redskill/interview-prep-zh-single.md   兜底：只收单文件时用
  dist/redskill/UPLOAD.md                     上传表单要填的字段，照抄
"""
import argparse, pathlib, re, shutil, sys, zipfile

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
PLACEHOLDER = "github.com/<user>/mock-interviewer"


def build_skill_files():
    out = []
    for d in sorted((ROOT / "skills").iterdir()):
        if not d.is_dir():
            continue
        target = DIST / f"{d.name}.skill"
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            target.unlink()
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(d.rglob("*")):
                if f.is_file() and not f.name.startswith("."):
                    z.write(f, f.relative_to(d.parent))
        out.append(target)
    return out


def split_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit("SKILL.md 缺少 frontmatter")
    return m.group(1), m.group(2)


def build_single_file(skill_dir, target):
    """把 references/ 和 assets/ 内联进一个自包含的 SKILL.md。"""
    fm, body = split_frontmatter((skill_dir / "SKILL.md").read_text())

    # 单文件版里没有可读的外部文件，所以把"读 references/xxx"的指令改成指向本文附录
    body = re.sub(r"读 `references/([^`]+)`。?", "见下方附录一。", body)
    body = re.sub(r"Read `references/([^`]+)`\.?", "See Appendix A below.", body)
    body = body.replace("`assets/` 里有每个文件的空白模板", "附录二是每个文件的空白模板")
    body = body.replace("Blank templates for each file are in `assets/`.",
                        "Blank templates for each file are in Appendix B.")

    # 末尾的「参考文件」清单指向的是不存在的路径，换成附录指引
    body = re.sub(r"\n#+ 参考文件\n.*$", """
## 本文结构

- 附录一 · 参考方法——三步的完整做法
- 附录二 · 空白模板——每个产出文件的格式，复制填写

这是单文件版，所有内容都在本文里，不需要额外文件。
""", body, flags=re.S)
    body = re.sub(r"\n#+ Reference files\n.*$", """
## How this document is organised

- Appendix A — the full method for all three steps
- Appendix B — a blank template for every output file

This is the single-file edition; everything is in this document.
""", body, flags=re.S)

    def deref(md):
        return (md.replace("模板见 `assets/story-card.md`。", "模板见附录二的 `story-card.md`。")
                  .replace("Template in `assets/story-card.md`.", "Template in Appendix B."))

    def demote(md):
        # 附录内容降一级，整份文档只保留一个 H1（代码块内的 # 不动）
        out, fence = [], False
        for line in md.split("\n"):
            if line.lstrip().startswith("```"):
                fence = not fence
            if not fence and re.match(r"^#{1,5} ", line):
                line = "#" + line
            out.append(line)
        return "\n".join(out)

    parts = [f"---\n{fm}\n---\n", body.rstrip(), "\n\n---\n\n# 附录一 · 参考方法\n"]
    for f in sorted((skill_dir / "references").glob("*.md")):
        parts.append("\n" + demote(deref(f.read_text().rstrip())) + "\n")

    parts.append("\n---\n\n# 附录二 · 空白模板\n")
    parts.append("\n下面每一节是一个产出文件的模板。用到哪个复制哪个，不要另创格式——"
                 "题库那节的格式会被模拟面试工具直接解析。\n")
    for f in sorted((skill_dir / "assets").glob("*.md")):
        parts.append(f"\n## 模板：`{f.name}`\n\n```markdown\n{f.read_text().rstrip()}\n```\n")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(parts))
    return target


def build_redskill():
    src = ROOT / "skills" / "interview-prep-zh"
    folder = DIST / "redskill" / "interview-prep-zh"
    if folder.exists():
        shutil.rmtree(folder)
    shutil.copytree(src, folder, ignore=shutil.ignore_patterns(".*"))
    single = build_single_file(src, DIST / "redskill" / "interview-prep-zh-single.md")
    return folder, single


def set_repo(slug):
    n = 0
    for f in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.sh")):
        if "dist" in f.parts or ".git" in f.parts:
            continue
        t = f.read_text()
        if PLACEHOLDER in t:
            f.write_text(t.replace(PLACEHOLDER, f"github.com/{slug}"))
            n += 1
    print(f"  替换了 {n} 个文件里的仓库占位符 -> github.com/{slug}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", help="你的 GitHub 仓库，形如 fukunyang/mock-interviewer")
    ap.add_argument("--redskill", action="store_true",
                    help="另外产出 RED Skill 上传包（粉丝够 1000 再用）")
    a = ap.parse_args()

    if a.repo:
        set_repo(a.repo)

    print("构建 .skill:")
    for p in build_skill_files():
        print(f"  {p.relative_to(ROOT)}  ({p.stat().st_size // 1024} KB)")

    if a.redskill:
        print("构建 RED Skill 上传包:")
        folder, single = build_redskill()
        print(f"  {folder.relative_to(ROOT)}/  (文件夹上传，整个拖进去)")
        print(f"  {single.relative_to(ROOT)}  ({single.stat().st_size // 1024} KB，兜底单文件)")
        upload = ROOT / "docs" / "redskill-upload.md"
        if upload.exists():
            shutil.copy(upload, DIST / "redskill" / "UPLOAD.md")
            print("  dist/redskill/UPLOAD.md  (表单照抄)")

    if PLACEHOLDER in (ROOT / "README.md").read_text():
        print("\n注意：README 里还是占位符。发布前跑 python3 build.py --repo 你的用户名/仓库名")


if __name__ == "__main__":
    main()

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

CORE_FILES = [
    ROOT / "README.md",
    ROOT / "slicing_script.py",
    ROOT / "requirements.txt",
    ROOT / "prolog" / "hgd0_04_02_reactions.pl",
]

PAPER_RESULT_FILES = [
    ROOT / "results" / "conditional_dependency_matrices" / "necessary_matrix_by_target_hga_a.pdf",
    ROOT / "results" / "conditional_dependency_matrices" / "necessary_matrix_by_target_hawk_a.pdf",
    ROOT / "results" / "conditional_dependency_matrices" / "necessary_matrix_by_target_sa.pdf",
    ROOT / "results" / "conditional_dependency_matrices" / "necessary_matrix_by_target_tyr_b.pdf",
    ROOT / "results" / "conditional_dependency_matrices" / "necessary_matrix_by_target_tyr_b_bh4_b.pdf",
    ROOT / "results" / "dynamic_negative_slicing" / "table_results_bicolor-1.pdf",
    ROOT / "results" / "dynamic_negative_slicing" / "table_results_bicolor-2.pdf",
]

REQUIRED_RUNTIME_FILES = [
    ROOT / "output" / "hgd0_04-02.dot",
]

FORBIDDEN_PATTERNS = [
    "/" + "Users/",
    "C:" + "\\\\Users\\\\",
]


def check_file(path: Path) -> bool:
    ok = path.exists()
    print(f"{'OK' if ok else 'MISSING'}  {path.relative_to(ROOT)}")
    return ok


def scan_for_private_paths() -> bool:
    bad = []
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".py", ".pl", ".md", ".txt"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in FORBIDDEN_PATTERNS:
                if pattern in text:
                    bad.append((path.relative_to(ROOT), pattern))
    if bad:
        print("\nPrivate/local paths found:")
        for path, pattern in bad:
            print(f"  {path}: {pattern}")
        return False
    print("OK  no private/local paths found")
    return True


def check_python_syntax() -> bool:
    path = ROOT / "slicing_script.py"
    try:
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
    except SyntaxError as exc:
        print(f"ERROR  slicing_script.py: {exc}")
        return False
    print("OK  slicing_script.py compiles")
    return True


def check_model_typo() -> bool:
    model = ROOT / "prolog" / "hgd0_04_02_reactions.pl"
    text = model.read_text(encoding="utf-8", errors="ignore")
    bad = "fahmgca_nul,h20,faa_a" in text
    good = "fahmgca_nul,h2o,faa_a" in text
    if bad or not good:
        print("ERROR  Appendix R38 h2o spelling check failed")
        return False
    print("OK  Appendix R38 uses h2o")
    return True


def check_slicing_engine() -> bool:
    engine = ROOT / "BioReSolvePositive.pl"
    if not engine.exists():
        print("MISSING  BioReSolvePositive.pl")
        return False
    text = engine.read_text(encoding="utf-8", errors="ignore")
    ok = "negslice" in text and "main_do" in text
    print(f"{'OK' if ok else 'MISSING'}  slicing main_do/negslice interface in BioReSolvePositive.pl")
    return ok


def main() -> None:
    print("Repository check\n================")

    print("\nCore paper repository files")
    core_ok = all(check_file(p) for p in CORE_FILES)

    print("\nPaper result artifacts")
    results_ok = all(check_file(p) for p in PAPER_RESULT_FILES)

    print("\nPython/model checks")
    syntax_ok = check_python_syntax()
    model_ok = check_model_typo()

    print("\nPath hygiene")
    paths_ok = scan_for_private_paths()

    print("\nFiles needed for the current full analysis run")
    runtime_files_ok = all(check_file(p) for p in REQUIRED_RUNTIME_FILES)
    engine_ok = check_slicing_engine()

    print("\nExternal executable")
    swipl = shutil.which("swipl")
    print(f"{'OK' if swipl else 'MISSING'}  SWI-Prolog executable 'swipl'")

    print("\nSummary")
    if core_ok and results_ok and syntax_ok and model_ok and paths_ok:
        print("OK: paper-aligned public package files pass the local consistency checks.")
    else:
        print("CHECK FAILED: fix the core/public-package issues listed above.")

    if runtime_files_ok and engine_ok and swipl:
        print("OK: runtime prerequisites detected for the current script.")
    else:
        print("NOT FULLY RUNNABLE FROM A CLEAN CLONE: missing runtime item(s) are listed above.")

    if (ROOT / "LICENSE-TODO.md").exists():
        print("WARNING: repository license has not yet been selected.")


if __name__ == "__main__":
    main()

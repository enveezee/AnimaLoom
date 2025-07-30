#!/usr/bin/env python3
import subprocess
import os
import datetime

def run_command(command, cwd=None):
    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    return process.stdout, process.stderr, process.returncode

def generate_test_report():
    report_content = []
    report_content.append(f"# AnimaLoom Test Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_content.append("This report details the output of basic functional tests for the AnimaLoom engine components.\n")
    report_content.append("Each test runs a specific module's `if __name__ == '__main__':` block.\n\n")

    tests = [
        {"name": "The Eidolon (Agent Class)", "command": "python3 the_loom/the_eidolon.py", "cwd": "the_loom"},
        {"name": "The Nexus (World State Manager)", "command": "python3 -m the_loom.the_nexus", "cwd": "."},
        {"name": "The Moirai (Formula Engine)", "command": "python3 -m the_loom.the_moirai", "cwd": "."},
        {"name": "The Alembic (Hyle Distiller)", "command": "python3 -m the_loom.the_alembic", "cwd": "."},
        {"name": "The Loomwright (GUI Application)", "command": "python3 -c \"import tkinter as tk; from the_loomwright.main import TheLoomwrightApp; root = tk.Tk(); app = TheLoomwrightApp(root); root.destroy();\"", "cwd": ".", "note": "This test attempts to initialize the Tkinter GUI application and immediately destroy it to confirm basic startup without errors."}
    ]

    for test in tests:
        report_content.append(f"## Test: {test['name']}\n")
        report_content.append(f"```bash\n{test['command']}\n```\n")
        if "note" in test:
            report_content.append(f"> Note: {test['note']}\n\n")

        # Adjust cwd for subprocess.run
        actual_cwd = os.path.join(os.path.dirname(__file__), test['cwd']) if test['cwd'] != "." else os.path.dirname(__file__)
        
        stdout, stderr, returncode = run_command(test['command'], cwd=actual_cwd)

        report_content.append("### Output\n")
        report_content.append("```\n")
        report_content.append(stdout)
        report_content.append("```\n")

        if stderr:
            report_content.append("### Errors (Stderr)\n")
            report_content.append("```\n")
            report_content.append(stderr)
            report_content.append("```\n")
        
        report_content.append(f"**Exit Code:** {returncode}\n\n")
        report_content.append("---\n\n") # Separator

    with open("TEST_REPORT.md", "w") as f:
        f.write("".join(report_content))

    print("TEST_REPORT.md generated successfully.")

if __name__ == "__main__":
    generate_test_report()

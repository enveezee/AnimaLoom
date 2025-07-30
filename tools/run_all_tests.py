#!/usr/bin/env python3
import subprocess
import os
import datetime
import re

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

    # All commands will be run from the AnimaLoom root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    tests = [
        {"name": "The Eidolon (Agent Class)", "command": "python3 -m the_loom.the_eidolon"},
        {"name": "The Nexus (World State Manager)", "command": "python3 -m the_loom.the_nexus"},
        {"name": "The Moirai (Formula Engine)", "command": "python3 -m the_loom.the_moirai"},
        {"name": "The Alembic (Hyle Distiller)", "command": "python3 -m the_loom.the_alembic"},
        {"name": "The Loomwright (GUI Application)", "command": "python3 -c \"import tkinter as tk; from the_loomwright.main import TheLoomwrightApp; root = tk.Tk(); app = TheLoomwrightApp(root); root.destroy();\"", "note": "This test attempts to initialize the Tkinter GUI application and immediately destroy it to confirm basic startup without errors."}
    ]

    for test in tests:
        report_content.append(f"## Test: {test['name']}\n")
        report_content.append(f"```bash\n{test['command']}\n```\n")
        if "note" in test:
            report_content.append(f"> Note: {test['note']}\n\n")

        stdout, stderr, returncode = run_command(test['command'], cwd=project_root)

        # Process stdout and stderr to remove absolute paths
        # This regex replaces the absolute path to the project root with a relative path
        processed_stdout = re.sub(re.escape(project_root) + r'/?', '', stdout)
        processed_stderr = re.sub(re.escape(project_root) + r'/?', '', stderr)

        report_content.append("### Output\n")
        report_content.append("```\n")
        report_content.append(processed_stdout)
        report_content.append("```\n")

        if processed_stderr:
            report_content.append("### Errors (Stderr)\n")
            report_content.append("```\n")
            report_content.append(processed_stderr)
            report_content.append("```\n")
        
        report_content.append(f"**Exit Code:** {returncode}\n\n")
        report_content.append("---\n\n") # Separator

    with open("TEST_REPORT.md", "w") as f:
        f.write("".join(report_content))

    print("TEST_REPORT.md generated successfully.")

if __name__ == "__main__":
    generate_test_report()
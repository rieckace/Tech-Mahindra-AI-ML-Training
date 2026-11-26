# AI assistance log

Assistant: ChatGPT. This is a truthful record of the initial project generation and a template for completing the three-prompt exercise. Only the first interaction below has occurred in this conversation. Suggested prompts are not evidence of completed interactions or student edits.

## Actual interaction 1
**User prompt:** “This is the second question and Day-2 task, go through this and make this as well. Keep it well aligned with the requirements and dont make the things much complicated too.” The attached assignment specifies a reproducible Python text-statistics CLI, tests, dependency manifest and documentation.

**Produced:** A modular Python CLI, text analyzer, environment checker, dependency manifest, tests and documentation.

**Implementation choices by the assistant:** Used standard-library unittest instead of requiring pytest; used alphabetical tie-breaking and clear exit codes; avoided a dashboard and external packages to keep the task simple. Added optional JSON output and unique word count. These are assistant design choices, not claimed student edits.

**Verification:** Executed `python -m unittest discover -s tests -v` (12 passing tests), `python main.py samples/sample.txt --top 3` (8 words, 6 unique, average 5.62), and `python env_check.py` (Python 3.13.5).

## Suggested interaction 2 — run this prompt during your practice
**Prompt to send:** Review src/text_stats.py for punctuation handling, case normalization and deterministic top-word ties. Explain any changes you recommend.

**Actual assistant output:** [Fill after sending.]
**What I changed or rejected and why:** [Fill after review.]
**Verification:** [Record the actual test command and outcome.]

## Suggested interaction 3 — run this prompt during your practice
**Prompt to send:** Review the CLI and tests for missing files, whitespace-only files, invalid UTF-8 and invalid --top values. Suggest the smallest useful improvement.

**Actual assistant output:** [Fill after sending.]
**What I changed or rejected and why:** [Fill after review.]
**Verification:** [Record actual outcomes.]

## Optional fourth interaction
**Prompt to send:** Review the README setup instructions for a clean Windows computer and check if any step is missing.

Record the actual output, your changes or rejections, reasons and verification if you use this prompt. Do not invent historical prompts or verification results.

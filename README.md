# AI Decision Helper

A local Python decision-support demo for a delivery manager. It chooses a suitable technique for a business requirement, not whether a specific trained model will succeed. All attributes are manually declared; no actual predictions, PAN checks, GST computations or AI model calls are performed.

## Run in VS Code

1. Extract the ZIP and open the `ai_decision_helper` folder in VS Code.
2. Install Python 3.10 or later if necessary. No third-party packages or API keys are required.
3. Open the integrated terminal in that folder and run:

```sh
python test_decision.py
python app.py
```

4. Open http://127.0.0.1:8000 in your browser. Select a demo row to view its rationale and lifecycle, or enter a custom requirement and select its attributes. Download the CSV files using the buttons. Stop the server with Ctrl+C. If the port is busy, run `python app.py --port 8080` and open the corresponding URL. On Windows, `py` may be used instead of `python`.

For a command-line-only run and fresh CSV files:

```sh
python app.py --report-only
```

## AI, ML, deep learning and generative AI

- **AI** is the broad field of systems performing tasks associated with intelligence. Not every business problem needs AI.
- **No AI (rules/code)**: explicit logic, arithmetic, sorting and validation. A PAN format check is syntactic only, not proof of validity or ownership; GST calculation assumes applicable rates and tax rules are supplied.
- **Analytics/BI**: descriptive aggregation, historical dashboards and reporting; no learned prediction is necessary here.
- **Classical ML**: a subset of AI that learns patterns from data; use simpler regression, trees or statistical forecasting baselines for structured predictive tasks.
- **Deep Learning**: a subset of ML using multilayer neural networks; useful for complex visual or other perceptual patterns. Simple image rules may suffice in other contexts.
- **Generative AI**: models that create content such as text, often using deep learning. HR PDF questions use retrieval-augmented generation (RAG) with citations and abstention, assuming natural-language answers are required. Extractive search may suffice if generation is not required.

These are overlapping technical concepts, but the helper assigns one primary delivery category. The rule priority is fixed rules, descriptive analytics, generation, complex perception, then learning. Ambiguous requirements are flagged for clarification rather than automatically recommended AI. Missing data blocks readiness without changing the appropriate technique. The two added requirements are monthly sales trends (BI) and late delivery prediction (ML). Data availability is hypothetical for this demo, not verified business data.

## Project layout

- `decision.py`: typed requirement records, validated attributes, classification, concrete lifecycle tasks and CSV writer.
- `app.py`: CLI and local HTTP server, JSON API, input validation and error handling.
- `index.html`: responsive browser interface, category counts, interactive register and CSV downloads.
- `test_decision.py`: assert-based tests for all ten cases, readiness, invalid combinations, custom lifecycle and CSV row counts.
- `reports/decision_report.csv`: one row per built-in requirement with decision, reasons, risks, first next step and readiness.
- `reports/lifecycle_map.csv`: five stages per AI-suitable case, including task and accountable role. Blocked AI cases retain a proposed lifecycle; do not proceed to model development until data is ready.

Custom evaluations persist only during the current browser session. Browser downloads include custom evaluations; CLI reports contain the ten built-in cases. The app is intended for localhost practice, not production hosting. No external dependencies or real business datasets are included.

## Sample output (actual CLI run)

```text
No AI (rules/code)     | Validate PAN number format
Classical ML           | Predict which customers will cancel next month
Generative AI          | Summarise long support emails
Deep Learning          | Detect defects in product photos
No AI (rules/code)     | Calculate GST on an invoice
Classical ML           | Forecast weekly product demand
Generative AI          | Answer employee questions from the HR policy PDF
No AI (rules/code)     | Sort invoices by amount
Analytics/BI           | Show monthly sales and regional revenue trends
Classical ML           | Predict late deliveries from order history
Reports written to reports/

```

Expected test output:

```text
PASS: all 10 classifications, lifecycle stages, readiness, validation and CSV exports.
```

"""Explainable requirement triage; no trained model or external service required."""
from dataclasses import dataclass, fields
from collections import Counter
import csv
import json
from pathlib import Path

@dataclass(frozen=True)
class Requirement:
    name: str
    fixed_rules: bool = False
    historical_summary: bool = False
    learning: bool = False
    unstructured: bool = False
    complex_perception: bool = False
    generation: bool = False
    data_available: bool = True

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError('Requirement name must not be empty.')
        for f in fields(self)[1:]:
            if type(getattr(self, f.name)) is not bool:
                raise ValueError(f'{f.name} must be yes/no (boolean).')
        if self.complex_perception and not (self.learning and self.unstructured):
            raise ValueError('Complex perception requires learning and unstructured input.')
        if self.fixed_rules and (self.learning or self.generation or self.complex_perception):
            raise ValueError('Fixed rules conflict with essential learning or generation.')
        if self.historical_summary and (self.learning or self.generation):
            raise ValueError('Historical summary conflicts with prediction or generation; split the requirement.')

@dataclass(frozen=True)
class Decision:
    category: str
    reasons: str
    risks: str
    first_next_step: str
    readiness: str

REQUIREMENTS = [
    Requirement('Validate PAN number format', fixed_rules=True),
    Requirement('Predict which customers will cancel next month', learning=True),
    Requirement('Summarise long support emails', unstructured=True, generation=True),
    Requirement('Detect defects in product photos', learning=True, unstructured=True, complex_perception=True),
    Requirement('Calculate GST on an invoice', fixed_rules=True),
    Requirement('Forecast weekly product demand', learning=True),
    Requirement('Answer employee questions from the HR policy PDF', unstructured=True, generation=True),
    Requirement('Sort invoices by amount', fixed_rules=True),
    Requirement('Show monthly sales and regional revenue trends', historical_summary=True),
    Requirement('Predict late deliveries from order history', learning=True, data_available=False),
]

AI_CATEGORIES = {'Classical ML', 'Deep Learning', 'Generative AI'}

def classify(r: Requirement) -> Decision:
    """Choose the simplest sufficient approach; data readiness is separate."""
    if r.fixed_rules:
        d = Decision('No AI (rules/code)', 'Explicit deterministic rules are sufficient.', 'Incorrect rules or malformed input.', 'Define rules and test boundary cases.', 'Ready to scope')
    elif r.historical_summary:
        d = Decision('Analytics/BI', 'Aggregate existing facts; no prediction or generated content needed.', 'Missing records or misleading aggregations.', 'Define metrics and validate source totals.', 'Ready to scope')
    elif r.generation:
        d = Decision('Generative AI', 'The output requires newly composed language or content.', 'Hallucinations, privacy leakage and unsupported claims.', 'Collect approved examples and define human review.', 'Ready to scope')
    elif r.complex_perception:
        d = Decision('Deep Learning', 'Complex unstructured patterns require learned representations.', 'Biased training images, missed defects and distribution shift.', 'Collect and label representative inputs; establish a baseline.', 'Ready to scope')
    elif r.learning:
        d = Decision('Classical ML', 'Learn predictive patterns; start with a simpler statistical or ML baseline.', 'Leakage, bias, drift and inaccurate predictions.', 'Define target, baseline and time-aware validation split.', 'Ready to scope')
    else:
        d = Decision('No AI (rules/code)', 'No essential prediction, generation or analytics objective was specified.', 'Ambiguous requirements may hide a genuine AI need.', 'Clarify expected outputs before implementation.', 'Needs clarification')
    if not r.data_available and d.category != 'No AI (rules/code)':
        return Decision(d.category, d.reasons + ' Required data is not yet available.', d.risks + ' Data readiness is a blocker.', 'Obtain permission and collect representative data before building.', 'Blocked: data missing')
    return d

STAGES = ('Problem framing', 'Data', 'Model', 'Deployment', 'Monitoring')
ROLES = ('Product owner', 'Data engineer', 'Data scientist', 'ML engineer', 'ML engineer')
# Concrete tasks for every AI-suitable built-in requirement, in stage order.
TASKS = {
    REQUIREMENTS[1].name: ('Define cancellation within next month and recall target.', 'Join historical customer activity with cancellation labels.', 'Compare logistic regression and gradient boosting using chronological splits.', 'Publish monthly risk scores to authorised retention staff.', 'Track precision, recall and subgroup drift monthly.'),
    REQUIREMENTS[2].name: ('Define summary length and required action items.', 'Redact personal data from representative support emails.', 'Evaluate prompted summaries against human-written summaries.', 'Integrate a reviewable summary draft into support workflow.', 'Audit omissions, hallucinations and privacy incidents.'),
    REQUIREMENTS[3].name: ('Define defect types and acceptable missed-defect rate.', 'Label photos across lighting, products and production batches.', 'Fine-tune a pretrained vision model and test on held-out batches.', 'Deploy an inspection service with manual review for uncertain photos.', 'Monitor missed defects and camera/lighting drift.'),
    REQUIREMENTS[5].name: ('Set weekly forecast horizon and error metric.', 'Collect weekly sales, stockouts, promotions and calendar features.', 'Compare seasonal naive and lag-feature regression using rolling backtests.', 'Publish weekly forecasts to inventory planners.', 'Monitor MAE and forecast bias by product.'),
    REQUIREMENTS[6].name: ('Define policy question scope and citation requirement.', 'Extract and index approved versioned HR PDF sections with permissions.', 'Evaluate retrieval-augmented generation for grounded answers and abstention.', 'Deploy access-controlled assistant with source references.', 'Audit citation accuracy and refresh indexes after policy changes.'),
    REQUIREMENTS[9].name: ('Define late delivery against promised delivery date.', 'Acquire permission and collect historical delivery outcomes.', 'Compare logistic regression and tree models without future information.', 'Integrate risk scores into dispatch review workflow.', 'Track calibration and recall by route and season.'),
}

def lifecycle(r):
    d = classify(r)
    if d.category not in AI_CATEGORIES:
        return []
    tasks = TASKS.get(r.name)
    if tasks is None:
        model = {'Classical ML': 'Compare a simple predictive baseline with a validated model.', 'Deep Learning': 'Fine-tune a pretrained model and evaluate held-out inputs.', 'Generative AI': 'Evaluate prompted or retrieval-grounded outputs against human references.'}[d.category]
        tasks = (f'Define measurable success and failure for: {r.name}.', 'Collect approved representative inputs and evaluation examples.', model, 'Release a pilot with human review and rollback.', 'Track quality, drift, failures and user feedback.')
    return [{'stage': s, 'task': t, 'role': role} for s,t,role in zip(STAGES,tasks,ROLES)]

def report_rows(requirements):
    return [{'requirement': r.name, 'decision': d.category, 'reasons': d.reasons, 'risks': d.risks, 'first_next_step': d.first_next_step, 'readiness': d.readiness} for r in requirements for d in [classify(r)]]

def export_reports(requirements, folder='reports'):
    requirements = list(requirements)
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True)
    rows = report_rows(requirements)
    with (folder/'decision_report.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['requirement','decision','reasons','risks','first_next_step','readiness']); writer.writeheader(); writer.writerows(rows)
    maps = [{'requirement': r.name, 'decision': classify(r).category, **stage} for r in requirements for stage in lifecycle(r)]
    with (folder/'lifecycle_map.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['requirement','decision','stage','task','role']); writer.writeheader(); writer.writerows(maps)
    return rows

from typing import Optional
from loguru import logger


class ReportEngine:
    def __init__(self):
        self.template_css = """
        <style>
            :root {
                --bg-primary: #0a0a0f;
                --bg-secondary: #12121a;
                --bg-card: #1a1a2e;
                --text-primary: #e8e8f0;
                --text-secondary: #9d9db0;
                --accent-teal: #1dd1a1;
                --accent-blue: #4facfe;
                --accent-yellow: #feca57;
                --accent-red: #ff6b6b;
                --border: #2a2a3e;
                --verified: #1dd1a1;
                --needs-review: #feca57;
                --not-found: #ff6b6b;
            }
            body { font-family: 'Inter', -apple-system, sans-serif; background: var(--bg-primary); color: var(--text-primary); line-height: 1.7; max-width: 900px; margin: 0 auto; padding: 40px 24px; }
            h1 { font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, var(--accent-teal), var(--accent-blue)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; }
            h2 { font-size: 1.4rem; color: var(--accent-teal); border-bottom: 1px solid var(--border); padding-bottom: 8px; margin-top: 36px; }
            h3 { font-size: 1.1rem; color: var(--text-primary); margin-top: 24px; }
            .badge { display: inline-block; padding: 2px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
            .badge-verified { background: rgba(29, 209, 161, 0.15); color: var(--verified); border: 1px solid rgba(29, 209, 161, 0.3); }
            .badge-review { background: rgba(254, 202, 87, 0.15); color: var(--needs-review); border: 1px solid rgba(254, 202, 87, 0.3); }
            .badge-notfound { background: rgba(255, 107, 107, 0.15); color: var(--not-found); border: 1px solid rgba(255, 107, 107, 0.3); }
            table { width: 100%; border-collapse: collapse; margin: 16px 0; background: var(--bg-card); border-radius: 8px; overflow: hidden; }
            th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.9rem; }
            th { background: rgba(29, 209, 161, 0.08); color: var(--accent-teal); font-weight: 600; }
            .card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 16px 0; }
            .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin: 16px 0; }
            .stat-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 16px; text-align: center; }
            .stat-value { font-size: 1.8rem; font-weight: 700; color: var(--accent-teal); }
            .stat-label { font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px; }
            .finding { border-left: 3px solid var(--accent-yellow); padding: 12px 16px; margin: 8px 0; background: rgba(254, 202, 87, 0.05); border-radius: 0 4px 4px 0; }
            .finding.critical { border-left-color: var(--accent-red); background: rgba(255, 107, 107, 0.05); }
            .finding.positive { border-left-color: var(--accent-teal); background: rgba(29, 209, 161, 0.05); }
            .source-ref { color: var(--accent-blue); font-size: 0.8rem; cursor: pointer; text-decoration: underline; text-decoration-style: dotted; }
            .confidence-indicator { display: inline-flex; align-items: center; gap: 4px; font-size: 0.8rem; }
            .ci-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
            .ci-verified { background: var(--verified); }
            .ci-review { background: var(--needs-review); }
            .ci-notfound { background: var(--not-found); }
            ul { padding-left: 20px; }
            li { margin: 6px 0; }
            .header-section { text-align: center; padding: 32px 0; border-bottom: 1px solid var(--border); margin-bottom: 32px; }
            .subtitle { color: var(--text-secondary); font-size: 1rem; }
            .divider { border: none; border-top: 1px solid var(--border); margin: 24px 0; }
            .evidence-box { background: rgba(79, 172, 254, 0.05); border: 1px solid rgba(79, 172, 254, 0.2); border-radius: 6px; padding: 12px; margin: 8px 0; font-size: 0.85rem; }
            .evidence-box .label { color: var(--accent-blue); font-weight: 600; }
            @media print { body { background: white; color: black; } .card, .stat-card { border-color: #ddd; } }
        </style>
        """

    def generate_full_report(self, data: dict) -> str:
        sections = []
        sections.append(self._build_header(data))
        sections.append(self._build_quick_summary(data))
        sections.append(self._build_benefits_table(data))
        sections.append(self._build_coverage_table(data))
        sections.append(self._build_exclusions(data))
        sections.append(self._build_waiting_periods(data))
        sections.append(self._build_hidden_conditions(data))
        sections.append(self._build_claim_score(data))
        sections.append(self._build_coverage_adequacy(data))
        sections.append(self._build_suggestions(data))
        sections.append(self._build_mis_selling(data))
        sections.append(self._build_claim_scenarios(data))
        sections.append(self._build_trust_score(data))
        sections.append(self._build_sources(data))
        sections.append(self._build_verdict(data))
        sections.append(self._build_footer())

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('title', 'Your Insurance Explained')} - Insurance Copilot</title>
    {self.template_css}
</head>
<body>
    {''.join(sections)}
</body>
</html>"""

    def _build_header(self, data: dict) -> str:
        return f"""
        <div class="header-section">
            <h1>📋 {data.get('title', 'Your Insurance Explained')}</h1>
            <p class="subtitle">{data.get('subtitle', 'Comprehensive policy analysis report')}</p>
            <p class="subtitle" style="font-size:0.8rem;margin-top:4px;">
                Generated by Insurance Copilot &middot; {data.get('generated_at', '')}
                &middot; <span class="badge badge-verified">Evidence-Based Report</span>
            </p>
        </div>"""

    def _build_quick_summary(self, data: dict) -> str:
        summary = data.get("summary", {})
        return f"""
        <h2>Quick Summary</h2>
        <div class="card">
            <p>{summary.get('overview', 'No summary available.')}</p>
        </div>
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-value">{summary.get('total_benefits', 0)}</div>
                <div class="stat-label">Total Benefits</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('total_coverage', 'N/A')}</div>
                <div class="stat-label">Total Coverage</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('claim_score', 'N/A')}/10</div>
                <div class="stat-label">Claim Experience Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('confidence', 'N/A')}</div>
                <div class="stat-label">Overall Confidence</div>
            </div>
        </div>"""

    def _build_benefits_table(self, data: dict) -> str:
        benefits = data.get("benefits", [])
        if not benefits:
            return ""
        rows = ""
        for b in benefits:
            conf = b.get("confidence", "verified")
            badge = "badge-verified" if conf == "verified" else ("badge-review" if conf == "needs_review" else "badge-notfound")
            rows += f"""
            <tr>
                <td>{b.get('name', '')}</td>
                <td>{b.get('description', 'N/A')[:100]}</td>
                <td>{b.get('coverage_amount', 'N/A')}</td>
                <td><span class="badge {badge}">{conf.replace('_', ' ')}</span></td>
            </tr>"""
        return f"""
        <h2>Benefits Breakdown</h2>
        <table>
            <thead>
                <tr>
                    <th>Benefit</th>
                    <th>Description</th>
                    <th>Coverage Amount</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>"""

    def _build_coverage_table(self, data: dict) -> str:
        coverages = data.get("coverage_items", [])
        if not coverages:
            return ""
        rows = ""
        for c in coverages:
            conf = c.get("confidence", "verified")
            badge = "badge-verified" if conf == "verified" else ("badge-review" if conf == "needs_review" else "badge-notfound")
            rows += f"""
            <tr>
                <td>{c.get('benefit', '')}</td>
                <td>{c.get('covered', 'N/A')}</td>
                <td>{c.get('amount', 'N/A')}</td>
                <td>{c.get('waiting_period', 'N/A')}</td>
                <td>{c.get('conditions', 'N/A')[:60]}</td>
                <td><span class="badge {badge}">{c.get('status', 'N/A')}</span></td>
                <td style="font-size:0.8rem;">{c.get('source', 'N/A')}</td>
            </tr>"""
        return f"""
        <h2>Coverage Table</h2>
        <table>
            <thead>
                <tr>
                    <th>Benefit</th>
                    <th>Covered</th>
                    <th>Amount Covered</th>
                    <th>Waiting Period</th>
                    <th>Conditions</th>
                    <th>Status</th>
                    <th>Source</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>"""

    def _build_exclusions(self, data: dict) -> str:
        exclusions = data.get("exclusions", [])
        if not exclusions:
            return ""
        items = "".join(f"<li>{e}</li>" for e in exclusions)
        return f"""
        <h2>Exclusions</h2>
        <div class="card">
            <ul>{items}</ul>
        </div>"""

    def _build_waiting_periods(self, data: dict) -> str:
        periods = data.get("waiting_periods", [])
        if not periods:
            return ""
        items = "".join(f"<li><strong>{p.get('benefit', '')}:</strong> {p.get('period', '')}</li>" for p in periods)
        return f"""
        <h2>Waiting Periods</h2>
        <div class="card">
            <ul>{items}</ul>
        </div>"""

    def _build_hidden_conditions(self, data: dict) -> str:
        conditions = data.get("hidden_conditions", [])
        if not conditions:
            return ""
        items = "".join(
            f'<div class="finding {c.get("severity", "info")}"><strong>{c.get("title", "")}</strong><p>{c.get("description", "")}</p></div>'
            for c in conditions
        )
        return f"""
        <h2>Hidden Conditions & Clauses</h2>
        {items}"""

    def _build_claim_score(self, data: dict) -> str:
        cs = data.get("claim_score", {})
        return f"""
        <h2>Claim Experience Score</h2>
        <div class="card">
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-value">{cs.get('score', 'N/A')}/10</div>
                    <div class="stat-label">Overall Score</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{cs.get('ease', 'N/A')}/10</div>
                    <div class="stat-label">Claim Ease</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{cs.get('documentation', 'N/A')}/10</div>
                    <div class="stat-label">Doc Readiness</div>
                </div>
            </div>
            <p>{cs.get('explanation', '')}</p>
        </div>"""

    def _build_coverage_adequacy(self, data: dict) -> str:
        ca = data.get("coverage_adequacy", {})
        return f"""
        <h2>Coverage Adequacy</h2>
        <div class="card">
            <p><strong>Rating:</strong> {ca.get('rating', 'N/A')}/10</p>
            <p>{ca.get('analysis', '')}</p>
            <ul>{"".join(f'<li>{s}</li>' for s in ca.get('gaps', []))}</ul>
        </div>"""

    def _build_suggestions(self, data: dict) -> str:
        suggestions = data.get("suggestions", [])
        if not suggestions:
            return ""
        items = "".join(f'<div class="finding positive"><strong>{s.get("title", "")}</strong><p>{s.get("description", "")}</p></div>' for s in suggestions)
        return f"""
        <h2>Suggestions & Recommendations</h2>
        {items}"""

    def _build_mis_selling(self, data: dict) -> str:
        ms = data.get("mis_selling", {})
        if not ms:
            return ""
        findings = ms.get("findings", [])
        items = "".join(
            f'<div class="finding {f.get("severity", "info")}"><span class="badge badge-{f.get("severity", "info")}">{f.get("severity", "info")}</span> <strong>{f.get("title", "")}</strong><p>{f.get("description", "")}</p></div>'
            for f in findings
        )
        return f"""
        <h2>Mis-Selling Detection</h2>
        {items}
        <p><strong>Severity:</strong> <span class="badge badge-{ms.get('severity', 'low')}">{ms.get('severity', 'low')}</span></p>
        <p>{ms.get('summary', '')}</p>"""

    def _build_claim_scenarios(self, data: dict) -> str:
        scenarios = data.get("claim_scenarios", [])
        if not scenarios:
            return ""
        items = "".join(
            f"""<div class="card">
                <h3>Scenario: {s.get('title', '')}</h3>
                <p>{s.get('description', '')}</p>
                <p><strong>Estimated Payout:</strong> {s.get('estimated_payout', 'N/A')}</p>
                <p><strong>Likelihood:</strong> {s.get('likelihood', 'N/A')}</p>
            </div>"""
            for s in scenarios
        )
        return f"""
        <h2>Example Claim Scenarios</h2>
        {items}"""

    def _build_trust_score(self, data: dict) -> str:
        ts = data.get("trust_score", {})
        return f"""
        <h2>Company Trust Score</h2>
        <div class="card">
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-value">{ts.get('score', 'N/A')}/10</div>
                    <div class="stat-label">Trust Score</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{ts.get('claim_ratio', 'N/A')}%</div>
                    <div class="stat-label">Claim Settlement Ratio</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{ts.get('solvency', 'N/A')}%</div>
                    <div class="stat-label">Solvency Ratio</div>
                </div>
            </div>
            <p>{ts.get('explanation', '')}</p>
        </div>"""

    def _build_sources(self, data: dict) -> str:
        sources = data.get("sources", [])
        if not sources:
            return ""
        items = "".join(
            f'<div class="evidence-box"><span class="label">📄 {s.get("title", "Source")}</span><br>{s.get("description", "")}<br><span style="color:var(--text-secondary);font-size:0.75rem;">Confidence: {s.get("confidence", "N/A")}</span></div>'
            for s in sources
        )
        return f"""
        <h2>Sources & Evidence</h2>
        {items}"""

    def _build_verdict(self, data: dict) -> str:
        verdict = data.get("verdict", {})
        return f"""
        <h2>Final Verdict</h2>
        <div class="card" style="border-color: var(--accent-teal);">
            <p><strong>Overall Rating:</strong> {verdict.get('rating', 'N/A')}/10</p>
            <p>{verdict.get('summary', '')}</p>
            <ul>{"".join(f'<li>{p}</li>' for p in verdict.get('pros', []))}</ul>
            <ul>{"".join(f'<li>{c}</li>' for c in verdict.get('cons', []))}</ul>
        </div>"""

    def _build_footer(self) -> str:
        return """
        <hr class="divider">
        <div style="text-align:center;font-size:0.75rem;color:var(--text-secondary);padding:20px 0;">
            <p>Generated by Insurance Copilot &mdash; Evidence-Based Insurance Intelligence Platform</p>
            <p>This report is for informational purposes only. Verify all details with your insurer.</p>
        </div>"""


report_engine = ReportEngine()

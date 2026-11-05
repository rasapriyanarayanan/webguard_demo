"""WebGuard Flask application."""
from __future__ import annotations

import io
from xml.sax.saxutils import escape

from flask import Flask, jsonify, render_template, request, send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from scanner import scan

app = Flask(__name__, template_folder="templates")


@app.get("/")
def home():
    # Flask looks for templates/index.html by default.
    return render_template("index.html")


@app.post("/api/scan")
def api_scan():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Send scan details as JSON."), 400

    if not data.get("consent"):
        return jsonify(error="Please confirm you own or have permission to test this site."), 400

    url = str(data.get("url", "")).strip()
    mode = str(data.get("mode", "public")).strip().lower()
    if mode not in ("public", "local"):
        return jsonify(error="Mode must be 'public' or 'local'."), 400

    try:
        return jsonify(scan(url, mode))
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    except Exception as exc:
        # Keep the API response readable instead of exposing a traceback to the browser.
        return jsonify(error=f"Scan failed: {type(exc).__name__}"), 502


@app.post("/api/report")
def api_report():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("findings"), list):
        return jsonify(error="Run a scan before generating the report."), 400

    styles = getSampleStyleSheet()
    buffer = io.BytesIO()

    target = escape(str(data.get("url", "Unknown")))
    scanned_at = escape(str(data.get("scanned_at", "Unknown")))
    score = escape(str(data.get("score", "N/A")))
    risk = escape(str(data.get("risk", "Unknown")))

    elements = [
        Paragraph("WebGuard Security Report", styles["Title"]),
        Paragraph(
            f"Target: {target}<br/>Scanned: {scanned_at}<br/>Score: {score}/100 ({risk})",
            styles["Normal"],
        ),
        Spacer(1, 12),
    ]

    rows = [["Check", "Status", "Details"]]
    for finding in data["findings"]:
        if not isinstance(finding, dict):
            continue
        rows.append([
            Paragraph(escape(str(finding.get("title", "Check"))), styles["Normal"]),
            escape(str(finding.get("status", "unknown")).upper()),
            Paragraph(escape(str(finding.get("detail", ""))), styles["Normal"]),
        ])

    table = Table(rows, colWidths=[150, 60, 280], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.extend([table, Spacer(1, 14), Paragraph("Recommended Fixes (nginx examples)", styles["Heading2"])])

    for finding in data["findings"]:
        if not isinstance(finding, dict) or finding.get("status") not in ("review", "info"):
            continue
        fix = finding.get("fix") or {}
        title = escape(str(finding.get("title", "Finding")))
        problem = escape(str(fix.get("problem", "")))
        solution = escape(str(fix.get("solution", "")))
        snippet = escape(str(fix.get("snippet", "")))
        elements.extend([
            Paragraph(f"<b>{title}</b>: {problem} {solution}", styles["Normal"]),
            Paragraph(f"<font name='Courier' size=8>{snippet}</font>", styles["Normal"]),
            Spacer(1, 6),
        ])

    elements.append(Paragraph(
        "Note: basic header assessment only; not a full penetration test.",
        styles["Italic"],
    ))
    SimpleDocTemplate(buffer, pagesize=A4).build(elements)
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="webguard_report.pdf",
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

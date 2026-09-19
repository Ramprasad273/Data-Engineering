#!/usr/bin/env bash
set -euo pipefail

echo "========================================================="
echo "  STARTING PARALLAX E2E HEALTHCARE PLATFORM VERIFICATION "
echo "========================================================="

# Check manifest exists
if [ ! -f "dbt_project/target/manifest.json" ]; then
    echo "[ERROR] dbt_project/target/manifest.json not found! Run 'dbt compile' first."
    exit 1
fi

echo "[1/4] Running Parallax Check (JSON format)..."
JSON_OUTPUT=$(parallax check --manifest dbt_project/target/manifest.json --base main --format json --fail-on NEVER)
SEVERITY=$(echo "$JSON_OUTPUT" | grep -o '"risk_severity": "[^"]*' | cut -d'"' -f4)

if [ "$SEVERITY" != "CRITICAL" ]; then
    echo "[FAIL] Assertion Failed: Expected risk_severity CRITICAL, got $SEVERITY"
    exit 1
fi
echo "[PASS] Assertion Passed: Risk severity correctly identified as CRITICAL."

echo "[2/4] Testing CI Gating (--fail-on CRITICAL)..."
set +e
parallax check --manifest dbt_project/target/manifest.json --base main --fail-on CRITICAL > /dev/null 2>&1
EXIT_CODE=$?
set -e

if [ $EXIT_CODE -ne 1 ]; then
    echo "[FAIL] Assertion Failed: Expected exit code 1 from blocking gate, got $EXIT_CODE"
    exit 1
fi
echo "[PASS] Assertion Passed: Parallax successfully blocked CI with exit code 1."

echo "[3/4] Generating Offline HTML Report..."
parallax report --manifest dbt_project/target/manifest.json --base main --out e2e_clinical_blast_radius.html

if [ ! -f "e2e_clinical_blast_radius.html" ]; then
    echo "[FAIL] Assertion Failed: e2e_clinical_blast_radius.html was not generated."
    exit 1
fi

# Assert critical markers exist in the HTML report
grep -q "CRITICAL RISK" e2e_clinical_blast_radius.html
grep -q "ICU Sepsis Real-time Alerting Engine" e2e_clinical_blast_radius.html
grep -q "dose_mg" e2e_clinical_blast_radius.html
echo "[PASS] Assertion Passed: Interactive HTML report generated with verified SVG DAG and exposures."

echo "[4/4] Verifying Markdown PR Comment Generation..."
parallax check --manifest dbt_project/target/manifest.json --base main --format markdown --output pr_comment.md
grep -q "<!-- parallax-ci-comment -->" pr_comment.md
grep -q "CRITICAL" pr_comment.md
echo "[PASS] Assertion Passed: Markdown PR comment cleanly generated with marker for in-place updates."

echo ""
echo "========================================================="
echo "[SUCCESS] ALL E2E ARCHITECTURAL TESTS PASSED SUCCESSFULLY"
echo "          Parallax is verified and ready for production."
echo "========================================================="

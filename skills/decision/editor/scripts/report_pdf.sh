#!/usr/bin/env bash
# Render a report to PDF (A4) and print the page count.
# Usage, from the project root: bash <skill dir>/scripts/report_pdf.sh runs/RNN-<slug>/out/report.md
set -euo pipefail
md="$1"; dir="$(dirname "$md")"; here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
pandoc "$md" -o "$tmp/report.docx" --resource-path="$dir" --reference-doc="$here/reference.docx"
soffice --headless --convert-to pdf --outdir "$tmp" "$tmp/report.docx" >/dev/null 2>&1
mv "$tmp/report.pdf" "$dir/report.pdf"
echo "pages: $(pdfinfo "$dir/report.pdf" | awk '/^Pages/ {print $2}')  file: $dir/report.pdf"

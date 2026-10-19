#!/usr/bin/env bash
# Render a brief to PDF (A4) and print the page count.
# Usage, from the project root: bash <skill dir>/scripts/brief_pdf.sh runs/RNN-<slug>/out/brief.md
set -euo pipefail
md="$1"; dir="$(dirname "$md")"; here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p scratch
pandoc "$md" -o scratch/brief.docx --resource-path="$dir" --reference-doc="$here/reference.docx"
soffice --headless --convert-to pdf --outdir scratch scratch/brief.docx >/dev/null 2>&1
mv scratch/brief.pdf "$dir/brief.pdf"
echo "pages: $(pdfinfo "$dir/brief.pdf" | awk '/^Pages/ {print $2}')  file: $dir/brief.pdf"

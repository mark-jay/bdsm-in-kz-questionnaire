#!/bin/bash

# Exit on any error
set -e

# Variables
README_FILE="README.md"
TEX_FILE="output.tex"
PDF_FILE="output.pdf"
DOCKER_IMAGE="texlive/texlive:latest"
WORKSPACE=$(pwd)

# Step 1: Ensure README.md exists
if [[ ! -f "$README_FILE" ]]; then
  echo "Error: $README_FILE does not exist."
  exit 1
fi

python3 convert_to_latex.py "$README_FILE" "$TEX_FILE"

# Verify TEX_FILE exists
if [[ ! -f "$TEX_FILE" ]]; then
  echo "Error: $TEX_FILE was not created."
  exit 1
fi

# Step 2: Build PDF using LaTeX in Docker
docker run --rm -v "$WORKSPACE":/workspace -w /workspace "$DOCKER_IMAGE" bash -c "\
  tlmgr install babel-russian && \
  pdflatex -interaction=nonstopmode $TEX_FILE && \
  pdflatex -interaction=nonstopmode $TEX_FILE"

# Verify PDF_FILE exists
if [[ ! -f "$PDF_FILE" ]]; then
  echo "Error: $PDF_FILE was not created."
  exit 1
fi

# Step 3: Output success message
echo "PDF built successfully: $PDF_FILE"

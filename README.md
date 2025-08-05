# C Code Rewriter with Guidelines using Mistral Codestral API and Streamlit

## Overview
This project is a Streamlit web application that allows users to upload a C code file and guideline text, then sends a request to the Mistral Codestral API to rewrite the code as per the guidelines. The app displays the improved code alongside the original, provides explanations, maintains a revision history, and allows feedback submission.

## Features
- Upload C code and guidelines or choose from pre-built guideline templates.
- Requests code rewriting from Mistral's Codestral API.
- Displays original and improved code side-by-side with syntax highlighting.
- Shows detailed explanations of code changes.
- Download improved code as a `.c` file.
- Save revision history with timestamps.
- User feedback system with star rating and comments.
- Attractive, fun UI with styled text and colors.

## Prerequisites
- Python 3.8 or higher
- Mistral Codestral API key (set as environment variable `MISTRAL_API_KEY`)

## Installation

1. Clone the repository or copy the project files.
2. Create and activate a Python virtual environment (optional but recommended):


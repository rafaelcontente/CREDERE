
> **This runbook provides the operational procedures required to install, execute, troubleshoot and maintain the public CREDERE demonstration repository.**

The objective is to allow any developer, researcher or evaluator to reproduce the published results without requiring assistance from the original author.

---

# Intended Audience

This document is intended for:

- Software Engineers
- AI Engineers
- Researchers
- Students
- Reviewers
- Recruiters
- Technical Evaluators

No prior knowledge of the internal CREDERE platform is required.

---

# Repository Scope

This public repository demonstrates two production-oriented modules extracted from the complete CREDERE architecture:

- Compliance Engine
- Explanation Engine

The demonstration intentionally excludes infrastructure components such as APIs, databases and cloud deployment.

---

# System Requirements

Minimum requirements:

| Component | Requirement |
|------------|-------------|
| Operating System | Windows, Linux or macOS |
| Python | 3.11 or newer |
| pip | Latest version recommended |
| RAM | 4 GB minimum |
| Disk Space | <500 MB |
| Internet | Required only for installation |

---

# Repository Structure

```
credere/

├── credere/
│   ├── compliance/
│   ├── explanation/
│   └── ...
│
├── tests/
│
├── docs/
│
├── run_demo_isolated.py
│
├── pyproject.toml
│
├── README.md
│
└── LICENSE
```

---

# Initial Setup

Clone the repository:

```bash
git clone <repository-url>

cd credere
```

---

## Create Virtual Environment

Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -e .
```

Verify installation:

```bash
python --version
```

Expected:

```
Python 3.11+
```

---

# Running the Demonstration

Execute:

```bash
python run_demo_isolated.py
```

Expected behaviour:

- sample decision is created;
- Compliance Engine evaluates legal constraints;
- Explanation Engine generates customer explanation;
- Fact Checker verifies numerical consistency;
- results are displayed in the console.

No additional configuration is required.

---

# Expected Output

Typical execution demonstrates:

```
Prediction

↓

Compliance Evaluation

↓

Explanation Generation

↓

Fact Verification

↓

Final Decision
```

You should observe:

- compliance verdict;
- explanation text;
- verification result;
- audit information.

---

# Running the Test Suite

Execute:

```bash
pytest
```

or

```bash
python -m pytest
```

Expected result:

```
All tests passed
```

---

# Updating Dependencies

Update pip:

```bash
python -m pip install --upgrade pip
```

Reinstall project:

```bash
pip install -e .
```

---

# Common Operational Tasks

## Run Demonstration

```bash
python run_demo_isolated.py
```

---

## Execute Tests

```bash
pytest
```

---

## Reinstall Package

```bash
pip uninstall credere

pip install -e .
```

---

## Clean Python Cache

Linux/macOS

```bash
find . -name "__pycache__" -type d -exec rm -r {} +
```

Windows

Delete all

```
__pycache__
```

folders.

---

# Troubleshooting

## ModuleNotFoundError

### Cause

Package not installed.

### Solution

```bash
pip install -e .
```

---

## Import Errors

### Cause

Incorrect working directory.

### Solution

Run commands from the repository root.

---

## Missing Dependencies

### Cause

Incomplete installation.

### Solution

```bash
pip install -e .
```

---

## Pytest Not Found

Install pytest:

```bash
pip install pytest
```

---

## Virtual Environment Not Activated

Symptoms:

- packages cannot be found;
- imports fail.

Solution:

Activate the virtual environment before executing the project.

---

## Permission Errors

Linux/macOS

```bash
chmod +x run_demo_isolated.py
```

Windows

Run terminal as normal user (administrator privileges are not required).

---

# Expected Demonstration Behaviour

## Compliance Module

Expected:

- compliant applications remain unchanged;
- illegal applications are vetoed;
- manual review is triggered when appropriate.

Unexpected:

- compliance rule ignored;
- veto not applied.

---

## Explanation Module

Expected:

- explanation generated;
- numerical values match decision;
- Fact Checker returns success.

Unexpected:

- inconsistent numbers;
- hallucinated values;
- failed verification.

---

# Debugging Guide

## Step 1

Confirm installation.

```bash
pip install -e .
```

---

## Step 2

Run demonstration.

```bash
python run_demo_isolated.py
```

---

## Step 3

Run automated tests.

```bash
pytest
```

---

## Step 4

Inspect console output.

Look for:

- import errors;
- validation failures;
- assertion failures;
- traceback messages.

---

## Step 5

If behaviour differs from the published documentation:

- verify Python version;
- verify package installation;
- reinstall dependencies;
- rerun tests.

---

# Operational Assumptions

The demonstration assumes:

- trusted local execution;
- standard Python environment;
- no external services;
- no network dependencies after installation.

---

# Known Limitations

The public repository intentionally does not include:

- REST API
- Authentication
- Database
- Cloud deployment
- Monitoring
- CI/CD
- Production infrastructure

These components belong to the complete CREDERE platform and are outside the scope of this demonstration.

---

# Reproducing Published Results

To reproduce the repository demonstration:

1. Clone the repository.
2. Create a virtual environment.
3. Install the package.
4. Execute:

```bash
python run_demo_isolated.py
```

5. Run:

```bash
pytest
```

The observed behaviour should match the examples described in the documentation.

---

# Reporting Issues

When reporting an issue, include:

- Operating System
- Python version
- Repository version
- Exact command executed
- Complete error message
- Stack trace (if available)
- Steps required to reproduce the issue

Providing this information significantly improves reproducibility and debugging.

---

# Escalation

For issues that cannot be reproduced using this runbook:

1. Verify the installation procedure.
2. Verify the Python version.
3. Execute the complete test suite.
4. Compare behaviour against the documentation.
5. Open a GitHub Issue including all diagnostic information.

---

# Maintenance Recommendations

Before updating the repository:

- execute the complete test suite;
- review documentation;
- verify demonstration scripts;
- ensure reproducibility remains unchanged.

Documentation should evolve alongside the codebase.

---

# Operational Principles

The public repository is intentionally designed to be:

- simple to install;
- deterministic to execute;
- easy to reproduce;
- straightforward to validate;
- independent of proprietary infrastructure.

Every published demonstration should produce consistent behaviour across supported environments.

---

# Conclusion

This runbook provides the operational procedures required to install, execute, validate and troubleshoot the public CREDERE repository.

Its purpose is to ensure that the published work remains reproducible, transparent and independently verifiable, allowing reviewers, researchers and practitioners to evaluate the project without relying on the original author.

> **Reproducibility is a cornerstone of trustworthy software engineering. A system that cannot be independently reproduced cannot be independently trusted.**
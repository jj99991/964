# PrescriptionForecast: Pharmaceutical Demand Planning Platform
**Target Platform:** Windows / macOS / Linux (Browser-Based Streamlit Application)  
**Project Deployment URL:** [StreamLit Cloud](https://qi9q5gz3camhcwkogkzjjs.streamlit.app/)  

## Project Overview
PrescriptionForecast is a supervised machine learning web application developed for a retail pharmacy chain. The platform addresses the critical operational challenge of balancing pharmaceutical overstocking costs (and subsequent medicine expiration waste) against the risks of drug stockouts. 

Utilizing historical [daily transactional data](https://www.kaggle.com/datasets/milanzdravkovic/pharma-sales-data) across 8 Anatomical Therapeutic Chemical (ATC) drug classifications, the system trains a supervised Multiple Linear Regression model to forecast future continuous numerical sales demand based on user-selected year and month values.

You can view the live application by clicking on this [link](https://qi9q5gz3camhcwkogkzjjs.streamlit.app/)  

---

## Directory Structure
The submitted zip archive (`SourceCode.zip`) contains the complete local development environment structured as follows:

```text
PrescriptionForecast/
│
├── app.py                      # Monolithic Streamlit UI and dashboard layout
├── requirements.txt            # Frozen environment package dependency manifest
├── README.md                   # Evaluator deployment and execution guide (This file)
│
├── data/
│   └── salesdaily.csv          # Raw pre-aggregated historical daily sales dataset
│
└── src/
    ├── __init__.py             # Structural Python package initializer
    ├── preprocessing.py        # Feature reduction and One-Hot encoding pipelines
    └── model_trainer.py        # Train/test split and regression training engines

```

---

## Local Deployment Instructions

### Step 1: Extract the Archive

1. Download the archive file `SourceCode.zip`.
2. Right-click the file and select `Extract All...`.
3. Choose a convenient local directory and complete the extraction.

### Step 2: Open Terminal Context

1. Open the Windows Start Menu, search for **PowerShell** and launch it.
2. Navigate directly into the root directory of your extracted project folder by executing:

### Step 3a: Verify Python Version

Check the version of Python installed in your system:

```powershell
python --version
```
Ensure that the version of python matches the following:
| Python Version | Patch Level | Status |
| :------------- | ----------- | --------: |
| Python 3.12 | 3.12.10 | ✅ |
| Python 3.13 | 3.13.14 | ✅ |
| Python 3.14 | 3.14.6 | ✅ |

### Step 3b: Activate the Python Virtual Environment

Set up the virtual environment:

```powershell
# Create the local virtual environment folder
python -m venv .venv

# Activate the virtual environment shell
# Note: If PowerShell blocks execution, run: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

```

*(When successfully activated, your terminal prompt string will be prepended with `(.venv)`).*

### Step 4: Install the required packages

Utilize the requirements.txt with pip to resolve all required dependencies

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

```

### Step 5: Execute the Streamlit Web Application

Launch the live local rendering server by executing the primary script hook which automatically opens a browser tab:

```powershell
streamlit run app.py
```

*If a browser tab does not automatically open, then go to the following link:*
```powershell
http://localhost:8501
```

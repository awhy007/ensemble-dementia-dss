# Ensemble Machine Learning Framework for Dementia-Related Cognitive-Status Classification

This repository supports the MSc project **Development of an Ensemble Machine Learning Framework for Early Dementia and Alzheimer's Disease Classification with a Prototype Decision Support System**.

The project compares five individual machine-learning classifiers with soft-voting and stacking ensembles. Eligible OASIS-1 records are used for model development and internal validation. Baseline records from OASIS-2 are kept separately to evaluate performance on previously unseen participants.

## Scope

The model predicts two CDR-based categories:

- `CDR = 0`: no recorded cognitive impairment.
- `CDR > 0`: recorded cognitive impairment or dementia.

The software was developed for university research. Its output must not be interpreted as a medical diagnosis or used to make treatment or care decisions.

## Locked modelling result

Soft voting was selected using mean outer-fold Macro F1 on OASIS-1. On the independent OASIS-2 test sample, it achieved:

- Accuracy: 0.8733
- Macro F1: 0.8684
- ROC-AUC: 0.9350
- Sensitivity: 0.7846
- Specificity: 0.9412

Its internal advantage over Random Forest was very small. The dissertation therefore treats the findings as a comparison of approaches rather than proof that an ensemble is always superior.

## Dataset

The tabular files were obtained from Jacob Boysen's [MRI and Alzheimers dataset on Kaggle](https://www.kaggle.com/datasets/jboysen/mri-and-alzheimers). The underlying data originate from the Open Access Series of Imaging Studies (OASIS).

The dataset files are not included in this repository. See [data/README.md](data/README.md) for the expected filenames, provenance and citations.

## Prototype

The repository includes a local Gradio interface that loads the locked soft-voting model, validates the seven required inputs and returns a CDR-based category and probability. It accepts fictional demonstration data only and does not store submissions.

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/app.py
```

After the application starts, open the local address printed by Gradio on the same computer. This is for local development and is not a public deployment link.

To run the automated checks, install the development requirements and execute:

```powershell
pip install -r requirements-dev.txt
python -m pytest -q
```

## Repository status

The validated modelling notebook, locked result files, working prototype, automated tests and technical design and testing evidence are included. Ethics documents, participant responses and the dissertation appendices are retained separately and are not published in this repository.

## Repository structure

```text
data/       Dataset instructions only; no participant-level files
docs/       Design, risk and testing evidence
models/     Fitted model used by the research prototype
notebooks/  Final reproducible modelling notebook
results/    Locked model-evaluation evidence
src/        Prototype source code
tests/      Automated tests and fictional test cases
```

## Reproducibility environment

- Python 3.13.15
- scikit-learn 1.6.1
- NumPy 2.1.3
- pandas 2.2.3
- Random seed 42

Full dataset fingerprints are recorded in `results/reproducibility_record.json`.

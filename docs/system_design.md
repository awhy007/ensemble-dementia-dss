# Prototype system design

## High-level design

```text
Fictional case inputs
        |
        v
Input validation
        |
        v
DataFrame with seven model fields
        |
        v
Locked soft-voting bundle
  - fitted preprocessing
  - five tuned base models
  - probability averaging
        |
        v
CDR-based category and probability
        |
        v
Research-only result explanation
```

## Component responsibilities

- `src/prediction.py` will load the trusted model bundle, validate inputs and calculate the ensemble probability.
- `src/app.py` will define the Gradio interface and present the result.
- `tests/` will verify valid inputs, boundaries, error handling and deterministic predictions.
- `models/selected_model_bundle.joblib` is the locked model produced by the final notebook.

The prediction function is kept separate from the interface so it can be tested without launching a web page.


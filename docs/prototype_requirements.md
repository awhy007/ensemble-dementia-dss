# Prototype requirements

## Purpose

The prototype demonstrates how the selected soft-voting model can be accessed through a simple decision-support interface. It predicts the likelihood of the two CDR-based categories used during model development. It is a university research prototype, not a diagnostic or treatment system.

## Intended evaluation users

The interface is intended for usability evaluation by the participant groups approved through the project ethics process. Evaluation must use fictional demonstration cases only. Users must not enter information about themselves, patients, relatives or another identifiable person.

## Model inputs

The interface must collect the seven variables used by the locked model, in the same order and with the same column names.

| Display name | Model field | Accepted values | Guidance |
|---|---|---:|---|
| Sex | `M/F` | Female or Male | Encoded by the fitted preprocessing pipeline. |
| Age | `Age` | 33-96 years | Range observed across the eligible analysis samples. |
| Socioeconomic status | `SES` | 1-5 | OASIS SES scale; 1 is highest status and 5 is lowest. |
| MMSE score | `MMSE` | 14-30 | Range observed in the eligible analysis samples. |
| Estimated total intracranial volume | `eTIV` | 1123-1992 cm3 | Derived MRI-volume measure in the source files. |
| Normalised whole-brain volume | `nWBV` | 0.644-0.847 | Proportion reported in the source files. |
| Atlas scaling factor | `ASF` | 0.881-1.563 | Scaling measure reported in the source files. |

The prototype must reject missing, non-numeric and out-of-range values with a clear field-specific message. It must not silently modify a user's input.

## Model output

For a valid fictional case, the prototype must show:

1. The model used: Soft Voting Ensemble.
2. The predicted category: `CDR = 0` or `CDR > 0`.
3. The predicted probability of `CDR > 0`, rounded to one decimal percentage point.
4. A short explanation that the probability describes model output, not certainty about a person's health.
5. A persistent statement that the result is not a medical diagnosis or treatment recommendation.

Avoid labels such as "high risk," "low risk," "Alzheimer's detected," or "cognitively normal." These phrases would claim more than the model target supports.

## Interface requirements

- Display the full project title in shortened, readable form.
- Explain CDR the first time it appears.
- Display the research-only notice before the input form and beside the result.
- Provide a Predict button and a Clear button.
- Do not store submitted values.
- Do not request names, email addresses, patient identifiers or free-text clinical information.
- Include two or more fictional example cases for testing and participant evaluation.
- Remain usable on a laptop without horizontal scrolling.

## Functional acceptance criteria

| ID | Test | Expected result |
|---|---|---|
| PT-01 | Submit a valid fictional case | A category and probability are displayed without an error. |
| PT-02 | Submit the minimum permitted value for every numeric field | The case is accepted. |
| PT-03 | Submit the maximum permitted value for every numeric field | The case is accepted. |
| PT-04 | Leave a required value blank | A clear validation message identifies the missing field. |
| PT-05 | Enter a value below an accepted range | The prediction is blocked and the permitted range is shown. |
| PT-06 | Enter a value above an accepted range | The prediction is blocked and the permitted range is shown. |
| PT-07 | Select Clear after entering values | Inputs and outputs return to their initial state. |
| PT-08 | Review the page before entering data | The research-only and fictional-data notices are visible. |
| PT-09 | Run repeated valid predictions | The same inputs return the same result. |
| PT-10 | Inspect application behaviour | No submitted values are written to a local data file or log. |

## Evidence to retain

- Screenshot of the initial interface.
- Screenshot of one valid fictional result.
- Screenshot of one blocked invalid input.
- Automated test output.
- Completed manual acceptance-test table.
- Measured response time for a small set of fictional cases.
- Version of the model bundle and software requirements used by the prototype.


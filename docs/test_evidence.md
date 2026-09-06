# Prototype test evidence

## Test environment

- Test date: 3 September 2026
- Operating system: Windows
- Prototype framework: Gradio 6.26.0
- Model compatibility environment: scikit-learn 1.6.1, NumPy 2.1.3 and pandas 2.2.3
- Test data: fictional demonstration values only

## Automated verification

Thirteen automated tests passed. These tests cover valid cases, both output categories, minimum and maximum accepted values, missing values, out-of-range values, non-integer values where whole numbers are required, invalid sex values, repeatability and model-bundle integrity.

```text
.............                                                            [100%]
13 passed in 4.37s
```

## Browser-based acceptance checks

| Criterion | Evidence | Result |
|---|---|---|
| PT-01 Valid fictional case | Example B returned `CDR > 0` and displayed a probability | Pass |
| PT-04 Required value omitted | A blank age was rejected with `Age is required and must be numeric.` | Pass |
| PT-07 Clear control | Clear reset the age field and output | Pass |
| PT-08 Research notice | The initial page displayed the fictional-data and non-diagnostic warning | Pass |
| Laptop layout | At a 1440-pixel viewport, page and content widths were both 1440 pixels | Pass |

The remaining range-boundary and repeatability criteria are covered by the automated tests. Source inspection confirmed that the application contains no file-writing or database operation for submitted values.

## Response-time check

Two fictional cases were alternated for 20 predictions on the local test computer. Loading the model and making the first prediction took 2,424.568 ms. Once loaded, mean prediction time was 52.477 ms, median time was 51.938 ms and the maximum was 59.586 ms. These figures describe the local test environment and should not be generalised to every computer.

## Retained screenshots

- `prototype_initial.png`: initial interface and research warning.
- `prototype_valid_result.png`: fictional example B after prediction.
- `prototype_invalid_input.png`: missing-age validation message.

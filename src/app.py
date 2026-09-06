"""Gradio interface for the university research prototype."""

from __future__ import annotations

import os

import gradio as gr

try:
    from .prediction import predict_case
except ImportError:  # Allows `python src/app.py` from the repository root.
    from prediction import predict_case


NOTICE = """
### University research prototype

Use **fictional demonstration values only**. Do not enter information about
yourself, a patient, a relative or another identifiable person. The output is a
model prediction of a CDR-based category and is **not a medical diagnosis or a
treatment recommendation**.
"""


def present_prediction(sex, age, ses, mmse, etiv, nwbv, asf):
    """Format a valid prediction or a field-specific validation error."""
    try:
        result = predict_case(sex, age, ses, mmse, etiv, nwbv, asf)
    except (ValueError, TypeError) as error:
        return f"### Input required\n\n{error}"

    percentage = result["probability"] * 100
    return f"""
### Research classification: `{result['category']}`

**Category description:** {result['category_explanation']}  
**Model-estimated probability of `CDR > 0`:** {percentage:.1f}%  
**Model used:** {result['model']}

This percentage is the model's output for the fictional values entered. It is
not certainty about a person's health and must not be interpreted as a medical
diagnosis or treatment recommendation.
"""


with gr.Blocks(
    title="CDR-Based Cognitive-Status Research Prototype",
    analytics_enabled=False,
    fill_width=False,
) as demo:
    gr.Markdown(
        "# Ensemble Machine Learning Prototype for Dementia-Related Classification\n"
        "### Research decision-support interface using CDR-based categories"
    )
    gr.Markdown(NOTICE)

    with gr.Row():
        with gr.Column():
            sex = gr.Radio(["Female", "Male"], label="Sex", value=None)
            age = gr.Number(label="Age (years)", minimum=33, maximum=96, step=1, value=None)
            ses = gr.Number(
                label="Socioeconomic status (1 = highest, 5 = lowest)",
                minimum=1,
                maximum=5,
                step=1,
                value=None,
            )
            mmse = gr.Number(label="MMSE score", minimum=14, maximum=30, step=1, value=None)
        with gr.Column():
            etiv = gr.Number(
                label="Estimated total intracranial volume (eTIV, cm3)",
                minimum=1123,
                maximum=1992,
                value=None,
            )
            nwbv = gr.Number(
                label="Normalised whole-brain volume (nWBV)",
                minimum=0.644,
                maximum=0.847,
                value=None,
            )
            asf = gr.Number(
                label="Atlas scaling factor (ASF)",
                minimum=0.881,
                maximum=1.563,
                value=None,
            )

    result = gr.Markdown("### Result\n\nLoad a sample case and select **Predict**.")

    inputs = [sex, age, ses, mmse, etiv, nwbv, asf]
    with gr.Row():
        predict_button = gr.Button("Predict", variant="primary")
        clear_button = gr.ClearButton(inputs + [result], value="Clear")

    gr.Markdown("### Sample cases for evaluation")
    with gr.Row():
        example_a = gr.Button("Load sample case 1")
        example_b = gr.Button("Load sample case 2")

    predict_button.click(
        fn=present_prediction,
        inputs=inputs,
        outputs=result,
        api_visibility="private",
    )

    reset_result = "### Result\n\nReview the fictional values and select **Predict**."
    example_a.click(
        fn=lambda: ("Female", 72, 2, 28, 1400, 0.755, 1.250, reset_result),
        inputs=[],
        outputs=inputs + [result],
        api_visibility="private",
    )
    example_b.click(
        fn=lambda: ("Male", 80, 3, 22, 1500, 0.690, 1.170, reset_result),
        inputs=[],
        outputs=inputs + [result],
        api_visibility="private",
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
        show_error=True,
    )

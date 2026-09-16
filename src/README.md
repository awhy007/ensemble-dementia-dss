# Prototype source

This directory contains the implemented Gradio research prototype:

- `app.py` defines the participant-facing interface, sample cases, warnings and result display.
- `prediction.py` validates the seven inputs, loads the locked soft-voting model bundle and returns the CDR-based category and model-estimated probability.
- `__init__.py` identifies the directory as the prototype source package.

The interface accepts fictional demonstration values only. It is not a medical device and must not be used for diagnosis, treatment or care decisions.

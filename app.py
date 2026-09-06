"""Deployment entry point for the Gradio research prototype."""

import os

from src.app import demo


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
        show_error=True,
    )

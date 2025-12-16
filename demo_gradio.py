import gradio as gr
from main import run_pipeline_async
import asyncio

def gradio_pipeline(input_text):
    return asyncio.run(run_pipeline_async({"text": input_text}))

iface = gr.Interface(
    fn=gradio_pipeline,
    inputs=gr.Textbox(lines=8, placeholder="Enter your scenario here..."),
    outputs=gr.Textbox(lines=30),
    title="AI Judge Demo",
    description="Paste any scenario and see the AI agents, Judge reasoning, and final decision."
)

iface.launch()

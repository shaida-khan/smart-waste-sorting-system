import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image

model = tf.keras.models.load_model("model/smart_waste_model.keras")

class_names = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

def predict_waste(image):
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array)
    predicted_index = np.argmax(predictions[0])
    predicted_class = class_names[predicted_index]
    confidence = float(predictions[0][predicted_index])

    recyclable = {
        "cardboard": "Yes ♻️",
        "glass": "Yes ♻️",
        "metal": "Yes ♻️",
        "paper": "Yes ♻️",
        "plastic": "Sometimes ♻️",
        "trash": "No ❌"
    }

    bin_type = {
        "cardboard": "Recycling Bin",
        "glass": "Recycling Bin",
        "metal": "Recycling Bin",
        "paper": "Recycling Bin",
        "plastic": "Check Local Rules",
        "trash": "General Waste Bin"
    }

    return f"""
🧠 Prediction: {predicted_class.upper()}

📊 Confidence: {confidence * 100:.2f}%

♻️ Recyclable: {recyclable[predicted_class]}

🗑️ Recommended Bin: {bin_type[predicted_class]}
"""

custom_css = """
body {
    background: #0f172a;
}

.gradio-container {
    max-width: 100% !important;
    padding: 20px 60px !important;
}

#hero {
    width: 100%;
}

#title {
    text-align: center;
    padding: 25px;
    background: linear-gradient(135deg, #064e3b, #0f766e);
    color: white;
    border-radius: 18px;
    margin-bottom: 20px;
}

#title h1 {
    font-size: 34px;
    margin-bottom: 8px;
}

#title p {
    font-size: 16px;
    color: #ecfeff;
}
"""

with gr.Blocks(css=custom_css, title="Smart Waste Sorting System") as app:

    gr.HTML("""
    <div id="title">
        <h1>♻️ Smart Waste Sorting System</h1>
        <p>AI-powered waste image classification for smarter recycling decisions</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=2):
            image_input = gr.Image(
                type="pil",
                label="Upload Waste Image",
                height=350
            )

        with gr.Column(scale=1):
            result_output = gr.Textbox(
                label="♻️ AI Waste Analysis",
                lines=6
            )

    with gr.Row():
        predict_button = gr.Button("♻️ Classify Waste", variant="primary")
        clear_button = gr.Button("Clear")

    gr.Markdown("""
    ### Supported Categories
    Cardboard • Glass • Metal • Paper • Plastic • Trash

    ### Real-World Use
    Used in recycling plants, smart cities, and waste sorting automation.
    """)

    predict_button.click(
        fn=predict_waste,
        inputs=image_input,
        outputs=result_output
    )

    clear_button.click(
        fn=lambda: (None, ""),
        inputs=None,
        outputs=[image_input, result_output]
    )

app.launch(inbrowser=True)

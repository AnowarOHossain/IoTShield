
# TinyLlama Setup Guide (Step-by-Step)

This guide provides a clear, step-by-step process to set up TinyLlama for local inference and integrate it into your IoTShield project for anomaly detection.

---

## Step 1: System Requirements

- Python 3.8 or newer
- pip (Python package manager)
- At least 4GB RAM (8GB recommended)
- Sufficient disk space for model weights (~1-2GB)
- (Optional) GPU for faster inference

---

## Step 2: Create and Activate a Virtual Environment (Recommended)

Open a terminal in your project directory and run:

**Windows:**
```
python -m venv .venv
.venv\Scripts\activate
```
**Linux/Mac:**
```
python3 -m venv .venv
source .venv/bin/activate
```

---

## Step 3: Install Required Python Packages

Install PyTorch and HuggingFace Transformers:
```
pip install torch transformers
```

> **Note:** You do NOT need to install TinyLlama from GitHub or PyPI. The model is available via HuggingFace and can be loaded directly using transformers.

---

## Step 4: Download TinyLlama Model Weights

The model weights will be downloaded automatically the first time you load the model using transformers. If you want to download manually, visit:
- https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0

---

## Step 5: Test TinyLlama Model Loading

Create a new Python file (e.g., `test_tinylama.py`) and add the following code:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

prompt = "Is this sensor reading anomalous? Data: 23.5, 45.2, 67.1"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=32)
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
```

Run the script:
```
python test_tinylama.py
```

If you see a response, TinyLlama is set up correctly.

---

## Step 6: Integrate TinyLlama into Your Project

1. Create a new file in your backend, e.g., `iotshield_backend/tinylama_anomaly_detector.py`.
2. Move the model loading and inference code into this file.
3. Replace all Gemini API calls in your project with calls to your TinyLlama-based detector.
4. Design clear prompts for anomaly detection (e.g., include sensor type, value, and context).
5. Test with real sensor data to validate results.

---

## Step 7: Troubleshooting

- **Out of Memory:** Ensure you have enough RAM. Try running on CPU if you have CUDA errors.
- **Slow Inference:** Use a machine with a GPU or reduce the input size.
- **Model Not Downloading:** Check your internet connection and HuggingFace access.

---

## References

- [TinyLlama GitHub](https://github.com/jzhang38/TinyLlama)
- [HuggingFace Model Card](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)
- [Transformers Documentation](https://huggingface.co/docs/transformers/index)

---

For further help, consult the official TinyLlama and HuggingFace documentation.
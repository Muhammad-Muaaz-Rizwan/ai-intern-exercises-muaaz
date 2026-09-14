from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
    device_map="cpu"
)

class GenerateRequest(BaseModel):
    prompt: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate")
def generate(req: GenerateRequest):
    if not req.prompt or not req.prompt.strip():
        return {"error": "Prompt cannot be empty"}

    try:
        inputs = tokenizer(req.prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=200, do_sample=True, temperature=0.7)
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"response": response_text}

    except Exception as e:
        return {"error": f"Model failed to generate a response: {str(e)}"}
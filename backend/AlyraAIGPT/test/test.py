import torch
from transformers import AutoTokenizer, AutoModelForCausalLM,BitsAndBytesConfig

# MODEL_ID = "OxOv3rH4uL/alyra-houseplan-qwen2.5-3b"
BASE_MODEL = r"C:\Users\91994\.cache\huggingface\hub\models--OxOv3rH4uL--alyra-houseplan-qwen2.5-3b\snapshots\2eefd156f08fa7e4dc3a949a1a0bc1e4d6d67086"

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

quantization = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)


model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    device_map="auto",
    torch_dtype="auto",
    quantization_config= quantization,
)

print("Model loaded successfully!")

prompt = """
Generate a HousePlan JSON based on the user's house requirements.
I need a house with a living room, kitchen, toilet and bedroom.
"""

messages = [
    {
        "role": "user",
        "content": prompt
    }
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

inputs = tokenizer(
    text,
    return_tensors="pt"
).to(model.device)

print("\nGenerating...\n")

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=1024,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )

new_tokens = outputs[0][inputs.input_ids.shape[1]:]

response = tokenizer.decode(
    new_tokens,
    skip_special_tokens=True
)

print("MODEL OUTPUT:")
print("=" * 80)
print(response)
print("=" * 80)
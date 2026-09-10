from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
import torch
from validation import LayoutValidator

from pydantic import BaseModel
from data_models import HousePlan


class GenerateRequest(BaseModel):
    request: str

app = FastAPI()

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

validator = LayoutValidator()


def generate_plan(model,tokenizer,prompt):
    p = """
Generate a HousePlan JSON based on the user's house requirements.
\n
"""
    p = p+prompt
    messages = [
        {
            "role": "user",
            "content": p
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

    return response


@app.post("/generate")
def generate(request: GenerateRequest):

    og_request = request.request
    generation_prompt = og_request
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):

        response = generate_plan(
            model,
            tokenizer,
            generation_prompt
        )
        print(response)
        plan = HousePlan.model_validate_json(response)
        validation_errors = validator.validate(plan)
        print(validation_errors)
        if len(validation_errors) == 0:
            print("HousePlan is valid!")
            return {
                "success": True,
                "house_plan": response
            }
        if attempt == max_attempts:
            return {
                "success": False,
                "message": "Model failed to generate a valid HousePlan.",
                "errors": validation_errors
            }

        generation_prompt = f"""
Original request:
{og_request}
The previously generated HousePlan was invalid.
Validation errors:
{validation_errors}
Generate a completely new HousePlan that satisfies the original request
and fixes ALL of the validation errors above.

Return only the HousePlan JSON.
"""

    
    return {
        "success": False,
        "message": "Unexpected generation failure."
    }
            
        

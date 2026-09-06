import torch
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from helpers import extract_floors_rooms
from prompt_builder import build_prompt
import sys,json

BASE_MODEL = r"C:\Users\91994\.cache\huggingface\hub\models--Qwen--Qwen2.5-1.5B-Instruct\snapshots\989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
MAX_SEQ_LENGTH = 512


#My gpu is 4gb vram so we need 4bit quantization
quantization = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=quantization,
    device_map="auto"
)

# print("model loaded finally")
# print(model.device)


def generate_text(model, tokenizer, prompt):

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
    )

    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    # print("Input tokens:", inputs["input_ids"].shape)
    print("Starting generation...")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=80,
            do_sample=True,
            temperature = 0.8,
            top_p = 0.9
        )


    new_tokens = outputs[0, inputs["input_ids"].shape[1]:]

    return tokenizer.decode(
        new_tokens,
        skip_special_tokens=True
    ).strip()


# def generate_house_plan_description(housePlan):
    




# def generate_text(model, tokenizer, prompt):
#     messages = [
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ]

#     text = tokenizer.apply_chat_template(
#         messages,
#         tokenize=False,
#         add_generation_prompt=True
#     )

#     inputs = tokenizer(
#         text,
#         return_tensors="pt"
#     ).to(model.device)

#     with torch.no_grad():
#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=100,
#             do_sample=True,
#             temperature=0.7,
#             top_p=0.9
#         )

#     new_tokens = outputs[0, inputs.input_ids.shape[1]:]

#     return tokenizer.decode(
#         new_tokens,
#         skip_special_tokens=True
#     ).strip()



# for line in sys.stdin:
#   line = line.strip()
#   if not line:
#     continue
#   try:
#     job = json.loads(line)
#     house_plan = job["house_plan"]
#     req = extract_floors_rooms(house_plan)
#     prompt = build_prompt(req)
#     res = generate_text(model,tokenizer,prompt)
#     result = {
#        "request" : res
#     }
#     print(json.dumps(result), flush=True)

    
#   except Exception as e:
#     error = {
#           "error": str(e)
#       }
#     print(
#         json.dumps(error),
#         flush=True
#     )
        





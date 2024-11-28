from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load pre-trained GPT-2 model and tokenizer for text generation
generation_model = GPT2LMHeadModel.from_pretrained("gpt2")
generation_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Function to generate detailed answer based on specialty and question
def generate_answer(specialty, question):
    # Combine specialty with the user's question to create a relevant prompt
    prompt = f"As an {specialty}, here is the treatment for {question}:"
    
    # Tokenize the input prompt
    inputs = generation_tokenizer(prompt, return_tensors="pt")

    # Generate the answer using the GPT-2 model
    outputs = generation_model.generate(inputs["input_ids"], max_length=200, num_return_sequences=1)
    
    # Decode the generated text
    response = generation_tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return response

# Example usage
specialty = "Endocrinologist"  # This should come from the classification model
question = "What are the treatments for diabetes?"
answer = generate_answer(specialty, question)
print(f"Answer: {answer}")

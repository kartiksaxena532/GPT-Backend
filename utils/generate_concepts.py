from dotenv import load_dotenv
load_dotenv()
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("API_KEY"))  # Update your environment variable accordingly
print("🔑 OpenAI API key loaded successfully.")
def generate_overview_and_concepts(description, claims):
    # Prepare claims section (include up to 3 claims for better depth)
    claim_text = "\n".join(claims[:3]) if claims else "No claims found."

    # Structured prompt for the model
    prompt = f"""
You are an experienced patent analyst and technical consultant with deep understanding of complex inventions across industries.

You are provided with the complete description and claims of a granted patent. Your task is to analyze the content very carefully and produce two outputs:

---

🧩 OUTPUT 1 — Overview  
Write a clear, concise technical overview in 1–2 paragraphs that:
- Summarizes the invention in plain technical terms
- Captures the main function and purpose of the invention
- Avoids marketing language and legal boilerplate
- Can be easily understood by engineers or technical professionals

---

🔬 OUTPUT 2 — In-depth Concept  
Write a deep, structured technical explanation in 4–6 paragraphs that:
- Breaks down the novel technical ideas and concepts
- Highlights the core problem the invention solves
- Explains how the invention solves it (compared to prior approaches)
- Describes the system or method step-by-step if applicable
- Clearly references at least one independent claim to justify the invention’s technical contribution
- Uses technical vocabulary from the patent — do not oversimplify

---

🧠 Important Instructions:
- Do not skip or summarize broadly. Read and process the entire content.
- Use original terminology when appropriate (e.g., antenna structure, transceiver, memory buffer)
- Be objective and technical, not promotional.
- Assume the reader is a technical person, not the patent author.

---

--- START OF DESCRIPTION ---
{description}
--- END OF DESCRIPTION ---

--- START OF CLAIMS ---
{claim_text}
--- END OF CLAIMS ---

Return output in the following JSON format:

{{
  "overview": "...",
  "in_depth_concept": "..."
}}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-nano",  # You can use "gpt-4.0" or fallback to "gpt-4"
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = completion.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print("❌ GPT-4 analysis failed:", str(e))
        return {
            "overview": "Failed to generate overview due to GPT error.",
            "in_depth_concept": "Failed to generate in-depth concept due to GPT error."
        }

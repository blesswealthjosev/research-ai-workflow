import os
import csv
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE")

def execute_vibe_workflow(input_csv_path, output_md_path):
    system_prompt = """
    You are a peer-level academic research assistant optimizing literature matrices.
    Process input raw strings into a strict hierarchical markdown structure.
    
    ## Structural Rules
    1. Never exceed 4 highly technical, data-anchored bullet points per segment.
    2. Isolate quantitative evidence, experimental cohorts, and statistical proofs.
    
    ## Target Output Format
    ### [Article Title]
    * **Source URL:** [Insert Link]
    * **Main Argument:** [1 Sentence overarching theme]
    * **Evidence Base:** [Isolate experimental numbers, cohorts, or specific test models]
    * **Definitive Conclusion:** [The primary theoretical or industrial takeaway]
    """
    
    compiled_summaries = ["# Literature Review Synthesis Matrix\n**Target Document Format:** Strict Academic Layout\n\n---\n"]
    

    with open(input_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row["Article Title"]
            url = row["Source Link"]
            domain = row["Core Domain/Tag"]
            
            user_context = f"Analyze and extract from: Title: {title} | Domain: {domain} | Link: {url}"
            
                        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_context}
                ],
                temperature=0.2
            )
            
            compiled_summaries.append(response.choices[0].message.content)
            compiled_summaries.append("\n---\n")
            
        with open(output_md_path, mode='w', encoding='utf-8') as output_file:
        output_file.writelines(compiled_summaries)

if __name__ == "__main__":
    execute_vibe_workflow("generated/research_workflow_dataset.csv", "generated/literature_summaries_output.md")

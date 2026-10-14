import os
import csv
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE")

def execute_vibe_workflow(input_csv_path, output_md_path):
    print("🚀 Initializing Literature Synthesis Workflow...")
    
        if not os.path.exists(input_csv_path):
        print(f"❌ Error: Cannot find input database at {input_csv_path}")
        return

    system_prompt = """
    You are a professional, peer-level academic research assistant optimizing literature matrices.
    Process the provided article context into a highly structured, standard markdown format.
    
    ## Structural Rules:
    1. Keep points concise, professional, and student-friendly.
    2. Isolate core methodologies, quantitative data, and experimental evidence.
    3. Ensure a consistent, predictable hierarchy for all summaries.
    """
    
       timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    compiled_summaries = [
        "# Research Literature Review Matrix\n",
        f"**Generated On:** {timestamp} | **Status:** Production Ready\n",
        "\n---\n"
    ]
    
        with open(input_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        article_count = 0
        
        for row in reader:
            article_count += 1
            title = row.get("Article Title", "Untitled Article")
            url = row.get("Source Link", "No Link Provided")
            domain = row.get("Core Domain/Tag", "General")
            
            print(f"📖 Processing [{article_count}]: {title}...")
            
            user_context = f"""
            Please summarize this article according to the standard layout:
            - **Article Title:** {title}
            - **Domain/Field:** {domain}
            - **Source Link:** {url}
            
            Provide:
            1. **Main Idea:** A clear 1-2 sentence overarching theme.
            2. **Supporting Points:** 3-4 data-anchored, technical bullet points.
            3. **Key Takeaways:** Practical conclusions or theoretical breakthroughs.
            """
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_context}
                    ],
                    temperature=0.2
                )
                
                # Append the structured markdown output
                compiled_summaries.append(response.choices[0].message.content)
                compiled_summaries.append("\n\n---\n\n")
            except Exception as e:
                print(f"⚠️ Failed to summarize '{title}': {str(e)}")
                
        with open(output_md_path, mode='w', encoding='utf-8') as output_file:
        output_file.writelines(compiled_summaries)
        
    print(f"✅ Success! Compiled {article_count} summaries inside: {output_md_path}")

if __name__ == "__main__":
    execute_vibe_workflow("generated/research_workflow_dataset.csv", "generated/literature_summaries_output.md")

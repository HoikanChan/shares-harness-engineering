import os

def consolidate_docs(source_dir, output_file, part_files):
    """
    Consolidates multiple Markdown files into one.
    """
    full_content = ["# Harness Engineering：駕馭 AI 的藝術 - 完整課程文檔\n"]
    
    # Add a brief intro
    full_content.append("本文件由李宏毅教授《AI Agent (1/3)：核心技術Context Engineering 基本概念解說》視頻字幕整理而成。\n")
    full_content.append("---\n")

    for part in part_files:
        file_path = os.path.join(source_dir, part)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                full_content.append(content)
                full_content.append("\n---\n")
        else:
            print(f"Warning: {file_path} not found.")

    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write('\n'.join(full_content))
    
    print(f"✅ Consolidated document created: {output_file}")

if __name__ == "__main__":
    SOURCE_DIR = "hungyi-lee-harness-engineering"
    OUTPUT_FILE = os.path.join(SOURCE_DIR, "Harness_Engineering_Full_Document.md")
    
    PART_FILES = [
        "part_01_intro_experiment.md",
        "part_02_model_behavior.md",
        "part_03_ai_agent_components.md",
        "part_04_cognitive_framework.md",
        "part_05_tool_boundary.md",
        "part_06_workflow.md",
        "part_07_feedback_learning.md",
        "part_08_model_emotion.md",
        "part_09_lifelong_agent.md",
        "part_10_verbalized_feedback.md",
        "part_11_evaluation_challenge.md",
        "part_12_meta_harness.md",
    ]

    consolidate_docs(SOURCE_DIR, OUTPUT_FILE, PART_FILES)

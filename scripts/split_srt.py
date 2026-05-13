import os
import re

def clean_and_split_srt(input_file, tasks, output_dir):
    """
    Splits an SRT file into multiple Markdown parts and removes indices and timestamps.
    
    :param input_file: Path to the original .srt file
    :param tasks: List of dicts, e.g., [{"name": "part_01.md", "title": "Title", "start": 1, "end": 616}, ...]
    :param output_dir: Directory to save the output files
    """
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()

    # Regex for SRT timestamps: 00:00:00,000 --> 00:00:00,000
    timestamp_pattern = re.compile(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}')

    for task in tasks:
        file_name = os.path.join(output_dir, task['name'])
        title = task.get('title', '')
        start_idx = task['start'] - 1  # Convert to 0-based
        end_idx = task['end']          # Slicing is exclusive at the end

        segment_lines = all_lines[start_idx:end_idx]
        cleaned_content = []

        if title:
            cleaned_content.append(f"# {title}\n")

        for line in segment_lines:
            stripped = line.strip()
            # Skip empty lines
            if not stripped:
                continue
            # Skip SRT indices (purely numeric lines)
            if stripped.isdigit():
                continue
            # Skip timestamp lines
            if timestamp_pattern.match(stripped):
                continue
            
            cleaned_content.append(stripped)

        with open(file_name, 'w', encoding='utf-8') as out_f:
            out_f.write('\n'.join(cleaned_content) + '\n')
        
        print(f"✅ Generated: {file_name} ({len(cleaned_content)} lines of text)")

if __name__ == "__main__":
    # --- 配置區 ---
    INPUT_SRT = os.path.join("hungyi-lee-harness-engineering", "raw", "youtube_transcript.zh-TW.srt")
    OUTPUT_DIR = "hungyi-lee-harness-engineering"
    
    SPLIT_TASKS = [
        {"name": "part_01_intro_experiment.md", "title": "Part 01: 引言與失敗的初次實驗", "start": 1, "end": 616},
        {"name": "part_02_model_behavior.md", "title": "Part 02: 模型行為轉變與成功案例", "start": 617, "end": 984},
        {"name": "part_03_ai_agent_components.md", "title": "Part 03: AI Agent 的構成與演進", "start": 985, "end": 1944},
        {"name": "part_04_cognitive_framework.md", "title": "Part 04: 認知框架與自然語言 Harness", "start": 1945, "end": 3448},
        {"name": "part_05_tool_boundary.md", "title": "Part 05: 工具邊界與 Agent First 介面", "start": 3449, "end": 4888},
        {"name": "part_06_workflow.md", "title": "Part 06: 標準工作流程 (SOP)", "start": 4889, "end": 5752},
        {"name": "part_07_feedback_learning.md", "title": "Part 07: Feedback 學習與 Textual Gradient", "start": 5753, "end": 6748},
        {"name": "part_08_model_emotion.md", "title": "Part 08: 模型情緒與 Steering 實驗", "start": 6749, "end": 8120},
        {"name": "part_09_lifelong_agent.md", "title": "Part 09: Lifelong Agent：終身伴侶計畫", "start": 8121, "end": 9552},
        {"name": "part_10_verbalized_feedback.md", "title": "Part 10: Verbalized Feedback：從對話中進化", "start": 9553, "end": 11124},
        {"name": "part_11_evaluation_challenge.md", "title": "Part 11: 評量的挑戰與 AI Judge 局限性", "start": 11125, "end": 11864},
        {"name": "part_12_meta_harness.md", "title": "Part 12: Meta Harness 與未來展望", "start": 11865, "end": 12141},
    ]

    clean_and_split_srt(INPUT_SRT, SPLIT_TASKS, OUTPUT_DIR)

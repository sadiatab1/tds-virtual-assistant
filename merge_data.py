import os
import json

COURSE_CONTENT_FILE = "course_content.json"
MARKDOWN_DIR = "markdown_files"
MERGED_OUTPUT_FILE = "merged_data.json"

def load_course_content():
    if not os.path.exists(COURSE_CONTENT_FILE):
        print("❌ Course content file not found.")
        return []

    with open(COURSE_CONTENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_discourse_threads():
    threads = []
    if not os.path.exists(MARKDOWN_DIR):
        print("❌ Markdown directory not found.")
        return threads

    for filename in os.listdir(MARKDOWN_DIR):
        if filename.endswith(".md"):
            thread_title = filename.replace(".md", "")
            with open(os.path.join(MARKDOWN_DIR, filename), "r", encoding="utf-8") as f:
                content = f.read()
            threads.append({
                "title": thread_title,
                "content": content
            })
    return threads

def merge_data(course_content, threads):
    merged = []

    for week_data in course_content:
        merged.append({
            "week": week_data.get("week", "Unknown"),
            "title": week_data.get("title", ""),
            "videos": week_data.get("videos", []),
            "assignments": week_data.get("assignments", []),
            "discourse_threads": []  # Placeholder for now
        })

    # Option 1: If you want to just add all threads to the end (generic approach)
    merged.append({
        "week": "Discourse Threads",
        "title": "Community Discussions",
        "videos": [],
        "assignments": [],
        "discourse_threads": threads
    })

    return merged

def save_merged_data(data):
    with open(MERGED_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Merged data saved to {MERGED_OUTPUT_FILE}")

if __name__ == "__main__":
    print("🔄 Merging course content with discourse threads...")
    course_data = load_course_content()
    discourse_threads = load_discourse_threads()
    merged_result = merge_data(course_data, discourse_threads)
    save_merged_data(merged_result)



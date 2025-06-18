import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import html2text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_ID = "34"
CATEGORY_JSON_URL = f"{BASE_URL}/c/courses/tds-kb/{CATEGORY_ID}.json"
DOWNLOAD_DIR = "downloaded_threads"
MARKDOWN_DIR = "markdown_files"

# Ensure directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(MARKDOWN_DIR, exist_ok=True)

# Fetch and save HTML files (simulated or via JSON if possible)
async def fetch_json(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def download_threads():
    async with aiohttp.ClientSession() as session:
        print("📡 Fetching category JSON...")
        try:
            data = await fetch_json(session, CATEGORY_JSON_URL)
        except:
            print("⚠️ Couldn't fetch category JSON. Skipping live download.")
            return

        topic_list = data.get("topic_list", {}).get("topics", [])
        print(f"📥 Found {len(topic_list)} topics")

        for i, topic in enumerate(topic_list):
            topic_id = topic["id"]
            slug = topic["slug"]
            thread_url = f"{BASE_URL}/t/{slug}/{topic_id}"
            print(f"🔗 [{i+1}] Downloading: {thread_url}")
            thread_html = await fetch_page(session, thread_url)
            with open(f"{DOWNLOAD_DIR}/{slug}_{topic_id}.html", "w", encoding="utf-8") as f:
                f.write(thread_html)

# Convert downloaded HTML to Markdown
def html_to_markdown(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    posts = soup.select('.cooked')

    text_maker = html2text.HTML2Text()
    text_maker.body_width = 0

    full_markdown = ""
    for post in posts:
        html = str(post)
        md = text_maker.handle(html)
        full_markdown += md + "\n---\n"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_markdown)

if __name__ == "__main__":
    # Optionally run scraping (if API accessible)
    try:
        asyncio.run(download_threads())
    except Exception as e:
        print(f"❌ Error during download: {e}")

    # Convert all downloaded HTML files to Markdown
    for filename in os.listdir(DOWNLOAD_DIR):
        if filename.endswith(".html"):
            input_file = os.path.join(DOWNLOAD_DIR, filename)
            output_file = os.path.join(MARKDOWN_DIR, filename.replace(".html", ".md"))
            html_to_markdown(input_file, output_file)
            print(f"✅ Converted {filename} → Markdown")

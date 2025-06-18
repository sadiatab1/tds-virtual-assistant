import asyncio
import json
from playwright.async_api import async_playwright

URL = "https://tds.s-anand.net/#/2025-01/"
OUTPUT_FILE = "course_content.json"

async def scrape_course_content():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print(f"🌐 Navigating to {URL}")
        await page.goto(URL)
        
        print("⏳ Waiting for lecture items to load...")
        await page.wait_for_selector("li.file")  # Updated selector
        
        lecture_elements = await page.query_selector_all("li.file")
        print(f"📄 Found {len(lecture_elements)} lecture entries")

        lectures = []

        for element in lecture_elements:
            anchor = await element.query_selector("a")
            if anchor:
                title = await anchor.inner_text()
                href = await anchor.get_attribute("href")
                if title and href:
                    lectures.append({
                        "title": title.strip(),
                        "url": f"https://tds.s-anand.net{href}"
                    })

        await browser.close()

        # Save to JSON
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(lectures, f, indent=2, ensure_ascii=False)

        print(f"✅ Scraped {len(lectures)} lectures. Saved to {OUTPUT_FILE}.")

if __name__ == "__main__":
    asyncio.run(scrape_course_content())

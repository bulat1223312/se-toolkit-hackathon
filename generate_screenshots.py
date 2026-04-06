#!/usr/bin/env python3
"""Generate screenshots for presentation using Playwright"""

import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        
        # Start the server first
        import subprocess
        server = subprocess.Popen(
            ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        await asyncio.sleep(2)  # Wait for server to start
        
        try:
            # Screenshot 1: FAQ Search
            await page.goto("http://localhost:8000")
            await page.wait_for_timeout(1000)
            
            # Type a question
            await page.fill("#question", "when is the deadline for project")
            await page.wait_for_timeout(500)
            
            # Press Enter
            await page.press("#question", "Enter")
            await page.wait_for_timeout(1500)
            
            await page.screenshot(path="/root/smart-faq-helper/screenshot_search.png", full_page=True)
            print("✓ Screenshot 1: Search saved")
            
            # Screenshot 2: Category Browse
            await page.goto("http://localhost:8000")
            await page.wait_for_timeout(1000)
            
            # Click on "exams" category
            exams_cat = page.locator(".cat-item", has_text="exams")
            if await exams_cat.count() > 0:
                await exams_cat.first.click()
                await page.wait_for_timeout(1500)
                await page.screenshot(path="/root/smart-faq-helper/screenshot_categories.png", full_page=True)
                print("✓ Screenshot 2: Categories saved")
            else:
                # Fallback: show main page
                await page.screenshot(path="/root/smart-faq-helper/screenshot_categories.png", full_page=True)
                print("✓ Screenshot 2: Main page (fallback)")
            
            # Screenshot 3: Dark Mode
            await page.goto("http://localhost:8000")
            await page.wait_for_timeout(1000)
            
            # Click dark mode button
            dark_btn = page.locator("#darkBtn")
            if await dark_btn.count() > 0:
                await dark_btn.click()
                await page.wait_for_timeout(500)
            
            # Type something to show dark mode
            await page.fill("#question", "exam rules")
            await page.press("#question", "Enter")
            await page.wait_for_timeout(1500)
            
            await page.screenshot(path="/root/smart-faq-helper/screenshot_dark.png", full_page=True)
            print("✓ Screenshot 3: Dark mode saved")
            
        finally:
            server.terminate()
            server.wait()
            await browser.close()
    
    print("\n✅ All screenshots generated!")

if __name__ == "__main__":
    asyncio.run(main())

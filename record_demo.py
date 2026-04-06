#!/usr/bin/env python3
"""
Record automated demo video for Smart FAQ Helper
Shows: search, autocomplete, categories, dark mode, tic-tac-toe, history
Output: MP4 video (uses Playwright's built-in video)
"""

import asyncio
import subprocess
import os
from playwright.async_api import async_playwright

async def main():
    print("🚀 Starting FAQ server...")
    server = subprocess.Popen(
        ["python3", "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8003"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    await asyncio.sleep(2)

    print("🎬 Recording demo video...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir="/root/smart-faq-helper/",
            record_video_size={"width": 1280, "height": 720}
        )
        page = await context.new_page()
        
        await page.goto("http://127.0.0.1:8003")
        await page.wait_for_timeout(1500)
        
        # Scene 1: FAQ Search with autocomplete
        print("📝 1. FAQ Search (15s)")
        await page.type("#question", "when is the deadline for project", delay=60)
        await page.wait_for_timeout(2000)
        await page.press("#question", "Enter")
        await page.wait_for_timeout(3000)
        
        # Scene 2: Another search
        print("🔍 2. Another search (10s)")
        await page.fill("#question", "exam rules")
        await page.wait_for_timeout(800)
        await page.press("#question", "Enter")
        await page.wait_for_timeout(3000)
        
        # Scene 3: Category Browse
        print("📂 3. Category Browse (15s)")
        await page.goto("http://127.0.0.1:8003")
        await page.wait_for_timeout(1000)
        try:
            await page.locator(".cat-item", has_text="exams").first.click()
            await page.wait_for_timeout(3000)
            await page.mouse.wheel(0, 300)
            await page.wait_for_timeout(2000)
        except:
            await page.wait_for_timeout(5000)
        
        # Scene 4: Dark Mode
        print("🌙 4. Dark Mode (12s)")
        await page.goto("http://127.0.0.1:8003")
        await page.wait_for_timeout(1000)
        try:
            await page.click("#darkBtn")
            await page.wait_for_timeout(1500)
            await page.type("#question", "where is the gym", delay=60)
            await page.wait_for_timeout(1000)
            await page.press("#question", "Enter")
            await page.wait_for_timeout(2500)
        except:
            await page.wait_for_timeout(5000)
        
        # Scene 5: Tic-Tac-Toe
        print("🎮 5. Tic-Tac-Toe (15s)")
        await page.goto("http://127.0.0.1:8003")
        await page.wait_for_timeout(1000)
        try:
            cells = page.locator(".ttt-cell")
            await cells.nth(0).click()
            await page.wait_for_timeout(800)
            await cells.nth(4).click()
            await page.wait_for_timeout(800)
            await cells.nth(2).click()
            await page.wait_for_timeout(800)
            await cells.nth(6).click()
            await page.wait_for_timeout(2000)
            await page.locator(".ttt-reset").click()
            await page.wait_for_timeout(1500)
        except:
            await page.wait_for_timeout(7000)
        
        # Scene 6: History
        print("📋 6. History (10s)")
        await page.mouse.wheel(0, 600)
        await page.wait_for_timeout(1000)
        try:
            await page.click("text=Load full history")
            await page.wait_for_timeout(3000)
        except:
            await page.wait_for_timeout(5000)
        
        # Scene 7: Final search
        print("📊 7. Final search (10s)")
        await page.mouse.wheel(0, -1000)
        await page.wait_for_timeout(500)
        await page.fill("#question", "wifi password")
        await page.wait_for_timeout(1000)
        await page.press("#question", "Enter")
        await page.wait_for_timeout(3000)
        
        print("💾 Saving video...")
        await page.close()
        await context.close()
        await browser.close()
    
    server.terminate()
    server.wait()
    
    # Find and rename video
    video_dir = "/root/smart-faq-helper/"
    video_files = [f for f in os.listdir(video_dir) if f.endswith(".webm")]
    if video_files:
        src = os.path.join(video_dir, video_files[-1])
        dst = "/root/smart-faq-helper/demo_video.webm"
        os.rename(src, dst)
        print(f"✅ Video saved: {dst}")
        
        # Get size
        size_mb = os.path.getsize(dst) / (1024 * 1024)
        print(f"📦 Size: {size_mb:.1f} MB")
    else:
        print("❌ No video found")

if __name__ == "__main__":
    asyncio.run(main())

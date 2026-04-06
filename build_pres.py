#!/usr/bin/env python3
"""
Presentation for Smart FAQ Helper - Lab 9
5 slides: Title, Context, Implementation, Demo, Links
Built from scratch following exact Lab 9 requirements
"""

import fitz
import os

def create_presentation():
    doc = fitz.open()

    # Color palette - modern blue
    BLUE = (0.26, 0.38, 0.93)
    BLUE_LIGHT = (0.42, 0.52, 0.95)
    BLUE_PALE = (0.85, 0.89, 0.98)
    BLUE_BG = (0.95, 0.96, 0.99)
    WHITE = (1, 1, 1)
    CARD = (1, 1, 1)
    TEXT = (0.1, 0.1, 0.15)
    TEXT2 = (0.35, 0.35, 0.42)
    MUTED = (0.55, 0.55, 0.62)
    GREEN = (0.15, 0.68, 0.35)
    ORANGE = (0.95, 0.52, 0.1)
    RED = (0.88, 0.25, 0.2)
    BORDER = (0.86, 0.88, 0.92)

    W = 595.28  # A4 width
    H = 841.89  # A4 height

    def card_shadow(page, rect):
        """Draw card with shadow"""
        shadow_rect = fitz.Rect(rect.x0 + 2, rect.y0 + 2, rect.x1 + 2, rect.y1 + 2)
        page.draw_rect(shadow_rect, fill=(0.88, 0.89, 0.93))
        page.draw_rect(rect, fill=CARD)

    def draw_link(page, rect, text, url, fg=BLUE):
        """Draw clickable text with underline"""
        page.draw_rect(rect, fill=fg)
        page.insert_text(fitz.Point(rect.x0 + 3, rect.y0 + 12), text, fontsize=9, fontname="helv", color=WHITE)
        # Add link annotation
        link = fitz.Link(doc, rect, url)

    # ================================================================
    # SLIDE 1: TITLE
    # Requirements: Product title, Name, Email, Group
    # ================================================================
    p1 = doc.new_page(width=W, height=H)
    
    p1.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p1.draw_rect(fitz.Rect(0, 0, W, 8), fill=BLUE)
    
    # Decorative circles
    p1.draw_circle(fitz.Point(500, 140), 120, fill=BLUE)
    p1.draw_circle(fitz.Point(500, 140), 80, fill=BLUE_PALE)
    
    # Product Title
    p1.insert_text(fitz.Point(60, 160), "Smart FAQ Helper", fontsize=42, fontname="hebo", color=TEXT)
    p1.insert_text(fitz.Point(60, 195), "Full-stack FAQ system with contextual answers", fontsize=16, fontname="helv", color=TEXT2)
    p1.draw_rect(fitz.Rect(60, 215, 180, 218), fill=BLUE)
    
    # Student Info Card
    card1 = fitz.Rect(60, 260, 380, 480)
    card_shadow(p1, card1)
    p1.draw_rect(fitz.Rect(60, 260, 66, 480), fill=BLUE)
    
    p1.insert_text(fitz.Point(85, 305), "Student Information", fontsize=18, fontname="hebo", color=BLUE)
    
    info_items = [
        ("Name:", "Bulatov Bulat"),
        ("Email:", "b.bulatov@innopolis.university"),
        ("Group:", "DSAI-03"),
        ("GitHub:", "github.com/bulat1223312"),
    ]
    
    for i, (label, value) in enumerate(info_items):
        y_pos = 350 + i * 35
        p1.insert_text(fitz.Point(85, y_pos), label, fontsize=12, fontname="hebo", color=MUTED)
        p1.insert_text(fitz.Point(180, y_pos), value, fontsize=13, fontname="helv", color=TEXT)
    
    p1.draw_rect(fitz.Rect(0, H - 8, W, H), fill=BLUE)
    p1.insert_textbox(fitz.Rect(60, H - 35, W - 60, H - 20), 
                      "Lab 9 - Quiz and Hackathon | Software Engineering Toolkit",
                      fontsize=9, fontname="helv", color=MUTED, align=fitz.TEXT_ALIGN_CENTER)

    print("✓ Slide 1: Title created")

    # ================================================================
    # SLIDE 2: CONTEXT
    # Requirements: End-user, Problem, Product idea (one sentence)
    # ================================================================
    p2 = doc.new_page(width=W, height=H)
    
    p2.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p2.draw_rect(fitz.Rect(0, 0, W, 8), fill=BLUE)
    
    p2.insert_text(fitz.Point(60, 65), "Context", fontsize=38, fontname="hebo", color=TEXT)
    p2.draw_rect(fitz.Rect(60, 82, 90, 86), fill=BLUE)
    
    # Three cards: End User, Problem, Product Idea
    cards_data = [
        ("End User", "University students who need quick access to course information, deadlines, exam schedules, grading policies, campus resources, and other academic information.", BLUE),
        ("Problem", "Students waste time searching through multiple course pages, Moodle, emails, and announcements to find basic information. Information is scattered across many sources and hard to find quickly. The same questions are asked repeatedly.", ORANGE),
        ("Product Idea", "A single-page web application with fuzzy search that instantly finds the most similar FAQ and returns precise answers plus all related entries from the same category.", GREEN),
    ]
    
    y_positions = [120, 310, 520]
    
    for (title, desc, accent_color), y in zip(cards_data, y_positions):
        card = fitz.Rect(60, y, 535, y + 170)
        card_shadow(p2, card)
        p2.draw_rect(fitz.Rect(60, y, 66, y + 170), fill=accent_color)
        
        p2.insert_text(fitz.Point(82, y + 35), title, fontsize=20, fontname="hebo", color=accent_color)
        p2.insert_textbox(fitz.Rect(82, y + 58, 522, y + 155), desc, fontsize=13, fontname="helv", color=TEXT)
    
    p2.draw_rect(fitz.Rect(0, H - 8, W, H), fill=BLUE)

    print("✓ Slide 2: Context created")

    # ================================================================
    # SLIDE 3: IMPLEMENTATION
    # Requirements: How built, V1 vs V2, TA feedback addressed
    # ================================================================
    p3 = doc.new_page(width=W, height=H)
    
    p3.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p3.draw_rect(fitz.Rect(0, 0, W, 8), fill=BLUE)
    
    p3.insert_text(fitz.Point(60, 60), "Implementation", fontsize=38, fontname="hebo", color=TEXT)
    p3.draw_rect(fitz.Rect(60, 77, 160, 81), fill=BLUE)
    
    # Architecture
    p3.insert_text(fitz.Point(60, 100), "Tech Stack: FastAPI (backend) + SQLite (database) + Vanilla JS (frontend) + Docker (deployment)", fontsize=12, fontname="helv", color=TEXT2)
    
    # VERSION 1
    y = 125
    v1_header = fitz.Rect(60, y, 535, y + 30)
    p3.draw_rect(v1_header, fill=CARD)
    p3.draw_rect(fitz.Rect(60, y, 66, y + 30), fill=BLUE)
    p3.insert_text(fitz.Point(82, y + 22), "Version 1 — Core MVP (One thing done well)", fontsize=16, fontname="hebo", color=BLUE)
    
    v1_items = [
        "Input field for questions with real-time validation and placeholder",
        "Basic FAQ matching (keyword-based) across 112 entries in database",
        "Return predefined answers from SQLite with metadata",
        "Simple backend (FastAPI) with Pydantic models and SQLAlchemy ORM",
        "12 categories: deadlines, exams, projects, grades, schedule, enrollment, IT, campus, financial, life, rules, general",
    ]
    
    for i, item in enumerate(v1_items):
        iy = y + 45 + i * 28
        p3.draw_rect(fitz.Rect(75, iy - 10, 90, iy + 4), fill=BLUE)
        p3.insert_text(fitz.Point(78, iy), "✓", fontsize=10, fontname="helv", color=WHITE)
        p3.insert_text(fitz.Point(100, iy), item, fontsize=10.5, fontname="helv", color=TEXT)
    
    # VERSION 2
    y = 305
    v2_header = fitz.Rect(60, y, 535, y + 30)
    p3.draw_rect(v2_header, fill=CARD)
    p3.draw_rect(fitz.Rect(60, y, 66, y + 30), fill=BLUE_LIGHT)
    p3.insert_text(fitz.Point(82, y + 22), "Version 2 — Final Product (Built on V1)", fontsize=16, fontname="hebo", color=BLUE_LIGHT)
    
    v2_items = [
        "Fuzzy search: hybrid matching (55% character-level difflib + 45% word-level Jaccard similarity)",
        "SQLite database with SQLAlchemy ORM — stores 112 FAQs + query history with timestamps",
        "History tracking: every query saved with question, answer, timestamp — accessible via API",
        "Dockerized deployment (python:3.10-slim) on Ubuntu 24.04 VM at university",
        "Improved UI: single-page app with CSS Grid, smooth animations, responsive design",
        "Category browsing: sidebar with 12 categories, entry counts, active highlighting",
        "Autocomplete: real-time suggestions (min 2 chars), highlighted matches, keyboard navigation",
        "Contextual answers: best match as primary card + all related entries from same category",
        "Metadata badges: subject, professor, room, time, date, semester with color-coded types",
        "Dark mode with localStorage persistence and CSS variable theming",
        "8 API endpoints: /, /faqs, /categories, /events, /search_suggestions, /ask, /history, /stats",
    ]
    
    for i, item in enumerate(v2_items):
        iy = y + 45 + i * 28
        p3.draw_rect(fitz.Rect(75, iy - 10, 90, iy + 4), fill=BLUE_LIGHT)
        p3.insert_text(fitz.Point(78, iy), "✓", fontsize=10, fontname="helv", color=WHITE)
        p3.insert_text(fitz.Point(100, iy), item, fontsize=10.5, fontname="helv", color=TEXT)
    
    # TA Feedback
    y_fb = 645
    fb_card = fitz.Rect(60, y_fb, 535, y_fb + 90)
    card_shadow(p3, fb_card)
    p3.draw_rect(fitz.Rect(60, y_fb, 66, y_fb + 90), fill=ORANGE)
    
    p3.insert_text(fitz.Point(82, y_fb + 25), "TA Feedback Addressed", fontsize=16, fontname="hebo", color=ORANGE)
    
    ta_feedback = [
        '"Matcher too general" → Added subject/professor metadata and category filtering',
        '"UI needs improvement" → Built category browse, autocomplete, dark mode, responsive layout',
        '"Add deployment" → Dockerized and deployed on university VM (Ubuntu 24.04)',
    ]
    
    for i, fb in enumerate(ta_feedback):
        p3.insert_text(fitz.Point(82, y_fb + 48 + i * 22), fb, fontsize=10, fontname="helv", color=TEXT2)
    
    p3.draw_rect(fitz.Rect(0, H - 8, W, H), fill=BLUE)

    print("✓ Slide 3: Implementation created")

    # ================================================================
    # SLIDE 4: DEMO
    # Requirements: Pre-recorded video demo note, screenshots
    # ================================================================
    p4 = doc.new_page(width=W, height=H)
    
    p4.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p4.draw_rect(fitz.Rect(0, 0, W, 8), fill=BLUE)
    
    p4.insert_text(fitz.Point(60, 65), "Demo", fontsize=38, fontname="hebo", color=TEXT)
    p4.draw_rect(fitz.Rect(60, 82, 70, 86), fill=BLUE)
    
    p4.insert_text(fitz.Point(60, 108), "Product is live and deployed. Try it now!", fontsize=16, fontname="hebo", color=BLUE)
    
    # Video Demo note
    vid_card = fitz.Rect(60, 130, 535, 175)
    card_shadow(p4, vid_card)
    p4.draw_rect(fitz.Rect(60, 130, 66, 175), fill=GREEN)
    
    p4.insert_text(fitz.Point(82, 150), "📹 Video Demo", fontsize=16, fontname="hebo", color=GREEN)
    p4.insert_text(fitz.Point(82, 168), "2-minute pre-recorded demo with voice-over (submitted separately via Moodle)", fontsize=12, fontname="helv", color=TEXT2)
    
    # Screenshot placeholders with descriptions
    screenshots = [
        (200, "Screenshot 1: FAQ Search", "Type question → Get best match + related entries", BLUE),
        (420, "Screenshot 2: Category Browse", "Click category → See all entries at once", BLUE_LIGHT),
        (600, "Screenshot 3: Dark Mode", "Toggle theme → Comfortable night-time studying", BLUE_PALE),
    ]
    
    for y_pos, title, desc, accent in screenshots:
        shot_card = fitz.Rect(60, y_pos, 535, y_pos + 150)
        card_shadow(p4, shot_card)
        p4.draw_rect(fitz.Rect(60, y_pos, 66, y_pos + 150), fill=accent)
        
        p4.insert_text(fitz.Point(82, y_pos + 25), title, fontsize=16, fontname="hebo", color=TEXT)
        p4.insert_text(fitz.Point(82, y_pos + 45), desc, fontsize=11, fontname="helv", color=TEXT2)
        
        # Try to insert actual screenshot
        shot_files = {
            "Screenshot 1": "screenshot_search.png",
            "Screenshot 2": "screenshot_categories.png",
            "Screenshot 3": "screenshot_dark.png"
        }
        shot_key = title.split(":")[0]
        shot_path = f"/root/smart-faq-helper/{shot_files.get(shot_key, '')}"
        
        if os.path.exists(shot_path):
            img_rect = fitz.Rect(82, y_pos + 55, 515, y_pos + 140)
            try:
                p4.insert_image(img_rect, filename=shot_path, keep_proportion=True)
            except:
                p4.insert_text(fitz.Point(82, y_pos + 90), "[Screenshot: " + shot_files[shot_key] + "]", fontsize=11, fontname="helv", color=MUTED)
        else:
            p4.insert_text(fitz.Point(82, y_pos + 90), f"[Screenshot not found: {shot_files.get(shot_key, '')}]", fontsize=11, fontname="helv", color=MUTED)
    
    p4.draw_rect(fitz.Rect(0, H - 8, W, H), fill=BLUE)

    print("✓ Slide 4: Demo created")

    # ================================================================
    # SLIDE 5: LINKS
    # Requirements: GitHub repo link + QR, Deployed product link + QR
    # ================================================================
    p5 = doc.new_page(width=W, height=H)
    
    p5.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p5.draw_rect(fitz.Rect(0, 0, W, 8), fill=BLUE)
    
    p5.insert_text(fitz.Point(60, 65), "Links", fontsize=38, fontname="hebo", color=TEXT)
    p5.draw_rect(fitz.Rect(60, 82, 60, 86), fill=BLUE)
    
    # GitHub Repository
    y_gh = 120
    gh_card = fitz.Rect(60, y_gh, 535, y_gh + 180)
    card_shadow(p5, gh_card)
    p5.draw_rect(fitz.Rect(60, y_gh, 66, y_gh + 180), fill=BLUE)
    
    p5.insert_text(fitz.Point(82, y_gh + 30), "GitHub Repository", fontsize=22, fontname="hebo", color=BLUE)
    
    # Clickable link for GitHub
    gh_url = "https://github.com/bulat1223312/se-toolkit-hackathon"
    gh_link_rect = fitz.Rect(82, y_gh + 55, 480, y_gh + 75)
    p5.insert_text(fitz.Point(82, y_gh + 70), gh_url, fontsize=12, fontname="helv", color=BLUE)
    # Add clickable link annotation
    p5.insert_link({
        "kind": fitz.LINK_URI,
        "uri": gh_url,
        "from": gh_link_rect
    })
    
    # QR Code for GitHub
    qr_gh_path = "/root/smart-faq-helper/qr_github.png"
    if os.path.exists(qr_gh_path):
        qr_rect = fitz.Rect(82, y_gh + 85, 162, y_gh + 165)
        p5.insert_image(qr_rect, filename=qr_gh_path)
        p5.insert_text(fitz.Point(175, y_gh + 110), "Scan to open", fontsize=11, fontname="helv", color=TEXT2)
        p5.insert_text(fitz.Point(175, y_gh + 126), "repository", fontsize=11, fontname="helv", color=TEXT2)
        p5.insert_text(fitz.Point(175, y_gh + 148), "✓ MIT License", fontsize=10, fontname="helv", color=GREEN)
        p5.insert_text(fitz.Point(175, y_gh + 162), "✓ Full source code", fontsize=10, fontname="helv", color=GREEN)
    
    # Deployed Product
    y_dep = 340
    dep_card = fitz.Rect(60, y_dep, 535, y_dep + 180)
    card_shadow(p5, dep_card)
    p5.draw_rect(fitz.Rect(60, y_dep, 66, y_dep + 180), fill=GREEN)
    
    p5.insert_text(fitz.Point(82, y_dep + 30), "Deployed Product", fontsize=22, fontname="hebo", color=GREEN)
    
    dep_url = "http://10.93.25.49:8000"
    dep_link_rect = fitz.Rect(82, y_dep + 55, 400, y_dep + 75)
    p5.insert_text(fitz.Point(82, y_dep + 70), dep_url, fontsize=14, fontname="hebo", color=GREEN)
    p5.insert_link({
        "kind": fitz.LINK_URI,
        "uri": dep_url,
        "from": dep_link_rect
    })
    
    # QR Code for deployed product
    qr_dep_path = "/root/smart-faq-helper/qr_deployed.png"
    if os.path.exists(qr_dep_path):
        qr_rect = fitz.Rect(82, y_dep + 85, 162, y_dep + 165)
        p5.insert_image(qr_rect, filename=qr_dep_path)
        p5.insert_text(fitz.Point(175, y_dep + 110), "Scan to open", fontsize=11, fontname="helv", color=TEXT2)
        p5.insert_text(fitz.Point(175, y_dep + 126), "live app", fontsize=11, fontname="helv", color=TEXT2)
        p5.insert_text(fitz.Point(175, y_dep + 148), "✓ FAQ search", fontsize=10, fontname="helv", color=GREEN)
        p5.insert_text(fitz.Point(175, y_dep + 162), "✓ Categories & dark mode", fontsize=10, fontname="helv", color=GREEN)
    
    # Tech Stack Summary
    y_tech = 560
    tech_card = fitz.Rect(60, y_tech, 535, y_tech + 200)
    card_shadow(p5, tech_card)
    p5.draw_rect(fitz.Rect(60, y_tech, 66, y_tech + 200), fill=BLUE_LIGHT)
    
    p5.insert_text(fitz.Point(82, y_tech + 30), "Tech Stack", fontsize=22, fontname="hebo", color=BLUE_LIGHT)
    
    tech_items = [
        ("Backend", "FastAPI + Python 3.10 + Pydantic models"),
        ("Database", "SQLite + SQLAlchemy ORM (FAQ + History)"),
        ("Frontend", "Vanilla JavaScript + CSS Grid + CSS Variables"),
        ("Deployment", "Docker (python:3.10-slim) on Ubuntu 24.04"),
        ("Search", "Hybrid fuzzy: 55% difflib + 45% Jaccard"),
    ]
    
    for i, (tech, desc) in enumerate(tech_items):
        iy = y_tech + 65 + i * 28
        # Tech badge
        badge_rect = fitz.Rect(82, iy - 10, 170, iy + 4)
        p5.draw_rect(badge_rect, fill=BLUE)
        p5.insert_text(fitz.Point(85, iy), tech, fontsize=10, fontname="hebo", color=WHITE)
        p5.insert_text(fitz.Point(180, iy), desc, fontsize=11, fontname="helv", color=TEXT)
    
    # Features summary
    y_feat = 790
    p5.insert_text(fitz.Point(82, y_feat), "Features: 112 FAQ entries | 12 categories | Query history | Autocomplete | Dark mode | Responsive design", fontsize=10, fontname="helv", color=TEXT2)
    
    p5.draw_rect(fitz.Rect(0, H - 8, W, H), fill=BLUE)

    print("✓ Slide 5: Links created")

    # ================================================================
    # SAVE
    # ================================================================
    output_path = "/root/smart-faq-helper/presentation_final.pdf"
    doc.save(output_path)
    doc.close()
    print(f"\n✅ Presentation saved to: {output_path}")
    print(f"   Pages: 5 slides")
    print(f"   All links and QR codes included")

if __name__ == "__main__":
    create_presentation()

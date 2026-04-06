#!/usr/bin/env python3
"""
Presentation for Smart FAQ Helper - Lab 9
5 slides: Title, Context, Implementation, Demo, Links
WITH SCREENSHOTS - beautiful, modern design
"""

import fitz
import os

def create_presentation():
    doc = fitz.open()

    # Color palette
    BLUE = (0.26, 0.38, 0.93)
    BLUE_LIGHT = (0.42, 0.52, 0.95)
    BLUE_PALE = (0.75, 0.80, 0.97)
    BLUE_BG = (0.95, 0.96, 0.99)
    WHITE = (1, 1, 1)
    CARD = (1, 1, 1)
    TEXT = (0.1, 0.1, 0.15)
    TEXT2 = (0.35, 0.35, 0.42)
    MUTED = (0.55, 0.55, 0.62)
    GREEN = (0.15, 0.68, 0.35)
    ORANGE = (0.95, 0.52, 0.1)
    RED = (0.88, 0.25, 0.2)

    W = 595.28
    H = 841.89

    def card_shadow(page, rect):
        shadow = fitz.Rect(rect.x0 + 2, rect.y0 + 2, rect.x1 + 2, rect.y1 + 2)
        page.draw_rect(shadow, fill=(0.88, 0.89, 0.93))
        page.draw_rect(rect, fill=CARD)

    # ================================================================
    # SLIDE 1: TITLE
    # ================================================================
    p1 = doc.new_page(width=W, height=H)
    p1.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p1.draw_rect(fitz.Rect(0, 0, W, 8), fill=BLUE)

    # Decorative circles
    p1.draw_circle(fitz.Point(500, 140), 120, fill=BLUE)
    p1.draw_circle(fitz.Point(500, 140), 80, fill=BLUE_PALE)

    p1.insert_text(fitz.Point(60, 160), "Smart FAQ Helper", fontsize=42, fontname="hebo", color=TEXT)
    p1.insert_text(fitz.Point(60, 195), "Full-stack FAQ system with contextual answers", fontsize=16, fontname="helv", color=TEXT2)
    p1.draw_rect(fitz.Rect(60, 215, 180, 218), fill=BLUE)

    # Student Info Card
    info_card = fitz.Rect(60, 260, 380, 480)
    card_shadow(p1, info_card)
    p1.draw_rect(fitz.Rect(60, 260, 66, 480), fill=BLUE)

    p1.insert_text(fitz.Point(85, 305), "Student Information", fontsize=18, fontname="hebo", color=BLUE)

    info = [
        ("Name:", "Bulatov Bulat"),
        ("Email:", "b.bulatov@innopolis.university"),
        ("Group:", "DSAI-03"),
        ("GitHub:", "github.com/bulat1223312"),
    ]

    for i, (label, value) in enumerate(info):
        y = 350 + i * 35
        p1.insert_text(fitz.Point(85, y), label, fontsize=12, fontname="hebo", color=MUTED)
        p1.insert_text(fitz.Point(180, y), value, fontsize=13, fontname="helv", color=TEXT)

    # Bottom
    p1.draw_rect(fitz.Rect(0, H - 8, W, H), fill=BLUE)
    p1.insert_textbox(fitz.Rect(60, H - 35, W - 60, H - 20),
                      "Lab 9 - Quiz and Hackathon", fontsize=9, fontname="helv", color=MUTED, align=fitz.TEXT_ALIGN_CENTER)

    print("✓ Slide 1: Title")

    # ================================================================
    # SLIDE 2: CONTEXT
    # ================================================================
    p2 = doc.new_page(width=W, height=H)
    p2.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p2.draw_rect(fitz.Rect(0, 0, W, 8), fill=BLUE)

    p2.insert_text(fitz.Point(60, 65), "Context", fontsize=38, fontname="hebo", color=TEXT)
    p2.draw_rect(fitz.Rect(60, 82, 90, 86), fill=BLUE)

    # Three cards
    cards_data = [
        ("End User", "University students who need quick access to course information, deadlines, exam schedules, grading policies, campus resources, and other academic information.", BLUE),
        ("Problem", "Students waste time searching through multiple course pages, Moodle, emails, and announcements to find basic information. Information is scattered across many sources and hard to find quickly.", ORANGE),
        ("Product Idea", "The system finds the most similar question from a database using fuzzy matching and returns the best answer instantly, plus all related entries from the same category.", GREEN),
    ]

    y_positions = [120, 310, 520]

    for (title, desc, accent_color), y in zip(cards_data, y_positions):
        h = 160 if title == "Problem" else 150
        card = fitz.Rect(60, y, 535, y + h)
        card_shadow(p2, card)
        p2.draw_rect(fitz.Rect(60, y, 66, y + h), fill=accent_color)

        p2.insert_text(fitz.Point(82, y + 35), title, fontsize=20, fontname="hebo", color=accent_color)
        p2.insert_textbox(fitz.Rect(82, y + 58, 522, y + h - 15), desc, fontsize=13, fontname="helv", color=TEXT)

    p2.draw_rect(fitz.Rect(0, H - 8, W, H), fill=BLUE)

    print("✓ Slide 2: Context")

    # ================================================================
    # SLIDE 3: IMPLEMENTATION
    # ================================================================
    p3 = doc.new_page(width=W, height=H)
    p3.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p3.draw_rect(fitz.Rect(0, 0, W, 8), fill=BLUE)

    p3.insert_text(fitz.Point(60, 60), "Implementation", fontsize=38, fontname="hebo", color=TEXT)
    p3.draw_rect(fitz.Rect(60, 77, 160, 81), fill=BLUE)

    # Tech stack line
    p3.insert_text(fitz.Point(60, 100), "Tech Stack: FastAPI (backend) + SQLite (database) + Vanilla JS (frontend) + Docker (deployment)", fontsize=12, fontname="helv", color=TEXT2)

    # VERSION 1
    y = 125
    v1h = fitz.Rect(60, y, 535, y + 30)
    p3.draw_rect(v1h, fill=CARD)
    p3.draw_rect(fitz.Rect(60, y, 66, y + 30), fill=BLUE)
    p3.insert_text(fitz.Point(82, y + 22), "Version 1 — Core MVP", fontsize=16, fontname="hebo", color=BLUE)

    v1 = [
        "Input field for questions with real-time validation and placeholder",
        "Basic FAQ matching (keyword-based) across 112 entries in database",
        "Return predefined answers from SQLite with metadata",
        "Simple backend (FastAPI) with Pydantic models and SQLAlchemy ORM",
        "12 categories: deadlines, exams, projects, grades, schedule, enrollment, IT, campus, financial, life, rules, general",
    ]

    for i, item in enumerate(v1):
        iy = y + 45 + i * 28
        p3.draw_rect(fitz.Rect(75, iy - 10, 90, iy + 4), fill=BLUE)
        p3.insert_text(fitz.Point(78, iy), "✓", fontsize=10, fontname="helv", color=WHITE)
        p3.insert_text(fitz.Point(100, iy), item, fontsize=10.5, fontname="helv", color=TEXT)

    # VERSION 2
    y = 305
    v2h = fitz.Rect(60, y, 535, y + 30)
    p3.draw_rect(v2h, fill=CARD)
    p3.draw_rect(fitz.Rect(60, y, 66, y + 30), fill=BLUE_LIGHT)
    p3.insert_text(fitz.Point(82, y + 22), "Version 2 — Final Product", fontsize=16, fontname="hebo", color=BLUE_LIGHT)

    v2 = [
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

    for i, item in enumerate(v2):
        iy = y + 45 + i * 28
        p3.draw_rect(fitz.Rect(75, iy - 10, 90, iy + 4), fill=BLUE_LIGHT)
        p3.insert_text(fitz.Point(78, iy), "✓", fontsize=10, fontname="helv", color=WHITE)
        p3.insert_text(fitz.Point(100, iy), item, fontsize=10.5, fontname="helv", color=TEXT)

    # TA Feedback
    y_fb = 640
    fb_card = fitz.Rect(60, y_fb, 535, y_fb + 80)
    card_shadow(p3, fb_card)
    p3.draw_rect(fitz.Rect(60, y_fb, 66, y_fb + 80), fill=ORANGE)

    p3.insert_text(fitz.Point(82, y_fb + 24), "TA Feedback Addressed", fontsize=16, fontname="hebo", color=ORANGE)

    ta_feedback = [
        '"Matcher is too general, allow filters?"',
        "→ Added category filtering + subject/professor metadata badges",
    ]

    for i, fb in enumerate(ta_feedback):
        p3.insert_text(fitz.Point(82, y_fb + 48 + i * 18), fb, fontsize=10, fontname="helv", color=TEXT2)

    p3.draw_rect(fitz.Rect(0, H - 8, W, H), fill=BLUE)

    print("✓ Slide 3: Implementation")

    # ================================================================
    # SLIDE 4: DEMO — WITH SCREENSHOTS
    # ================================================================
    p4 = doc.new_page(width=W, height=H)
    p4.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p4.draw_rect(fitz.Rect(0, 0, W, 8), fill=BLUE)

    p4.insert_text(fitz.Point(60, 75), "Demo", fontsize=38, fontname="hebo", color=TEXT)
    p4.draw_rect(fitz.Rect(60, 92, 70, 96), fill=BLUE)

    # Video Demo note
    vid_card = fitz.Rect(60, 118, 535, 155)
    card_shadow(p4, vid_card)
    p4.draw_rect(fitz.Rect(60, 118, 66, 155), fill=GREEN)
    p4.insert_text(fitz.Point(82, 136), "📹 Video Demo", fontsize=16, fontname="hebo", color=GREEN)
    p4.insert_text(fitz.Point(210, 136), "Pre-recorded demo video available in the GitHub repository", fontsize=12, fontname="helv", color=TEXT2)
    p4.insert_text(fitz.Point(82, 152), "File: demo_video.webm — github.com/bulat1223312/se-toolkit-hackathon", fontsize=10, fontname="helv", color=BLUE)

    # Screenshot 1 - full width
    y = 180
    s1_header = fitz.Rect(60, y, 535, y + 28)
    p4.draw_rect(s1_header, fill=CARD)
    p4.draw_rect(fitz.Rect(60, y, 66, y + 28), fill=BLUE)
    p4.insert_text(fitz.Point(82, y + 20), "Screenshot 1: FAQ Search", fontsize=14, fontname="hebo", color=TEXT)

    shot1 = "/root/smart-faq-helper/screenshot_search.png"
    if os.path.exists(shot1):
        p4.insert_image(fitz.Rect(60, y + 35, 535, y + 250), filename=shot1, keep_proportion=True)

    # Screenshot 2 and 3 side by side
    y2 = y + 400
    # Left
    s2_header = fitz.Rect(60, y2, 295, y2 + 28)
    p4.draw_rect(s2_header, fill=CARD)
    p4.draw_rect(fitz.Rect(60, y2, 66, y2 + 28), fill=BLUE_LIGHT)
    p4.insert_text(fitz.Point(82, y2 + 20), "Screenshot 2: Categories", fontsize=13, fontname="hebo", color=TEXT)

    shot2 = "/root/smart-faq-helper/screenshot_categories.png"
    if os.path.exists(shot2):
        p4.insert_image(fitz.Rect(60, y2 + 33, 295, y2 + 200), filename=shot2, keep_proportion=True)

    # Right
    s3_header = fitz.Rect(315, y2, 535, y2 + 28)
    p4.draw_rect(s3_header, fill=CARD)
    p4.draw_rect(fitz.Rect(315, y2, 321, y2 + 28), fill=BLUE_PALE)
    p4.insert_text(fitz.Point(333, y2 + 20), "Screenshot 3: Dark Mode", fontsize=13, fontname="hebo", color=TEXT)

    shot3 = "/root/smart-faq-helper/screenshot_dark.png"
    if os.path.exists(shot3):
        p4.insert_image(fitz.Rect(315, y2 + 33, 535, y2 + 200), filename=shot3, keep_proportion=True)

    p4.draw_rect(fitz.Rect(0, H - 8, W, H), fill=BLUE)

    print("✓ Slide 4: Demo")

    # ================================================================
    # SLIDE 5: LINKS
    # ================================================================
    p5 = doc.new_page(width=W, height=H)
    p5.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p5.draw_rect(fitz.Rect(0, 0, W, 8), fill=BLUE)

    p5.insert_text(fitz.Point(60, 75), "Links", fontsize=38, fontname="hebo", color=TEXT)
    p5.draw_rect(fitz.Rect(60, 92, 60, 96), fill=BLUE)

    # GitHub Repository
    y_gh = 135
    gh_card = fitz.Rect(60, y_gh, 535, y_gh + 140)
    card_shadow(p5, gh_card)
    p5.draw_rect(fitz.Rect(60, y_gh, 66, y_gh + 140), fill=BLUE)

    p5.insert_text(fitz.Point(82, y_gh + 30), "GitHub Repository", fontsize=20, fontname="hebo", color=BLUE)
    p5.insert_text(fitz.Point(82, y_gh + 52), "github.com/bulat1223312/se-toolkit-hackathon", fontsize=12, fontname="helv", color=TEXT2)

    # Clickable link
    gh_url = "https://github.com/bulat1223312/se-toolkit-hackathon"
    gh_link_rect = fitz.Rect(82, y_gh + 55, 480, y_gh + 72)
    p5.insert_link({"kind": fitz.LINK_URI, "uri": gh_url, "from": gh_link_rect})

    # QR code
    qr_gh = "/root/smart-faq-helper/qr_github.png"
    if os.path.exists(qr_gh):
        p5.insert_image(fitz.Rect(82, y_gh + 75, 162, y_gh + 130), filename=qr_gh)
        p5.insert_text(fitz.Point(175, y_gh + 90), "Scan to open repository", fontsize=11, fontname="helv", color=TEXT2)
        p5.insert_text(fitz.Point(175, y_gh + 106), "✓ MIT License  ✓ Full source code", fontsize=10, fontname="helv", color=GREEN)

    # Deployed Product
    y_dep = 310
    dep_card = fitz.Rect(60, y_dep, 535, y_dep + 140)
    card_shadow(p5, dep_card)
    p5.draw_rect(fitz.Rect(60, y_dep, 66, y_dep + 140), fill=GREEN)

    p5.insert_text(fitz.Point(82, y_dep + 30), "Deployed Product", fontsize=20, fontname="hebo", color=GREEN)
    p5.insert_text(fitz.Point(82, y_dep + 52), "http://10.93.25.49:8000", fontsize=14, fontname="hebo", color=GREEN)

    dep_url = "http://10.93.25.49:8000"
    dep_link_rect = fitz.Rect(82, y_dep + 55, 400, y_dep + 72)
    p5.insert_link({"kind": fitz.LINK_URI, "uri": dep_url, "from": dep_link_rect})

    qr_dep = "/root/smart-faq-helper/qr_deployed.png"
    if os.path.exists(qr_dep):
        p5.insert_image(fitz.Rect(82, y_dep + 75, 162, y_dep + 130), filename=qr_dep)
        p5.insert_text(fitz.Point(175, y_dep + 90), "Scan to open live app", fontsize=11, fontname="helv", color=TEXT2)
        p5.insert_text(fitz.Point(175, y_dep + 106), "✓ FAQ search  ✓ Categories  ✓ Dark mode", fontsize=10, fontname="helv", color=GREEN)

    # Tech Stack
    y_tech = 490
    tech_card = fitz.Rect(60, y_tech, 535, y_tech + 170)
    card_shadow(p5, tech_card)
    p5.draw_rect(fitz.Rect(60, y_tech, 66, y_tech + 170), fill=BLUE_LIGHT)

    p5.insert_text(fitz.Point(82, y_tech + 30), "Tech Stack", fontsize=20, fontname="hebo", color=BLUE_LIGHT)

    tech = [
        ("Backend", "FastAPI + Python 3.10"),
        ("Database", "SQLite + SQLAlchemy ORM"),
        ("Frontend", "Vanilla JS + CSS Grid"),
        ("Deployment", "Docker on Ubuntu 24.04"),
    ]
    for i, (name, val) in enumerate(tech):
        iy = y_tech + 65 + i * 28
        badge_rect = fitz.Rect(82, iy - 10, 170, iy + 6)
        p5.draw_rect(badge_rect, fill=BLUE)
        p5.insert_text(fitz.Point(85, iy), name, fontsize=10, fontname="hebo", color=WHITE)
        p5.insert_text(fitz.Point(180, iy), val, fontsize=12, fontname="helv", color=TEXT)

    p5.draw_rect(fitz.Rect(0, H - 8, W, H), fill=BLUE)

    print("✓ Slide 5: Links")

    # ================================================================
    # SAVE
    # ================================================================
    output_path = "/root/smart-faq-helper/presentation_final.pdf"
    doc.save(output_path)
    doc.close()
    print(f"\n✅ Done: {output_path}")
    print(f"   5 slides | Screenshots included | Clickable links | QR codes")

if __name__ == "__main__":
    create_presentation()

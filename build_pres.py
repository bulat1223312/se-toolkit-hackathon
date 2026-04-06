#!/usr/bin/env python3
"""
Presentation for Smart FAQ Helper - Lab 9
5 slides: Title, Context, Implementation, Demo, Links
Content-focused: maximum essence, minimum decoration
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
    p1.draw_rect(fitz.Rect(0, 0, W, 6), fill=BLUE)

    p1.insert_text(fitz.Point(60, 120), "Smart FAQ Helper", fontsize=48, fontname="hebo", color=TEXT)
    p1.insert_text(fitz.Point(60, 160), "Full-stack FAQ system with contextual answers", fontsize=18, fontname="helv", color=TEXT2)
    p1.draw_rect(fitz.Rect(60, 180, 200, 183), fill=BLUE)

    # Info card
    info_card = fitz.Rect(60, 230, 400, 460)
    card_shadow(p1, info_card)
    p1.draw_rect(fitz.Rect(60, 230, 66, 460), fill=BLUE)

    p1.insert_text(fitz.Point(85, 275), "Student", fontsize=20, fontname="hebo", color=BLUE)

    info = [
        ("Name:", "Bulatov Bulat"),
        ("Email:", "b.bulatov@innopolis.university"),
        ("Group:", "DSAI-03"),
        ("GitHub:", "github.com/bulat1223312"),
    ]

    for i, (label, value) in enumerate(info):
        y = 320 + i * 35
        p1.insert_text(fitz.Point(85, y), label, fontsize=13, fontname="hebo", color=MUTED)
        p1.insert_text(fitz.Point(190, y), value, fontsize=14, fontname="helv", color=TEXT)

    # Tech stack preview
    tech_card = fitz.Rect(60, 510, 400, 660)
    card_shadow(p1, tech_card)
    p1.draw_rect(fitz.Rect(60, 510, 66, 660), fill=BLUE_LIGHT)

    p1.insert_text(fitz.Point(85, 545), "Tech Stack", fontsize=18, fontname="hebo", color=BLUE_LIGHT)

    tech = [
        "Backend: FastAPI + Python 3.10",
        "Database: SQLite + SQLAlchemy ORM",
        "Frontend: Vanilla JS + CSS Grid",
        "Search: Hybrid fuzzy (difflib + Jaccard)",
        "Deployment: Docker on Ubuntu 24.04",
    ]

    for i, t in enumerate(tech):
        p1.insert_text(fitz.Point(85, 580 + i * 24), t, fontsize=12, fontname="helv", color=TEXT)

    p1.draw_rect(fitz.Rect(0, H - 6, W, H), fill=BLUE)
    p1.insert_textbox(fitz.Rect(60, H - 32, W - 60, H - 18),
                      "Lab 9 - Quiz and Hackathon", fontsize=10, fontname="helv", color=MUTED, align=fitz.TEXT_ALIGN_CENTER)

    print("✓ Slide 1: Title")

    # ================================================================
    # SLIDE 2: CONTEXT
    # ================================================================
    p2 = doc.new_page(width=W, height=H)
    p2.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p2.draw_rect(fitz.Rect(0, 0, W, 6), fill=BLUE)

    p2.insert_text(fitz.Point(60, 60), "Context", fontsize=42, fontname="hebo", color=TEXT)
    p2.draw_rect(fitz.Rect(60, 78, 100, 82), fill=BLUE)

    # End User
    y = 115
    eu_card = fitz.Rect(60, y, 535, y + 140)
    card_shadow(p2, eu_card)
    p2.draw_rect(fitz.Rect(60, y, 66, y + 140), fill=BLUE)
    p2.insert_text(fitz.Point(82, y + 30), "End User", fontsize=22, fontname="hebo", color=BLUE)
    p2.insert_textbox(fitz.Rect(82, y + 58, 522, y + 128),
                      "University students who need quick access to course information, deadlines, exam schedules, grading policies, campus resources, and other academic information.",
                      fontsize=14, fontname="helv", color=TEXT)

    # Problem
    y = 285
    prob_card = fitz.Rect(60, y, 535, y + 195)
    card_shadow(p2, prob_card)
    p2.draw_rect(fitz.Rect(60, y, 66, y + 195), fill=ORANGE)
    p2.insert_text(fitz.Point(82, y + 30), "Problem", fontsize=22, fontname="hebo", color=ORANGE)

    problems = [
        "Students waste time searching through multiple course pages, Moodle, emails, and announcements",
        "Same questions asked repeatedly (deadlines, exam rooms, office hours, submission rules)",
        "Information scattered across many sources, hard to find quickly",
        "No single place to get instant, precise answers with related context",
    ]

    for i, prob in enumerate(problems):
        p2.insert_text(fitz.Point(82, y + 62 + i * 32), f"• {prob}", fontsize=13, fontname="helv", color=TEXT)

    # Product Idea
    y = 515
    idea_card = fitz.Rect(60, y, 535, y + 140)
    card_shadow(p2, idea_card)
    p2.draw_rect(fitz.Rect(60, y, 66, y + 140), fill=GREEN)
    p2.insert_text(fitz.Point(82, y + 30), "Product Idea", fontsize=22, fontname="hebo", color=GREEN)
    p2.insert_textbox(fitz.Rect(82, y + 58, 522, y + 128),
                      "A single-page web application with fuzzy search that instantly finds the most similar FAQ and returns the best answer plus all related entries from the same category — 112 entries across 12 categories.",
                      fontsize=14, fontname="helv", color=TEXT)

    # Key metrics
    y = 685
    metrics = [
        ("112", "FAQ entries"),
        ("12", "Categories"),
        ("<1s", "Response time"),
        ("8", "API endpoints"),
    ]

    for i, (num, label) in enumerate(metrics):
        x = 60 + i * 125
        mcard = fitz.Rect(x, y, x + 115, y + 60)
        card_shadow(p2, mcard)
        p2.insert_textbox(fitz.Rect(x + 5, y + 8, x + 110, y + 35), num, fontsize=26, fontname="hebo", color=BLUE, align=fitz.TEXT_ALIGN_CENTER)
        p2.insert_textbox(fitz.Rect(x + 5, y + 38, x + 110, y + 55), label, fontsize=9, fontname="helv", color=MUTED, align=fitz.TEXT_ALIGN_CENTER)

    p2.draw_rect(fitz.Rect(0, H - 6, W, H), fill=BLUE)

    print("✓ Slide 2: Context")

    # ================================================================
    # SLIDE 3: IMPLEMENTATION
    # ================================================================
    p3 = doc.new_page(width=W, height=H)
    p3.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p3.draw_rect(fitz.Rect(0, 0, W, 6), fill=BLUE)

    p3.insert_text(fitz.Point(60, 50), "Implementation", fontsize=42, fontname="hebo", color=TEXT)
    p3.draw_rect(fitz.Rect(60, 68, 170, 72), fill=BLUE)

    # VERSION 1
    y = 95
    v1h = fitz.Rect(60, y, 535, y + 28)
    p3.draw_rect(v1h, fill=CARD)
    p3.draw_rect(fitz.Rect(60, y, 66, y + 28), fill=BLUE)
    p3.insert_text(fitz.Point(82, y + 20), "Version 1 — Core MVP", fontsize=17, fontname="hebo", color=BLUE)

    v1 = [
        "Input field for questions — text input with placeholder and real-time validation",
        "Basic FAQ matching — keyword-based search across 112 entries in database",
        "Return predefined answers — seeded SQLite database with Q&A pairs",
        "Simple backend (FastAPI) — Pydantic models, SQLAlchemy ORM, REST API",
        "12 categories with metadata — subject, professor, room, time, date, semester, type",
        "Web UI — responsive single-page app with CSS Grid and smooth animations",
    ]

    for i, item in enumerate(v1):
        iy = y + 42 + i * 28
        p3.draw_rect(fitz.Rect(75, iy - 9, 90, iy + 5), fill=BLUE)
        p3.insert_text(fitz.Point(78, iy), "✓", fontsize=10, fontname="helv", color=WHITE)
        p3.insert_text(fitz.Point(100, iy), item, fontsize=11, fontname="helv", color=TEXT)

    # VERSION 2
    y = 295
    v2h = fitz.Rect(60, y, 535, y + 28)
    p3.draw_rect(v2h, fill=CARD)
    p3.draw_rect(fitz.Rect(60, y, 66, y + 28), fill=BLUE_LIGHT)
    p3.insert_text(fitz.Point(82, y + 20), "Version 2 — Final Product", fontsize=17, fontname="hebo", color=BLUE_LIGHT)

    v2 = [
        "Fuzzy search engine — 55% character-level (difflib) + 45% word-level (Jaccard similarity)",
        "History tracking — every query saved with timestamp, accessible via /history API",
        "Autocomplete — real-time suggestions (min 2 chars), highlighted matches, keyboard navigation",
        "Category browsing — sidebar with 12 categories, entry counts, click to see all entries",
        "Contextual answers — best match as primary card + all related entries from same category",
        "Metadata badges — subject, professor, room, time, date, semester with color-coded types",
        "Dark mode — toggle with localStorage persistence, full CSS variable theming",
        "Dockerized deployment — python:3.10-slim image on Ubuntu 24.04 university VM",
        "8 API endpoints — /, /faqs, /categories, /events, /search_suggestions, /ask, /history, /stats",
        "Responsive design — mobile-friendly layout, collapsible sidebar, hamburger menu",
    ]

    for i, item in enumerate(v2):
        iy = y + 42 + i * 28
        p3.draw_rect(fitz.Rect(75, iy - 9, 90, iy + 5), fill=BLUE_LIGHT)
        p3.insert_text(fitz.Point(78, iy), "✓", fontsize=10, fontname="helv", color=WHITE)
        p3.insert_text(fitz.Point(100, iy), item, fontsize=11, fontname="helv", color=TEXT)

    # Architecture diagram
    y = 600
    arch_card = fitz.Rect(60, y, 535, y + 95)
    card_shadow(p3, arch_card)
    p3.draw_rect(fitz.Rect(60, y, 66, y + 95), fill=GREEN)
    p3.insert_text(fitz.Point(82, y + 22), "Architecture", fontsize=18, fontname="hebo", color=GREEN)

    arch = [
        "Client (Browser) → REST API → FastAPI Server → SQLite Database",
        "User types question → Autocomplete suggests → Fuzzy match finds best answer → Returns result + related entries",
        "Each query → Saved to History table → Available via /history and /stats endpoints",
    ]

    for i, a in enumerate(arch):
        p3.insert_text(fitz.Point(82, y + 48 + i * 24), a, fontsize=11, fontname="helv", color=TEXT2)

    # TA Feedback
    y = 715
    fb_card = fitz.Rect(60, y, 535, y + 80)
    card_shadow(p3, fb_card)
    p3.draw_rect(fitz.Rect(60, y, 66, y + 80), fill=ORANGE)
    p3.insert_text(fitz.Point(82, y + 20), "TA Feedback Addressed", fontsize=16, fontname="hebo", color=ORANGE)

    ta = [
        '"Matcher too general" → Added subject/professor metadata, category filtering, confidence scores',
        '"UI needs work" → Category browse, autocomplete, dark mode, responsive design',
        '"Deploy it" → Dockerized + deployed on university VM (Ubuntu 24.04)',
    ]

    for i, t in enumerate(ta):
        p3.insert_text(fitz.Point(82, y + 44 + i * 22), t, fontsize=10, fontname="helv", color=TEXT2)

    p3.draw_rect(fitz.Rect(0, H - 6, W, H), fill=BLUE)

    print("✓ Slide 3: Implementation")

    # ================================================================
    # SLIDE 4: DEMO
    # ================================================================
    p4 = doc.new_page(width=W, height=H)
    p4.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p4.draw_rect(fitz.Rect(0, 0, W, 6), fill=BLUE)

    p4.insert_text(fitz.Point(60, 60), "Demo", fontsize=42, fontname="hebo", color=TEXT)
    p4.draw_rect(fitz.Rect(60, 78, 70, 82), fill=BLUE)

    # Video Demo note
    vid_card = fitz.Rect(60, 110, 535, 160)
    card_shadow(p4, vid_card)
    p4.draw_rect(fitz.Rect(60, 110, 66, 160), fill=GREEN)
    p4.insert_text(fitz.Point(82, 130), "📹 Video Demo", fontsize=18, fontname="hebo", color=GREEN)
    p4.insert_text(fitz.Point(82, 150), "2-minute pre-recorded demo with voice-over — submitted separately via Moodle", fontsize=12, fontname="helv", color=TEXT2)

    # Feature highlights instead of screenshots
    features = [
        ("FAQ Search", "Type 'exam deadline' → Get best match (confidence 85%) + 4 related entries from exams category", BLUE),
        ("Category Browse", "Click 'deadlines' in sidebar → See all 9 deadline entries at once with metadata badges", BLUE_LIGHT),
        ("Autocomplete", "Type 'math' → Get real-time suggestions with category badges, navigate with arrow keys", BLUE),
        ("Contextual Results", "Search 'gym' → Best match as primary card + 2 more campus entries with room, time, type badges", GREEN),
        ("Dark Mode", "Toggle moon icon → Full theme swap via CSS variables, preference saved in localStorage", BLUE_PALE),
    ]

    for i, (title, desc, accent) in enumerate(features):
        y = 185 + i * 105
        fcard = fitz.Rect(60, y, 535, y + 95)
        card_shadow(p4, fcard)
        p4.draw_rect(fitz.Rect(60, y, 66, y + 95), fill=accent)

        p4.insert_text(fitz.Point(82, y + 25), f"{i+1}. {title}", fontsize=16, fontname="hebo", color=accent)
        p4.insert_textbox(fitz.Rect(82, y + 48, 522, y + 85), desc, fontsize=12, fontname="helv", color=TEXT)

    p4.draw_rect(fitz.Rect(0, H - 6, W, H), fill=BLUE)

    print("✓ Slide 4: Demo")

    # ================================================================
    # SLIDE 5: LINKS
    # ================================================================
    p5 = doc.new_page(width=W, height=H)
    p5.draw_rect(fitz.Rect(0, 0, W, H), fill=BLUE_BG)
    p5.draw_rect(fitz.Rect(0, 0, W, 6), fill=BLUE)

    p5.insert_text(fitz.Point(60, 60), "Links", fontsize=42, fontname="hebo", color=TEXT)
    p5.draw_rect(fitz.Rect(60, 78, 60, 82), fill=BLUE)

    # GitHub Repository
    y_gh = 115
    gh_card = fitz.Rect(60, y_gh, 535, y_gh + 170)
    card_shadow(p5, gh_card)
    p5.draw_rect(fitz.Rect(60, y_gh, 66, y_gh + 170), fill=BLUE)
    p5.insert_text(fitz.Point(82, y_gh + 30), "GitHub Repository", fontsize=24, fontname="hebo", color=BLUE)

    gh_url = "https://github.com/bulat1223312/se-toolkit-hackathon"
    gh_link_rect = fitz.Rect(82, y_gh + 55, 490, y_gh + 75)
    p5.insert_text(fitz.Point(82, y_gh + 70), gh_url, fontsize=12, fontname="helv", color=BLUE)
    p5.insert_link({"kind": fitz.LINK_URI, "uri": gh_url, "from": gh_link_rect})

    # QR code
    qr_gh = "/root/smart-faq-helper/qr_github.png"
    if os.path.exists(qr_gh):
        p5.insert_image(fitz.Rect(82, y_gh + 85, 162, y_gh + 155), filename=qr_gh)
        p5.insert_text(fitz.Point(175, y_gh + 105), "Scan to open repository", fontsize=11, fontname="helv", color=TEXT2)
        p5.insert_text(fitz.Point(175, y_gh + 123), "✓ MIT License  ✓ Full source code", fontsize=10, fontname="helv", color=GREEN)
        p5.insert_text(fitz.Point(175, y_gh + 140), "✓ Docker support  ✓ README.md", fontsize=10, fontname="helv", color=GREEN)

    # Deployed Product
    y_dep = 320
    dep_card = fitz.Rect(60, y_dep, 535, y_dep + 170)
    card_shadow(p5, dep_card)
    p5.draw_rect(fitz.Rect(60, y_dep, 66, y_dep + 170), fill=GREEN)
    p5.insert_text(fitz.Point(82, y_dep + 30), "Deployed Product", fontsize=24, fontname="hebo", color=GREEN)

    dep_url = "http://10.93.25.49:8000"
    dep_link_rect = fitz.Rect(82, y_dep + 55, 400, y_dep + 75)
    p5.insert_text(fitz.Point(82, y_dep + 70), dep_url, fontsize=14, fontname="hebo", color=GREEN)
    p5.insert_link({"kind": fitz.LINK_URI, "uri": dep_url, "from": dep_link_rect})

    qr_dep = "/root/smart-faq-helper/qr_deployed.png"
    if os.path.exists(qr_dep):
        p5.insert_image(fitz.Rect(82, y_dep + 85, 162, y_dep + 155), filename=qr_dep)
        p5.insert_text(fitz.Point(175, y_dep + 105), "Scan to open live app", fontsize=11, fontname="helv", color=TEXT2)
        p5.insert_text(fitz.Point(175, y_dep + 123), "✓ FAQ search  ✓ Categories", fontsize=10, fontname="helv", color=GREEN)
        p5.insert_text(fitz.Point(175, y_dep + 140), "✓ Dark mode  ✓ History  ✓ API", fontsize=10, fontname="helv", color=GREEN)

    # Tech Stack Summary
    y_tech = 525
    tech_card = fitz.Rect(60, y_tech, 535, y_tech + 190)
    card_shadow(p5, tech_card)
    p5.draw_rect(fitz.Rect(60, y_tech, 66, y_tech + 190), fill=BLUE_LIGHT)
    p5.insert_text(fitz.Point(82, y_tech + 28), "Tech Stack", fontsize=22, fontname="hebo", color=BLUE_LIGHT)

    tech_items = [
        ("Backend", "FastAPI + Python 3.10 + Pydantic models"),
        ("Database", "SQLite + SQLAlchemy ORM (FAQ + History tables)"),
        ("Frontend", "Vanilla JavaScript + CSS Grid + CSS Variables"),
        ("Deployment", "Docker (python:3.10-slim) on Ubuntu 24.04 VM"),
        ("Search", "Hybrid fuzzy: 55% difflib + 45% Jaccard similarity"),
    ]

    for i, (tech, desc) in enumerate(tech_items):
        iy = y_tech + 62 + i * 26
        badge = fitz.Rect(82, iy - 9, 170, iy + 5)
        p5.draw_rect(badge, fill=BLUE)
        p5.insert_text(fitz.Point(85, iy), tech, fontsize=10, fontname="hebo", color=WHITE)
        p5.insert_text(fitz.Point(180, iy), desc, fontsize=11, fontname="helv", color=TEXT)

    # Features count
    y_feat = 745
    p5.insert_text(fitz.Point(82, y_feat), "Features: 112 FAQ entries | 12 categories | Query history | Autocomplete | Dark mode | Responsive | 8 API endpoints", fontsize=10, fontname="helv", color=TEXT2)

    p5.draw_rect(fitz.Rect(0, H - 6, W, H), fill=BLUE)

    print("✓ Slide 5: Links")

    # ================================================================
    # SAVE
    # ================================================================
    output_path = "/root/smart-faq-helper/presentation_final.pdf"
    doc.save(output_path)
    doc.close()
    print(f"\n✅ Done: {output_path}")
    print(f"   5 slides | Clickable links | QR codes")

if __name__ == "__main__":
    create_presentation()

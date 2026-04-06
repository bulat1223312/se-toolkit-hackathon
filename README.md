# Smart FAQ Helper

Full-stack FAQ system with contextual answers — students instantly get precise answers plus all related entries from the same category.

## Author Information

- **Name**: Bulatov Bulat
- **Email**: b.bulatov@innopolis.university
- **Group**: DSAI-03
- **GitHub**: github.com/bulat1223312

## Demo

### FAQ Search
Type a question, get the best match + all related entries from the same category.

![FAQ Search](screenshot_search.png)

### Category Browse
Click any category in the sidebar to see all entries at once.

![Category Browse](screenshot_categories.png)

### Dark Mode
Toggle dark mode for comfortable night-time studying.

![Dark Mode](screenshot_dark.png)

## Product Context

### End Users

University students who need quick access to course information, deadlines, exam schedules, grading policies, campus resources, and other academic information.

### Problem

Students waste time searching through multiple course pages, Moodle, emails, and announcements to find basic information like deadlines, exam rooms, office hours, and submission rules. Information is scattered across many sources and hard to find quickly.

### Our Solution

A single-page web application with 112 FAQ entries across 12 categories. Hybrid fuzzy matching (55% character-level + 45% word-level Jaccard) finds the best match and returns all related entries from that category. Autocomplete, category browsing, dark mode, and query history make it fast and pleasant to use.

## Features

### Version 1 - Core MVP

| Feature | Status | Details |
|---------|--------|---------|
| Input field for questions | ✅ | Text input with placeholder and real-time validation |
| Basic FAQ matching (keyword-based) | ✅ | Keyword search across 112 FAQ entries |
| Return predefined answers | ✅ | Predefined answers seeded in SQLite database |
| Simple backend (FastAPI) | ✅ | FastAPI server with Pydantic models, SQLite + SQLAlchemy ORM |
| SQLite database with 112 FAQ entries | ✅ | 12 categories: deadlines, exams, projects, grades, schedule, enrollment, IT, campus, financial, life, rules, general |
| FAQ data model with metadata | ✅ | Each entry has: question, answer, category, subject, professor, room, time, date, semester, type |

### Version 2 - Final Product

| Feature | Status | Details |
|---------|--------|---------|
| **Fuzzy search engine** | ✅ | Hybrid matching: 55% character-level (difflib) + 45% word-level (Jaccard similarity) |
| **Database (FAQ + history)** | ✅ | SQLite with SQLAlchemy ORM — stores 112 FAQs + query history with timestamps |
| **History tracking** | ✅ | Every query saved with question, answer, and timestamp. Full history accessible via API |
| **Dockerized deployment** | ✅ | Docker image (python:3.10-slim), deployed on university VM (Ubuntu 24.04) |
| **Improved UI** | ✅ | Single-page app with CSS Grid, smooth animations, responsive design |
| **Category browsing** | ✅ | Sidebar with 12 categories, entry counts, active state highlighting |
| **Autocomplete** | ✅ | Real-time suggestions (min 2 chars), highlights matched text, shows category badges, keyboard navigation (↑↓ Enter Esc) |
| **Contextual answers** | ✅ | Best match displayed as primary card + all related entries from the same category in a grid |
| **Metadata badges** | ✅ | Color-coded badges: 📚 Subject, 👤 Professor, 📍 Room, 🕐 Time, 📅 Date, 🎓 Semester |
| **Color-coded severity types** | ✅ | 4 types: info (blue), warning (orange), success (green), danger (red) — affects card background and left border |
| **Dark mode** | ✅ | Toggle with moon/sun icon, localStorage persistence, full theme swap via CSS variables |
| **Search statistics API** | ✅ | `/stats` endpoint: total queries, top 10 most asked questions with counts |
| **Upcoming events sidebar** | ✅ | 11 events with tags: urgent, exam, event, info — color-coded badges |
| **Responsive design** | ✅ | Mobile-friendly layout, collapsible sidebar, hamburger menu on small screens |
| **API endpoints** | ✅ | 8 endpoints: `/`, `/faqs`, `/categories`, `/events`, `/search_suggestions`, `/ask`, `/history`, `/stats` |
| **Quick-ask from cards** | ✅ | Click any FAQ card in category browse or related results to instantly search for it |
| **Category-filtered autocomplete** | ✅ | Autocomplete respects currently selected category |
| **Confidence score** | ✅ | Each result shows match confidence percentage |
| **MIT License** | ✅ | Open-source, added to repository |

### Not Yet Implemented

| Feature | Priority |
|---------|----------|
| LLM-powered chatbot integration | Medium |
| Multi-language support | Low |
| Admin panel for managing FAQs | Medium |
| Telegram bot interface | Low |
| Analytics dashboard | Low |

## Usage

### Web Interface

1. Open the app in your browser at `http://<host>:8000`
2. Type your question in the search bar (e.g., "exam", "deadline", "gym")
3. Use autocomplete suggestions or press Enter to search
4. View the best match answer + all related entries from the same category
5. Click category cards in the sidebar to browse all entries
6. Toggle dark mode with the moon icon

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Frontend UI |
| GET | `/faqs?category=exam` | FAQ entries (optionally filtered) |
| GET | `/categories` | Category list with counts |
| GET | `/events` | Upcoming events |
| GET | `/search_suggestions?q` | Autocomplete (supports `&category=`) |
| POST | `/ask` | Get answer + all related category entries |
| GET | `/history` | Q&A history |
| GET | `/stats` | Search statistics |

## Deployment

### Requirements

- **OS**: Ubuntu 24.04 (or any Linux with Docker)
- **Docker** installed and running

### Step-by-Step Deployment

#### Option A: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/bulat1223312/se-toolkit-hackathon.git
cd se-toolkit-hackathon

# Build the Docker image
docker build -t smart-faq-helper .

# Run the container
docker run -d -p 8000:8000 --name faq-helper smart-faq-helper

# Open in browser
# http://<your-host-ip>:8000
```

#### Option B: Direct Python

```bash
# Clone the repository
git clone https://github.com/bulat1223312/se-toolkit-hackathon.git
cd se-toolkit-hackathon

# Install dependencies
pip install fastapi uvicorn sqlalchemy

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000

# Open in browser
# http://localhost:8000
```

### Stopping the Service

```bash
# Docker
docker stop faq-helper
docker rm faq-helper

# Direct Python
# Press Ctrl+C in the terminal
```

## Links

- **GitHub Repository**: https://github.com/bulat1223312/se-toolkit-hackathon
- **Deployed Product**: http://10.93.25.49:8000

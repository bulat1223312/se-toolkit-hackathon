import difflib
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

DATABASE_URL = "sqlite:///./faq.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class FAQ(Base):
    __tablename__ = "faqs"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String, default="general")
    meta_subject = Column(String, default="")
    meta_professor = Column(String, default="")
    meta_room = Column(String, default="")
    meta_time = Column(String, default="")
    meta_date = Column(String, default="")
    meta_semester = Column(String, default="")
    meta_type = Column(String, default="info")


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart FAQ Helper")


class AskRequest(BaseModel):
    question: str


# ── SEED DATA: (q, a, cat, subject, professor, room, time, date, semester, type) ──
SEED_DATA = [
    # ═══════════════════════════════════════════════════════════
    # DEADLINES
    # ═══════════════════════════════════════════════════════════
    ("deadline", "The general deadline is Thursday 23:59. Check your course page for specifics.", "deadlines", "", "", "", "", "Thursday", "Fall/Spring 2026", "info"),
    ("when is the deadline for project", "Project submission deadline: Thursday 23:59 via Moodle. Late = -20% penalty.", "deadlines", "Computer Science", "Prof. Smith", "", "23:59", "Thursday", "Fall 2026", "warning"),
    ("when is the exam deadline", "Exam registration deadline: 2 weeks before the exam date. Register at dean's office.", "deadlines", "All courses", "", "Dean's Office, Rm 200", "", "2 weeks before", "Fall 2026", "warning"),
    ("late submission", "Late submissions accepted within 24h with -20% penalty. After 24h — no submission at all.", "deadlines", "All courses", "", "", "", "24h grace", "Fall/Spring 2026", "danger"),
    ("extend deadline", "Deadline extensions only for medical/emergency cases. Email professor with documentation.", "deadlines", "All courses", "", "", "", "", "Fall/Spring 2026", "info"),
    ("assignment deadline", "Weekly assignments due every Sunday 23:59 via Moodle. Auto-graded, no exceptions.", "deadlines", "CS101, CS201", "Prof. Smith", "", "23:59", "Every Sunday", "Fall 2026", "warning"),
    ("final project deadline", "Final project: last day of semester, 18:00. No late submissions accepted under any circumstances.", "deadlines", "Computer Science", "Prof. Smith", "", "18:00", "Last day of semester", "Fall 2026", "danger"),
    ("exam retake deadline", "Retake registration: within 3 days after main exam results are published.", "deadlines", "All courses", "", "Dean's Office, Rm 200", "", "3 days after results", "Fall 2026", "warning"),
    ("enrollment deadline", "Enrollment deadline: first Friday of semester. Late enrollment fee: $50.", "deadlines", "", "", "Registrar, Rm 100", "", "First Friday", "Fall 2026", "warning"),
    ("tuition deadline", "Tuition payment: end of week 2. Late fee: $100/week. See bursar for installment options.", "deadlines", "", "", "Bursar's Office", "", "End of Week 2", "Fall 2026", "warning"),

    # ═══════════════════════════════════════════════════════════
    # EXAMS
    # ═══════════════════════════════════════════════════════════
    ("exam", "Exams scheduled during exam week. Check Moodle for your personalized schedule.", "exams", "All courses", "", "", "", "Exam week", "Fall 2026", "info"),
    ("exam schedule", "Math — Mon 10:00, CS — Wed 14:00, Physics — Fri 09:00. Check room assignments on Moodle.", "exams", "Math/CS/Physics", "Prof. Smith (CS), Prof. Brown (Math)", "Room 101-105", "Mon/Wed/Fri", "Exam week", "Fall 2026", "info"),
    ("exam rules", "Bring student ID. No phones. Non-programmable calculators allowed. No bags at desks.", "exams", "All courses", "", "", "", "", "Fall 2026", "warning"),
    ("math exam rules", "Math exam: no calculators allowed. Bring compass and ruler. Formula sheet provided.", "exams", "Mathematics", "Prof. Brown", "Room 101", "", "Exam week", "Fall 2026", "warning"),
    ("cs exam rules", "CS exam: IDE allowed on laptop. No internet access. USB drive permitted for code backup.", "exams", "Computer Science", "Prof. Smith", "Lab Room 305", "3 hours", "Exam week", "Fall 2026", "info"),
    ("physics exam rules", "Physics exam: non-programmable calculator allowed. Formula sheet provided. No smartwatches.", "exams", "Physics", "Prof. Wilson", "Room 103", "2.5 hours", "Exam week", "Fall 2026", "warning"),
    ("exam retake", "Retake is 2 weeks after the main exam. Register at the dean's office, Room 200. Fee: $25.", "exams", "All courses", "", "Dean's Office, Rm 200", "", "2 weeks after main", "Fall 2026", "info"),
    ("midterm", "Midterm covers chapters 1-5. Open book. 90 minutes. No electronic devices.", "exams", "Computer Science", "Prof. Smith", "Room 301", "90 min", "Week 8", "Fall 2026", "info"),
    ("math midterm", "Math midterm: chapters 1-6, closed book, 120 minutes. Allowed: one A4 cheat sheet.", "exams", "Mathematics", "Prof. Brown", "Room 101", "120 min", "Week 8", "Fall 2026", "info"),
    ("exam room", "Exam rooms posted on Moodle 1 week before. Check announcements section for updates.", "exams", "All courses", "", "", "", "1 week before", "Fall 2026", "info"),
    ("missed exam", "Missed exam for medical reasons: provide doctor's certificate within 48h. Contact dean's office.", "exams", "All courses", "", "Dean's Office, Rm 200", "", "Within 48h", "Fall 2026", "danger"),
    ("exam preparation tips", "Review lecture slides, solve past papers (available on Moodle), attend review sessions week before.", "exams", "All courses", "", "", "", "Week before exams", "Fall 2026", "success"),

    # ═══════════════════════════════════════════════════════════
    # PROJECTS
    # ═══════════════════════════════════════════════════════════
    ("project", "Submit your project via Moodle. Include README, source files, and test cases.", "projects", "Computer Science", "Prof. Smith", "", "", "Thursday", "Fall 2026", "info"),
    ("project topic", "Choose from Moodle list or propose your own. Get TA approval by week 4.", "projects", "Computer Science", "Prof. Smith", "", "", "Week 4", "Fall 2026", "info"),
    ("project team size", "Teams of 2-3 students. Solo projects allowed with written TA approval.", "projects", "Computer Science", "TA: John Davis", "", "", "", "Fall 2026", "info"),
    ("project submission", "Submit as .zip on Moodle. Filename: LastName1_LastName2_Project.zip. Include README.", "projects", "Computer Science", "Prof. Smith", "", "", "Thursday 23:59", "Fall 2026", "info"),
    ("submit project", "Submit via Moodle with all source files, README, and test cases. Max file size: 50MB.", "projects", "Computer Science", "Prof. Smith", "", "", "Thursday 23:59", "Fall 2026", "info"),
    ("group project", "Groups of 2-3. Register your team on Moodle by end of week 3. No changes after.", "projects", "Computer Science", "Prof. Smith", "", "", "Week 3", "Fall 2026", "info"),
    ("math project", "Math project: group proof assignment. 4-5 students. Submit LaTeX PDF. Topic: Group Theory.", "projects", "Mathematics", "Prof. Brown", "Room 101", "", "Week 12", "Fall 2026", "info"),
    ("assignment format", "PDF for reports. .zip for code with README. Include student ID in filename.", "projects", "All courses", "", "", "", "", "Fall 2026", "info"),
    ("plagiarism", "Any plagiarism = automatic fail + report to academic board. Turnitin checks all submissions.", "projects", "All courses", "", "", "", "", "Fall 2026", "danger"),
    ("project presentation", "Each team presents 10 min + 5 min Q&A. Schedule posted week 14. Room 301.", "projects", "Computer Science", "Prof. Smith", "Room 301", "10+5 min", "Week 14", "Fall 2026", "info"),
    ("resubmit project", "One resubmission within 1 week. Max grade after resubmit: 80%. Submit to TA directly.", "projects", "Computer Science", "TA: John Davis", "", "", "Within 1 week", "Fall 2026", "info"),

    # ═══════════════════════════════════════════════════════════
    # GRADES
    # ═══════════════════════════════════════════════════════════
    ("grade", "Grades posted on Moodle within 5 working days after each submission.", "grades", "All courses", "", "", "", "5 working days", "Fall 2026", "info"),
    ("grade scale", "A: 90-100, B: 80-89, C: 70-79, D: 60-69, F: below 60.", "grades", "All courses", "", "", "", "", "Fall 2026", "info"),
    ("grade appeal", "Appeal within 3 days of publication. Email TA with detailed justification. Fee: $10.", "grades", "All courses", "", "", "", "3 days", "Fall 2026", "warning"),
    ("passing grade", "Minimum passing grade: 60/100. Final exam counts 40% of total grade.", "grades", "All courses", "", "", "", "", "Fall 2026", "warning"),
    ("bonus points", "+5 perfect attendance, +3 early project submission, +2 peer review participation.", "grades", "All courses", "", "", "", "", "Fall 2026", "success"),
    ("grading breakdown", "Final: 40% exam + 30% project + 20% assignments + 10% attendance.", "grades", "All courses", "", "", "", "", "Fall 2026", "info"),
    ("math grading", "Math grading: 50% exam + 30% homework + 20% midterm. Curve applied if class avg < 65.", "grades", "Mathematics", "Prof. Brown", "", "", "", "Fall 2026", "info"),
    ("cs grading", "CS grading: 40% exam + 30% project + 20% assignments + 10% attendance.", "grades", "Computer Science", "Prof. Smith", "", "", "", "Fall 2026", "info"),
    ("gpa calculation", "GPA = sum(grade × credits) / total credits. Minimum GPA to pass: 2.0.", "grades", "", "", "", "", "", "Fall 2026", "info"),
    ("exam results", "Exam results published on Moodle within 5 working days. Check announcements.", "grades", "All courses", "", "", "", "5 working days", "Fall 2026", "info"),
    ("exam grade appeal", "Appeal exam grades within 3 days. Submit written request to the exam committee.", "grades", "All courses", "", "Exam Committee, Rm 210", "", "3 days", "Fall 2026", "warning"),
    ("project evaluation", "Graded on: code quality 30%, documentation 20%, presentation 20%, correctness 30%.", "grades", "Computer Science", "Prof. Smith", "", "", "", "Fall 2026", "info"),
    ("honors", "Summa Cum Laude: GPA 3.9+, Magna: 3.7+, Cum Laude: 3.5+. Dean's List: 3.3+.", "grades", "", "", "", "", "", "Fall 2026", "success"),
    ("failed course", "If you fail, retake next semester. Financial aid may be affected. See advisor.", "grades", "", "", "Advisor Office, Rm 220", "", "Next semester", "Fall 2026", "danger"),

    # ═══════════════════════════════════════════════════════════
    # SCHEDULE
    # ═══════════════════════════════════════════════════════════
    ("schedule", "Lectures: Mon/Wed 10:00-12:00 Room 301. Seminars: Fri 14:00-16:00 Room 205.", "schedule", "Computer Science", "Prof. Smith", "Room 301 / 205", "Mon/Wed 10:00, Fri 14:00", "", "Fall 2026", "info"),
    ("math schedule", "Math lectures: Tue/Thu 09:00-11:00 Room 101. Problem sessions: Fri 11:00-13:00.", "schedule", "Mathematics", "Prof. Brown", "Room 101", "Tue/Thu 09:00", "", "Fall 2026", "info"),
    ("physics schedule", "Physics lectures: Mon/Wed 14:00-16:00 Room 103. Lab: Thu 10:00-13:00 Lab 4.", "schedule", "Physics", "Prof. Wilson", "Room 103 / Lab 4", "Mon/Wed 14:00, Thu 10:00", "", "Fall 2026", "info"),
    ("timetable", "Full timetable on Moodle → Course → Schedule tab. Updates posted weekly.", "schedule", "All courses", "", "", "", "", "Fall 2026", "info"),
    ("room change", "Check Moodle for room changes. This week lectures moved to Room 410.", "schedule", "Computer Science", "Prof. Smith", "Room 410", "", "This week", "Fall 2026", "warning"),
    ("online classes", "Online only if announced on Moodle. Zoom link in the course page.", "schedule", "All courses", "", "", "", "", "Fall 2026", "info"),
    ("cancelled class", "If class is cancelled, check Moodle for make-up session announcements.", "schedule", "All courses", "", "", "", "", "Fall 2026", "info"),
    ("office hours", "Prof. Smith: Tue 15:00-17:00 Room 312. TA John: Thu 11:00-13:00 Room 205.", "schedule", "Computer Science", "Prof. Smith", "Room 312", "Tue 15:00-17:00", "", "Fall 2026", "info"),
    ("professor office hours", "Prof. Smith: Tue 15:00-17:00 Room 312. Book a slot via Moodle.", "schedule", "Computer Science", "Prof. Smith", "Room 312", "Tue 15:00-17:00", "", "Fall 2026", "info"),
    ("ta office hours", "TA John Davis: Thu 11:00-13:00 Room 205. Drop-in, no appointment needed.", "schedule", "Computer Science", "TA: John Davis", "Room 205", "Thu 11:00-13:00", "", "Fall 2026", "info"),
    ("math office hours", "Prof. Brown: Wed 13:00-15:00 Room 102. TA Sarah: Mon 10:00-12:00 Room 102.", "schedule", "Mathematics", "Prof. Brown", "Room 102", "Wed 13:00, Mon 10:00", "", "Fall 2026", "info"),
    ("holiday schedule", "No classes during university holidays. Check academic calendar on the website.", "schedule", "", "", "", "", "", "Fall 2026", "info"),
    ("summer school", "Summer school: June-July. Registration opens in April. Limited spots, apply early.", "schedule", "", "", "", "", "June-July", "Summer 2026", "info"),

    # ═══════════════════════════════════════════════════════════
    # ENROLLMENT
    # ═══════════════════════════════════════════════════════════
    ("enrollment", "Enrollment via student portal. Opens 2 weeks before semester starts.", "enrollment", "", "", "Registrar, Rm 100", "", "2 weeks before", "Fall 2026", "info"),
    ("drop a course", "Drop via student portal within first 2 weeks. No refund after week 2.", "enrollment", "", "", "Registrar, Rm 100", "", "First 2 weeks", "Fall 2026", "warning"),
    ("add a course", "Add courses during first 2 weeks. Get professor's approval signature.", "enrollment", "", "", "Registrar, Rm 100", "", "First 2 weeks", "Fall 2026", "info"),
    ("prerequisites", "Check course catalog for prerequisites. System blocks enrollment if not met.", "enrollment", "", "", "", "", "", "Fall 2026", "info"),
    ("course catalog", "Course catalog: university.edu/catalog. Updated each semester.", "enrollment", "", "", "", "", "", "Fall 2026", "info"),
    ("waitlist", "Course full? Join the waitlist. Notified if a spot opens.", "enrollment", "", "", "", "", "", "Fall 2026", "info"),
    ("switch section", "Switch seminar sections via portal if seats are available.", "enrollment", "", "", "", "", "", "Fall 2026", "info"),
    ("audit a course", "Auditing requires professor permission. No credit, no grade. Register as 'auditor'.", "enrollment", "", "", "Registrar, Rm 100", "", "", "Fall 2026", "info"),
    ("course load", "Full-time: 12-18 credits. Overload (>18) requires advisor approval.", "enrollment", "", "", "Advisor Office, Rm 220", "", "", "Fall 2026", "info"),

    # ═══════════════════════════════════════════════════════════
    # IT
    # ═══════════════════════════════════════════════════════════
    ("moodle", "Moodle: https://moodle.university.edu — login with university credentials.", "it", "", "", "", "", "", "", "info"),
    ("moodle login", "Login to Moodle with student ID and university password. Reset at it.university.edu.", "it", "", "", "", "", "", "", "info"),
    ("forgot password", "Reset at it.university.edu/reset or visit IT Help Desk Room 100.", "it", "", "", "IT Help Desk, Rm 100", "Mon-Fri 9:00-17:00", "", "", "info"),
    ("wifi", "WiFi: 'UniNet' with student credentials. Guest network 'UniNet-Guest' for visitors.", "it", "", "", "", "", "", "", "info"),
    ("email", "Student email: studentid@university.edu. Check daily — official notices sent there.", "it", "", "", "", "", "", "", "info"),
    ("student portal", "Portal: portal.university.edu — grades, schedule, enrollment, finances.", "it", "", "", "", "", "", "", "info"),
    ("it help desk", "IT Help Desk: Room 100, Mon-Fri 9:00-17:00. Email: helpdesk@university.edu.", "it", "", "", "Room 100", "Mon-Fri 9:00-17:00", "", "", "info"),
    ("software access", "Free: Office 365, MATLAB, JetBrains via university license. Download from it.university.edu.", "it", "", "", "", "", "", "", "success"),
    ("computer labs", "Labs: Building C, open 8:00-22:00. Printers require student card.", "it", "", "", "Building C", "8:00-22:00", "", "", "info"),

    # ═══════════════════════════════════════════════════════════
    # CAMPUS
    # ═══════════════════════════════════════════════════════════
    ("library", "Library: Mon-Fri 8:00-22:00, Sat 10:00-18:00. Renew books online at library.university.edu.", "campus", "", "", "Main Library", "Mon-Fri 8:00-22:00", "", "", "info"),
    ("library hours", "Mon-Fri 8:00-22:00, Sat 10:00-18:00, Sun 14:00-20:00 during exam period.", "campus", "", "", "Main Library", "Mon-Fri 8:00-22:00", "Exam period: Sun too", "", "info"),
    ("cafeteria", "Cafeteria: Building A, 7:30-19:00. Meal plans available. Vegan options daily.", "campus", "", "", "Building A", "7:30-19:00", "", "", "info"),
    ("parking", "Parking permit: $100/semester. Apply at security office. Student lot: Lot B.", "campus", "", "", "Security Office, Bldg A", "", "", "", "info"),
    ("gym", "Gym: Building D, 6:00-22:00. Free with student ID. Personal training: +$30/month.", "campus", "", "", "Building D", "6:00-22:00", "", "", "info"),
    ("where is the gym", "Gym is in Building D, open 6:00-22:00. Free with student ID.", "campus", "", "", "Building D", "6:00-22:00", "", "", "info"),
    ("dormitory", "Housing applications open May 1. Priority: 1st year, international, scholarship holders.", "campus", "", "", "Housing Office, Bldg F", "", "May 1", "", "info"),
    ("campus map", "Interactive map: university.edu/map. Download PDF at student services.", "campus", "", "", "Student Services, Bldg A", "", "", "", "info"),
    ("printing", "Printing: 200 free pages/semester. Extra: $0.05/page. Student card at any printer.", "campus", "", "", "Building C (Labs)", "", "", "", "info"),
    ("study rooms", "Book study rooms via library website. Max 4 people, 2-hour slots.", "campus", "", "", "Main Library", "", "", "", "info"),

    # ═══════════════════════════════════════════════════════════
    # FINANCIAL
    # ═══════════════════════════════════════════════════════════
    ("tuition", "Tuition: $5,000/semester. Payment due by week 2. Installment plans available at bursar.", "financial", "", "", "Bursar's Office", "", "Week 2", "Fall 2026", "warning"),
    ("scholarship", "Scholarship: GPA >3.5, apply March 1 at financial office. Covers 25-100% tuition.", "financial", "", "", "Financial Office, Bldg A", "", "March 1", "2026-2027", "success"),
    ("financial aid", "Financial aid: fafsa.gov + university form. Deadline: February 15.", "financial", "", "", "Financial Office, Bldg A", "", "February 15", "2026-2027", "info"),
    ("payment plan", "3-payment plan: 40% at start, 30% mid-semester, 30% before exams. Sign at bursar.", "financial", "", "", "Bursar's Office", "", "", "Fall 2026", "info"),
    ("refund", "Full refund if drop within 2 weeks. 50% weeks 3-4. No refund after week 5.", "financial", "", "", "Bursar's Office", "", "", "Fall 2026", "warning"),
    ("work study", "Work-study: up to 15 hrs/week during semester. Apply at career center. $15/hr.", "financial", "", "", "Career Center, Bldg B Rm 300", "", "", "Fall 2026", "success"),

    # ═══════════════════════════════════════════════════════════
    # STUDENT LIFE
    # ═══════════════════════════════════════════════════════════
    ("student organizations", "100+ clubs! Browse at university.edu/clubs. Recruitment during orientation week.", "life", "", "", "Student Union", "", "Orientation week", "", "info"),
    ("student union", "Student Union Building: events, meetings, games. Open 8:00-midnight.", "life", "", "", "Union Building", "8:00-midnight", "", "", "info"),
    ("events", "Events calendar: university.edu/events. Weekly newsletter sent to student email.", "life", "", "", "", "", "", "", "info"),
    ("volunteer", "Volunteer office: Student Union Room 205. 50+ hours = certificate + transcript note.", "life", "", "", "Union Rm 205", "", "", "", "success"),
    ("career center", "Career Center: Building B, Room 300. Resume reviews, mock interviews, job fairs.", "life", "", "", "Building B, Room 300", "Mon-Fri 9:00-17:00", "", "", "info"),
    ("internships", "Internship listings on Handshake portal. Career center helps with applications.", "life", "", "", "Career Center, Bldg B Rm 300", "", "", "", "info"),
    ("study abroad", "Study abroad: applications due October 1 (spring) / March 1 (fall). 50+ partner universities.", "life", "", "", "International Office", "", "Oct 1 / Mar 1", "", "info"),
    ("counseling", "Counseling services: Student Health, Room 150. Free, confidential. Book online.", "life", "", "", "Health Center, Rm 150", "", "", "", "info"),
    ("health services", "Health Center: Building E. Mon-Fri 8:00-17:00. Student health fee covers basic visits.", "life", "", "", "Building E", "Mon-Fri 8:00-17:00", "", "", "info"),

    # ═══════════════════════════════════════════════════════════
    # RULES
    # ═══════════════════════════════════════════════════════════
    ("code of conduct", "Full code: university.edu/conduct. Ignorance is not an excuse.", "rules", "", "", "", "", "", "", "warning"),
    ("academic dishonesty", "Academic dishonesty: plagiarism, cheating, unauthorized collaboration. Penalty: course failure + board report.", "rules", "All courses", "", "", "", "", "", "danger"),
    ("attendance policy", "Minimum 75% attendance required. Below 75% = cannot sit for final exam.", "rules", "All courses", "", "", "", "", "", "danger"),
    ("dress code", "No formal dress code. Lab safety: closed shoes, tied hair, no loose clothing.", "rules", "", "", "", "", "", "", "info"),
    ("phone policy", "Phones on silent during class. Exams: phones must be in bag, not on desk.", "rules", "All courses", "", "", "", "", "", "warning"),
    ("recording lectures", "Recording lectures requires professor's permission. Personal use only, no sharing.", "rules", "All courses", "", "", "", "", "", "info"),
    ("complaint procedure", "File complaints at dean's office. Written, signed, within 10 days of incident.", "rules", "", "", "Dean's Office, Rm 200", "", "Within 10 days", "", "info"),
    ("disability accommodations", "Disability Services: Building A, Room 200. Register early. Documentation required.", "rules", "", "", "Building A, Room 200", "", "", "", "info"),

    # ═══════════════════════════════════════════════════════════
    # GENERAL
    # ═══════════════════════════════════════════════════════════
    ("contact ta", "TA email: ta@university.edu. Response within 24h on weekdays. TA: John Davis.", "general", "Computer Science", "TA: John Davis", "", "", "24h response", "Fall 2026", "info"),
    ("contact professor", "Email professors with university account. Response: 48h. Office hours for urgent matters.", "general", "All courses", "", "", "", "48h response", "", "info"),
    ("textbook", "Required: 'Introduction to CS' by Smith, 3rd ed. Library has copies on reserve.", "general", "Computer Science", "Prof. Smith", "Library (reserve)", "", "", "Fall 2026", "info"),
    ("math textbook", "Required: 'Linear Algebra Done Right' by Axler. Library Rm 210 has copies.", "general", "Mathematics", "Prof. Brown", "Library, Rm 210", "", "", "Fall 2026", "info"),
    ("academic calendar", "Academic calendar: university.edu/calendar. Key dates: start, end, holidays, exam week.", "general", "", "", "", "", "", "", "info"),
    ("semester dates", "Fall: Sep-Dec. Spring: Jan-May. Summer: Jun-Jul.", "general", "", "", "", "", "Sep-Dec / Jan-May", "", "info"),
    ("graduation", "Graduation application: semester before completion. Ceremony: June and December.", "general", "", "", "Registrar, Rm 100", "", "June / December", "", "info"),
    ("diploma", "Diplomas mailed 6-8 weeks after graduation. Pick-up at registrar available.", "general", "", "", "Registrar, Rm 100", "", "6-8 weeks", "", "info"),
    ("transcript request", "Official transcripts: registrar.university.edu. $10 fee, 3-day processing.", "general", "", "", "Registrar, Rm 100", "", "3-day processing", "", "info"),
    ("course materials", "All slides, handouts, recordings on Moodle under each course section.", "general", "All courses", "", "", "", "", "", "info"),
    ("how to pass this course", "Attend 75%+, submit all assignments, score 60+ on final. Study groups recommended.", "general", "Computer Science", "Prof. Smith", "", "", "", "Fall 2026", "success"),
    ("who to contact for help", "1) TA for assignments. 2) Professor for grades. 3) Advisor for schedule. 4) Dean's office for formal issues.", "general", "", "", "", "", "", "", "info"),
]

UPCOMING_EVENTS = [
    {"title": "Project Deadline", "date": "Thursday, 23:59", "tag": "urgent"},
    {"title": "Assignment #7 Due", "date": "Sunday, 23:59", "tag": "urgent"},
    {"title": "Math Midterm", "date": "Mon, 10:00, Room 101", "tag": "exam"},
    {"title": "CS Midterm", "date": "Wed, 14:00, Room 301", "tag": "exam"},
    {"title": "Physics Midterm", "date": "Fri, 09:00, Room 103", "tag": "exam"},
    {"title": "Guest Lecture: AI Ethics", "date": "Fri, 16:00, Room 301", "tag": "event"},
    {"title": "Career Fair", "date": "Next Tue, 10:00-16:00", "tag": "event"},
    {"title": "Office Hours (Prof. Smith)", "date": "Tue, 15:00-17:00", "tag": "info"},
    {"title": "TA Drop-in Help", "date": "Thu, 11:00-13:00", "tag": "info"},
    {"title": "Scholarship Deadline", "date": "March 1", "tag": "info"},
    {"title": "Enrollment Opens", "date": "Next month", "tag": "info"},
]


def seed_data():
    db = SessionLocal()
    if db.query(FAQ).count() == 0:
        for q, a, cat, subj, prof, room, time, date, sem, mtype in SEED_DATA:
            db.add(FAQ(
                question=q, answer=a, category=cat,
                meta_subject=subj, meta_professor=prof,
                meta_room=room, meta_time=time, meta_date=date,
                meta_semester=sem, meta_type=mtype,
            ))
        db.commit()
    db.close()


seed_data()


def _similarity(a: str, b: str) -> float:
    char_score = difflib.SequenceMatcher(None, a, b).ratio()
    wa, wb = set(a.split()), set(b.split())
    if not wa or not wb:
        return char_score
    word_score = len(wa & wb) / len(wa | wb)
    return 0.55 * char_score + 0.45 * word_score


# ── ENDPOINTS ──────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r") as f:
        return f.read()


@app.get("/faqs")
def get_faqs(category: str = ""):
    db = SessionLocal()
    q = db.query(FAQ)
    if category:
        q = q.filter(FAQ.category == category)
    faqs = q.all()
    result = [{
        "id": f.id, "question": f.question, "answer": f.answer,
        "category": f.category, "meta_subject": f.meta_subject,
        "meta_professor": f.meta_professor, "meta_room": f.meta_room,
        "meta_time": f.meta_time, "meta_date": f.meta_date,
        "meta_semester": f.meta_semester, "meta_type": f.meta_type,
    } for f in faqs]
    db.close()
    return result


@app.get("/categories")
def get_categories():
    db = SessionLocal()
    rows = db.query(FAQ.category, func.count(FAQ.id)).group_by(FAQ.category).all()
    db.close()
    return [{"category": r[0], "count": r[1]} for r in sorted(rows, key=lambda x: x[0])]


@app.get("/events")
def get_events():
    return UPCOMING_EVENTS


@app.get("/search_suggestions")
def search_suggestions(q: str, category: str = ""):
    if not q or len(q.strip()) < 2:
        return []
    db = SessionLocal()
    faq_q = db.query(FAQ)
    if category:
        faq_q = faq_q.filter(FAQ.category == category)
    faqs = faq_q.all()
    db.close()
    user_q = q.lower().strip()
    scored = []
    for faq in faqs:
        score = _similarity(user_q, faq.question.lower())
        if score >= 0.2:
            scored.append((score, faq.question, faq.category))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [{"question": s[1], "category": s[2], "score": round(s[0], 3)} for s in scored[:10]]


@app.get("/stats")
def get_stats():
    db = SessionLocal()
    total = db.query(History).count()
    top_questions = (
        db.query(History.question, func.count(History.question).label("cnt"))
        .group_by(History.question)
        .order_by(func.count(History.question).desc())
        .limit(10)
        .all()
    )
    db.close()
    return {
        "total_queries": total,
        "top_questions": [{"question": t[0], "count": t[1]} for t in top_questions],
    }


@app.post("/ask")
def ask(req: AskRequest):
    db = SessionLocal()
    faqs = db.query(FAQ).all()

    best_score = 0
    best_faq = None

    user_q = req.question.lower().strip()
    for faq in faqs:
        score = _similarity(user_q, faq.question.lower())
        if score > best_score:
            best_score = score
            best_faq = faq

    if best_score <= 0.4 or best_faq is None:
        db.add(History(question=req.question, answer="I don't know, ask TA"))
        db.commit()
        db.close()
        return {
            "answer": "I don't know, ask TA",
            "matched_question": None,
            "confidence": round(best_score, 3),
            "category": None,
            "primary": None,
            "related": [],
            "category_name": None,
        }

    matched_category = best_faq.category
    primary = {
        "question": best_faq.question,
        "answer": best_faq.answer,
        "meta_subject": best_faq.meta_subject,
        "meta_professor": best_faq.meta_professor,
        "meta_room": best_faq.meta_room,
        "meta_time": best_faq.meta_time,
        "meta_date": best_faq.meta_date,
        "meta_semester": best_faq.meta_semester,
        "meta_type": best_faq.meta_type,
    }

    related_faqs = db.query(FAQ).filter(
        FAQ.category == matched_category,
        FAQ.id != best_faq.id,
    ).all()
    related = [{
        "question": f.question, "answer": f.answer,
        "meta_subject": f.meta_subject,
        "meta_professor": f.meta_professor,
        "meta_room": f.meta_room, "meta_time": f.meta_time,
        "meta_date": f.meta_date, "meta_semester": f.meta_semester,
        "meta_type": f.meta_type,
    } for f in related_faqs]

    db.add(History(question=req.question, answer=best_faq.answer))
    db.commit()
    db.close()

    return {
        "primary": primary,
        "matched_question": primary["question"],
        "answer": primary["answer"],
        "confidence": round(best_score, 3),
        "category": matched_category,
        "related": related,
        "category_name": matched_category,
    }


@app.get("/history")
def get_history():
    db = SessionLocal()
    items = db.query(History).order_by(History.id.desc()).all()
    result = [
        {"question": h.question, "answer": h.answer, "timestamp": h.timestamp.isoformat()}
        for h in items
    ]
    db.close()
    return result

import os
import psycopg2
from psycopg2.extras import RealDictCursor


DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set.")

    conn = psycopg2.connect(DATABASE_URL)
    return conn


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id SERIAL PRIMARY KEY,
            total_score INTEGER NOT NULL,
            percentage REAL NOT NULL,
            security_level TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            question_text TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id SERIAL PRIMARY KEY,
            assessment_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            response TEXT NOT NULL,
            score INTEGER NOT NULL,
            FOREIGN KEY (assessment_id) REFERENCES assessments(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def save_assessment(total_score, percentage, security_level):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO assessments
        (total_score, percentage, security_level)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (total_score, percentage, security_level))

    assessment_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return assessment_id


def save_response(assessment_id, question_id, response, score):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO responses
        (assessment_id, question_id, response, score)
        VALUES (%s, %s, %s, %s)
    """, (
        assessment_id,
        question_id,
        response,
        score
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_assessments():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT * FROM assessments
        ORDER BY id DESC
    """)

    assessments = cursor.fetchall()

    cursor.close()
    conn.close()

    return assessments


def get_questions():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT * FROM questions
        ORDER BY id
    """)

    questions = cursor.fetchall()

    cursor.close()
    conn.close()

    return questions


def seed_questions():
    conn = get_db_connection()
    cursor = conn.cursor()

    questions = [
        (15, "I use a password or PIN to protect my online accounts.", "Authentication"),
        (16, "I avoid sharing my passwords with other people.", "Authentication"),
        (17, "I use different passwords for different online accounts.", "Authentication"),
        (18, "I have heard of two-factor authentication (2FA).", "Authentication"),
        (19, "I use an additional verification step, such as a code sent to my phone, when available.", "Authentication"),
        (20, "I understand that weak passwords can make an account easier to compromise.", "Authentication"),
        (21, "I check carefully before entering my password on a website.", "Authentication"),
        (22, "I understand that logging out of an account on a shared computer helps protect my account.", "Authentication"),
        (23, "I receive security alerts when someone tries to access my online accounts.", "Authentication"),
        (24, "I would like to learn more about how to protect my accounts from unauthorized access.", "Authentication"),

        (25, "Information sent through the university Wi-Fi should be protected from people who should not have access to it.", "Protection"),
        (26, "I believe the university Wi-Fi provides adequate protection for information sent through it.", "Protection"),
        (27, "I feel safe carrying out academic activities involving personal information while using the university Wi-Fi.", "Protection"),
        (28, "Sensitive information should not be sent through an unprotected wireless connection.", "Protection"),
        (29, "Secure wireless connections can help protect users' information.", "Protection"),
        (30, "The university should use modern security methods to protect information sent over its Wi-Fi.", "Protection"),
        (31, "Outdated wireless security methods can expose users to security risks.", "Protection"),
        (32, "Users should be informed when they are connected to an insecure wireless network.", "Protection"),
        (33, "The university should regularly review the methods used to protect information transmitted over its wireless network.", "Protection"),
        (34, "Overall, I believe information transmitted through the university wireless network is adequately protected.", "Protection")
    ]

    for question in questions:
        cursor.execute("""
            INSERT INTO questions
            (id, question_text, category)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, question)

    conn.commit()
    cursor.close()
    conn.close()
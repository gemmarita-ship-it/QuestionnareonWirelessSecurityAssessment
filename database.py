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
        # =========================
        # AUTHENTICATION (15–24)
        # =========================
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

        # =========================
        # PROTECTION (25–34)
        # =========================
        (25, "Information sent through the university Wi-Fi should be protected from people who should not have access to it.", "Protection"),
        (26, "I believe the university Wi-Fi provides adequate protection for information sent through it.", "Protection"),
        (27, "I feel safe carrying out academic activities involving personal information while using the university Wi-Fi.", "Protection"),
        (28, "Sensitive information should not be sent through an unprotected wireless connection.", "Protection"),
        (29, "Secure wireless connections can help protect users' information.", "Protection"),
        (30, "The university should use modern security methods to protect information sent over its Wi-Fi.", "Protection"),
        (31, "Outdated wireless security methods can expose users to security risks.", "Protection"),
        (32, "Users should be informed when they are connected to an insecure wireless network.", "Protection"),
        (33, "The university should regularly review the methods used to protect information transmitted over its wireless network.", "Protection"),
        (34, "Overall, I believe information transmitted through the university wireless network is adequately protected.", "Protection"),

        # =========================
        # ACCESS CONTROL (35–44)
        # =========================
        (35, "Wireless network access should be restricted to authorized students and staff.", "Access Control"),
        (36, "The university should control which devices are allowed to connect to its wireless network.", "Access Control"),
        (37, "Users who are no longer authorized to use the network should lose their wireless access.", "Access Control"),
        (38, "Unauthorized devices should be prevented from connecting to the university wireless network.", "Access Control"),
        (39, "Different categories of users should have appropriate levels of access to wireless resources.", "Access Control"),
        (40, "Wireless network access should be reviewed regularly to ensure that only authorized users have access.", "Access Control"),
        (41, "The university has measures for detecting unauthorized users on its wireless network.", "Access Control"),
        (42, "Users should not share their wireless network login details with unauthorized persons.", "Access Control"),
        (43, "Proper control of wireless network access reduces security risks.", "Access Control"),
        (44, "The current measures used by the university to control wireless network access are adequate.", "Access Control"),

        # =========================
        # CONFIGURATION (45–54)
        # =========================
        (45, "Wireless network equipment and security settings should be updated regularly.", "Configuration"),
        (46, "Default passwords and settings should be changed before wireless equipment is put into use.", "Configuration"),
        (47, "Wireless equipment should be configured according to recommended security practices.", "Configuration"),
        (48, "The security settings of the university wireless network should be checked regularly.", "Configuration"),
        (49, "Using outdated wireless equipment can increase security risks.", "Configuration"),
        (50, "Unnecessary wireless services that may create security risks should be restricted.", "Configuration"),
        (51, "Sensitive university resources should be separated from ordinary wireless users where necessary.", "Configuration"),
        (52, "Wireless security settings should be reviewed after major changes are made to the network.", "Configuration"),
        (53, "Proper configuration of wireless network equipment can reduce unauthorized access and security threats.", "Configuration"),
        (54, "The university wireless network is properly configured to provide adequate security.", "Configuration"),

        # =========================
        # MONITORING (55–64)
        # =========================
        (55, "The university wireless network should be monitored regularly for security problems.", "Monitoring"),
        (56, "Attempts by unauthorized users to access the wireless network should be detected.", "Monitoring"),
        (57, "Suspicious activities on the wireless network should be identified promptly.", "Monitoring"),
        (58, "Important activities on the university wireless network should be recorded for security purposes.", "Monitoring"),
        (59, "Network administrators should review security records to identify unusual activities.", "Monitoring"),
        (60, "Wireless security incidents should be reported to the appropriate university administrators.", "Monitoring"),
        (61, "The university should have clear procedures for responding to wireless security incidents.", "Monitoring"),
        (62, "Users should be informed when serious security problems affect the university wireless network.", "Monitoring"),
        (63, "Regular monitoring of the wireless network can help reduce security threats.", "Monitoring"),
        (64, "The university has adequate measures for detecting wireless network security problems.", "Monitoring"),

        # =========================
        # AWARENESS (65–74)
        # =========================
        (65, "Users should avoid sharing their university wireless network login details with other people.", "Awareness"),
        (66, "Users should avoid connecting to suspicious or unfamiliar wireless networks.", "Awareness"),
        (67, "Users should use strong passwords for their online accounts.", "Awareness"),
        (68, "Users should understand the risks associated with public or unsecured wireless networks.", "Awareness"),
        (69, "Users know where to report a suspected wireless security problem at the university.", "Awareness"),
        (70, "Users take precautions when sending personal or sensitive information over wireless networks.", "Awareness"),
        (71, "Students and staff should receive regular training on wireless security.", "Awareness"),
        (72, "The university provides sufficient information to help users safely use its wireless network.", "Awareness"),
        (73, "Greater user awareness can improve the security of the university wireless network.", "Awareness"),
        (74, "Users of the university wireless network generally follow safe security practices.", "Awareness")
    ]

    for question_id, question_text, section in questions:
        cursor.execute("""
            INSERT INTO questions (id, question_text, section)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (question_id, question_text, section))

    conn.commit()
    cursor.close()
    conn.close()
    
"""PNG 学生证生成模块 - Penn State LionPATH (高级随机版+修复)"""
import random
from datetime import datetime, timedelta
from io import BytesIO

# ---------------- 配置区域 ----------------
CURRENT_TERM = "Spring 2026"
TERM_DATES = "(Jan 12 - May 08)"
COPYRIGHT_YEAR = "2026"
# -----------------------------------------

def generate_psu_id():
    """生成随机 PSU ID (9位数字)"""
    return f"9{random.randint(10000000, 99999999)}"

def generate_psu_email(first_name, last_name):
    """
    生成 PSU 邮箱 (这是之前缺失的函数)
    格式: firstName.lastName + 3-4位数字 @psu.edu
    """
    digit_count = random.choice([3, 4])
    digits = ''.join([str(random.randint(0, 9)) for _ in range(digit_count)])
    email = f"{first_name.lower()}.{last_name.lower()}{digits}@psu.edu"
    return email

def generate_random_course():
    """生成一门随机课程信息"""
    subjects = [
        ('CMPSC', 'Computer Science'), ('MATH', 'Mathematics'), 
        ('STAT', 'Statistics'), ('ENGL', 'English'), 
        ('PHYS', 'Physics'), ('CHEM', 'Chemistry'), 
        ('ECON', 'Economics'), ('PSY', 'Psychology'),
        ('HIST', 'History'), ('ART', 'Art History')
    ]
    
    sub_code, sub_name = random.choice(subjects)
    course_num = random.randint(100, 499)
    class_nbr = random.randint(10000, 99999)
    
    titles = ['Intro to', 'Advanced', 'Principles of', 'Applied', 'Theory of', 'Seminar in']
    title = f"{random.choice(titles)} {sub_name}"
    
    days_opts = ['MoWeFr', 'TuTh', 'MoWe', 'Fr']
    days = random.choice(days_opts)
    
    start_hour = random.randint(8, 16)
    start_min = random.choice(['00', '05', '15', '30'])
    end_time_map = {'MoWeFr': 50, 'TuTh': 75, 'MoWe': 75, 'Fr': 180}
    duration = end_time_map.get(days, 50)
    
    start_dt = datetime.strptime(f"{start_hour}:{start_min}", "%H:%M")
    end_dt = start_dt + timedelta(minutes=duration)
    time_str = f"{days} {start_dt.strftime('%I:%M%p').lstrip('0')} - {end_dt.strftime('%I:%M%p').lstrip('0')}"
    
    buildings = ['Willard', 'Thomas', 'Osmond', 'Boucke', 'Westgate', 'Davey', 'Huck']
    room = f"{random.choice(buildings)} {random.randint(100, 399)}"
    
    units = random.choice(['3.00', '4.00'])
    
    return {
        'nbr': class_nbr,
        'code': f"{sub_code} {course_num}",
        'title': title,
        'time': time_str,
        'room': room,
        'units': units
    }

def generate_html(first_name, last_name, school_id='2565'):
    psu_id = generate_psu_id()
    name = f"{first_name} {last_name}"
    random_days = random.randint(0, 2)
    random_seconds = random.randint(0, 86400)
    fake_now = datetime.now() - timedelta(days=random_days, seconds=random_seconds)
    date_str = fake_now.strftime('%m/%d/%Y, %I:%M:%S %p')

    courses = [generate_random_course() for _ in range(random.randint(4, 6))]
    
    rows_html = ""
    for c in courses:
        rows_html += f"""
        <tr>
            <td>{c['nbr']}</td>
            <td class="course-code">{c['code']}</td>
            <td class="course-title">{c['title']}</td>
            <td>{c['time']}</td>
            <td>{c['room']}</td>
            <td>{c['units']}</td>
        </tr>
        """

    majors = [
        'Computer Science (BS)', 'Software Engineering (BS)', 'Data Science (BS)',
        'Mechanical Engineering (BS)', 'Business Admin (BS)', 'Cybersecurity (BS)'
    ]
    major = random.choice(majors)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LionPATH - Student Home</title>
    <style>
        :root {{ --psu-blue: #1E407C; --bg-gray: #f4f4f4; --text-color: #333; }}
        body {{ font-family: "Roboto", Helvetica, Arial, sans-serif; background-color: #e0e0e0; margin: 0; padding: 20px; color: var(--text-color); display: flex; justify-content: center; }}
        .viewport {{ width: 100%; max-width: 1100px; background-color: #fff; box-shadow: 0 5px 20px rgba(0,0,0,0.15); min-height: 800px; display: flex; flex-direction: column; }}
        .header {{ background-color: var(--psu-blue); color: white; padding: 0 20px; height: 60px; display: flex; align-items: center; justify-content: space-between; }}
        .brand {{ display: flex; align-items: center; gap: 15px; }}
        .psu-logo {{ font-family: "Georgia", serif; font-size: 20px; font-weight: bold; letter-spacing: 1px; border-right: 1px solid rgba(255,255,255,0.3); padding-right: 15px; }}
        .system-name {{ font-size: 18px; font-weight: 300; }}
        .user-menu {{ font-size: 14px; display: flex; align-items: center; gap: 20px; }}
        .nav-bar {{ background-color: #f8f8f8; border-bottom: 1px solid #ddd; padding: 10px 20px; font-size: 13px; color: #666; display: flex; gap: 20px; }}
        .nav-item.active {{ color: var(--psu-blue); font-weight: bold; border-bottom: 2px solid var(--psu-blue); padding-bottom: 8px; }}
        .content {{ padding: 30px; flex: 1; }}
        .page-header {{ display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .page-title {{ font-size: 24px; color: var(--psu-blue); margin: 0; }}
        .term-selector {{ background: #fff; border: 1px solid #ccc; padding: 5px 10px; border-radius: 4px; font-size: 14px; color: #333; font-weight: bold; }}
        .student-card {{ background: #fcfcfc; border: 1px solid #e0e0e0; padding: 15px; margin-bottom: 25px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; font-size: 13px; }}
        .info-label {{ color: #777; font-size: 11px; text-transform: uppercase; margin-bottom: 4px; }}
        .info-val {{ font-weight: bold; color: #333; font-size: 14px; }}
        .status-badge {{ background-color: #e6fffa; color: #007a5e; padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #b2f5ea; }}
        .schedule-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        .schedule-table th {{ text-align: left; padding: 12px; background-color: #f0f0f0; border-bottom: 2px solid #ccc; color: #555; }}
        .schedule-table td {{ padding: 15px 12px; border-bottom: 1px solid #eee; }}
        .course-code {{ font-weight: bold; color: var(--psu-blue); }}
        .course-title {{ font-weight: 500; }}
    </style>
</head>
<body>
<div class="viewport">
    <div class="header">
        <div class="brand"><div class="psu-logo">PennState</div><div class="system-name">LionPATH</div></div>
        <div class="user-menu"><span>Welcome, <strong>{name}</strong></span><span>|</span><span>Sign Out</span></div>
    </div>
    <div class="nav-bar">
        <div class="nav-item">Student Home</div><div class="nav-item active">My Class Schedule</div>
        <div class="nav-item">Academics</div><div class="nav-item">Finances</div><div class="nav-item">Campus Life</div>
    </div>
    <div class="content">
        <div class="page-header">
            <h1 class="page-title">My Class Schedule</h1>
            <div class="term-selector">Term: <strong>{CURRENT_TERM}</strong> {TERM_DATES}</div>
        </div>
        <div class="student-card">
            <div><div class="info-label">Student Name</div><div class="info-val">{name}</div></div>
            <div><div class="info-label">PSU ID</div><div class="info-val">{psu_id}</div></div>
            <div><div class="info-label">Academic Program</div><div class="info-val">{major}</div></div>
            <div><div class="info-label">Enrollment Status</div><div class="status-badge">✅ Enrolled</div></div>
        </div>
        <div style="margin-bottom: 10px; font-size: 12px; color: #666; text-align: right;">Data retrieved: <span>{date_str}</span></div>
        <table class="schedule-table">
            <thead>
                <tr><th width="10%">Class Nbr</th><th width="15%">Course</th><th width="35%">Title</th><th width="20%">Days & Times</th><th width="10%">Room</th><th width="10%">Units</th></tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        <div style="margin-top: 50px; border-top: 1px solid #ddd; padding-top: 10px; font-size: 11px; color: #888; text-align: center;">
            &copy; {COPYRIGHT_YEAR} The Pennsylvania State University. All rights reserved.<br>LionPATH is the student information system for Penn State.
        </div>
    </div>
</div>
</body>
</html>
"""
    return html

def generate_image(first_name, last_name, school_id='2565'):
    try:
        from playwright.sync_api import sync_playwright
        html_content = generate_html(first_name, last_name, school_id)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1200, 'height': 900})
            page.set_content(html_content, wait_until='load')
            page.wait_for_timeout(500)
            screenshot_bytes = page.screenshot(type='png', full_page=True)
            browser.close()
        return screenshot_bytes
    except ImportError:
        raise Exception("需要安装 playwright")
    except Exception as e:
        raise Exception(f"生成图片失败: {str(e)}")

if __name__ == '__main__':
    # 本地测试代码
    import sys, io
    if sys.platform == 'win32': sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print("生成随机测试图片...")
    img = generate_image("Test", "User")
    with open("test_random_schedule.png", "wb") as f: f.write(img)
    print("生成完成: test_random_schedule.png")
from flask import Flask, render_template, request

app = Flask(_name_)

COLLEGES_DATA = [
    # ঢাকা বোর্ড
    {"name": "ঢাকা কলেজ (Dhaka College)", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "ঢাকা"},
    {"name": "ঢাকা কলেজ (Dhaka College)", "board": "dhaka", "group": "commerce", "min_gpa": 4.50, "location": "ঢাকা"},
    {"name": "ঢাকা কলেজ (Dhaka College)", "board": "dhaka", "group": "arts", "min_gpa": 4.00, "location": "ঢাকা"},
    {"name": "নটর ডেম কলেজ (Notre Dame College)", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "ঢাকা"},
    {"name": "ভিকারুন্নিসা নূন স্কুল অ্যান্ড কলেজ", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "ঢাকা"},
    {"name": "গভ. সাইন্স কলেজ (Govt. Science College)", "board": "dhaka", "group": "science", "min_gpa": 4.80, "location": "ঢাকা"},
    {"name": "রাজউক উত্তরা মডেল কলেজ", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "ঢাকা"},
    {"name": "রাজউক উত্তরা মডেল কলেজ", "board": "dhaka", "group": "commerce", "min_gpa": 4.75, "location": "ঢাকা"},
    {"name": "মোহাম্মদপুর সরকারি কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.50, "location": "ঢাকা"},
    {"name": "মোহাম্মদপুর সরকারি কলেজ", "board": "dhaka", "group": "arts", "min_gpa": 3.80, "location": "ঢাকা"},
    {"name": "লালমাটিয়া সরকারি মহিলা কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.25, "location": "ঢাকা"},
    {"name": "মিরপুর সরকারি কলেজ", "board": "dhaka", "group": "commerce", "min_gpa": 3.50, "location": "ঢাকা"},

    # রাজশাহী বোর্ড
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "board": "rajshahi", "group": "science", "min_gpa": 5.00, "location": "রাজশাহী"},
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "board": "rajshahi", "group": "commerce", "min_gpa": 4.50, "location": "রাজশাহী"},
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "board": "rajshahi", "group": "arts", "min_gpa": 4.00, "location": "রাজশাহী"},
    {"name": "নিউ গভ. ডিগ্রি কলেজ", "board": "rajshahi", "group": "science", "min_gpa": 4.80, "location": "রাজশাহী"},

    # চট্টগ্রাম বোর্ড
    {"name": "চট্টগ্রাম কলেজ (Chittagong College)", "board": "chittagong", "group": "science", "min_gpa": 5.00, "location": "চট্টগ্রাম"},
    {"name": "সরকারি হাজী মহসিন কলেজ", "board": "chittagong", "group": "science", "min_gpa": 4.75, "location": "চট্টগ্রাম"},

    # অন্যান্য বোর্ড
    {"name": "কুমিল্লা ভিক্টোরিয়া সরকারি কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.85, "location": "কুমিল্লা"},
    {"name": "সিলেট সরকারি কলেজ", "board": "sylhet", "group": "science", "min_gpa": 4.50, "location": "সিলেট"},
    {"name": "খুলনা সরকারি মজিদ মেমোরিয়াল সিটি কলেজ", "board": "khulna", "group": "science", "min_gpa": 4.75, "location": "খুলনা"},
    {"name": "সরকারি ব্রজমোহন (BM) কলেজ", "board": "barisal", "group": "science", "min_gpa": 4.60, "location": "বরিশাল"},
    {"name": "দিনাজপুর সরকারি কলেজ", "board": "dinajpur", "group": "science", "min_gpa": 4.50, "location": "দিনাজপুর"},
    {"name": "ময়মনসিংহ আনন্দ মোহন কলেজ", "board": "mymensingh", "group": "science", "min_gpa": 4.90, "location": "ময়মনসিংহ"}
]

@app.route('/', methods=['GET', 'POST'])
def home():
    high_chance = []
    medium_chance = []
    low_chance = []
    submitted = False
    student_info = {}

    if request.method == 'POST':
        submitted = True
        board = request.form.get('board')
        group = request.form.get('group')
        try:
            gpa = float(request.form.get('gpa', 0))
        except ValueError:
            gpa = 0.0

        student_info = {
            'board': board.upper(),
            'group': group.capitalize(),
            'gpa': gpa
        }

        for college in COLLEGES_DATA:
            if college['group'] == group and (college['board'] == board or board == 'all'):
                min_gpa = college['min_gpa']
                if gpa >= min_gpa + 0.1:
                    high_chance.append(college)
                elif gpa >= min_gpa:
                    medium_chance.append(college)
                elif gpa >= min_gpa - 0.5:
                    low_chance.append(college)

    return render_template(
        'index.html',
        submitted=submitted,
        student_info=student_info,
        high_chance=high_chance,
        medium_chance=medium_chance,
        low_chance=low_chance
    )

if _name_ == '_main_':
    app.run(debug=True)

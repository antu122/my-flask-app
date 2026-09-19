from flask import Flask, render_template, request

app = Flask(__name__)

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
    {"name": "লালমাটিয়া সরকারি মহিলা কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.25, "location": "ঢাকা"},
    {"name": "মিরপুর সরকারি কলেজ", "board": "dhaka", "group": "commerce", "min_gpa": 3.50, "location": "ঢাকা"},
    
    # রাজশাহী বোর্ড
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "board": "rajshahi", "group": "science", "min_gpa": 5.00, "location": "রাজশাহী"},
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "board": "rajshahi", "group": "commerce", "min_gpa": 4.50, "location": "রাজশাহী"},
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "board": "rajshahi", "group": "arts", "min_gpa": 4.00, "location": "রাজশাহী"},
    {"name": "নিউ গভ. ডিগ্রি কলেজ", "board": "rajshahi", "group": "science", "min_gpa": 4.80, "location": "রাজশাহী"}
]

@app.route('/', methods=['GET', 'POST'])
def home():
    matched_colleges = []
    user_gpa = None
    selected_board = None
    selected_group = None

    if request.method == 'POST':
        try:
            user_gpa = float(request.form.get('gpa', 0))
            selected_board = request.form.get('board')
            selected_group = request.form.get('group')

            for college in COLLEGES_DATA:
                if (college['board'] == selected_board and 
                    college['group'] == selected_group and 
                    user_gpa >= college['min_gpa']):
                    matched_colleges.append(college)
        except ValueError:
            pass

    return render_template('index.html', 
                           colleges=matched_colleges, 
                           gpa=user_gpa, 
                           board=selected_board, 
                           group=selected_group)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

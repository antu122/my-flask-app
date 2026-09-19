from flask import Flask, render_template, request

app = Flask(__name__)

# বাংলাদেশের প্রধান শিক্ষা বোর্ড ও কলেজের ডেটাবেজ
COLLEGES_DATA = [
    # ঢাকা বোর্ড
    {"name": "ঢাকা কলেজ (Dhaka College)", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "ঢাকা"},
    {"name": "ঢাকা কলেজ (Dhaka College)", "board": "dhaka", "group": "commerce", "min_gpa": 4.50, "location": "ঢাকা"},
    {"name": "নটর ডেম কলেজ (Notre Dame College)", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "ঢাকা"},
    {"name": "ভিকারুন্নিসা নূন স্কুল অ্যান্ড কলেজ", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "ঢাকা"},
    {"name": "গভ. সাইন্স কলেজ (Govt. Science College)", "board": "dhaka", "group": "science", "min_gpa": 4.80, "location": "ঢাকা"},
    {"name": "রাজউক উত্তরা মডেল কলেজ", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "ঢাকা"},
    {"name": "মোহাম্মদপুর সরকারি কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.50, "location": "ঢাকা"},
    {"name": "মোহাম্মদপুর সরকারি কলেজ", "board": "dhaka", "group": "arts", "min_gpa": 3.80, "location": "ঢাকা"},
    {"name": "লালমাটিয়া সরকারি মহিলা কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.25, "location": "ঢাকা"},
    {"name": "মিরপুর সরকারি কলেজ", "board": "dhaka", "group": "commerce", "min_gpa": 3.50, "location": "ঢাকা"},
    {"name": "তেজগাঁও সরকারি কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.00, "location": "ঢাকা"},

    # রাজশাহী বোর্ড
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "board": "rajshahi", "group": "science", "min_gpa": 5.00, "location": "রাজশাহী"},
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "board": "rajshahi", "group": "commerce", "min_gpa": 4.50, "location": "রাজশাহী"},
    {"name": "নিউ গভ. ডিগ্রি কলেজ", "board": "rajshahi", "group": "science", "min_gpa": 4.80, "location": "রাজশাহী"},
    {"name": "রাজশাহী সরকারি সিটি কলেজ", "board": "rajshahi", "group": "science", "min_gpa": 4.30, "location": "রাজশাহী"},

    # চট্টগ্রাম বোর্ড
    {"name": "চট্টগ্রাম কলেজ", "board": "chittagong", "group": "science", "min_gpa": 5.00, "location": "চট্টগ্রাম"},
    {"name": "সরকারি হাজি মুহাম্মদ মহসিন কলেজ", "board": "chittagong", "group": "science", "min_gpa": 4.80, "location": "চট্টগ্রাম"},

    # কুমিল্লা বোর্ড
    {"name": "কুমিল্লা ভিক্টোরিয়া সরকারি কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.75, "location": "কুমিল্লা"}
]

@app.route('/', methods=['GET', 'POST'])
def home():
    high_chance = []
    medium_chance = []
    low_chance = []
    
    user_gpa = None
    selected_board = None
    selected_group = None

    if request.method == 'POST':
        try:
            user_gpa = float(request.form.get('gpa', 0))
            selected_board = request.form.get('board')
            selected_group = request.form.get('group')

            for college in COLLEGES_DATA:
                # বোর্ড ও গ্রুপ ফিল্টার
                if college['board'] == selected_board and college['group'] == selected_group:
                    min_gpa = college['min_gpa']
                    diff = user_gpa - min_gpa

                    # চান্স পাওয়ার সম্ভাবনা হিসাব
                    if diff >= 0.25:
                        high_chance.append(college)  # চান্স অনেক বেশি
                    elif 0.0 <= diff < 0.25:
                        medium_chance.append(college) # চান্স মাঝারি
                    elif -0.30 <= diff < 0.0:
                        low_chance.append(college)    # চান্স কিছুটা কম/ঝুঁকিপূর্ণ
        except ValueError:
            pass

    return render_template('index.html', 
                           high_chance=high_chance,
                           medium_chance=medium_chance,
                           low_chance=low_chance,
                           gpa=user_gpa, 
                           board=selected_board, 
                           group=selected_group)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

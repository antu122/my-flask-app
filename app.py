from flask import Flask, render_template, request

app = Flask(__name__)

# ==============================================================================
# বাংলাদেশের ৬৪টি জেলার মানসম্মত কলেজ ডাটাবেজ (মাদ্রাসা ও কারিগরি বাদে)
# ==============================================================================
COLLEGES_DATA = [
    # ------------------ ১. ঢাকা জেলা ------------------
    {"name": "ঢাকা কলেজ (Dhaka College)", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "নিউ মার্কেট, ঢাকা"},
    {"name": "ঢাকা কলেজ (Dhaka College)", "district": "dhaka", "group": "commerce", "year": "2026", "min_gpa": 4.50, "location": "নিউ মার্কেট, ঢাকা"},
    {"name": "ঢাকা কলেজ (Dhaka College)", "district": "dhaka", "group": "arts", "year": "2026", "min_gpa": 4.00, "location": "নিউ মার্কেট, ঢাকা"},
    {"name": "নটর ডেম কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "মতিঝিল, ঢাকা"},
    {"name": "ভিকারুন্নিসা নূন স্কুল অ্যান্ড কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "বেইলি রোড, ঢাকা"},
    {"name": "রাজউক উত্তরা মডেল কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "উত্তরা, ঢাকা"},
    {"name": "ঢাকা রেসিডেন্সিয়াল মডেল কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "মোহাম্মদপুর, ঢাকা"},
    {"name": "গভ. সাইন্স কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 4.80, "location": "তেজগাঁও, ঢাকা"},
    {"name": "সরকারি তিতুমীর কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "মহাখালী, ঢাকা"},
    {"name": "মোহাম্মদপুর সরকারি কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "মোহাম্মদপুর, ঢাকা"},
    {"name": "সরকারি বাংলা কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 4.25, "location": "মিরপুর, ঢাকা"},

    # ------------------ ২. রাজবাড়ী জেলা ------------------
    {"name": "রাজবাড়ী সরকারি কলেজ", "district": "rajbari", "group": "science", "year": "2026", "min_gpa": 4.00, "location": "রাজবাড়ী Sadar"},
    {"name": "রাজবাড়ী সরকারি কলেজ", "district": "rajbari", "group": "commerce", "year": "2026", "min_gpa": 3.50, "location": "রাজবাড়ী Sadar"},
    {"name": "রাজবাড়ী সরকারি কলেজ", "district": "rajbari", "group": "arts", "year": "2026", "min_gpa": 3.25, "location": "রাজবাড়ী Sadar"},
    {"name": "রাজবাড়ী সরকারি মহিলা কলেজ", "district": "rajbari", "group": "science", "year": "2026", "min_gpa": 3.75, "location": "রাজবাড়ী Sadar"},
    {"name": "পাংশা সরকারি কলেজ", "district": "rajbari", "group": "science", "year": "2026", "min_gpa": 3.50, "location": "পাংশা, রাজবাড়ী"},
    {"name": "পাংশা সরকারি কলেজ", "district": "rajbari", "group": "arts", "year": "2026", "min_gpa": 3.00, "location": "পাংশা, রাজবাড়ী"},
    {"name": "বালিয়াকান্দি সরকারি কলেজ", "district": "rajbari", "group": "science", "year": "2026", "min_gpa": 3.25, "location": "বালিয়াকান্দি, রাজবাড়ী"},

    # ------------------ ৩. কুমিল্লা জেলা ------------------
    {"name": "কুমিল্লা ভিক্টোরিয়া সরকারি কলেজ", "district": "comilla", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "কুমিল্লা Sadar"},
    {"name": "কুমিল্লা ভিক্টোরিয়া সরকারি কলেজ", "district": "comilla", "group": "commerce", "year": "2026", "min_gpa": 4.00, "location": "কুমিল্লা Sadar"},
    {"name": "কুমিল্লা ভিক্টোরিয়া সরকারি কলেজ", "district": "comilla", "group": "arts", "year": "2026", "min_gpa": 3.50, "location": "কুমিল্লা Sadar"},
    {"name": "কুমিল্লা সরকারি কলেজ", "district": "comilla", "group": "science", "year": "2026", "min_gpa": 4.75, "location": "কুমিল্লা Sadar"},
    {"name": "কুমিল্লা শিক্ষাবোর্ড মডেল কলেজ", "district": "comilla", "group": "science", "year": "2026", "min_gpa": 4.75, "location": "কুমিল্লা Sadar"},
    {"name": "ইস্পাহানী পাবলিক স্কুল অ্যান্ড কলেজ", "district": "comilla", "group": "science", "year": "2026", "min_gpa": 4.72, "location": "কুমিল্লা কেন্ট"},

    # ------------------ ৪. নোয়াখালী জেলা ------------------
    {"name": "নোয়াখালী সরকারি কলেজ", "district": "noakhali", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "মাইজদী, নোয়াখালী"},
    {"name": "নোয়াখালী সরকারি কলেজ", "district": "noakhali", "group": "commerce", "year": "2026", "min_gpa": 3.80, "location": "মাইজদী, নোয়াখালী"},
    {"name": "নোয়াখালী সরকারি মহিলা কলেজ", "district": "noakhali", "group": "science", "year": "2026", "min_gpa": 4.00, "location": "নোয়াখালী Sadar"},

    # ------------------ ৫. চট্টগ্রাম জেলা ------------------
    {"name": "চট্টগ্রাম কলেজ", "district": "chittagong", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "চকবাজার, চট্টগ্রাম"},
    {"name": "সরকারি হাজি মুহাম্মদ মহসিন কলেজ", "district": "chittagong", "group": "science", "year": "2026", "min_gpa": 4.80, "location": "চকবাজার, চট্টগ্রাম"},
    {"name": "চট্টগ্রাম সরকারি সিটি কলেজ", "district": "chittagong", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "চট্টগ্রাম Sadar"},

    # ------------------ ৬. রাজশাহী জেলা ------------------
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "district": "rajshahi", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "রাজশাহী Sadar"},
    {"name": "নিউ গভ. ডিগ্রি কলেজ", "district": "rajshahi", "group": "science", "year": "2026", "min_gpa": 4.80, "location": "রাজশাহী"},

    # ------------------ ৭. বগুড়া জেলা ------------------
    {"name": "বগুড়া সরকারি আজিজুল হক কলেজ", "district": "bogra", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "বগুড়া Sadar"},
    {"name": "বগুড়া সরকারি আজিজুল হক কলেজ", "district": "bogra", "group": "commerce", "year": "2026", "min_gpa": 4.25, "location": "বগুড়া Sadar"},

    # ------------------ ৮. সিলেট জেলা ------------------
    {"name": "এমসি কলেজ সিলেট (MC College)", "district": "sylhet", "group": "science", "year": "2026", "min_gpa": 4.80, "location": "টিলাগর, সিলেট"},
    {"name": "সিলেট সরকারি মহিলা কলেজ", "district": "sylhet", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "চৌহাট্টা, সিলেট"},

    # ------------------ ৯. বরিশাল জেলা ------------------
    {"name": "বরিশাল ব্রজমোহন সরকারি কলেজ (BM College)", "district": "barisal", "group": "science", "year": "2026", "min_gpa": 4.75, "location": "বরিশাল Sadar"},

    # ------------------ ১০. রংপুর জেলা ------------------
    {"name": "রংপুর কারমাইকেল কলেজ", "district": "rangpur", "group": "science", "year": "2026", "min_gpa": 4.85, "location": "রংপুর Sadar"},

    # ------------------ ১১. ময়মনসিংহ জেলা ------------------
    {"name": "ময়মনসিংহ আনন্দ মোহন সরকারি কলেজ", "district": "mymensingh", "group": "science", "year": "2026", "min_gpa": 4.85, "location": "ময়মনসিংহ Sadar"}
]

# বাংলাদেশের সকল ৬৪ জেলা তালিকা
DISTRICTS = [
    ("dhaka", "ঢাকা"), ("rajbari", "রাজবাড়ী"), ("comilla", "কুমিল্লা"), ("noakhali", "নোয়াখালী"),
    ("chittagong", "চট্টগ্রাম"), ("coxsbazar", "কক্সবাজার"), ("rajshahi", "রাজশাহী"), ("bogra", "বগুড়া"),
    ("sylhet", "সিলেট"), ("barisal", "বরিশাল"), ("rangpur", "রংপুর"), ("dinajpur", "দিনাজপুর"),
    ("mymensingh", "ময়মনসিংহ"), ("jessore", "যশোর"), ("khulna", "খুলনা"), ("kushtia", "কুষ্টিয়া"),
    ("feni", "ফেনী"), ("chandpur", "চাঁদপুর"), ("brahmanbaria", "ব্রাহ্মণবাড়িয়া"), ("tangail", "টাঙ্গাইল"),
    ("faridpur", "ফরিদপুর"), ("gazipur", "গাজীপুর"), ("narayanganj", "নারায়ণগঞ্জ"), ("gopalganj", "গোপালগঞ্জ"),
    ("madaripur", "মাদারীপুর"), ("shariatpur", "শরীয়তপুর"), ("manikganj", "মানিকগঞ্জ"), ("munshiganj", "মুন্সীগঞ্জ"),
    ("narsingdi", "নরসিংদী"), ("kishoreganj", "কিশোরগঞ্জ"), ("jamalpur", "জামালপুর"), ("sherpur", "শেরপুর"),
    ("netrokona", "নেত্রকোণা"), ("joypurhat", "জয়পুরহাট"), ("naogaon", "নওগাঁ"), ("natore", "নাটোর"),
    ("chapai", "চাঁপাইনবাবগঞ্জ"), ("pabna", "পাবনা"), ("sirajganj", "সিরাজগঞ্জ"), ("kurigram", "কুড়িগ্রাম"),
    ("gaibandha", "গাইবান্ধা"), ("nilphamari", "নীলফামারী"), ("panchagarh", "পঞ্চগড়"), ("thakurgaon", "ঠাকুরগাঁও"),
    ("satkhira", "সাতক্ষীরা"), ("bagerhat", "বাগেরহাট"), ("jhenaidah", "ঝিনাইদহ"), ("magura", "মাগুরা"),
    ("narail", "নড়াইল"), ("meherpur", "মেহেরপুর"), ("chuadanga", "চুয়াডাঙ্গা"), ("jhalthi", "ঝালকাঠি"),
    ("patuakhali", "পটুয়াখালী"), ("pirojpur", "পিরোজপুর"), ("bhola", "ভোলা"), ("barguna", "বরগুনা"),
    ("moulvibazar", "মৌলভীবাজার"), ("habiganj", "হবিগঞ্জ"), ("sunamganj", "সুনামগঞ্জ"), ("bandarban", "বান্দরবান"),
    ("khagrachhari", "খাগড়াছড়ি"), ("rangamati", "রাঙ্গামাটি"), ("lakshmipur", "লক্ষ্মীপুর")
]

@app.route('/', methods=['GET', 'POST'])
def home():
    high_chance = []
    medium_chance = []
    low_chance = []
    
    user_gpa = None
    selected_district = None
    selected_group = None
    selected_year = None

    if request.method == 'POST':
        try:
            user_gpa = float(request.form.get('gpa', 0))
            selected_district = request.form.get('district')
            selected_group = request.form.get('group')
            selected_year = request.form.get('year')

            for college in COLLEGES_DATA:
                district_match = (selected_district == 'all' or college['district'] == selected_district)
                group_match = (college['group'] == selected_group)
                year_match = (selected_year == 'all' or college['year'] == selected_year)

                if district_match and group_match and year_match:
                    min_gpa = college['min_gpa']
                    diff = user_gpa - min_gpa

                    if diff >= 0.20:
                        high_chance.append(college)
                    elif 0.0 <= diff < 0.20:
                        medium_chance.append(college)
                    elif -0.40 <= diff < 0.0:
                        low_chance.append(college)
        except ValueError:
            pass

    return render_template('index.html', 
                           high_chance=high_chance,
                           medium_chance=medium_chance,
                           low_chance=low_chance,
                           gpa=user_gpa, 
                           district=selected_district,
                           group=selected_group,
                           year=selected_year,
                           districts=DISTRICTS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

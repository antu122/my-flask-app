from flask import Flask, render_template, request

app = Flask(__name__)

# ==============================================================================
# বাংলাদেশের ৬৪ জেলার বিস্তৃত ও মানসম্মত কলেজের ডাটাবেজ (সাধারণ ও উচ্চমাধ্যমিক)
# ==============================================================================
COLLEGES_DATA = [
    # ------------------ ১. ঢাকা ------------------
    {"name": "ঢাকা কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "নিউ মার্কেট, ঢাকা"},
    {"name": "ঢাকা কলেজ", "district": "dhaka", "group": "commerce", "year": "2026", "min_gpa": 4.50, "location": "নিউ মার্কেট, ঢাকা"},
    {"name": "ঢাকা কলেজ", "district": "dhaka", "group": "arts", "year": "2026", "min_gpa": 4.00, "location": "নিউ মার্কেট, ঢাকা"},
    {"name": "নটর ডেম কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "মতিঝিল, ঢাকা"},
    {"name": "নটর ডেম কলেজ", "district": "dhaka", "group": "commerce", "year": "2026", "min_gpa": 4.50, "location": "মতিঝিল, ঢাকা"},
    {"name": "ভিকারুন্নিসা নূন স্কুল অ্যান্ড কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "বেইলি রোড, ঢাকা"},
    {"name": "রাজউক উত্তরা মডেল কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "উত্তরা, ঢাকা"},
    {"name": "ঢাকা রেসিডেন্সিয়াল মডেল কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "মোহাম্মদপুর, ঢাকা"},
    {"name": "গভ. সাইন্স কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 4.80, "location": "তেজগাঁও, ঢাকা"},
    {"name": "সরকারি তিতুমীর কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "মহাখালী, ঢাকা"},
    {"name": "সরকারি তিতুমীর কলেজ", "district": "dhaka", "group": "commerce", "year": "2026", "min_gpa": 4.00, "location": "মহাখালী, ঢাকা"},
    {"name": "মোহাম্মদপুর সরকারি কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "মোহাম্মদপুর, ঢাকা"},
    {"name": "সরকারি বাংলা কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 4.25, "location": "মিরপুর, ঢাকা"},
    {"name": "সরকারি শহীদ সোহরাওয়ার্দী কলেজ", "district": "dhaka", "group": "science", "year": "2026", "min_gpa": 4.30, "location": "লক্ষ্মীবাজার, ঢাকা"},

    # ------------------ ২. রাজবাড়ী ------------------
    {"name": "রাজবাড়ী সরকারি কলেজ", "district": "rajbari", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "রাজবাড়ী সদর"},
    {"name": "রাজবাড়ী সরকারি কলেজ", "district": "rajbari", "group": "commerce", "year": "2026", "min_gpa": 3.80, "location": "রাজবাড়ী সদর"},
    {"name": "রাজবাড়ী সরকারি কলেজ", "district": "rajbari", "group": "arts", "year": "2026", "min_gpa": 3.50, "location": "রাজবাড়ী সদর"},
    {"name": "রাজবাড়ী সরকারি মহিলা কলেজ", "district": "rajbari", "group": "science", "year": "2026", "min_gpa": 4.00, "location": "রাজবাড়ী সদর"},
    {"name": "রাজবাড়ী সরকারি মহিলা কলেজ", "district": "rajbari", "group": "arts", "year": "2026", "min_gpa": 3.25, "location": "রাজবাড়ী সদর"},
    {"name": "পাংশা সরকারি কলেজ", "district": "rajbari", "group": "science", "year": "2026", "min_gpa": 3.75, "location": "পাংশা, রাজবাড়ী"},
    {"name": "পাংশা সরকারি কলেজ", "district": "rajbari", "group": "commerce", "year": "2026", "min_gpa": 3.25, "location": "পাংশা, রাজবাড়ী"},
    {"name": "পাংশা সরকারি কলেজ", "district": "rajbari", "group": "arts", "year": "2026", "min_gpa": 3.00, "location": "পাংশা, রাজবাড়ী"},
    {"name": "বালিয়াকান্দি সরকারি কলেজ", "district": "rajbari", "group": "science", "year": "2026", "min_gpa": 3.50, "location": "বালিয়াকান্দি, রাজবাড়ী"},
    {"name": "কালুখালী সরকারি কলেজ", "district": "rajbari", "group": "science", "year": "2026", "min_gpa": 3.25, "location": "কালুখালী, রাজবাড়ী"},
    {"name": "গোয়ালন্দ কামরুল ইসলাম সরকারি কলেজ", "district": "rajbari", "group": "science", "year": "2026", "min_gpa": 3.50, "location": "গোয়ালন্দ, রাজবাড়ী"},

    # ------------------ ৩. চট্টগ্রাম ------------------
    {"name": "চট্টগ্রাম কলেজ", "district": "chattogram", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "চকবাজার, চট্টগ্রাম"},
    {"name": "সরকারি হাজি মুহাম্মদ মহসিন কলেজ", "district": "chattogram", "group": "science", "year": "2026", "min_gpa": 4.85, "location": "চকবাজার, চট্টগ্রাম"},
    {"name": "চট্টগ্রাম সরকারি সিটি কলেজ", "district": "chattogram", "group": "science", "year": "2026", "min_gpa": 4.60, "location": "আইস ফ্যাক্টরি রোড, চট্টগ্রাম"},
    {"name": "চট্টগ্রাম সরকারি মহিলা কলেজ", "district": "chattogram", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "খুলশী, চট্টগ্রাম"},

    # ------------------ ৪. কুমিল্লা ------------------
    {"name": "কুমিল্লা ভিক্টোরিয়া সরকারি কলেজ", "district": "comilla", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "কুমিল্লা সদর"},
    {"name": "কুমিল্লা ভিক্টোরিয়া সরকারি কলেজ", "district": "comilla", "group": "commerce", "year": "2026", "min_gpa": 4.25, "location": "কুমিল্লা সদর"},
    {"name": "কুমিল্লা সরকারি কলেজ", "district": "comilla", "group": "science", "year": "2026", "min_gpa": 4.65, "location": "কুমিল্লা সদর"},
    {"name": "কুমিল্লা শিক্ষাবোর্ড মডেল কলেজ", "district": "comilla", "group": "science", "year": "2026", "min_gpa": 4.70, "location": "কুমিল্লা সদর"},
    {"name": "ইস্পাহানী পাবলিক স্কুল অ্যান্ড কলেজ", "district": "comilla", "group": "science", "year": "2026", "min_gpa": 4.75, "location": "কুমিল্লা সেনানিবাস"},

    # ------------------ ৫. রাজশাহী ------------------
    {"name": "রাজশাহী কলেজ", "district": "rajshahi", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "রাজশাহী সদর"},
    {"name": "নিউ গভ. ডিগ্রি কলেজ", "district": "rajshahi", "group": "science", "year": "2026", "min_gpa": 4.80, "location": "রাজশাহী"},
    {"name": "রাজশাহী সরকারি মহিলা কলেজ", "district": "rajshahi", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "রাজশাহী"},

    # ------------------ ৬. বগুড়া ------------------
    {"name": "বগুড়া সরকারি আজিজুল হক কলেজ", "district": "bogra", "group": "science", "year": "2026", "min_gpa": 5.00, "location": "বগুড়া সদর"},
    {"name": "বগুড়া সরকারি আজিজুল হক কলেজ", "district": "bogra", "group": "commerce", "year": "2026", "min_gpa": 4.30, "location": "বগুড়া সদর"},
    {"name": "বগুড়া সরকারি শাহসুলতান কলেজ", "district": "bogra", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "বগুড়া"},
    {"name": "বগুড়া সরকারি মহিলা কলেজ", "district": "bogra", "group": "science", "year": "2026", "min_gpa": 4.40, "location": "বগুড়া"},

    # ------------------ ৭. সিলেট ------------------
    {"name": "এমসি কলেজ (MC College)", "district": "sylhet", "group": "science", "year": "2026", "min_gpa": 4.80, "location": "টিলাগর, সিলেট"},
    {"name": "সিলেট সরকারি মহিলা কলেজ", "district": "sylhet", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "চৌহাট্টা, সিলেট"},

    # ------------------ ৮. বরিশাল ------------------
    {"name": "বরিশাল ব্রজমোহন সরকারি কলেজ (BM College)", "district": "barisal", "group": "science", "year": "2026", "min_gpa": 4.75, "location": "বরিশাল সদর"},
    {"name": "বরিশাল সরকারি মহিলা কলেজ", "district": "barisal", "group": "science", "year": "2026", "min_gpa": 4.25, "location": "বরিশাল"},

    # ------------------ ৯. রংপুর ------------------
    {"name": "কারমাইকেল কলেজ, রংপুর", "district": "rangpur", "group": "science", "year": "2026", "min_gpa": 4.85, "location": "রংপুর সদর"},
    {"name": "রংপুর সরকারি কলেজ", "district": "rangpur", "group": "science", "year": "2026", "min_gpa": 4.50, "location": "রংপুর"},

    # ------------------ ১০. ময়মনসিংহ ------------------
    {"name": "আনন্দ মোহন সরকারি কলেজ", "district": "mymensingh", "group": "science", "year": "2026", "min_gpa": 4.85, "location": "ময়মনসিংহ সদর"},
    {"name": "ময়মনসিংহ সরকারি কলেজ", "district": "mymensingh", "group": "science", "year": "2026", "min_gpa": 4.40, "location": "ময়মনসিংহ"},

    # ------------------ ১১. ফরিদপুর ------------------
    {"name": "সরকারি রাজেন্দ্র কলেজ", "district": "faridpur", "group": "science", "year": "2026", "min_gpa": 4.60, "location": "ফরিদপুর সদর"},
    {"name": "সরকারি রাজেন্দ্র কলেজ", "district": "faridpur", "group": "commerce", "year": "2026", "min_gpa": 4.00, "location": "ফরিদপুর সদর"},
    {"name": "সরকারি সারদা সুন্দরী মহিলা কলেজ", "district": "faridpur", "group": "science", "year": "2026", "min_gpa": 4.20, "location": "ফরিদপুর"},

    # ------------------ ১২. পাবনা ------------------
    {"name": "সরকারি এডওয়ার্ড কলেজ", "district": "pabna", "group": "science", "year": "2026", "min_gpa": 4.75, "location": "পাবনা সদর"},
    {"name": "পাবনা সরকারি মহিলা কলেজ", "district": "pabna", "group": "science", "year": "2026", "min_gpa": 4.30, "location": "পাবনা"},

    # ------------------ ১৩. যশোর ------------------
    {"name": "যশোর সরকারি এম. এম. কলেজ", "district": "jessore", "group": "science", "year": "2026", "min_gpa": 4.75, "location": "যশোর সদর"},
    {"name": "যশোর সরকারি মহিলা কলেজ", "district": "jessore", "group": "science", "year": "2026", "min_gpa": 4.30, "location": "যশোর"}
]

# ==============================================================================
# বাংলা বর্ণানুক্রমিক ৬৪ জেলার তালিকা (ক, খ, গ, ঘ... পর্যায়ক্রমে)
# ==============================================================================
DISTRICTS = [
    ("coxsbazar", "কক্সবাজার"), ("kishoreganj", "কিশোরগঞ্জ"), ("kurigram", "কুড়িগ্রাম"),
    ("kushtia", "কুষ্টিয়া"), ("comilla", "কুমিল্লা"), ("khagrachhari", "খাগড়াছড়ি"),
    ("khulna", "খুলনা"), ("gaibandha", "গাইবান্ধা"), ("gazipur", "গাজীপুর"),
    ("gopalganj", "গোপালগঞ্জ"), ("chattogram", "চট্টগ্রাম"), ("chandpur", "চাঁদপুর"),
    ("chapai", "চাঁপাইনবাবগঞ্জ"), ("chuadanga", "চুয়াডাঙ্গা"), ("jamalpur", "জামালপুর"),
    ("jhenaidah", "ঝিনাইদহ"), ("jhalthi", "ঝালকাঠি"), ("tangail", "টাঙ্গাইল"),
    ("thakurgaon", "ঠাকুরগাঁও"), ("dhaka", "ঢাকা"), ("dinajpur", "দিনাজপুর"),
    ("naogaon", "নওগাঁ"), ("narail", "নড়াইল"), ("narsingdi", "নরসিংদী"),
    ("natore", "নাটোর"), ("narayanganj", "নারায়ণগঞ্জ"), ("nilphamari", "নীলফামারী"),
    ("netrokona", "নেত্রকোণা"), ("noakhali", "নোয়াখালী"), ("pabna", "পাবনা"),
    ("panchagarh", "পঞ্চগড়"), ("patuakhali", "পটুয়াখালী"), ("pirojpur", "পিরোজপুর"),
    ("feni", "ফেনী"), ("faridpur", "ফরিদপুর"), ("bagerhat", "বাগেরহাট"),
    ("bandarban", "বান্দরবান"), ("barguna", "বরগুনা"), ("barisal", "বরিশাল"),
    ("bogra", "বগুড়া"), ("brahmanbaria", "ব্রাহ্মণবাড়িয়া"), ("bhola", "ভোলা"),
    ("manikganj", "মানিকগঞ্জ"), ("madaripur", "মাদারীপুর"), ("magura", "মাগুরা"),
    ("munshiganj", "মুন্সীগঞ্জ"), ("meherpur", "মেহেরপুর"), ("moulvibazar", "মৌলভীবাজার"),
    ("mymensingh", "ময়মনসিংহ"), ("jessore", "যশোর"), ("rangamati", "রাঙ্গামাটি"),
    ("rajbari", "রাজবাড়ী"), ("rajshahi", "রাজশাহী"), ("rangpur", "রংপুর"),
    ("lakshmipur", "লক্ষ্মীপুর"), ("shariatpur", "শরীয়তপুর"), ("sherpur", "শেরপুর"),
    ("satkhira", "সাতক্ষীরা"), ("sirajganj", "সিরাজগঞ্জ"), ("sylhet", "সিলেট"),
    ("sunamganj", "সুনামগঞ্জ"), ("habiganj", "হবিগঞ্জ")
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

                    # সুন্দর ক্যাটাগরি ও চান্স পাওয়ার সম্ভাবনা
                    if diff >= 0.25:
                        high_chance.append(college)
                    elif 0.0 <= diff < 0.25:
                        medium_chance.append(college)
                    elif -0.50 <= diff < 0.0:
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

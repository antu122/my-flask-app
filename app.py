from flask import Flask, render_template, request

app = Flask(__name__)

# ==============================================================================
# বাংলাদেশের সকল শিক্ষা বোর্ডের মানসম্মত (১ম, ২য় ও ৩য় সারির) সরকারি ও নামকরা বেসরকারি কলেজ ডাটাবেজ
# (ফালতু ও মানহীন কলেজ সম্পূর্ণ বাদ দেওয়া হয়েছে)
# ==============================================================================
COLLEGES_DATA = [
    # ------------------ ১. ঢাকা বোর্ড (Dhaka Board) ------------------
    {"name": "ঢাকা কলেজ (Dhaka College)", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "নিউ মার্কেট, ঢাকা"},
    {"name": "ঢাকা কলেজ (Dhaka College)", "board": "dhaka", "group": "commerce", "min_gpa": 4.50, "location": "নিউ মার্কেট, ঢাকা"},
    {"name": "ঢাকা কলেজ (Dhaka College)", "board": "dhaka", "group": "arts", "min_gpa": 4.00, "location": "নিউ মার্কেট, ঢাকা"},
    
    {"name": "নটর ডেম কলেজ (Notre Dame College)", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "মতিঝিল, ঢাকা"},
    {"name": "নটর ডেম কলেজ (Notre Dame College)", "board": "dhaka", "group": "commerce", "min_gpa": 4.50, "location": "মতিঝিল, ঢাকা"},
    {"name": "নটর ডেম কলেজ (Notre Dame College)", "board": "dhaka", "group": "arts", "min_gpa": 4.00, "location": "মতিঝিল, ঢাকা"},

    {"name": "ভিকারুন্নিসা নূন স্কুল অ্যান্ড কলেজ", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "বেইলি রোড, ঢাকা"},
    {"name": "ভিকারুন্নিসা নূন স্কুল অ্যান্ড কলেজ", "board": "dhaka", "group": "commerce", "min_gpa": 4.75, "location": "বেইলি রোড, ঢাকা"},
    {"name": "ভিকারুন্নিসা নূন স্কুল অ্যান্ড কলেজ", "board": "dhaka", "group": "arts", "min_gpa": 4.25, "location": "বেইলি রোড, ঢাকা"},

    {"name": "রাজউক উত্তরা মডেল কলেজ", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "উত্তরা, ঢাকা"},
    {"name": "রাজউক উত্তরা মডেল কলেজ", "board": "dhaka", "group": "commerce", "min_gpa": 4.75, "location": "উত্তরা, ঢাকা"},

    {"name": "ঢাকা রেসিডেন্সিয়াল মডেল কলেজ", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "মোহাম্মদপুর, ঢাকা"},
    {"name": "আদমজী ক্যান্টনমেন্ট কলেজ", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "ঢাকা কেন্ট, ঢাকা"},
    {"name": "গভ. সাইন্স কলেজ (Govt. Science College)", "board": "dhaka", "group": "science", "min_gpa": 4.80, "location": "তেজগাঁও, ঢাকা"},
    {"name": "বিএএফ শাহীন কলেজ ঢাকা", "board": "dhaka", "group": "science", "min_gpa": 4.75, "location": "তেজগাঁও, ঢাকা"},
    {"name": "ঢাকা সিটি কলেজ", "board": "dhaka", "group": "science", "min_gpa": 5.00, "location": "ধানমন্ডি, ঢাকা"},
    
    {"name": "সরকারি তিতুমীর কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.50, "location": "মহাখালী, ঢাকা"},
    {"name": "সরকারি তিতুমীর কলেজ", "board": "dhaka", "group": "commerce", "min_gpa": 4.25, "location": "মহাখালী, ঢাকা"},
    {"name": "সরকারি তিতুমীর কলেজ", "board": "dhaka", "group": "arts", "min_gpa": 3.75, "location": "মহাখালী, ঢাকা"},

    {"name": "মোহাম্মদপুর সরকারি কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.50, "location": "মোহাম্মদপুর, ঢাকা"},
    {"name": "মোহাম্মদপুর সরকারি কলেজ", "board": "dhaka", "group": "commerce", "min_gpa": 4.00, "location": "মোহাম্মদপুর, ঢাকা"},
    {"name": "মোহাম্মদপুর সরকারি কলেজ", "board": "dhaka", "group": "arts", "min_gpa": 3.80, "location": "মোহাম্মদপুর, ঢাকা"},

    {"name": "সরকারি বাংলা কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.25, "location": "মিরপুর, ঢাকা"},
    {"name": "কবি নজরুল সরকারি কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.30, "location": "লক্ষ্মীবাজার, ঢাকা"},
    {"name": "তেজগাঁও সরকারি কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.00, "location": "ফার্মগেট, ঢাকা"},
    {"name": "মিরপুর সরকারি কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.00, "location": "মিরপুর, ঢাকা"},
    {"name": "লালমাটিয়া সরকারি মহিলা কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.25, "location": "লালমাটিয়া, ঢাকা"},
    {"name": "ইডেন মহিলা কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.60, "location": "আজিমপুর, ঢাকা"},

    # রাজবাড়ী ও আশেপাশের জেলা
    {"name": "রাজবাড়ী সরকারি কলেজ", "board": "dhaka", "group": "science", "min_gpa": 4.00, "location": "রাজবাড়ী Sadar"},
    {"name": "রাজবাড়ী সরকারি কলেজ", "board": "dhaka", "group": "commerce", "min_gpa": 3.50, "location": "রাজবাড়ী Sadar"},
    {"name": "রাজবাড়ী সরকারি কলেজ", "board": "dhaka", "group": "arts", "min_gpa": 3.25, "location": "রাজবাড়ী Sadar"},
    {"name": "রাজবাড়ী সরকারি মহিলা কলেজ", "board": "dhaka", "group": "science", "min_gpa": 3.75, "location": "রাজবাড়ী Sadar"},
    {"name": "পাংশা সরকারি কলেজ", "board": "dhaka", "group": "science", "min_gpa": 3.50, "location": "পাংশা, রাজবাড়ী"},
    {"name": "পাংশা সরকারি কলেজ", "board": "dhaka", "group": "arts", "min_gpa": 3.00, "location": "পাংশা, রাজবাড়ী"},
    {"name": "বালিয়াকান্দি সরকারি কলেজ", "board": "dhaka", "group": "science", "min_gpa": 3.25, "location": "বালিয়াকান্দি, রাজবাড়ী"},

    # ------------------ ২. কুমিল্লা বোর্ড (Comilla Board) ------------------
    {"name": "কুমিল্লা ভিক্টোরিয়া সরকারি কলেজ", "board": "comilla", "group": "science", "min_gpa": 5.00, "location": "কুমিল্লা Sadar"},
    {"name": "কুমিল্লা ভিক্টোরিয়া সরকারি কলেজ", "board": "comilla", "group": "commerce", "min_gpa": 4.00, "location": "কুমিল্লা Sadar"},
    {"name": "কুমিল্লা ভিক্টোরিয়া সরকারি কলেজ", "board": "comilla", "group": "arts", "min_gpa": 3.50, "location": "কুমিল্লা Sadar"},
    {"name": "কুমিল্লা ক্যাডেট কলেজ", "board": "comilla", "group": "science", "min_gpa": 5.00, "location": "কুমিল্লা"},
    {"name": "কুমিল্লা সরকারি কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.75, "location": "কুমিল্লা Sadar"},
    {"name": "কুমিল্লা শিক্ষাবোর্ড মডেল কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.75, "location": "কুমিল্লা Sadar"},
    {"name": "ইস্পাহানী পাবলিক স্কুল অ্যান্ড কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.72, "location": "কুমিল্লা কেন্ট"},
    {"name": "কুমিল্লা সরকারি মহিলা কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.50, "location": "কুমিল্লা Sadar"},
    {"name": "ইবনে তাইমিয়া স্কুল অ্যান্ড কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.50, "location": "কুমিল্লা Sadar"},
    {"name": "ক্যান্টনমেন্ট কলেজ কুমিল্লা", "board": "comilla", "group": "science", "min_gpa": 4.50, "location": "কুমিল্লা কেন্ট"},
    {"name": "নোয়াখালী সরকারি কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.50, "location": "নোয়াখালী Sadar"},
    {"name": "নোয়াখালী সরকারি কলেজ", "board": "comilla", "group": "commerce", "min_gpa": 3.80, "location": "নোয়াখালী Sadar"},
    {"name": "নোয়াখালী সরকারি মহিলা কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.00, "location": "নোয়াখালী Sadar"},
    {"name": "ফেনী সরকারি কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.50, "location": "ফেনী Sadar"},
    {"name": "চাঁদপুর সরকারি কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.50, "location": "চাঁদপুর Sadar"},
    {"name": "ব্রাহ্মণবাড়িয়া সরকারি কলেজ", "board": "comilla", "group": "science", "min_gpa": 4.25, "location": "ব্রাহ্মণবাড়িয়া"},

    # ------------------ ৩. রাজশাহী বোর্ড (Rajshahi Board) ------------------
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "board": "rajshahi", "group": "science", "min_gpa": 5.00, "location": "রাজশাহী Sadar"},
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "board": "rajshahi", "group": "commerce", "min_gpa": 4.50, "location": "রাজশাহী Sadar"},
    {"name": "রাজশাহী কলেজ (Rajshahi College)", "board": "rajshahi", "group": "arts", "min_gpa": 4.00, "location": "রাজশাহী Sadar"},
    {"name": "নিউ গভ. ডিগ্রি কলেজ", "board": "rajshahi", "group": "science", "min_gpa": 4.80, "location": "রাজশাহী"},
    {"name": "রাজশাহী সরকারি সিটি কলেজ", "board": "rajshahi", "group": "science", "min_gpa": 4.30, "location": "রাজশাহী"},
    {"name": "রাজশাহী সরকারি মহিলা কলেজ", "board": "rajshahi", "group": "science", "min_gpa": 4.20, "location": "রাজশাহী"},
    {"name": "বগুড়া সরকারি আজিজুল হক কলেজ", "board": "rajshahi", "group": "science", "min_gpa": 5.00, "location": "বগুড়া Sadar"},
    {"name": "বগুড়া সরকারি আজিজুল হক কলেজ", "board": "rajshahi", "group": "commerce", "min_gpa": 4.25, "location": "বগুড়া Sadar"},
    {"name": "বগুড়া সরকারি মজিবর রহমান মহিলা কলেজ", "board": "rajshahi", "group": "science", "min_gpa": 4.50, "location": "বগুড়া"},

    # ------------------ ৪. চট্টগ্রাম বোর্ড (Chittagong Board) ------------------
    {"name": "চট্টগ্রাম কলেজ", "board": "chittagong", "group": "science", "min_gpa": 5.00, "location": "চকবাজার, চট্টগ্রাম"},
    {"name": "সরকারি হাজি মুহাম্মদ মহসিন কলেজ", "board": "chittagong", "group": "science", "min_gpa": 4.80, "location": "চকবাজার, চট্টগ্রাম"},
    {"name": "চট্টগ্রাম সরকারি সিটি কলেজ", "board": "chittagong", "group": "science", "min_gpa": 4.50, "location": "চট্টগ্রাম Sadar"},
    {"name": "সরকারি কমার্স কলেজ", "board": "chittagong", "group": "commerce", "min_gpa": 4.50, "location": "আগ্রাবাদ, চট্টগ্রাম"},
    {"name": "চট্টগ্রাম সরকারি মহিলা কলেজ", "board": "chittagong", "group": "science", "min_gpa": 4.25, "location": "নাছিরাবাদ, চট্টগ্রাম"},
    {"name": "কক্সবাজার সরকারি কলেজ", "board": "chittagong", "group": "science", "min_gpa": 4.25, "location": "কক্সবাজার Sadar"},

    # ------------------ ৫. যশোর বোর্ড (Jessore Board) ------------------
    {"name": "যশোর এম এম সরকারি কলেজ (MM College)", "board": "jessore", "group": "science", "min_gpa": 4.75, "location": "যশোর Sadar"},
    {"name": "যশোর এম এম সরকারি কলেজ (MM College)", "board": "jessore", "group": "commerce", "min_gpa": 4.00, "location": "যশোর Sadar"},
    {"name": "যশোর সরকারি মহিলা কলেজ", "board": "jessore", "group": "science", "min_gpa": 4.25, "location": "যশোর Sadar"},
    {"name": "যশোর কেন্ট পাবলিক স্কুল এন্ড কলেজ", "board": "jessore", "group": "science", "min_gpa": 4.80, "location": "যশোর কেন্ট"},
    {"name": "খুলনা সরকারি বি এল কলেজ (BL College)", "board": "jessore", "group": "science", "min_gpa": 4.85, "location": "দৌলতপুর, খুলনা"},
    {"name": "খুলনা সরকারি পাইওনিয়ার মহিলা কলেজ", "board": "jessore", "group": "science", "min_gpa": 4.30, "location": "খুলনা Sadar"},
    {"name": "কুষ্টিয়া সরকারি কলেজ", "board": "jessore", "group": "science", "min_gpa": 4.50, "location": "কুষ্টিয়া Sadar"},

    # ------------------ ৬. সিলেট বোর্ড (Sylhet Board) ------------------
    {"name": "এমসি কলেজ সিলেট (MC College)", "board": "sylhet", "group": "science", "min_gpa": 4.80, "location": "টিলাগর, সিলেট"},
    {"name": "এমসি কলেজ সিলেট (MC College)", "board": "sylhet", "group": "commerce", "min_gpa": 4.00, "location": "টিলাগর, সিলেট"},
    {"name": "সিলেট সরকারি মহিলা কলেজ", "board": "sylhet", "group": "science", "min_gpa": 4.50, "location": "চৌহাট্টা, সিলেট"},
    {"name": "সিলেট সরকারি কলেজ", "board": "sylhet", "group": "science", "min_gpa": 4.25, "location": "সিলেট Sadar"},
    {"name": "স্কলার্সহোম সিলেট", "board": "sylhet", "group": "science", "min_gpa": 4.50, "location": "শাহী ইদগাহ, সিলেট"},

    # ------------------ ৭. বরিশাল বোর্ড (Barisal Board) ------------------
    {"name": "বরিশাল ব্রজমোহন সরকারি কলেজ (BM College)", "board": "barisal", "group": "science", "min_gpa": 4.75, "location": "বরিশাল Sadar"},
    {"name": "বরিশাল ব্রজমোহন সরকারি কলেজ (BM College)", "board": "barisal", "group": "commerce", "min_gpa": 4.00, "location": "বরিশাল Sadar"},
    {"name": "বরিশাল সরকারি মহিলা কলেজ", "board": "barisal", "group": "science", "min_gpa": 4.30, "location": "বরিশাল Sadar"},
    {"name": "বরিশাল সরকারি মডেল স্কুল এন্ড কলেজ", "board": "barisal", "group": "science", "min_gpa": 4.50, "location": "বরিশাল Sadar"},
    {"name": "পটুয়াখালী সরকারি কলেজ", "board": "barisal", "group": "science", "min_gpa": 4.20, "location": "পটুয়াখালী Sadar"},

    # ------------------ ৮. দিনাজপুর বোর্ড (Dinajpur Board) ------------------
    {"name": "দিনাজপুর সরকারি কলেজ", "board": "dinajpur", "group": "science", "min_gpa": 4.75, "location": "দিনাজপুর Sadar"},
    {"name": "দিনাজপুর সরকারি মহিলা কলেজ", "board": "dinajpur", "group": "science", "min_gpa": 4.25, "location": "দিনাজপুর Sadar"},
    {"name": "রংপুর কারমাইকেল কলেজ (Carmichael College)", "board": "dinajpur", "group": "science", "min_gpa": 4.85, "location": "রংপুর Sadar"},
    {"name": "রংপুর সরকারি কলেজ", "board": "dinajpur", "group": "science", "min_gpa": 4.50, "location": "রংপুর Sadar"},
    {"name": "রংপুর ক্যাডেট কলেজ", "board": "dinajpur", "group": "science", "min_gpa": 5.00, "location": "রংপুর"},

    # ------------------ ৯. ময়মনসিংহ বোর্ড (Mymensingh Board) ------------------
    {"name": "ময়মনসিংহ আনন্দ মোহন সরকারি কলেজ", "board": "mymensingh", "group": "science", "min_gpa": 4.85, "location": "ময়মনসিংহ Sadar"},
    {"name": "ময়মনসিংহ আনন্দ মোহন সরকারি কলেজ", "board": "mymensingh", "group": "commerce", "min_gpa": 4.20, "location": "ময়মনসিংহ Sadar"},
    {"name": "ময়মনসিংহ সরকারি মুমিনুন্নিসা মহিলা কলেজ", "board": "mymensingh", "group": "science", "min_gpa": 4.50, "location": "ময়মনসিংহ Sadar"},
    {"name": "ময়মনসিংহ শহীদ সৈয়দ নজরুল ইসলাম কলেজ", "board": "mymensingh", "group": "science", "min_gpa": 4.75, "location": "ময়মনসিংহ Sadar"},
    {"name": "নেত্রকোণা সরকারি কলেজ", "board": "mymensingh", "group": "science", "min_gpa": 4.20, "location": "নেত্রকোণা Sadar"},
    {"name": "জামালপুর সরকারি আশেক মাহমুদ কলেজ", "board": "mymensingh", "group": "science", "min_gpa": 4.30, "location": "জামালপুর Sadar"}
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
                if college['board'] == selected_board and college['group'] == selected_group:
                    min_gpa = college['min_gpa']
                    diff = user_gpa - min_gpa

                    # চান্স পাওয়ার সঠিক সম্ভাবনা
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
                           board=selected_board, 
                           group=selected_group)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

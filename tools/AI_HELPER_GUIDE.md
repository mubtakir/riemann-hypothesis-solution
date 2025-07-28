# 🤖 دليل مساعد الذكاء الاصطناعي لفرز النصوص

## 🎯 الهدف
برنامج مخصص لمساعدة الذكاء الاصطناعي في فرز وتحليل النصوص الطويلة بسرعة ودقة، مع تحديد أرقام الأسطر للتشابهات والتكرارات والمفاهيم المحددة.

## ⚡ الاستخدام السريع

### 🔍 **البحث عن التكرارات:**
```bash
python ai_helper_commands.py find_dups riemann_research_ideas.md
```
**النتيجة:** قائمة بجميع الأسطر المكررة مع أرقامها

### 🔍 **البحث عن مصطلح محدد:**
```bash
python ai_helper_commands.py search riemann_research_ideas.md "هاملتوني"
```
**النتيجة:** جميع الأسطر التي تحتوي على "هاملتوني" مع أرقامها

### 🗺️ **خريطة المصطلحات:**
```bash
python ai_helper_commands.py map riemann_research_ideas.md "طيف,قيمة ذاتية,برهان"
```
**النتيجة:** خريطة تُظهر في أي أسطر يظهر كل مصطلح

### 🔍 **البحث عن التشابهات:**
```bash
python ai_helper_commands.py find_similar riemann_research_ideas.md 0.8
```
**النتيجة:** الأسطر المتشابهة بدرجة 80% أو أكثر

## 📊 نتائج الاختبار الفعلي

### ✅ **ما اكتشفه البرنامج في ملف الأفكار:**

#### **التكرارات المكتشفة:**
- **168 تكرار** لسطر "**التاريخ:** 2025-07-25" في الأسطر: 189, 195, 205, 211, 219...
- **32 تكرار** لسطر "**التاريخ:** 2025-07-26" في الأسطر: 1425, 1448, 1466...
- **15 تكرار** لسطر "## مقارنة مع الأفكار السابقة:" في الأسطر: 327, 442, 544...

#### **خريطة المصطلحات:**
- **"طيف":** 85 مرة في الأسطر: 112, 117, 126, 127, 173, 758, 759...
- **"برهان":** 158 مرة في الأسطر: 78, 87, 88, 89, 90, 91, 95...
- **"قيمة ذاتية":** 2 مرة في الأسطر: 1852, 1869

## 🛠️ الأوامر المتاحة

### 📋 **أوامر التكرارات والتشابه:**
```bash
find_dups <file>              # العثور على التكرارات المطابقة
find_similar <file> [threshold] # العثور على التشابهات (افتراضي: 0.7)
```

### 🔍 **أوامر البحث:**
```bash
search <file> <term>          # البحث عن مصطلح محدد
search_multi <file> <term1,term2,term3> # البحث عن عدة مصطلحات
pattern <file> <regex>        # البحث بنمط regex
```

### 🗺️ **أوامر التحليل:**
```bash
map <file> <term1,term2>      # خريطة المصطلحات مع أرقام الأسطر
structure <file>              # تحليل هيكل النص (عناوين، معادلات، إلخ)
```

### 📊 **أوامر التقارير:**
```bash
report <file>                 # تقرير شامل للذكاء الاصطناعي
quick_check <file>            # فحص سريع للمشاكل الشائعة
```

### 🎯 **أوامر خاصة:**
```bash
interactive <file>            # وضع تفاعلي للبحث المتقدم
help                          # عرض المساعدة
```

## 💡 أمثلة عملية لمساعدة الذكاء الاصطناعي

### **1. عند نقل المحتوى من ملف لآخر:**
```bash
# تحقق من التكرارات أولاً
python ai_helper_commands.py find_dups source_file.md

# ابحث عن المفاهيم المهمة
python ai_helper_commands.py map source_file.md "فكرة,نظرية,برهان"
```

### **2. عند البحث عن محتوى محدد:**
```bash
# ابحث عن مصطلح واحد
python ai_helper_commands.py search file.md "هاملتوني"

# ابحث عن عدة مصطلحات
python ai_helper_commands.py search_multi file.md "طيف,قيمة ذاتية,تناظر"
```

### **3. عند تحليل هيكل النص:**
```bash
# تحليل شامل للهيكل
python ai_helper_commands.py structure file.md

# فحص سريع للمشاكل
python ai_helper_commands.py quick_check file.md
```

### **4. عند البحث بأنماط معقدة:**
```bash
# البحث عن الأفكار المرقمة
python ai_helper_commands.py pattern file.md "### .+\(\d+\)"

# البحث عن التواريخ
python ai_helper_commands.py pattern file.md "\d{4}-\d{2}-\d{2}"
```

## 🎯 فوائد للذكاء الاصطناعي

### ✅ **توفير الوقت:**
- بدلاً من قراءة 3000 سطر، يحدد البرنامج المواقع المهمة فوراً
- يكشف التكرارات التي قد تفوت العين البشرية

### ✅ **دقة أعلى:**
- يحدد أرقام الأسطر بدقة
- يحسب درجات التشابه رقمياً
- يتعامل مع النصوص العربية بشكل صحيح

### ✅ **تحليل شامل:**
- يكشف أنماط التكرار في النص
- يحلل هيكل المحتوى تلقائياً
- ينتج خرائط مفصلة للمفاهيم

## 🚀 نصائح للاستخدام الأمثل

### **1. ابدأ بالفحص السريع:**
```bash
python ai_helper_commands.py quick_check your_file.md
```

### **2. استخدم خريطة المصطلحات للمفاهيم المهمة:**
```bash
python ai_helper_commands.py map your_file.md "مفهوم1,مفهوم2,مفهوم3"
```

### **3. للبحث المتقدم استخدم الوضع التفاعلي:**
```bash
python ai_helper_commands.py interactive your_file.md
```

### **4. احفظ النتائج للمراجعة:**
```bash
python ai_helper_commands.py report your_file.md > analysis_report.txt
```

## 📁 الملفات المُنتجة

عند تشغيل التقرير الشامل، ينتج البرنامج:
- `ai_assistant_report.txt` - تقرير مفصل بجميع النتائج
- تقارير فورية في الطرفية مع أرقام الأسطر

## 🔧 متطلبات التشغيل

```bash
# المكتبات الأساسية (مُثبتة مع Python)
- re, json, hashlib, difflib, collections

# لا يحتاج مكتبات خارجية إضافية!
```

## 💡 مثال شامل للاستخدام

```bash
# 1. فحص سريع للملف
python ai_helper_commands.py quick_check riemann_research_ideas.md

# 2. البحث عن المفاهيم الرئيسية
python ai_helper_commands.py map riemann_research_ideas.md "هاملتوني,طيف,برهان,نظرية"

# 3. البحث عن تكرارات محددة
python ai_helper_commands.py search riemann_research_ideas.md "التاريخ:"

# 4. تحليل الهيكل
python ai_helper_commands.py structure riemann_research_ideas.md

# 5. تقرير شامل
python ai_helper_commands.py report riemann_research_ideas.md
```

---

**🎯 الهدف النهائي:** تسهيل عمل الذكاء الاصطناعي في فرز وتحليل النصوص الطويلة بدقة وسرعة، مع تحديد المواقع بأرقام الأسطر للمراجعة السريعة.

# نظام معالجة النصوص العلمية الذكي
## Intelligent Scientific Text Processing System

### 🎯 الهدف
نظام متقدم لمعالجة وتنظيم النصوص العلمية العربية تلقائياً، مع إمكانيات الذكاء الاصطناعي لكشف التكرارات وتصنيف الأفكار وإنتاج التقارير البصرية.

### ✨ الميزات الرئيسية

#### 🔍 **معالجة النصوص المتقدمة**
- استخراج الأفكار العلمية تلقائياً من النصوص
- كشف وإزالة التكرارات بدقة عالية
- تصنيف الأفكار حسب المحتوى (نظرية، برهان، معادلة، إلخ)
- استخراج المعادلات الرياضية والكلمات المفتاحية

#### 🧠 **الذكاء الاصطناعي**
- تحليل التشابه باستخدام TF-IDF وCosine Similarity
- حساب درجة أهمية كل فكرة تلقائياً
- تجميع الأفكار المتشابهة
- كشف الأنماط في النصوص العلمية

#### 📊 **التقارير والتصور**
- إنتاج تقارير إحصائية شاملة
- رسوم بيانية تفاعلية
- سحابة كلمات للمفاهيم الرئيسية
- لوحة تحكم بصرية

#### 💾 **التصدير المتعدد**
- تصدير إلى JSON, CSV, Markdown
- قاعدة بيانات قابلة للبحث
- ملفات منظمة حسب الفئات

### 🚀 التثبيت والاستخدام

#### 1. **التثبيت الأساسي**
```bash
# تثبيت المكتبات الأساسية
pip install numpy matplotlib scipy pandas

# تثبيت جميع المكتبات (مُنصح به)
pip install -r requirements.txt
```

#### 2. **الاستخدام السريع**
```bash
# تشغيل أساسي
python run_text_analysis.py

# تحليل متقدم مع جميع الميزات
python run_text_analysis.py --advanced --export-all --visualize

# معالجة ملف محدد
python run_text_analysis.py --file my_research.md --advanced
```

#### 3. **خيارات التشغيل**
```bash
# فحص المكتبات المطلوبة
python run_text_analysis.py --check-deps

# تحديد مجلد الإخراج
python run_text_analysis.py --output-dir my_results

# تعديل عتبة التشابه
python run_text_analysis.py --similarity-threshold 0.8
```

### 📁 **هيكل الملفات**

```
riemann_research_complete/
├── intelligent_text_processor.py    # المعالج الرئيسي
├── run_text_analysis.py            # ملف التشغيل السريع
├── requirements.txt                 # المكتبات المطلوبة
├── TEXT_PROCESSOR_README.md         # هذا الملف
└── analysis_output/                 # مجلد النتائج (يُنشأ تلقائياً)
    ├── organized_ideas.md           # الأفكار المنظمة
    ├── ideas_database.json          # قاعدة البيانات
    ├── ideas_export.json            # تصدير JSON
    ├── ideas_export.csv             # تصدير CSV
    ├── wordcloud.png                # سحابة الكلمات
    └── visualizations/              # الرسوم البيانية
        └── dashboard.png            # لوحة التحكم
```

### 🔧 **الاستخدام المتقدم**

#### **في الكود Python**
```python
from intelligent_text_processor import AdvancedTextAnalyzer

# إنشاء المحلل
analyzer = AdvancedTextAnalyzer()

# معالجة ملف
results = analyzer.processor.process_text_file('my_research.md')

# تحليل التشابه
similarity_results = analyzer.advanced_similarity_analysis(results['new_ideas'])

# إنتاج التقارير
analyzer.create_visual_dashboard(results['new_ideas'], 'output_dir')
analyzer.generate_word_cloud(results['new_ideas'], 'wordcloud.png')
```

#### **تخصيص المعالجة**
```python
from intelligent_text_processor import ArabicScientificTextProcessor

processor = ArabicScientificTextProcessor()

# إضافة فئات جديدة
processor.categories['تجربة'] = ['تجربة', 'اختبار', 'قياس']

# تخصيص أنماط المعادلات
processor.equation_patterns.append(r'النتيجة\s*:\s*[^\.]+')

# معالجة النص
results = processor.process_text_file('research.md')
```

### 📊 **أمثلة النتائج**

#### **تقرير إحصائي**
```
📊 النتائج الإجمالية:
  📝 إجمالي الأفكار: 687
  ✨ أفكار جديدة: 22
  🔄 تكرارات: 3
  📊 الفئات: 6
  🔢 المعادلات: 45
  🔑 الكلمات المفتاحية: 28
```

#### **أهم الكلمات المفتاحية**
```
🏷️  أهم الكلمات المفتاحية:
  - هاملتوني: 15
  - طيف: 12
  - فرضية ريمان: 10
  - قيمة ذاتية: 8
  - تناظر: 6
```

### 🎨 **التصورات البصرية**

#### **لوحة التحكم**
- رسم دائري لتوزيع الفئات
- هيستوجرام لدرجات الأهمية
- رسم بياني للكلمات المفتاحية
- منحنى التوزيع الزمني

#### **سحابة الكلمات**
- عرض بصري للمفاهيم الرئيسية
- دعم النصوص العربية
- ألوان متدرجة حسب التكرار

### ⚙️ **الإعدادات المتقدمة**

#### **تخصيص التصنيف**
```python
# إضافة فئات جديدة
processor.categories.update({
    'خوارزمية': ['خوارزمية', 'طريقة', 'منهج'],
    'نتيجة': ['نتيجة', 'خلاصة', 'استنتاج']
})
```

#### **تخصيص الكلمات المفتاحية**
```python
# إضافة كلمات مفتاحية جديدة
scientific_keywords.extend([
    'ديناميكا', 'كمومي', 'طيفي', 'عددي'
])
```

#### **تخصيص درجة الأهمية**
```python
def custom_importance_score(idea):
    score = 0.0
    score += len(idea.equations) * 3.0      # وزن أكبر للمعادلات
    score += len(idea.keywords) * 2.0       # وزن متوسط للكلمات المفتاحية
    score += min(len(idea.content) / 50, 10.0)  # وزن للطول
    return score
```

### 🔍 **استكشاف الأخطاء**

#### **مشاكل شائعة وحلولها**

1. **خطأ في استيراد المكتبات**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **مشاكل الترميز العربي**
   ```python
   # تأكد من استخدام UTF-8
   with open(file, 'r', encoding='utf-8') as f:
       content = f.read()
   ```

3. **مشاكل الخطوط العربية في الرسوم**
   ```bash
   # تثبيت خطوط عربية
   pip install arabic-reshaper python-bidi
   ```

### 📈 **الأداء والتحسين**

#### **نصائح للأداء الأمثل**
- استخدم ملفات أصغر للاختبار أولاً
- قم بتشغيل التحليل المتقدم على دفعات
- احفظ قاعدة البيانات لتجنب إعادة المعالجة

#### **استخدام الذاكرة**
- الملفات الكبيرة (>10MB) قد تحتاج ذاكرة إضافية
- استخدم المعالجة على دفعات للملفات الضخمة

### 🤝 **المساهمة والتطوير**

#### **إضافة ميزات جديدة**
1. أنشئ فئة جديدة ترث من `ArabicScientificTextProcessor`
2. أضف دوال معالجة مخصصة
3. اختبر على عينات صغيرة أولاً

#### **تحسين الخوارزميات**
- تحسين خوارزميات كشف التشابه
- إضافة نماذج ذكاء اصطناعي متقدمة
- تحسين دقة استخراج المعادلات

### 📞 **الدعم والمساعدة**

للحصول على المساعدة:
1. راجع هذا الدليل أولاً
2. تحقق من ملف `requirements.txt`
3. جرب الأمثلة البسيطة قبل المعقدة
4. استخدم `--check-deps` لفحص المكتبات

### 📝 **الترخيص**
هذا البرنامج جزء من مشروع حل مسألة ريمان ومتاح للاستخدام الأكاديمي والبحثي.

---

**تم تطوير هذا النظام كجزء من مشروع حل فرضية ريمان باستخدام النموذج الزمني المتكامل ونظرية الطيف العددي.**

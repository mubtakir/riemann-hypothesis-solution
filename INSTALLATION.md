# دليل التثبيت والتشغيل - أدوات الفرز الذكي

## 🎯 نظرة عامة

هذا الدليل يشرح كيفية تثبيت وتشغيل أدوات الفرز الذكي المتكامل المستخدمة في مشروع حل فرضية ريمان.

---

## 📋 المتطلبات الأساسية

### متطلبات النظام
- **🐍 Python:** الإصدار 3.8 أو أحدث
- **💾 الذاكرة:** 4 GB RAM كحد أدنى (8 GB مستحسن)
- **💿 مساحة القرص:** 2 GB مساحة فارغة
- **🌐 الاتصال:** اتصال إنترنت للتحديثات

### أنظمة التشغيل المدعومة
- ✅ **Linux:** Ubuntu 18.04+, CentOS 7+, Debian 9+
- ✅ **macOS:** 10.14 (Mojave) أو أحدث
- ✅ **Windows:** Windows 10 أو أحدث

---

## 🚀 التثبيت السريع

### الخطوة 1: استنساخ المستودع
```bash
git clone https://github.com/username/riemann-hypothesis-complete-solution.git
cd riemann-hypothesis-complete-solution
```

### الخطوة 2: إنشاء بيئة افتراضية
```bash
# إنشاء البيئة الافتراضية
python -m venv riemann_env

# تفعيل البيئة (Linux/macOS)
source riemann_env/bin/activate

# تفعيل البيئة (Windows)
riemann_env\Scripts\activate
```

### الخطوة 3: تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### الخطوة 4: التحقق من التثبيت
```bash
python tools/ai_helper_commands.py --version
```

---

## 📦 المتطلبات التفصيلية

### مكتبات Python الأساسية
```txt
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
pandas>=1.3.0
sympy>=1.8
```

### مكتبات معالجة النصوص
```txt
nltk>=3.6
spacy>=3.4
textblob>=0.17
fuzzywuzzy>=0.18
python-levenshtein>=0.12
```

### مكتبات التحليل المتقدم
```txt
scikit-learn>=1.0
networkx>=2.6
plotly>=5.0
seaborn>=0.11
```

### مكتبات إضافية
```txt
tqdm>=4.62
colorama>=0.4
rich>=10.0
click>=8.0
```

---

## 🔧 التكوين المتقدم

### إعداد متغيرات البيئة
```bash
# إضافة إلى ~/.bashrc أو ~/.zshrc
export RIEMANN_PROJECT_PATH="/path/to/riemann-hypothesis-complete-solution"
export RIEMANN_DATA_PATH="$RIEMANN_PROJECT_PATH/data"
export RIEMANN_OUTPUT_PATH="$RIEMANN_PROJECT_PATH/output"
```

### تكوين ملف الإعدادات
```python
# config.py
ANALYSIS_CONFIG = {
    'similarity_threshold': 0.8,
    'context_window': 25,
    'max_iterations': 1000,
    'output_format': 'markdown',
    'language': 'arabic'
}

PROCESSING_CONFIG = {
    'chunk_size': 1000,
    'parallel_workers': 4,
    'memory_limit': '4GB',
    'cache_enabled': True
}
```

---

## 🎯 الاستخدام الأساسي

### الأوامر السريعة
```bash
# فحص سريع للملف
python tools/ai_helper_commands.py quick_check original/riemann_research_ideas.md

# البحث عن مفهوم محدد
python tools/ai_helper_commands.py search original/riemann_research_ideas.md "هاملتوني"

# إنشاء خريطة المفاهيم
python tools/ai_helper_commands.py map original/riemann_research_ideas.md "طيف,قيمة ذاتية"

# العثور على المحتوى المشابه
python tools/ai_helper_commands.py find_similar original/riemann_research_ideas.md 0.8
```

### الوضع التفاعلي
```bash
# تشغيل الوضع التفاعلي
python tools/ai_helper_commands.py interactive original/riemann_research_ideas.md
```

### معالجة متقدمة
```bash
# تحليل شامل مع تقرير مفصل
python tools/ai_assistant_helper.py --input original/riemann_research_ideas.md --output reports/ --detailed

# فرز ذكي مع تصنيف
python tools/ai_assistant_helper.py --smart-sort --classify --output docs/
```

---

## 🔍 استكشاف الأخطاء

### مشاكل شائعة وحلولها

#### خطأ: "Module not found"
```bash
# الحل: تأكد من تفعيل البيئة الافتراضية
source riemann_env/bin/activate
pip install -r requirements.txt
```

#### خطأ: "Permission denied"
```bash
# الحل: تغيير صلاحيات الملفات
chmod +x tools/ai_helper_commands.py
```

#### خطأ: "Memory error"
```bash
# الحل: تقليل حجم المعالجة
export RIEMANN_CHUNK_SIZE=500
export RIEMANN_MEMORY_LIMIT=2GB
```

#### خطأ: "Encoding error"
```bash
# الحل: تعيين ترميز UTF-8
export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
```

### سجلات الأخطاء
```bash
# تشغيل مع سجل مفصل
python tools/ai_helper_commands.py --verbose --log-file debug.log

# فحص سجل الأخطاء
tail -f debug.log
```

---

## 🧪 اختبار التثبيت

### اختبارات أساسية
```bash
# اختبار الوظائف الأساسية
python -m pytest tests/test_basic_functions.py

# اختبار معالجة النصوص
python -m pytest tests/test_text_processing.py

# اختبار التحليل المتقدم
python -m pytest tests/test_advanced_analysis.py
```

### اختبار الأداء
```bash
# قياس سرعة المعالجة
python tools/benchmark.py --input original/riemann_research_ideas.md

# اختبار استهلاك الذاكرة
python tools/memory_test.py --profile
```

---

## 📊 مراقبة الأداء

### مؤشرات الأداء
```bash
# مراقبة استهلاك الموارد
python tools/monitor.py --real-time

# تقرير الأداء
python tools/performance_report.py --output reports/performance.html
```

### تحسين الأداء
```python
# تحسين إعدادات المعالجة
OPTIMIZATION_CONFIG = {
    'use_multiprocessing': True,
    'cache_results': True,
    'optimize_memory': True,
    'parallel_threshold': 1000
}
```

---

## 🔄 التحديث والصيانة

### تحديث المكتبات
```bash
# تحديث جميع المكتبات
pip install --upgrade -r requirements.txt

# تحديث مكتبة محددة
pip install --upgrade numpy
```

### تنظيف البيانات المؤقتة
```bash
# حذف ملفات التخزين المؤقت
python tools/cleanup.py --cache

# حذف ملفات السجل القديمة
python tools/cleanup.py --logs --older-than 30d
```

### النسخ الاحتياطي
```bash
# إنشاء نسخة احتياطية
python tools/backup.py --output backups/$(date +%Y%m%d)

# استعادة من نسخة احتياطية
python tools/restore.py --input backups/20250726
```

---

## 🤝 الدعم والمساعدة

### الحصول على المساعدة
```bash
# عرض المساعدة العامة
python tools/ai_helper_commands.py --help

# مساعدة لأمر محدد
python tools/ai_helper_commands.py search --help

# دليل المستخدم التفاعلي
python tools/interactive_guide.py
```

### الإبلاغ عن المشاكل
1. **🔍 تحقق من السجلات:** راجع ملفات السجل للأخطاء
2. **📋 جمع المعلومات:** احفظ رسائل الخطأ والإعدادات
3. **🐛 إنشاء تقرير:** افتح issue في GitHub مع التفاصيل
4. **📞 التواصل:** استخدم قنوات الدعم المتاحة

### الموارد الإضافية
- **📚 الوثائق:** [docs/](docs/)
- **🎓 الدروس:** [tutorials/](tutorials/)
- **❓ الأسئلة الشائعة:** [FAQ.md](FAQ.md)
- **🤝 المجتمع:** [discussions/](../../discussions)

---

## 📝 ملاحظات مهمة

### أفضل الممارسات
- ✅ **استخدم بيئة افتراضية:** لتجنب تضارب المكتبات
- ✅ **احتفظ بنسخ احتياطية:** للبيانات المهمة
- ✅ **راقب الأداء:** لضمان الكفاءة المثلى
- ✅ **حدث بانتظام:** للحصول على أحدث الميزات

### تحذيرات
- ⚠️ **استهلاك الذاكرة:** قد تحتاج ملفات كبيرة لذاكرة أكثر
- ⚠️ **وقت المعالجة:** التحليل المتقدم قد يستغرق وقتاً طويلاً
- ⚠️ **دقة النتائج:** تعتمد على جودة البيانات المدخلة
- ⚠️ **التوافق:** تأكد من توافق إصدارات المكتبات

---

*آخر تحديث: 2025-07-26*  
*الإصدار: 5.0.0*

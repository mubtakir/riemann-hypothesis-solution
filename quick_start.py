#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل سريع ومبسط لمعالج النصوص العلمية
Quick Start for Scientific Text Processor

الاستخدام البسيط:
python quick_start.py

أو:
python quick_start.py my_research_file.md
"""

import sys
import os
from pathlib import Path

def simple_text_analysis(input_file=None):
    """تحليل نصوص مبسط"""
    
    print("🚀 معالج النصوص العلمية - التشغيل السريع")
    print("=" * 50)
    
    # تحديد الملف
    if input_file and os.path.exists(input_file):
        file_to_process = input_file
        print(f"📄 معالجة الملف: {file_to_process}")
    elif os.path.exists('riemann_research_ideas.md'):
        file_to_process = 'riemann_research_ideas.md'
        print(f"📄 معالجة الملف الافتراضي: {file_to_process}")
    else:
        print("❌ لم يتم العثور على ملف للمعالجة")
        print("💡 ضع ملف riemann_research_ideas.md في نفس المجلد")
        print("💡 أو استخدم: python quick_start.py your_file.md")
        return
    
    try:
        # استيراد المعالج
        from intelligent_text_processor import ArabicScientificTextProcessor
        
        print("✅ تم تحميل المعالج بنجاح")
        
        # إنشاء المعالج
        processor = ArabicScientificTextProcessor()
        
        # معالجة الملف
        print("⚙️  جاري المعالجة...")
        results = processor.process_text_file(file_to_process)
        
        # عرض النتائج
        new_ideas = results.get('new_ideas', [])
        duplicates = results.get('duplicates', [])
        
        print(f"\n📊 النتائج:")
        print(f"  ✨ أفكار جديدة: {len(new_ideas)}")
        print(f"  🔄 تكرارات: {len(duplicates)}")
        
        if new_ideas:
            # أهم الأفكار
            top_ideas = sorted(new_ideas, key=lambda x: x.importance_score, reverse=True)[:5]
            print(f"\n🌟 أهم 5 أفكار:")
            for i, idea in enumerate(top_ideas, 1):
                print(f"  {i}. {idea.title}")
                print(f"     الفئة: {idea.category} | الأهمية: {idea.importance_score:.1f}")
                if idea.keywords:
                    print(f"     الكلمات المفتاحية: {', '.join(idea.keywords[:3])}")
                print()
            
            # إحصائيات الفئات
            categories = {}
            for idea in new_ideas:
                categories[idea.category] = categories.get(idea.category, 0) + 1
            
            print(f"📋 توزيع الفئات:")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"  {category}: {count} فكرة")
            
            # إنتاج ملف منظم
            output_file = 'organized_ideas_simple.md'
            processor.generate_organized_output(output_file)
            print(f"\n💾 تم حفظ الأفكار المنظمة في: {output_file}")
            
            # حفظ قاعدة بيانات بسيطة
            db_file = 'ideas_simple.json'
            processor.save_database(db_file)
            print(f"💾 تم حفظ قاعدة البيانات في: {db_file}")
            
        else:
            print("⚠️  لم يتم العثور على أفكار جديدة")
        
        print(f"\n✅ تم الانتهاء بنجاح!")
        
        # نصائح للاستخدام المتقدم
        print(f"\n💡 للمزيد من الميزات:")
        print(f"  python run_text_analysis.py --advanced --visualize")
        
    except ImportError:
        print("❌ خطأ: لا يمكن استيراد معالج النصوص")
        print("💡 تأكد من وجود ملف intelligent_text_processor.py")
        print("💡 أو استخدم: python run_text_analysis.py")
        
    except Exception as e:
        print(f"❌ خطأ في المعالجة: {e}")
        print("💡 جرب: python run_text_analysis.py --check-deps")

def install_basic_requirements():
    """تثبيت المتطلبات الأساسية"""
    import subprocess
    
    basic_packages = ['numpy', 'matplotlib', 'scipy']
    
    print("📦 تثبيت المكتبات الأساسية...")
    
    for package in basic_packages:
        try:
            print(f"  تثبيت {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  ✅ تم تثبيت {package}")
        except:
            print(f"  ❌ فشل تثبيت {package}")
    
    print("✅ انتهى التثبيت")

def show_help():
    """عرض المساعدة"""
    print("""
🔧 معالج النصوص العلمية - دليل الاستخدام السريع

📖 الاستخدام:
  python quick_start.py                    # معالجة الملف الافتراضي
  python quick_start.py my_file.md         # معالجة ملف محدد
  python quick_start.py --install          # تثبيت المكتبات الأساسية
  python quick_start.py --help             # عرض هذه المساعدة

📁 الملفات المطلوبة:
  - intelligent_text_processor.py          # المعالج الرئيسي
  - riemann_research_ideas.md              # الملف الافتراضي (اختياري)

📊 النتائج:
  - organized_ideas_simple.md              # الأفكار المنظمة
  - ideas_simple.json                      # قاعدة البيانات

🚀 للمزيد من الميزات:
  python run_text_analysis.py --advanced --visualize --export-all

💡 نصائح:
  - ضع ملفاتك النصية في نفس المجلد
  - استخدم ترميز UTF-8 للنصوص العربية
  - للملفات الكبيرة، استخدم run_text_analysis.py
    """)

def main():
    """الدالة الرئيسية"""
    
    # معالجة المعاملات
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg in ['--help', '-h', 'help']:
            show_help()
            return
        elif arg in ['--install', '-i', 'install']:
            install_basic_requirements()
            return
        else:
            # ملف محدد
            simple_text_analysis(arg)
            return
    
    # تشغيل عادي
    simple_text_analysis()

if __name__ == "__main__":
    main()

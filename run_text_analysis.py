#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل سريع لنظام معالجة النصوص العلمية الذكي
Quick Run for Intelligent Scientific Text Processing System

الاستخدام:
python run_text_analysis.py

أو مع خيارات متقدمة:
python run_text_analysis.py --advanced --export-all --visualize
"""

import argparse
import sys
import os
from pathlib import Path

# إضافة المجلد الحالي للمسار
sys.path.append(str(Path(__file__).parent))

try:
    from intelligent_text_processor import AdvancedTextAnalyzer, ArabicScientificTextProcessor
except ImportError:
    print("❌ خطأ: لا يمكن استيراد معالج النصوص")
    print("تأكد من وجود ملف intelligent_text_processor.py في نفس المجلد")
    sys.exit(1)

def check_dependencies():
    """فحص المكتبات المطلوبة"""
    required_basic = ['numpy', 'matplotlib', 'json', 're', 'hashlib']
    optional = ['scikit-learn', 'wordcloud', 'seaborn', 'arabic_reshaper']
    
    missing_basic = []
    missing_optional = []
    
    for lib in required_basic:
        try:
            __import__(lib)
        except ImportError:
            missing_basic.append(lib)
    
    for lib in optional:
        try:
            __import__(lib)
        except ImportError:
            missing_optional.append(lib)
    
    if missing_basic:
        print(f"❌ مكتبات أساسية مفقودة: {', '.join(missing_basic)}")
        print("يرجى تثبيتها باستخدام: pip install " + ' '.join(missing_basic))
        return False
    
    if missing_optional:
        print(f"⚠️  مكتبات اختيارية مفقودة: {', '.join(missing_optional)}")
        print("للحصول على جميع الميزات، قم بتثبيتها: pip install " + ' '.join(missing_optional))
    
    return True

def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(
        description='نظام معالجة النصوص العلمية الذكي',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
  python run_text_analysis.py                    # تشغيل أساسي
  python run_text_analysis.py --advanced         # تحليل متقدم
  python run_text_analysis.py --export-all       # تصدير جميع الصيغ
  python run_text_analysis.py --visualize        # إنشاء الرسوم البيانية
  python run_text_analysis.py --file custom.md   # معالجة ملف محدد
        """
    )
    
    parser.add_argument('--file', '-f', 
                       help='ملف محدد للمعالجة (افتراضي: riemann_research_ideas.md)')
    parser.add_argument('--advanced', '-a', action='store_true',
                       help='تشغيل التحليل المتقدم مع الذكاء الاصطناعي')
    parser.add_argument('--export-all', '-e', action='store_true',
                       help='تصدير النتائج لجميع الصيغ (JSON, CSV, MD)')
    parser.add_argument('--visualize', '-v', action='store_true',
                       help='إنشاء الرسوم البيانية وسحابة الكلمات')
    parser.add_argument('--output-dir', '-o', default='analysis_output',
                       help='مجلد الإخراج (افتراضي: analysis_output)')
    parser.add_argument('--similarity-threshold', '-s', type=float, default=0.7,
                       help='عتبة التشابه لكشف التكرارات (افتراضي: 0.7)')
    parser.add_argument('--check-deps', action='store_true',
                       help='فحص المكتبات المطلوبة فقط')
    
    args = parser.parse_args()
    
    # فحص المكتبات
    if args.check_deps:
        check_dependencies()
        return
    
    if not check_dependencies():
        print("يرجى تثبيت المكتبات المطلوبة أولاً")
        return
    
    print("🚀 بدء نظام معالجة النصوص العلمية الذكي")
    print("=" * 60)
    
    # إنشاء مجلد الإخراج
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # تحديد الملفات للمعالجة
    if args.file:
        files_to_process = [args.file]
    else:
        files_to_process = [
            'riemann_research_ideas.md',
            'riemann_hypothesis_solution_book.md',
            'conversation_archive.txt'
        ]
    
    # إنشاء المعالج
    if args.advanced:
        analyzer = AdvancedTextAnalyzer()
        processor = analyzer.processor
    else:
        processor = ArabicScientificTextProcessor()
        analyzer = None
    
    # معالجة الملفات
    all_ideas = []
    total_new = 0
    total_duplicates = 0
    
    for file_path in files_to_process:
        if not os.path.exists(file_path):
            print(f"⚠️  الملف غير موجود: {file_path}")
            continue
        
        print(f"\n📄 معالجة الملف: {file_path}")
        print("-" * 40)
        
        try:
            results = processor.process_text_file(file_path)
            
            new_ideas = results.get('new_ideas', [])
            duplicates = results.get('duplicates', [])
            
            all_ideas.extend(new_ideas)
            total_new += len(new_ideas)
            total_duplicates += len(duplicates)
            
            print(f"  ✅ أفكار جديدة: {len(new_ideas)}")
            print(f"  🔄 تكرارات: {len(duplicates)}")
            
            # عرض أهم الأفكار
            if new_ideas:
                top_ideas = sorted(new_ideas, key=lambda x: x.importance_score, reverse=True)[:3]
                print("  🌟 أهم الأفكار:")
                for i, idea in enumerate(top_ideas, 1):
                    print(f"    {i}. {idea.title} (أهمية: {idea.importance_score:.2f})")
            
        except Exception as e:
            print(f"  ❌ خطأ في معالجة الملف: {e}")
            continue
    
    # عرض النتائج الإجمالية
    print(f"\n📊 النتائج الإجمالية:")
    print(f"  📝 إجمالي الأفكار: {len(all_ideas)}")
    print(f"  ✨ أفكار جديدة: {total_new}")
    print(f"  🔄 تكرارات: {total_duplicates}")
    
    if not all_ideas:
        print("❌ لم يتم العثور على أفكار للمعالجة")
        return
    
    # إنتاج التقارير الأساسية
    print(f"\n📈 إنتاج التقارير...")
    
    # ملف منظم
    organized_file = output_dir / 'organized_ideas.md'
    processor.generate_organized_output(str(organized_file))
    print(f"  📋 ملف منظم: {organized_file}")
    
    # قاعدة بيانات
    db_file = output_dir / 'ideas_database.json'
    processor.save_database(str(db_file))
    print(f"  💾 قاعدة البيانات: {db_file}")
    
    # التحليل المتقدم
    if args.advanced and analyzer:
        print(f"\n🧠 التحليل المتقدم...")
        
        # تحليل التشابه
        similarity_results = analyzer.advanced_similarity_analysis(all_ideas)
        if similarity_results:
            similar_pairs = similarity_results.get('similar_pairs', [])
            print(f"  🔍 أزواج متشابهة: {len(similar_pairs)}")
            
            if similar_pairs:
                print("  📋 أمثلة على التشابه:")
                for pair in similar_pairs[:3]:
                    print(f"    - {pair['idea1'].title} ↔ {pair['idea2'].title} "
                          f"(تشابه: {pair['similarity']:.2f})")
        
        # إحصائيات
        stats = analyzer.generate_statistics_report(all_ideas)
        print(f"  📊 الفئات: {len(stats['categories'])}")
        print(f"  🔢 المعادلات: {stats['equations_count']}")
        print(f"  🔑 الكلمات المفتاحية: {len(stats['keywords_frequency'])}")
        
        # أهم الكلمات المفتاحية
        if stats['keywords_frequency']:
            top_keywords = sorted(stats['keywords_frequency'].items(), 
                                key=lambda x: x[1], reverse=True)[:5]
            print("  🏷️  أهم الكلمات المفتاحية:")
            for keyword, count in top_keywords:
                print(f"    - {keyword}: {count}")
    
    # التصدير
    if args.export_all:
        print(f"\n📤 تصدير البيانات...")
        export_base = output_dir / 'ideas_export'
        
        if analyzer:
            analyzer.export_to_formats(all_ideas, str(export_base))
        else:
            # تصدير أساسي
            import json
            json_data = [
                {
                    'id': idea.id,
                    'title': idea.title,
                    'category': idea.category,
                    'importance': idea.importance_score
                }
                for idea in all_ideas
            ]
            
            with open(f"{export_base}.json", 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"  💾 ملفات التصدير: {export_base}.*")
    
    # التصور
    if args.visualize and analyzer:
        print(f"\n🎨 إنشاء التصورات...")
        
        # لوحة التحكم
        visual_dir = output_dir / 'visualizations'
        analyzer.create_visual_dashboard(all_ideas, str(visual_dir))
        print(f"  📊 لوحة التحكم: {visual_dir}/dashboard.png")
        
        # سحابة الكلمات
        wordcloud_file = output_dir / 'wordcloud.png'
        analyzer.generate_word_cloud(all_ideas, str(wordcloud_file))
        print(f"  ☁️  سحابة الكلمات: {wordcloud_file}")
    
    print(f"\n✅ تم الانتهاء من التحليل بنجاح!")
    print(f"📁 جميع النتائج في: {output_dir}")
    
    # نصائح للخطوات التالية
    print(f"\n💡 الخطوات التالية:")
    print(f"  1. راجع الملف المنظم: {organized_file}")
    print(f"  2. استخدم قاعدة البيانات للبحث: {db_file}")
    if args.visualize:
        print(f"  3. اطلع على التصورات في: {output_dir}/visualizations/")
    if not args.advanced:
        print(f"  4. جرب التحليل المتقدم: --advanced")
    if not args.export_all:
        print(f"  5. صدّر البيانات: --export-all")

if __name__ == "__main__":
    main()

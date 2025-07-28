#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أوامر سريعة لمساعدة الذكاء الاصطناعي في فرز النصوص
Quick Commands for AI Assistant Text Processing

الاستخدام:
python ai_helper_commands.py <command> <file> [options]

الأوامر:
- find_dups: العثور على التكرارات
- find_similar: العثور على التشابهات  
- search: البحث عن مصطلح
- map: خريطة المصطلحات
- structure: تحليل الهيكل
- report: تقرير شامل
"""

import sys
import os
from ai_assistant_helper import AIAssistantHelper, QuickAssistant, ai_assistant_workflow

def show_usage():
    """عرض طريقة الاستخدام"""
    print("""
🤖 أوامر مساعد الذكاء الاصطناعي

الاستخدام:
  python ai_helper_commands.py <command> <file> [options]

الأوامر المتاحة:

📋 أوامر التكرارات والتشابه:
  find_dups <file>              - العثور على التكرارات المطابقة
  find_similar <file> [threshold] - العثور على التشابهات (افتراضي: 0.7)
  
🔍 أوامر البحث:
  search <file> <term>          - البحث عن مصطلح محدد
  search_context <file> <term> [context_words] - البحث مع تجميع السياق
  search_multi <file> <term1,term2,term3> - البحث عن عدة مصطلحات
  pattern <file> <regex>        - البحث بنمط regex
  related <file> <term1,term2,term3> - العثور على المفاهيم المترابطة
  
🗺️ أوامر التحليل:
  map <file> <term1,term2>      - خريطة المصطلحات مع أرقام الأسطر
  structure <file>              - تحليل هيكل النص (عناوين، معادلات، إلخ)
  
📊 أوامر التقارير:
  report <file>                 - تقرير شامل للذكاء الاصطناعي
  quick_check <file>            - فحص سريع للمشاكل الشائعة

🧹 أوامر الفرز الذكي:
  remove_ai <file>              - حذف ردود الذكاء الاصطناعي
  extract_method <file> <method_name> <keyword1,keyword2> - استخراج طريقة حل
  smart_sort <file>             - الفرز الذكي الكامل
  
🎯 أوامر خاصة:
  interactive <file>            - وضع تفاعلي للبحث المتقدم
  help                          - عرض هذه المساعدة

أمثلة:
  python ai_helper_commands.py find_dups riemann_research_ideas.md
  python ai_helper_commands.py search conversation_archive.txt "هاملتوني"
  python ai_helper_commands.py map riemann_research_ideas.md "طيف,قيمة ذاتية,برهان"
  python ai_helper_commands.py report riemann_research_ideas.md
    """)

def cmd_find_dups(file_path: str):
    """أمر العثور على التكرارات"""
    print("🔍 البحث عن التكرارات المطابقة...")
    result = QuickAssistant.quick_find_duplicates(file_path)
    print(result)

def cmd_find_similar(file_path: str, threshold: str = "0.7"):
    """أمر العثور على التشابهات"""
    try:
        thresh = float(threshold)
        print(f"🔍 البحث عن التشابهات (عتبة: {thresh})...")
        result = QuickAssistant.quick_similarity_check(file_path, thresh)
        print(result)
    except ValueError:
        print("❌ عتبة التشابه يجب أن تكون رقم بين 0 و 1")

def cmd_search(file_path: str, term: str):
    """أمر البحث عن مصطلح"""
    helper = AIAssistantHelper()
    if not helper.load_file(file_path):
        return

    print(f"🔍 البحث عن: '{term}'")
    results = helper.search_concept(term, context_lines=1)

    if not results:
        print("❌ لم يتم العثور على نتائج")
        return

    print(f"📋 تم العثور على {len(results)} نتيجة:")
    for i, result in enumerate(results[:20]):  # أول 20 نتيجة
        print(f"\n{i+1}. السطر {result['line_number']}:")
        print(f"   {result['content']}")

def cmd_search_context(file_path: str, term: str, context_words: str = "10"):
    """أمر البحث مع تجميع السياق"""
    try:
        context_size = int(context_words)
        helper = AIAssistantHelper(context_words=context_size)
        if not helper.load_file(file_path):
            return

        print(f"🔍 البحث مع السياق: '{term}' (معامل: {context_size})")
        results = helper.search_concept_with_context(term)

        if not results:
            print("❌ لم يتم العثور على نتائج")
            return

        print(f"📋 تم العثور على {len(results)} سياق مترابط:")
        for i, result in enumerate(results[:10]):  # أول 10 سياقات
            print(f"\n{i+1}. السياق {result['context_start']}-{result['context_end']} ({result['matches_count']} تطابق):")
            print(f"   الأسطر: {', '.join(map(str, result['line_numbers']))}")
            print(f"   عدد الكلمات: {result['word_count']}")
            print("   المحتوى:")
            for line in result['context_text'][:5]:  # أول 5 أسطر من السياق
                print(f"     {line}")
            if len(result['context_text']) > 5:
                print(f"     ... و {len(result['context_text']) - 5} سطر آخر")

    except ValueError:
        print("❌ معامل السياق يجب أن يكون رقم")

def cmd_search_multi(file_path: str, terms_str: str):
    """أمر البحث عن عدة مصطلحات"""
    terms = [t.strip() for t in terms_str.split(',')]
    print(f"🔍 البحث عن {len(terms)} مصطلحات...")
    result = QuickAssistant.quick_search_multiple(file_path, terms)
    print(result)

def cmd_pattern(file_path: str, pattern: str):
    """أمر البحث بنمط regex"""
    helper = AIAssistantHelper()
    if not helper.load_file(file_path):
        return
    
    print(f"🔍 البحث بالنمط: '{pattern}'")
    results = helper.find_ideas_by_pattern(pattern)
    
    if not results:
        print("❌ لم يتم العثور على نتائج")
        return
    
    print(f"📋 تم العثور على {len(results)} نتيجة:")
    for i, result in enumerate(results[:15]):
        print(f"{i+1}. السطر {result['line_number']}: {result['match']}")

def cmd_map(file_path: str, terms_str: str):
    """أمر خريطة المصطلحات"""
    terms = [t.strip() for t in terms_str.split(',')]
    helper = AIAssistantHelper()
    if not helper.load_file(file_path):
        return
    
    print(f"🗺️ إنشاء خريطة لـ {len(terms)} مصطلحات...")
    line_map = helper.generate_line_map(terms)
    
    print("📍 خريطة المصطلحات:")
    for term, locations in line_map.items():
        if locations:
            line_numbers = [str(loc['line_number']) for loc in locations]
            print(f"\n'{term}' ({len(locations)} مرة):")
            print(f"  الأسطر: {', '.join(line_numbers[:20])}")
            if len(locations) > 20:
                print(f"  ... و {len(locations) - 20} موقع آخر")
        else:
            print(f"\n'{term}': لم يتم العثور عليه")

def cmd_structure(file_path: str):
    """أمر تحليل الهيكل"""
    helper = AIAssistantHelper()
    if not helper.load_file(file_path):
        return
    
    print("📊 تحليل هيكل النص...")
    structure = helper.analyze_section_structure()
    
    print("\n📋 تقرير الهيكل:")
    for section_type, items in structure.items():
        print(f"\n{section_type} ({len(items)} عنصر):")
        if items:
            for i, item in enumerate(items[:10]):  # أول 10 عناصر
                print(f"  {i+1}. السطر {item['line_number']}: {item['match'][:80]}...")
            if len(items) > 10:
                print(f"  ... و {len(items) - 10} عنصر آخر")

def cmd_report(file_path: str):
    """أمر التقرير الشامل"""
    print("📊 إنتاج تقرير شامل للذكاء الاصطناعي...")
    ai_assistant_workflow(file_path, "full_analysis")

def cmd_quick_check(file_path: str):
    """أمر الفحص السريع"""
    print("⚡ فحص سريع للمشاكل الشائعة...")
    ai_assistant_workflow(file_path, "quick_check")

def cmd_related(file_path: str, terms_str: str):
    """أمر العثور على المفاهيم المترابطة"""
    terms = [t.strip() for t in terms_str.split(',')]
    helper = AIAssistantHelper()
    if not helper.load_file(file_path):
        return

    print(f"🔗 البحث عن المفاهيم المترابطة: {', '.join(terms)}")
    results = helper.find_related_concepts(terms)

    print(f"\n📍 مواقع المفاهيم:")
    for concept, locations in results['concept_locations'].items():
        if locations:
            print(f"  '{concept}': {len(locations)} مرة في الأسطر {', '.join(map(str, locations[:10]))}")
            if len(locations) > 10:
                print(f"    ... و {len(locations) - 10} موقع آخر")

    related_groups = results['related_groups']
    if related_groups:
        print(f"\n🔗 المجموعات المترابطة ({len(related_groups)}):")

        # تجميع حسب المفاهيم المترابطة
        unique_groups = {}
        for group in related_groups:
            key = tuple(sorted(group['related_concepts']))
            if key not in unique_groups:
                unique_groups[key] = []
            unique_groups[key].append(group)

        for i, (concepts, groups) in enumerate(unique_groups.items(), 1):
            print(f"\n{i}. المفاهيم المترابطة: {', '.join(concepts)}")
            print(f"   عدد السياقات: {len(groups)}")
            print(f"   الأسطر: {', '.join(str(g['center_line']) for g in groups[:5])}")
            if len(groups) > 5:
                print(f"   ... و {len(groups) - 5} سياق آخر")
    else:
        print("\n❌ لم يتم العثور على مفاهيم مترابطة")

def cmd_remove_ai(file_path: str):
    """أمر حذف ردود الذكاء الاصطناعي"""
    helper = AIAssistantHelper()
    if not helper.load_file(file_path):
        return

    print("🤖 تحديد ردود الذكاء الاصطناعي للحذف...")
    removed_sections = helper.remove_ai_responses()

    if removed_sections:
        print(f"📋 الأقسام المحددة للحذف:")
        for i, (start, end) in enumerate(removed_sections[:10], 1):
            print(f"  {i}. الأسطر {start}-{end}")

        if len(removed_sections) > 10:
            print(f"  ... و {len(removed_sections) - 10} قسم آخر")

        # حفظ قائمة بالأقسام المحذوفة
        with open('ai_responses_to_remove.txt', 'w', encoding='utf-8') as f:
            f.write("أقسام ردود الذكاء الاصطناعي المحددة للحذف:\n\n")
            for start, end in removed_sections:
                f.write(f"الأسطر {start}-{end}\n")

        print(f"💾 تم حفظ القائمة في: ai_responses_to_remove.txt")
    else:
        print("✅ لم يتم العثور على ردود ذكاء اصطناعي واضحة")

def cmd_extract_method(file_path: str, method_name: str, keywords_str: str):
    """أمر استخراج طريقة حل محددة"""
    keywords = [k.strip() for k in keywords_str.split(',')]
    helper = AIAssistantHelper()
    if not helper.load_file(file_path):
        return

    print(f"🔬 استخراج طريقة: {method_name}")
    method_data = helper.extract_solution_method(keywords, method_name)

    if method_data['sections']:
        print(f"📋 تم العثور على {method_data['total_sections']} قسم:")

        for i, section in enumerate(method_data['sections'], 1):
            print(f"\n{i}. الأسطر {section['start_line']}-{section['end_line']}:")
            print(f"   الكلمة المفتاحية: {section['trigger_keyword']}")
            print(f"   عدد الكلمات: {section['word_count']}")
            print(f"   عدد الأسطر: {section['line_count']}")

            # عرض بداية النص
            preview = section['text'][:200] + "..." if len(section['text']) > 200 else section['text']
            print(f"   المعاينة: {preview}")

        # مقارنة النسخ
        if len(method_data['sections']) > 1:
            print(f"\n⚖️ مقارنة النسخ...")
            comparison = helper.compare_method_versions(method_data['sections'])

            print(f"📊 التوصية: {comparison['recommendation']}")
            if comparison['recommendation'] == 'keep_best':
                best_section = comparison['sections'][0]
                print(f"🏆 أفضل نسخة: الأسطر {best_section['start_line']}-{best_section['end_line']} (درجة: {best_section['quality_score']:.2f})")
            elif comparison['recommendation'] == 'keep_all':
                print("📝 النسخ مختلفة بما يكفي للاحتفاظ بها جميعاً")
            else:
                print("⚠️ يُنصح بالمراجعة اليدوية")

        # حفظ النتائج
        output_file = f"method_{method_name.replace(' ', '_')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(method_data, f, ensure_ascii=False, indent=2)

        print(f"💾 تم حفظ التفاصيل في: {output_file}")
    else:
        print("❌ لم يتم العثور على أقسام لهذه الطريقة")

def cmd_smart_sort(file_path: str):
    """أمر الفرز الذكي الكامل"""
    print("🧠 بدء الفرز الذكي الكامل...")

    # طرق الحل المعروفة
    solution_methods = {
        'الطيف العددي': ['طيف', 'هاملتوني', 'قيمة ذاتية', 'مشغل'],
        'نظرية RLC': ['rlc', 'مقاومة', 'محاثة', 'سعة', 'دائرة'],
        'التشتت الكمومي': ['تشتت', 'موجة', 'انتشار', 'تداخل'],
        'نظرية هيلبرت': ['هيلبرت', 'فضاء', 'متجه', 'إسقاط'],
        'التحليل الطيفي': ['فورييه', 'تحويل', 'تردد', 'طيف'],
        'النظرية الكمومية': ['كمومي', 'كوانتم', 'ميكانيكا', 'حالة']
    }

    helper = AIAssistantHelper()
    if not helper.load_file(file_path):
        return

    print("1️⃣ حذف ردود الذكاء الاصطناعي...")
    removed_sections = helper.remove_ai_responses()
    print(f"   تم تحديد {len(removed_sections)} قسم للحذف")

    print("\n2️⃣ استخراج طرق الحل...")
    extracted_methods = {}

    for method_name, keywords in solution_methods.items():
        print(f"   🔬 استخراج: {method_name}")
        method_data = helper.extract_solution_method(keywords, method_name)

        if method_data['sections']:
            extracted_methods[method_name] = method_data
            print(f"      ✅ {method_data['total_sections']} قسم")
        else:
            print(f"      ❌ لا توجد أقسام")

    print(f"\n📊 ملخص الفرز:")
    print(f"   ردود الذكاء الاصطناعي: {len(removed_sections)} قسم")
    print(f"   طرق الحل المستخرجة: {len(extracted_methods)}")

    total_extracted_sections = sum(len(data['sections']) for data in extracted_methods.values())
    print(f"   إجمالي الأقسام المستخرجة: {total_extracted_sections}")

    # حفظ النتائج الشاملة
    with open('smart_sort_results.json', 'w', encoding='utf-8') as f:
        import json
        results = {
            'removed_ai_sections': removed_sections,
            'extracted_methods': extracted_methods,
            'summary': {
                'ai_sections_count': len(removed_sections),
                'methods_count': len(extracted_methods),
                'total_sections': total_extracted_sections
            }
        }
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"💾 تم حفظ النتائج الشاملة في: smart_sort_results.json")

def cmd_interactive(file_path: str):
    """أمر الوضع التفاعلي"""
    helper = AIAssistantHelper()
    if helper.load_file(file_path):
        helper.interactive_search()

def main():
    """الدالة الرئيسية"""
    if len(sys.argv) < 2:
        show_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        show_usage()
        return
    
    if len(sys.argv) < 3:
        print("❌ يجب تحديد ملف للمعالجة")
        print("استخدم: python ai_helper_commands.py help للمساعدة")
        return
    
    file_path = sys.argv[2]
    
    if not os.path.exists(file_path):
        print(f"❌ الملف غير موجود: {file_path}")
        return
    
    # تنفيذ الأوامر
    try:
        if command == "find_dups":
            cmd_find_dups(file_path)
        
        elif command == "find_similar":
            threshold = sys.argv[3] if len(sys.argv) > 3 else "0.7"
            cmd_find_similar(file_path, threshold)
        
        elif command == "search":
            if len(sys.argv) < 4:
                print("❌ يجب تحديد مصطلح البحث")
                return
            term = sys.argv[3]
            cmd_search(file_path, term)

        elif command == "search_context":
            if len(sys.argv) < 4:
                print("❌ يجب تحديد مصطلح البحث")
                return
            term = sys.argv[3]
            context_words = sys.argv[4] if len(sys.argv) > 4 else "10"
            cmd_search_context(file_path, term, context_words)
        
        elif command == "search_multi":
            if len(sys.argv) < 4:
                print("❌ يجب تحديد المصطلحات مفصولة بفواصل")
                return
            terms = sys.argv[3]
            cmd_search_multi(file_path, terms)
        
        elif command == "pattern":
            if len(sys.argv) < 4:
                print("❌ يجب تحديد نمط البحث")
                return
            pattern = sys.argv[3]
            cmd_pattern(file_path, pattern)
        
        elif command == "map":
            if len(sys.argv) < 4:
                print("❌ يجب تحديد المصطلحات مفصولة بفواصل")
                return
            terms = sys.argv[3]
            cmd_map(file_path, terms)

        elif command == "related":
            if len(sys.argv) < 4:
                print("❌ يجب تحديد المصطلحات مفصولة بفواصل")
                return
            terms = sys.argv[3]
            cmd_related(file_path, terms)
        
        elif command == "structure":
            cmd_structure(file_path)
        
        elif command == "report":
            cmd_report(file_path)
        
        elif command == "quick_check":
            cmd_quick_check(file_path)
        
        elif command == "remove_ai":
            cmd_remove_ai(file_path)

        elif command == "extract_method":
            if len(sys.argv) < 5:
                print("❌ يجب تحديد اسم الطريقة والكلمات المفتاحية")
                print("مثال: extract_method file.md 'الطيف العددي' 'طيف,هاملتوني,قيمة ذاتية'")
                return
            method_name = sys.argv[3]
            keywords = sys.argv[4]
            cmd_extract_method(file_path, method_name, keywords)

        elif command == "smart_sort":
            cmd_smart_sort(file_path)

        elif command == "interactive":
            cmd_interactive(file_path)

        else:
            print(f"❌ أمر غير معروف: {command}")
            print("استخدم: python ai_helper_commands.py help للمساعدة")
    
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف العملية")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    main()

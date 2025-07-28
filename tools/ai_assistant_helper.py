#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مساعد الذكاء الاصطناعي لفرز وتحليل النصوص
AI Assistant Helper for Text Sorting and Analysis

الغرض: مساعدة الذكاء الاصطناعي في:
1. العثور على التشابهات بين النصوص مع أرقام الأسطر
2. البحث عن أفكار محددة في النصوص الطويلة
3. تحديد مواقع المحتوى المكرر
4. تسهيل عملية الفرز والتنظيم
"""

import re
import json
from typing import List, Dict, Tuple, Set
from difflib import SequenceMatcher
from collections import defaultdict
import hashlib

class AIAssistantHelper:
    """مساعد الذكاء الاصطناعي لفرز النصوص"""
    
    def __init__(self, context_words=10):
        self.file_content = ""
        self.lines = []
        self.similarity_threshold = 0.7
        self.context_words = context_words  # معامل السياق
        
    def load_file(self, file_path: str) -> bool:
        """تحميل ملف للتحليل"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.file_content = f.read()
                self.lines = self.file_content.split('\n')
            print(f"✅ تم تحميل الملف: {file_path}")
            print(f"📊 عدد الأسطر: {len(self.lines)}")
            return True
        except Exception as e:
            print(f"❌ خطأ في تحميل الملف: {e}")
            return False
    
    def find_similar_lines(self, threshold: float = 0.7) -> List[Dict]:
        """العثور على الأسطر المتشابهة مع أرقام الأسطر"""
        print(f"\n🔍 البحث عن التشابهات (عتبة: {threshold})...")
        
        similar_groups = []
        processed_lines = set()
        
        for i, line1 in enumerate(self.lines):
            if i in processed_lines or len(line1.strip()) < 10:
                continue
                
            similar_lines = [(i + 1, line1)]  # رقم السطر (1-based)
            
            for j, line2 in enumerate(self.lines[i+1:], i+1):
                if len(line2.strip()) < 10:
                    continue
                    
                similarity = self._calculate_similarity(line1, line2)
                if similarity >= threshold:
                    similar_lines.append((j + 1, line2))
                    processed_lines.add(j)
            
            if len(similar_lines) > 1:
                similar_groups.append({
                    'similarity_score': max([self._calculate_similarity(similar_lines[0][1], line[1]) 
                                           for line in similar_lines[1:]]),
                    'lines': similar_lines
                })
                processed_lines.add(i)
        
        # ترتيب حسب درجة التشابه
        similar_groups.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        print(f"📋 تم العثور على {len(similar_groups)} مجموعة متشابهة")
        return similar_groups
    
    def search_concept(self, concept: str, context_lines: int = 2) -> List[Dict]:
        """البحث عن مفهوم محدد في النص مع السياق"""
        print(f"\n🔍 البحث عن: '{concept}'")
        
        results = []
        concept_lower = concept.lower()
        
        for i, line in enumerate(self.lines):
            if concept_lower in line.lower():
                # جمع السياق
                start_line = max(0, i - context_lines)
                end_line = min(len(self.lines), i + context_lines + 1)
                
                context = []
                for j in range(start_line, end_line):
                    marker = ">>> " if j == i else "    "
                    context.append(f"{marker}السطر {j+1}: {self.lines[j]}")
                
                results.append({
                    'line_number': i + 1,
                    'content': line,
                    'context': context
                })
        
        print(f"📋 تم العثور على {len(results)} نتيجة")
        return results
    
    def find_duplicates_exact(self) -> List[Dict]:
        """العثور على التكرارات المطابقة تماماً"""
        print(f"\n🔍 البحث عن التكرارات المطابقة...")
        
        line_hash_map = defaultdict(list)
        
        for i, line in enumerate(self.lines):
            cleaned_line = re.sub(r'\s+', ' ', line.strip().lower())
            if len(cleaned_line) > 10:  # تجاهل الأسطر القصيرة
                line_hash = hashlib.md5(cleaned_line.encode()).hexdigest()
                line_hash_map[line_hash].append((i + 1, line))
        
        duplicates = []
        for hash_key, line_list in line_hash_map.items():
            if len(line_list) > 1:
                duplicates.append({
                    'hash': hash_key,
                    'count': len(line_list),
                    'lines': line_list
                })
        
        # ترتيب حسب عدد التكرارات
        duplicates.sort(key=lambda x: x['count'], reverse=True)
        
        print(f"📋 تم العثور على {len(duplicates)} مجموعة مكررة")
        return duplicates
    
    def find_ideas_by_pattern(self, pattern: str) -> List[Dict]:
        """البحث عن الأفكار باستخدام نمط regex"""
        print(f"\n🔍 البحث بالنمط: '{pattern}'")
        
        results = []
        try:
            regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            
            for i, line in enumerate(self.lines):
                matches = regex.finditer(line)
                for match in matches:
                    results.append({
                        'line_number': i + 1,
                        'content': line,
                        'match': match.group(),
                        'start_pos': match.start(),
                        'end_pos': match.end()
                    })
        
        except re.error as e:
            print(f"❌ خطأ في النمط: {e}")
            return []
        
        print(f"📋 تم العثور على {len(results)} نتيجة")
        return results
    
    def analyze_section_structure(self) -> Dict:
        """تحليل هيكل الأقسام والعناوين"""
        print(f"\n📊 تحليل هيكل النص...")
        
        sections = {
            'main_headers': [],      # ###
            'sub_headers': [],       # **text**
            'numbered_items': [],    # 1. 2. 3.
            'bullet_points': [],     # - * •
            'equations': [],         # $$ أو معادلات
            'dates': []             # تواريخ
        }
        
        patterns = {
            'main_headers': r'^#{1,6}\s+(.+)',
            'sub_headers': r'\*\*(.+?)\*\*',
            'numbered_items': r'^\s*\d+\.\s+(.+)',
            'bullet_points': r'^\s*[-*•]\s+(.+)',
            'equations': r'\$\$?.+?\$\$?',
            'dates': r'\d{4}-\d{2}-\d{2}'
        }
        
        for i, line in enumerate(self.lines):
            for section_type, pattern in patterns.items():
                matches = re.finditer(pattern, line)
                for match in matches:
                    sections[section_type].append({
                        'line_number': i + 1,
                        'content': line.strip(),
                        'match': match.group()
                    })
        
        # طباعة الإحصائيات
        for section_type, items in sections.items():
            print(f"  {section_type}: {len(items)} عنصر")
        
        return sections
    
    def generate_line_map(self, search_terms: List[str]) -> Dict:
        """إنشاء خريطة أسطر للمصطلحات المهمة"""
        print(f"\n🗺️ إنشاء خريطة الأسطر...")
        
        line_map = {}
        
        for term in search_terms:
            term_lower = term.lower()
            line_map[term] = []
            
            for i, line in enumerate(self.lines):
                if term_lower in line.lower():
                    line_map[term].append({
                        'line_number': i + 1,
                        'content': line.strip()[:100] + "..." if len(line.strip()) > 100 else line.strip()
                    })
        
        return line_map
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """حساب درجة التشابه بين نصين"""
        # تنظيف النصوص
        clean1 = re.sub(r'[^\w\s]', '', text1.lower().strip())
        clean2 = re.sub(r'[^\w\s]', '', text2.lower().strip())

        if not clean1 or not clean2:
            return 0.0

        return SequenceMatcher(None, clean1, clean2).ratio()

    def _count_words_between_lines(self, line1: int, line2: int) -> int:
        """حساب عدد الكلمات بين سطرين"""
        start_line = min(line1, line2)
        end_line = max(line1, line2)

        word_count = 0
        for i in range(start_line, end_line + 1):
            if i < len(self.lines):
                words = len(self.lines[i].split())
                word_count += words

        return word_count

    def _is_same_context(self, line1: int, line2: int) -> bool:
        """تحديد ما إذا كان السطران في نفس السياق"""
        word_count = self._count_words_between_lines(line1, line2)
        return word_count <= (self.context_words * 2)  # ضعف المعامل للأمان

    def _find_context_boundaries(self, center_line: int) -> Tuple[int, int]:
        """العثور على حدود السياق حول سطر معين"""
        start_line = center_line
        end_line = center_line
        words_before = 0
        words_after = 0

        # البحث للخلف
        for i in range(center_line - 1, -1, -1):
            if i < len(self.lines):
                line_words = len(self.lines[i].split())
                if words_before + line_words <= self.context_words:
                    words_before += line_words
                    start_line = i
                    # التوقف عند العناوين
                    if self.lines[i].strip().startswith('###'):
                        break
                else:
                    break

        # البحث للأمام
        for i in range(center_line + 1, len(self.lines)):
            line_words = len(self.lines[i].split())
            if words_after + line_words <= self.context_words:
                words_after += line_words
                end_line = i
                # التوقف عند العناوين
                if self.lines[i].strip().startswith('###'):
                    break
            else:
                break

        return start_line, end_line

    def search_concept_with_context(self, concept: str) -> List[Dict]:
        """البحث عن مفهوم مع تجميع السياق المترابط"""
        print(f"\n🔍 البحث عن: '{concept}' مع تجميع السياق (معامل: {self.context_words})")

        # العثور على جميع المواقع أولاً
        raw_results = []
        concept_lower = concept.lower()

        for i, line in enumerate(self.lines):
            if concept_lower in line.lower():
                raw_results.append(i)

        if not raw_results:
            print("❌ لم يتم العثور على نتائج")
            return []

        # تجميع المواقع المترابطة
        grouped_results = []
        processed_lines = set()

        for line_num in raw_results:
            if line_num in processed_lines:
                continue

            # العثور على حدود السياق
            start_line, end_line = self._find_context_boundaries(line_num)

            # جمع جميع المواقع في هذا السياق
            context_matches = []
            for other_line in raw_results:
                if start_line <= other_line <= end_line:
                    context_matches.append(other_line)
                    processed_lines.add(other_line)

            # إنشاء السياق الكامل
            context_text = []
            for i in range(start_line, end_line + 1):
                if i < len(self.lines):
                    marker = ">>> " if i in context_matches else "    "
                    context_text.append(f"{marker}السطر {i+1}: {self.lines[i]}")

            grouped_results.append({
                'concept': concept,
                'matches_count': len(context_matches),
                'line_numbers': [l + 1 for l in context_matches],  # تحويل إلى 1-based
                'context_start': start_line + 1,
                'context_end': end_line + 1,
                'context_text': context_text,
                'word_count': self._count_words_between_lines(start_line, end_line)
            })

        print(f"📋 تم العثور على {len(grouped_results)} سياق مترابط")
        return grouped_results

    def analyze_duplicates_with_context(self) -> List[Dict]:
        """تحليل التكرارات مع مراعاة السياق"""
        print(f"\n🔍 تحليل التكرارات مع السياق (معامل: {self.context_words})...")

        duplicates = self.find_duplicates_exact()
        context_analysis = []

        for dup_group in duplicates:
            line_numbers = [line[0] - 1 for line in dup_group['lines']]  # تحويل إلى 0-based

            # تحليل السياق لكل تكرار
            contexts = []
            for line_num in line_numbers:
                start_line, end_line = self._find_context_boundaries(line_num)
                context_info = {
                    'line_number': line_num + 1,
                    'context_start': start_line + 1,
                    'context_end': end_line + 1,
                    'word_count': self._count_words_between_lines(start_line, end_line)
                }
                contexts.append(context_info)

            # تحديد ما إذا كانت التكرارات في نفس السياق
            same_context_groups = []
            processed = set()

            for i, context1 in enumerate(contexts):
                if i in processed:
                    continue

                group = [context1]
                processed.add(i)

                for j, context2 in enumerate(contexts[i+1:], i+1):
                    if j in processed:
                        continue

                    # فحص ما إذا كانا في نفس السياق
                    if self._is_same_context(context1['line_number'] - 1, context2['line_number'] - 1):
                        group.append(context2)
                        processed.add(j)

                same_context_groups.append(group)

            context_analysis.append({
                'content': dup_group['lines'][0][1],
                'total_occurrences': len(dup_group['lines']),
                'context_groups': same_context_groups,
                'analysis': 'same_context' if len(same_context_groups) == 1 else 'different_contexts'
            })

        return context_analysis

    def find_related_concepts(self, concepts: List[str]) -> Dict:
        """العثور على المفاهيم المترابطة في نفس السياق"""
        print(f"\n🔗 البحث عن المفاهيم المترابطة...")

        concept_locations = {}

        # العثور على مواقع كل مفهوم
        for concept in concepts:
            locations = []
            concept_lower = concept.lower()

            for i, line in enumerate(self.lines):
                if concept_lower in line.lower():
                    locations.append(i)

            concept_locations[concept] = locations

        # العثور على المفاهيم المترابطة
        related_groups = []

        for concept1, locations1 in concept_locations.items():
            for location1 in locations1:
                related_in_context = [concept1]
                context_start, context_end = self._find_context_boundaries(location1)

                for concept2, locations2 in concept_locations.items():
                    if concept1 == concept2:
                        continue

                    for location2 in locations2:
                        if context_start <= location2 <= context_end:
                            if concept2 not in related_in_context:
                                related_in_context.append(concept2)

                if len(related_in_context) > 1:
                    related_groups.append({
                        'center_line': location1 + 1,
                        'context_range': (context_start + 1, context_end + 1),
                        'related_concepts': related_in_context,
                        'context_text': [f"السطر {i+1}: {self.lines[i]}"
                                       for i in range(context_start, context_end + 1)
                                       if i < len(self.lines)]
                    })

        return {
            'concept_locations': {k: [l+1 for l in v] for k, v in concept_locations.items()},
            'related_groups': related_groups
        }

    def remove_ai_responses(self) -> List[Tuple[int, int]]:
        """حذف ردود وتعليقات الذكاء الاصطناعي"""
        print(f"\n🤖 حذف ردود الذكاء الاصطناعي...")

        ai_patterns = [
            r'ممتاز!',
            r'رائع!',
            r'فكرة عبقرية',
            r'هذا تطوير مذهل',
            r'أفهم تماماً',
            r'دعني أ',
            r'سأقوم ب',
            r'الآن سأ',
            r'ممكن أن أ',
            r'يمكنني أن أ',
            r'✅.*تم',
            r'📊.*النتائج',
            r'🎯.*الهدف',
            r'💡.*فكرة',
            r'🔍.*البحث',
            r'## 📊.*تقرير',
            r'### ✅.*ما تم',
            r'### 🎯.*الهدف'
        ]

        removed_sections = []
        lines_to_remove = set()

        for i, line in enumerate(self.lines):
            line_lower = line.lower().strip()

            # فحص الأنماط
            for pattern in ai_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # تحديد حدود القسم للحذف
                    start_line = i
                    end_line = i

                    # البحث عن نهاية القسم
                    for j in range(i + 1, min(i + 20, len(self.lines))):
                        next_line = self.lines[j].strip()
                        # التوقف عند عنوان جديد أو فقرة جديدة
                        if (next_line.startswith('###') and
                            not any(re.search(p, next_line, re.IGNORECASE) for p in ai_patterns)):
                            break
                        if (next_line.startswith('**') and
                            not any(re.search(p, next_line, re.IGNORECASE) for p in ai_patterns)):
                            break
                        end_line = j

                    # إضافة الأسطر للحذف
                    for k in range(start_line, end_line + 1):
                        lines_to_remove.add(k)

                    removed_sections.append((start_line + 1, end_line + 1))
                    break

        print(f"📋 تم تحديد {len(removed_sections)} قسم للحذف")
        return removed_sections

    def extract_solution_method(self, keywords: List[str], method_name: str) -> Dict:
        """استخراج طريقة حل محددة بالكلمات المفتاحية"""
        print(f"\n🔬 استخراج طريقة: {method_name}")
        print(f"🔑 الكلمات المفتاحية: {', '.join(keywords)}")

        method_sections = []
        processed_lines = set()

        for keyword in keywords:
            keyword_lower = keyword.lower()

            for i, line in enumerate(self.lines):
                if i in processed_lines:
                    continue

                if keyword_lower in line.lower():
                    # العثور على حدود القسم
                    start_line, end_line = self._find_method_boundaries(i, keywords)

                    # جمع النص
                    section_text = []
                    for j in range(start_line, end_line + 1):
                        if j < len(self.lines):
                            section_text.append(self.lines[j])
                            processed_lines.add(j)

                    method_sections.append({
                        'start_line': start_line + 1,
                        'end_line': end_line + 1,
                        'trigger_keyword': keyword,
                        'text': '\n'.join(section_text),
                        'word_count': len(' '.join(section_text).split()),
                        'line_count': len(section_text)
                    })

        return {
            'method_name': method_name,
            'keywords': keywords,
            'sections': method_sections,
            'total_sections': len(method_sections)
        }

    def _find_method_boundaries(self, center_line: int, keywords: List[str]) -> Tuple[int, int]:
        """العثور على حدود طريقة الحل"""
        start_line = center_line
        end_line = center_line

        # البحث للخلف حتى عنوان أو بداية طريقة أخرى
        for i in range(center_line - 1, max(0, center_line - 50), -1):
            line = self.lines[i].strip()

            # التوقف عند العناوين الرئيسية
            if line.startswith('###') or line.startswith('##'):
                start_line = i + 1
                break

            # التوقف عند كلمات مفتاحية لطرق أخرى
            if any(kw.lower() in line.lower() for kw in keywords):
                start_line = i
            else:
                start_line = i

        # البحث للأمام حتى عنوان أو بداية طريقة أخرى
        for i in range(center_line + 1, min(len(self.lines), center_line + 50)):
            line = self.lines[i].strip()

            # التوقف عند العناوين الرئيسية
            if line.startswith('###') or line.startswith('##'):
                end_line = i - 1
                break

            # التوقف عند كلمات مفتاحية لطرق أخرى
            if any(kw.lower() in line.lower() for kw in keywords):
                end_line = i
            else:
                end_line = i

        return start_line, end_line

    def compare_method_versions(self, sections: List[Dict]) -> Dict:
        """مقارنة نسخ مختلفة من نفس طريقة الحل"""
        print(f"\n⚖️ مقارنة {len(sections)} نسخة من الطريقة...")

        if len(sections) <= 1:
            return {'recommendation': 'keep_all', 'sections': sections}

        # حساب درجات الجودة
        scored_sections = []
        for section in sections:
            score = self._calculate_quality_score(section)
            scored_sections.append({**section, 'quality_score': score})

        # ترتيب حسب الجودة
        scored_sections.sort(key=lambda x: x['quality_score'], reverse=True)

        # تحليل التشابه
        similarity_matrix = []
        for i, sec1 in enumerate(scored_sections):
            row = []
            for j, sec2 in enumerate(scored_sections):
                if i == j:
                    row.append(1.0)
                else:
                    similarity = self._calculate_similarity(sec1['text'], sec2['text'])
                    row.append(similarity)
            similarity_matrix.append(row)

        # تحديد التوصية
        max_similarity = max(max(row) for row in similarity_matrix if len(row) > 1)

        if max_similarity > 0.8:
            recommendation = 'keep_best'  # متشابهة جداً، احتفظ بالأفضل
        elif max_similarity > 0.5:
            recommendation = 'review_manual'  # متشابهة نوعاً ما، مراجعة يدوية
        else:
            recommendation = 'keep_all'  # مختلفة، احتفظ بالكل

        return {
            'recommendation': recommendation,
            'sections': scored_sections,
            'similarity_matrix': similarity_matrix,
            'max_similarity': max_similarity
        }

    def _calculate_quality_score(self, section: Dict) -> float:
        """حساب درجة جودة القسم"""
        score = 0.0
        text = section['text']

        # نقاط للطول (المحتوى المفصل أفضل)
        score += min(section['word_count'] / 100, 5.0)

        # نقاط للمعادلات
        equations = len(re.findall(r'\$.*?\$|\\\[.*?\\\]', text))
        score += equations * 2.0

        # نقاط للتنظيم (عناوين فرعية)
        headers = len(re.findall(r'\*\*.*?\*\*', text))
        score += headers * 1.0

        # نقاط للأمثلة والتطبيقات
        examples = len(re.findall(r'مثال|تطبيق|حالة', text, re.IGNORECASE))
        score += examples * 1.5

        # نقاط للوضوح (جمل قصيرة ومفهومة)
        sentences = text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        if 10 <= avg_sentence_length <= 25:  # طول مثالي
            score += 2.0

        return score
    
    def interactive_search(self):
        """وضع البحث التفاعلي"""
        print("\n🎯 وضع البحث التفاعلي")
        print("الأوامر المتاحة:")
        print("  search <مصطلح>     - البحث عن مصطلح")
        print("  similar <عتبة>      - العثور على التشابهات")
        print("  duplicates          - العثور على التكرارات")
        print("  structure           - تحليل الهيكل")
        print("  pattern <نمط>       - البحث بنمط regex")
        print("  map <مصطلح1,مصطلح2> - خريطة المصطلحات")
        print("  quit                - خروج")
        
        while True:
            try:
                command = input("\n🔍 أدخل الأمر: ").strip()
                
                if command.lower() == 'quit':
                    break
                
                parts = command.split(' ', 1)
                cmd = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""
                
                if cmd == 'search' and arg:
                    results = self.search_concept(arg)
                    self._display_search_results(results)
                
                elif cmd == 'similar':
                    threshold = float(arg) if arg else 0.7
                    results = self.find_similar_lines(threshold)
                    self._display_similarity_results(results)
                
                elif cmd == 'duplicates':
                    results = self.find_duplicates_exact()
                    self._display_duplicate_results(results)
                
                elif cmd == 'structure':
                    structure = self.analyze_section_structure()
                    self._display_structure_results(structure)
                
                elif cmd == 'pattern' and arg:
                    results = self.find_ideas_by_pattern(arg)
                    self._display_pattern_results(results)
                
                elif cmd == 'map' and arg:
                    terms = [t.strip() for t in arg.split(',')]
                    line_map = self.generate_line_map(terms)
                    self._display_line_map(line_map)
                
                else:
                    print("❌ أمر غير صحيح أو مصطلح مفقود")
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ خطأ: {e}")
    
    def _display_search_results(self, results: List[Dict]):
        """عرض نتائج البحث"""
        if not results:
            print("❌ لم يتم العثور على نتائج")
            return
        
        print(f"\n📋 النتائج ({len(results)}):")
        for i, result in enumerate(results[:10]):  # أول 10 نتائج
            print(f"\n{i+1}. السطر {result['line_number']}:")
            for context_line in result['context']:
                print(f"  {context_line}")
    
    def _display_similarity_results(self, results: List[Dict]):
        """عرض نتائج التشابه"""
        if not results:
            print("❌ لم يتم العثور على تشابهات")
            return
        
        print(f"\n📋 التشابهات ({len(results)}):")
        for i, group in enumerate(results[:5]):  # أول 5 مجموعات
            print(f"\n{i+1}. مجموعة متشابهة (درجة: {group['similarity_score']:.2f}):")
            for line_num, content in group['lines']:
                print(f"  السطر {line_num}: {content[:100]}...")
    
    def _display_duplicate_results(self, results: List[Dict]):
        """عرض نتائج التكرارات"""
        if not results:
            print("❌ لم يتم العثور على تكرارات")
            return
        
        print(f"\n📋 التكرارات ({len(results)}):")
        for i, dup in enumerate(results[:5]):  # أول 5 مجموعات
            print(f"\n{i+1}. مكرر {dup['count']} مرات:")
            for line_num, content in dup['lines']:
                print(f"  السطر {line_num}: {content[:100]}...")
    
    def _display_structure_results(self, structure: Dict):
        """عرض نتائج تحليل الهيكل"""
        print(f"\n📊 هيكل النص:")
        for section_type, items in structure.items():
            if items:
                print(f"\n{section_type} ({len(items)}):")
                for item in items[:5]:  # أول 5 عناصر
                    print(f"  السطر {item['line_number']}: {item['match']}")
    
    def _display_pattern_results(self, results: List[Dict]):
        """عرض نتائج البحث بالنمط"""
        if not results:
            print("❌ لم يتم العثور على نتائج")
            return
        
        print(f"\n📋 نتائج النمط ({len(results)}):")
        for i, result in enumerate(results[:10]):
            print(f"{i+1}. السطر {result['line_number']}: {result['match']}")
    
    def _display_line_map(self, line_map: Dict):
        """عرض خريطة الأسطر"""
        print(f"\n🗺️ خريطة المصطلحات:")
        for term, locations in line_map.items():
            print(f"\n'{term}' ({len(locations)} مرة):")
            for loc in locations[:5]:  # أول 5 مواقع
                print(f"  السطر {loc['line_number']}: {loc['content']}")

def main():
    """الدالة الرئيسية"""
    print("🤖 مساعد الذكاء الاصطناعي لفرز النصوص")
    print("=" * 50)
    
    helper = AIAssistantHelper()
    
    # تحميل ملف
    file_path = input("📁 أدخل مسار الملف: ").strip()
    if not file_path:
        file_path = "riemann_research_ideas.md"  # افتراضي
    
    if helper.load_file(file_path):
        helper.interactive_search()
    else:
        print("❌ فشل في تحميل الملف")

class QuickAssistant:
    """مساعد سريع للمهام الشائعة"""

    @staticmethod
    def quick_find_duplicates(file_path: str) -> str:
        """بحث سريع عن التكرارات مع تقرير مختصر"""
        helper = AIAssistantHelper()
        if not helper.load_file(file_path):
            return "❌ فشل في تحميل الملف"

        duplicates = helper.find_duplicates_exact()

        report = f"📊 تقرير التكرارات السريع:\n"
        report += f"عدد المجموعات المكررة: {len(duplicates)}\n\n"

        for i, dup in enumerate(duplicates[:10]):  # أول 10
            report += f"{i+1}. مكرر {dup['count']} مرات في الأسطر: "
            line_numbers = [str(line[0]) for line in dup['lines']]
            report += ", ".join(line_numbers) + "\n"
            report += f"   المحتوى: {dup['lines'][0][1][:80]}...\n\n"

        return report

    @staticmethod
    def quick_search_multiple(file_path: str, terms: List[str]) -> str:
        """بحث سريع عن عدة مصطلحات"""
        helper = AIAssistantHelper()
        if not helper.load_file(file_path):
            return "❌ فشل في تحميل الملف"

        report = f"🔍 تقرير البحث المتعدد:\n\n"

        for term in terms:
            results = helper.search_concept(term, context_lines=0)
            report += f"'{term}': {len(results)} نتيجة في الأسطر "
            if results:
                line_numbers = [str(r['line_number']) for r in results[:10]]
                report += ", ".join(line_numbers)
            else:
                report += "لا توجد نتائج"
            report += "\n"

        return report

    @staticmethod
    def quick_similarity_check(file_path: str, threshold: float = 0.8) -> str:
        """فحص سريع للتشابهات العالية"""
        helper = AIAssistantHelper()
        if not helper.load_file(file_path):
            return "❌ فشل في تحميل الملف"

        similar_groups = helper.find_similar_lines(threshold)

        report = f"🔍 تقرير التشابهات (عتبة {threshold}):\n"
        report += f"عدد المجموعات المتشابهة: {len(similar_groups)}\n\n"

        for i, group in enumerate(similar_groups[:5]):
            report += f"{i+1}. تشابه {group['similarity_score']:.2f} في الأسطر: "
            line_numbers = [str(line[0]) for line in group['lines']]
            report += ", ".join(line_numbers) + "\n"

        return report

def quick_help_commands():
    """أوامر المساعدة السريعة للذكاء الاصطناعي"""
    commands = {
        'find_dups': 'البحث عن التكرارات المطابقة',
        'find_similar': 'البحث عن التشابهات',
        'search_terms': 'البحث عن مصطلحات متعددة',
        'analyze_structure': 'تحليل هيكل النص',
        'line_map': 'خريطة المصطلحات مع أرقام الأسطر'
    }

    print("🤖 أوامر المساعدة السريعة:")
    for cmd, desc in commands.items():
        print(f"  {cmd}: {desc}")

def ai_assistant_workflow(file_path: str, task: str = "full_analysis"):
    """سير عمل مخصص لمساعدة الذكاء الاصطناعي"""

    print(f"🤖 بدء سير العمل: {task}")
    print("=" * 50)

    helper = AIAssistantHelper()
    if not helper.load_file(file_path):
        return

    if task == "full_analysis":
        # تحليل شامل
        print("1️⃣ البحث عن التكرارات...")
        duplicates = helper.find_duplicates_exact()

        print("2️⃣ البحث عن التشابهات...")
        similarities = helper.find_similar_lines(0.7)

        print("3️⃣ تحليل الهيكل...")
        structure = helper.analyze_section_structure()

        print("4️⃣ خريطة المصطلحات المهمة...")
        important_terms = ['هاملتوني', 'طيف', 'فرضية ريمان', 'برهان', 'نظرية']
        line_map = helper.generate_line_map(important_terms)

        # تقرير موجز
        print(f"\n📊 التقرير الموجز:")
        print(f"  التكرارات: {len(duplicates)} مجموعة")
        print(f"  التشابهات: {len(similarities)} مجموعة")
        print(f"  العناوين الرئيسية: {len(structure['main_headers'])}")
        print(f"  المعادلات: {len(structure['equations'])}")

        # حفظ التقرير
        report = generate_ai_report(duplicates, similarities, structure, line_map)
        with open('ai_assistant_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"💾 تم حفظ التقرير في: ai_assistant_report.txt")

    elif task == "quick_check":
        # فحص سريع
        print("⚡ فحص سريع للمشاكل الشائعة...")

        duplicates = helper.find_duplicates_exact()
        if duplicates:
            print(f"⚠️  تم العثور على {len(duplicates)} مجموعة مكررة")
            for i, dup in enumerate(duplicates[:3]):
                line_nums = [str(line[0]) for line in dup['lines']]
                print(f"  {i+1}. الأسطر: {', '.join(line_nums)}")

        similarities = helper.find_similar_lines(0.8)
        if similarities:
            print(f"⚠️  تم العثور على {len(similarities)} تشابه عالي")
            for i, sim in enumerate(similarities[:3]):
                line_nums = [str(line[0]) for line in sim['lines']]
                print(f"  {i+1}. الأسطر: {', '.join(line_nums)} (تشابه: {sim['similarity_score']:.2f})")

def generate_ai_report(duplicates, similarities, structure, line_map):
    """إنتاج تقرير شامل للذكاء الاصطناعي"""

    report = "🤖 تقرير مساعد الذكاء الاصطناعي\n"
    report += "=" * 50 + "\n\n"

    # التكرارات
    report += "📋 التكرارات المطابقة:\n"
    if duplicates:
        for i, dup in enumerate(duplicates[:10]):
            line_nums = [str(line[0]) for line in dup['lines']]
            report += f"{i+1}. الأسطر {', '.join(line_nums)}: {dup['lines'][0][1][:100]}...\n"
    else:
        report += "لا توجد تكرارات مطابقة\n"

    report += "\n" + "="*30 + "\n\n"

    # التشابهات
    report += "🔍 التشابهات العالية:\n"
    if similarities:
        for i, sim in enumerate(similarities[:10]):
            line_nums = [str(line[0]) for line in sim['lines']]
            report += f"{i+1}. الأسطر {', '.join(line_nums)} (تشابه: {sim['similarity_score']:.2f})\n"
    else:
        report += "لا توجد تشابهات عالية\n"

    report += "\n" + "="*30 + "\n\n"

    # خريطة المصطلحات
    report += "🗺️ خريطة المصطلحات المهمة:\n"
    for term, locations in line_map.items():
        if locations:
            line_nums = [str(loc['line_number']) for loc in locations]
            report += f"'{term}': الأسطر {', '.join(line_nums[:10])}\n"

    return report

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        file_path = sys.argv[2] if len(sys.argv) > 2 else "riemann_research_ideas.md"

        if command == "quick_dups":
            print(QuickAssistant.quick_find_duplicates(file_path))
        elif command == "quick_similar":
            print(QuickAssistant.quick_similarity_check(file_path))
        elif command == "workflow":
            task = sys.argv[3] if len(sys.argv) > 3 else "full_analysis"
            ai_assistant_workflow(file_path, task)
        elif command == "help":
            quick_help_commands()
        else:
            print("أوامر متاحة: quick_dups, quick_similar, workflow, help")
    else:
        main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام معالجة النصوص العلمية الذكي
Intelligent Scientific Text Processing System

المؤلف: باسل يحيى عبدالله
التاريخ: 2025-07-26
الغرض: معالجة وتنظيم النصوص العلمية العربية تلقائياً
"""

import re
import json
import hashlib
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
import logging

# إعداد نظام السجلات
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ScientificIdea:
    """فئة لتمثيل فكرة علمية"""
    id: str
    title: str
    content: str
    category: str
    date: str
    equations: List[str]
    keywords: List[str]
    similarity_hash: str
    importance_score: float

class ArabicScientificTextProcessor:
    """معالج النصوص العلمية العربية المتقدم"""
    
    def __init__(self):
        self.ideas_database = {}
        self.categories = {
            'نظرية': ['نظرية', 'مبرهنة', 'قانون', 'مبدأ'],
            'معادلة': ['معادلة', 'صيغة', 'تعبير رياضي'],
            'برهان': ['برهان', 'إثبات', 'دليل', 'استنتاج'],
            'تطبيق': ['تطبيق', 'مثال', 'حالة خاصة'],
            'تحليل': ['تحليل', 'دراسة', 'فحص', 'تقييم'],
            'خلاصة': ['خلاصة', 'نتيجة', 'استنتاج نهائي']
        }
        self.equation_patterns = [
            r'\$\$.*?\$\$',  # LaTeX display equations
            r'\$.*?\$',      # LaTeX inline equations
            r'\\begin\{.*?\}.*?\\end\{.*?\}',  # LaTeX environments
            r'[A-Za-z]+\s*=\s*[^،\.]+',  # Simple equations
        ]
        
    def extract_equations(self, text: str) -> List[str]:
        """استخراج المعادلات من النص"""
        equations = []
        for pattern in self.equation_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            equations.extend(matches)
        return equations
    
    def extract_keywords(self, text: str) -> List[str]:
        """استخراج الكلمات المفتاحية العلمية"""
        scientific_keywords = [
            'هاملتوني', 'طيف', 'قيمة ذاتية', 'دالة زيتا', 'فرضية ريمان',
            'مشغل هيرميتي', 'تناظر', 'انحلال', 'كمومي', 'ديناميكا',
            'أعداد أولية', 'توزيع', 'تحليل', 'برهان', 'نظرية'
        ]
        
        found_keywords = []
        text_lower = text.lower()
        for keyword in scientific_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def calculate_similarity_hash(self, content: str) -> str:
        """حساب هاش التشابه للمحتوى"""
        # إزالة الرموز والمسافات الزائدة
        cleaned = re.sub(r'[^\w\s]', '', content)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
        return hashlib.md5(cleaned.encode('utf-8')).hexdigest()
    
    def calculate_importance_score(self, idea: ScientificIdea) -> float:
        """حساب درجة أهمية الفكرة"""
        score = 0.0
        
        # نقاط للمعادلات
        score += len(idea.equations) * 2.0
        
        # نقاط للكلمات المفتاحية
        score += len(idea.keywords) * 1.5
        
        # نقاط لطول المحتوى (المحتوى المفصل أهم)
        score += min(len(idea.content) / 100, 5.0)
        
        # نقاط إضافية للفئات المهمة
        important_categories = ['نظرية', 'برهان', 'معادلة']
        if idea.category in important_categories:
            score += 3.0
            
        return score
    
    def categorize_idea(self, content: str) -> str:
        """تصنيف الفكرة حسب المحتوى"""
        content_lower = content.lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword in content_lower:
                    return category
        
        return 'عام'
    
    def parse_idea_block(self, block: str) -> ScientificIdea:
        """تحليل كتلة نص لاستخراج فكرة علمية"""
        lines = block.strip().split('\n')
        
        # استخراج العنوان (السطر الأول عادة)
        title = lines[0].strip('#* ').strip()
        
        # استخراج التاريخ
        date_match = re.search(r'التاريخ.*?(\d{4}-\d{2}-\d{2})', block)
        date = date_match.group(1) if date_match else "2025-07-26"
        
        # استخراج المحتوى
        content = '\n'.join(lines[1:]).strip()
        
        # استخراج المعادلات
        equations = self.extract_equations(content)
        
        # استخراج الكلمات المفتاحية
        keywords = self.extract_keywords(content)
        
        # تصنيف الفكرة
        category = self.categorize_idea(content)
        
        # حساب هاش التشابه
        similarity_hash = self.calculate_similarity_hash(content)
        
        # إنشاء معرف فريد
        idea_id = f"idea_{len(self.ideas_database) + 1:03d}"
        
        idea = ScientificIdea(
            id=idea_id,
            title=title,
            content=content,
            category=category,
            date=date,
            equations=equations,
            keywords=keywords,
            similarity_hash=similarity_hash,
            importance_score=0.0
        )
        
        # حساب درجة الأهمية
        idea.importance_score = self.calculate_importance_score(idea)
        
        return idea
    
    def detect_duplicates(self, new_idea: ScientificIdea, threshold: float = 0.8) -> List[str]:
        """كشف الأفكار المكررة"""
        duplicates = []
        
        for existing_id, existing_idea in self.ideas_database.items():
            # مقارنة الهاش
            if new_idea.similarity_hash == existing_idea.similarity_hash:
                duplicates.append(existing_id)
                continue
            
            # مقارنة المحتوى
            similarity = self.calculate_content_similarity(new_idea.content, existing_idea.content)
            if similarity > threshold:
                duplicates.append(existing_id)
        
        return duplicates
    
    def calculate_content_similarity(self, content1: str, content2: str) -> float:
        """حساب تشابه المحتوى بطريقة بسيطة"""
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if len(union) == 0:
            return 0.0
        
        return len(intersection) / len(union)
    
    def process_text_file(self, file_path: str) -> Dict[str, List[ScientificIdea]]:
        """معالجة ملف نصي كامل"""
        logger.info(f"بدء معالجة الملف: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            logger.error(f"خطأ في قراءة الملف: {e}")
            return {}
        
        # تقسيم النص إلى كتل الأفكار
        idea_blocks = self.split_into_idea_blocks(content)
        
        results = {
            'new_ideas': [],
            'duplicates': [],
            'updated_ideas': []
        }
        
        for block in idea_blocks:
            if not block.strip():
                continue
                
            try:
                idea = self.parse_idea_block(block)
                duplicates = self.detect_duplicates(idea)
                
                if duplicates:
                    # التعامل مع التكرارات
                    best_duplicate = self.find_best_version(idea, duplicates)
                    if best_duplicate:
                        results['duplicates'].append({
                            'new': idea,
                            'existing': best_duplicate,
                            'action': 'keep_existing' if best_duplicate.importance_score > idea.importance_score else 'replace'
                        })
                else:
                    # فكرة جديدة
                    self.ideas_database[idea.id] = idea
                    results['new_ideas'].append(idea)
                    
            except Exception as e:
                logger.error(f"خطأ في معالجة كتلة الفكرة: {e}")
                continue
        
        logger.info(f"تم العثور على {len(results['new_ideas'])} فكرة جديدة")
        logger.info(f"تم العثور على {len(results['duplicates'])} تكرار")
        
        return results
    
    def split_into_idea_blocks(self, content: str) -> List[str]:
        """تقسيم النص إلى كتل الأفكار"""
        # البحث عن أنماط بداية الأفكار
        idea_patterns = [
            r'###\s+.*?\(\d+\)',  # ### عنوان الفكرة (رقم)
            r'\*\*.*?\(\d+\)\*\*',  # **عنوان الفكرة (رقم)**
            r'\d+\.\s+\*\*.*?\*\*',  # 1. **عنوان الفكرة**
        ]
        
        blocks = []
        current_block = ""
        
        lines = content.split('\n')
        
        for line in lines:
            is_new_idea = False
            
            for pattern in idea_patterns:
                if re.match(pattern, line.strip()):
                    is_new_idea = True
                    break
            
            if is_new_idea and current_block.strip():
                blocks.append(current_block.strip())
                current_block = line + '\n'
            else:
                current_block += line + '\n'
        
        # إضافة الكتلة الأخيرة
        if current_block.strip():
            blocks.append(current_block.strip())
        
        return blocks
    
    def find_best_version(self, new_idea: ScientificIdea, duplicate_ids: List[str]) -> ScientificIdea:
        """العثور على أفضل نسخة من الفكرة المكررة"""
        best_idea = new_idea
        best_score = new_idea.importance_score
        
        for dup_id in duplicate_ids:
            existing_idea = self.ideas_database[dup_id]
            if existing_idea.importance_score > best_score:
                best_idea = existing_idea
                best_score = existing_idea.importance_score
        
        return best_idea
    
    def generate_organized_output(self, output_file: str):
        """إنتاج ملف منظم للأفكار"""
        # ترتيب الأفكار حسب الفئة والأهمية
        categorized_ideas = defaultdict(list)
        
        for idea in self.ideas_database.values():
            categorized_ideas[idea.category].append(idea)
        
        # ترتيب كل فئة حسب الأهمية
        for category in categorized_ideas:
            categorized_ideas[category].sort(key=lambda x: x.importance_score, reverse=True)
        
        # كتابة الملف المنظم
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# الأفكار العلمية المنظمة\n")
            f.write(f"## إجمالي الأفكار: {len(self.ideas_database)}\n\n")
            
            for category, ideas in categorized_ideas.items():
                f.write(f"## فئة: {category} ({len(ideas)} فكرة)\n\n")
                
                for idea in ideas:
                    f.write(f"### {idea.title} ({idea.id})\n")
                    f.write(f"**التاريخ:** {idea.date}\n")
                    f.write(f"**الفئة:** {idea.category}\n")
                    f.write(f"**درجة الأهمية:** {idea.importance_score:.2f}\n")
                    
                    if idea.keywords:
                        f.write(f"**الكلمات المفتاحية:** {', '.join(idea.keywords)}\n")
                    
                    if idea.equations:
                        f.write(f"**المعادلات:** {len(idea.equations)} معادلة\n")
                    
                    f.write(f"\n{idea.content}\n\n")
                    f.write("---\n\n")
        
        logger.info(f"تم إنشاء الملف المنظم: {output_file}")
    
    def save_database(self, file_path: str):
        """حفظ قاعدة بيانات الأفكار"""
        data = {}
        for idea_id, idea in self.ideas_database.items():
            data[idea_id] = {
                'id': idea.id,
                'title': idea.title,
                'content': idea.content,
                'category': idea.category,
                'date': idea.date,
                'equations': idea.equations,
                'keywords': idea.keywords,
                'similarity_hash': idea.similarity_hash,
                'importance_score': idea.importance_score
            }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"تم حفظ قاعدة البيانات: {file_path}")
    
    def load_database(self, file_path: str):
        """تحميل قاعدة بيانات الأفكار"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for idea_id, idea_data in data.items():
                idea = ScientificIdea(**idea_data)
                self.ideas_database[idea_id] = idea
            
            logger.info(f"تم تحميل {len(self.ideas_database)} فكرة من قاعدة البيانات")
            
        except Exception as e:
            logger.error(f"خطأ في تحميل قاعدة البيانات: {e}")

def main():
    """الدالة الرئيسية للاختبار"""
    processor = ArabicScientificTextProcessor()
    
    # معالجة ملف الأفكار
    results = processor.process_text_file('riemann_research_ideas.md')
    
    # إنتاج تقرير
    print(f"تم العثور على {len(results['new_ideas'])} فكرة جديدة")
    print(f"تم العثور على {len(results['duplicates'])} تكرار")
    
    # حفظ النتائج
    processor.generate_organized_output('organized_ideas.md')
    processor.save_database('ideas_database.json')

class AdvancedTextAnalyzer:
    """محلل النصوص المتقدم مع الذكاء الاصطناعي"""

    def __init__(self):
        self.processor = ArabicScientificTextProcessor()

    def install_dependencies(self):
        """تثبيت المكتبات المطلوبة"""
        import subprocess
        import sys

        packages = [
            'scikit-learn',
            'numpy',
            'matplotlib',
            'seaborn',
            'wordcloud',
            'arabic-reshaper',
            'python-bidi'
        ]

        for package in packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                logger.info(f"تم تثبيت {package} بنجاح")
            except Exception as e:
                logger.error(f"فشل في تثبيت {package}: {e}")

    def advanced_similarity_analysis(self, ideas: List[ScientificIdea]) -> Dict:
        """تحليل التشابه المتقدم باستخدام TF-IDF"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np

            # استخراج النصوص
            texts = [idea.content for idea in ideas]

            # إنشاء مصفوفة TF-IDF
            vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words=None,  # يمكن إضافة كلمات الإيقاف العربية
                ngram_range=(1, 2)
            )

            tfidf_matrix = vectorizer.fit_transform(texts)

            # حساب مصفوفة التشابه
            similarity_matrix = cosine_similarity(tfidf_matrix)

            # العثور على الأزواج المتشابهة
            similar_pairs = []
            threshold = 0.7

            for i in range(len(ideas)):
                for j in range(i + 1, len(ideas)):
                    similarity = similarity_matrix[i][j]
                    if similarity > threshold:
                        similar_pairs.append({
                            'idea1': ideas[i],
                            'idea2': ideas[j],
                            'similarity': similarity
                        })

            return {
                'similarity_matrix': similarity_matrix,
                'similar_pairs': similar_pairs,
                'vectorizer': vectorizer
            }

        except ImportError:
            logger.warning("مكتبة scikit-learn غير متوفرة. يرجى تثبيتها أولاً.")
            return {}

    def generate_word_cloud(self, ideas: List[ScientificIdea], output_file: str):
        """إنتاج سحابة كلمات للأفكار"""
        try:
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt
            import arabic_reshaper
            from bidi.algorithm import get_display

            # جمع كل النصوص
            all_text = ' '.join([idea.content for idea in ideas])

            # معالجة النص العربي
            reshaped_text = arabic_reshaper.reshape(all_text)
            bidi_text = get_display(reshaped_text)

            # إنشاء سحابة الكلمات
            wordcloud = WordCloud(
                width=1200,
                height=800,
                background_color='white',
                max_words=100,
                font_path='NotoSansArabic-Regular.ttf',  # يحتاج خط عربي
                colormap='viridis'
            ).generate(bidi_text)

            # حفظ الصورة
            plt.figure(figsize=(15, 10))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('سحابة كلمات الأفكار العلمية', fontsize=16)
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()

            logger.info(f"تم إنشاء سحابة الكلمات: {output_file}")

        except ImportError:
            logger.warning("مكتبات سحابة الكلمات غير متوفرة")

    def generate_statistics_report(self, ideas: List[ScientificIdea]) -> Dict:
        """إنتاج تقرير إحصائي شامل"""
        stats = {
            'total_ideas': len(ideas),
            'categories': {},
            'equations_count': 0,
            'keywords_frequency': {},
            'importance_distribution': [],
            'monthly_distribution': {}
        }

        for idea in ideas:
            # إحصائيات الفئات
            if idea.category not in stats['categories']:
                stats['categories'][idea.category] = 0
            stats['categories'][idea.category] += 1

            # عدد المعادلات
            stats['equations_count'] += len(idea.equations)

            # تكرار الكلمات المفتاحية
            for keyword in idea.keywords:
                if keyword not in stats['keywords_frequency']:
                    stats['keywords_frequency'][keyword] = 0
                stats['keywords_frequency'][keyword] += 1

            # توزيع الأهمية
            stats['importance_distribution'].append(idea.importance_score)

            # التوزيع الشهري
            month = idea.date[:7]  # YYYY-MM
            if month not in stats['monthly_distribution']:
                stats['monthly_distribution'][month] = 0
            stats['monthly_distribution'][month] += 1

        return stats

    def create_visual_dashboard(self, ideas: List[ScientificIdea], output_dir: str):
        """إنشاء لوحة تحكم بصرية"""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            import numpy as np
            import os

            # إنشاء مجلد الإخراج
            os.makedirs(output_dir, exist_ok=True)

            # إعداد الخطوط العربية
            plt.rcParams['font.family'] = ['Arial Unicode MS', 'Tahoma', 'DejaVu Sans']

            stats = self.generate_statistics_report(ideas)

            # 1. رسم بياني للفئات
            plt.figure(figsize=(12, 8))
            categories = list(stats['categories'].keys())
            counts = list(stats['categories'].values())

            plt.subplot(2, 2, 1)
            plt.pie(counts, labels=categories, autopct='%1.1f%%', startangle=90)
            plt.title('توزيع الأفكار حسب الفئة')

            # 2. توزيع درجات الأهمية
            plt.subplot(2, 2, 2)
            plt.hist(stats['importance_distribution'], bins=20, alpha=0.7, color='skyblue')
            plt.xlabel('درجة الأهمية')
            plt.ylabel('عدد الأفكار')
            plt.title('توزيع درجات الأهمية')

            # 3. أهم الكلمات المفتاحية
            plt.subplot(2, 2, 3)
            top_keywords = sorted(stats['keywords_frequency'].items(),
                                key=lambda x: x[1], reverse=True)[:10]
            keywords, frequencies = zip(*top_keywords)

            plt.barh(range(len(keywords)), frequencies)
            plt.yticks(range(len(keywords)), keywords)
            plt.xlabel('التكرار')
            plt.title('أهم الكلمات المفتاحية')

            # 4. التوزيع الزمني
            plt.subplot(2, 2, 4)
            months = list(stats['monthly_distribution'].keys())
            month_counts = list(stats['monthly_distribution'].values())

            plt.plot(months, month_counts, marker='o')
            plt.xlabel('الشهر')
            plt.ylabel('عدد الأفكار')
            plt.title('التوزيع الزمني للأفكار')
            plt.xticks(rotation=45)

            plt.tight_layout()
            plt.savefig(f"{output_dir}/dashboard.png", dpi=300, bbox_inches='tight')
            plt.close()

            logger.info(f"تم إنشاء لوحة التحكم: {output_dir}/dashboard.png")

        except ImportError:
            logger.warning("مكتبات الرسم البياني غير متوفرة")

    def export_to_formats(self, ideas: List[ScientificIdea], base_filename: str):
        """تصدير الأفكار لصيغ متعددة"""

        # تصدير إلى JSON
        json_data = []
        for idea in ideas:
            json_data.append({
                'id': idea.id,
                'title': idea.title,
                'content': idea.content,
                'category': idea.category,
                'date': idea.date,
                'equations_count': len(idea.equations),
                'keywords': idea.keywords,
                'importance_score': idea.importance_score
            })

        with open(f"{base_filename}.json", 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        # تصدير إلى CSV
        try:
            import csv

            with open(f"{base_filename}.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Title', 'Category', 'Date', 'Keywords', 'Importance', 'Content_Length'])

                for idea in ideas:
                    writer.writerow([
                        idea.id,
                        idea.title,
                        idea.category,
                        idea.date,
                        '; '.join(idea.keywords),
                        idea.importance_score,
                        len(idea.content)
                    ])

            logger.info(f"تم التصدير إلى: {base_filename}.json, {base_filename}.csv")

        except Exception as e:
            logger.error(f"خطأ في التصدير: {e}")

def run_complete_analysis():
    """تشغيل التحليل الكامل"""
    print("🚀 بدء نظام معالجة النصوص العلمية الذكي")
    print("=" * 50)

    # إنشاء المحلل
    analyzer = AdvancedTextAnalyzer()

    # تثبيت المكتبات (اختياري)
    # analyzer.install_dependencies()

    # معالجة الملفات
    files_to_process = [
        'riemann_research_ideas.md',
        'conversation_archive.txt'
    ]

    all_ideas = []

    for file_path in files_to_process:
        if os.path.exists(file_path):
            print(f"📄 معالجة الملف: {file_path}")
            results = analyzer.processor.process_text_file(file_path)
            all_ideas.extend(results['new_ideas'])

            # طباعة النتائج
            print(f"  ✅ أفكار جديدة: {len(results['new_ideas'])}")
            print(f"  🔄 تكرارات: {len(results['duplicates'])}")
        else:
            print(f"⚠️  الملف غير موجود: {file_path}")

    if all_ideas:
        print(f"\n📊 إجمالي الأفكار المعالجة: {len(all_ideas)}")

        # إنتاج التقارير
        print("📈 إنتاج التقارير...")

        # تقرير إحصائي
        stats = analyzer.generate_statistics_report(all_ideas)
        print(f"  📋 الفئات: {len(stats['categories'])}")
        print(f"  🔢 المعادلات: {stats['equations_count']}")
        print(f"  🔑 الكلمات المفتاحية: {len(stats['keywords_frequency'])}")

        # تحليل التشابه
        similarity_results = analyzer.advanced_similarity_analysis(all_ideas)
        if similarity_results:
            print(f"  🔍 أزواج متشابهة: {len(similarity_results['similar_pairs'])}")

        # إنتاج الملفات
        analyzer.processor.generate_organized_output('organized_ideas_final.md')
        analyzer.export_to_formats(all_ideas, 'ideas_export')

        # لوحة التحكم البصرية
        analyzer.create_visual_dashboard(all_ideas, 'visual_reports')

        # سحابة الكلمات
        analyzer.generate_word_cloud(all_ideas, 'wordcloud.png')

        print("\n✅ تم الانتهاء من التحليل بنجاح!")
        print("📁 الملفات المُنتجة:")
        print("  - organized_ideas_final.md")
        print("  - ideas_export.json")
        print("  - ideas_export.csv")
        print("  - visual_reports/dashboard.png")
        print("  - wordcloud.png")

    else:
        print("❌ لم يتم العثور على أفكار للمعالجة")

if __name__ == "__main__":
    import os
    run_complete_analysis()

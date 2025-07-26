#!/usr/bin/env python3
"""
نظام تكامل الأفكار الجديدة
New Ideas Integration System

نظام ذكي لمقارنة الأفكار الجديدة مع الموجودة وتحديد موضعها المناسب في الكتاب
Intelligent system for comparing new ideas with existing ones and determining their appropriate place in the book

Author: Basil Yahya Abdullah
Date: 2025-07-25
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import difflib

class IdeaAnalyzer:
    """محلل الأفكار والمفاهيم"""
    
    def __init__(self):
        self.similarity_threshold = 0.8  # حد التشابه
        self.quality_criteria = {
            'clarity': 0.0,           # الوضوح
            'mathematical_beauty': 0.0,  # الجمال الرياضي
            'scientific_logic': 0.0,     # المنطق العلمي
            'mathematical_power': 0.0,   # القوة الرياضية
            'innovation': 0.0,           # الابتكار
            'literary_coherence': 0.0,   # التماسك الأدبي
            'applicability': 0.0         # القابلية للتطبيق
        }
    
    def extract_key_concepts(self, text: str) -> List[str]:
        """استخراج المفاهيم الرئيسية من النص"""
        # قائمة المفاهيم الرياضية والفيزيائية المهمة
        key_patterns = [
            r'دالة زيتا|zeta function',
            r'الأعداد الأولية|prime numbers',
            r'فرضية ريمان|riemann hypothesis',
            r'التوازن الطاقي|energy balance',
            r'الزمن الداخلي|internal time',
            r'التردد الرنيني|resonant frequency',
            r'المقاومة|resistance',
            r'نظرية الفتائل|filament theory',
            r'العدد النابض|pulsating number',
            r'الكثافة الزمنية|time density',
            r'اللوغاريتم|logarithm',
            r'التذبذب|oscillation',
            r'الرنين|resonance',
            r'التداخل الموجي|wave interference',
            r'الأصفار الحرجة|critical zeros'
        ]
        
        concepts = []
        for pattern in key_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            concepts.extend(matches)
        
        return list(set(concepts))  # إزالة التكرار
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """حساب درجة التشابه بين نصين"""
        # تنظيف النصوص
        clean_text1 = re.sub(r'[^\w\s]', '', text1.lower())
        clean_text2 = re.sub(r'[^\w\s]', '', text2.lower())
        
        # حساب التشابه باستخدام difflib
        similarity = difflib.SequenceMatcher(None, clean_text1, clean_text2).ratio()
        
        # حساب التشابه في المفاهيم
        concepts1 = set(self.extract_key_concepts(text1))
        concepts2 = set(self.extract_key_concepts(text2))
        
        if concepts1 or concepts2:
            concept_similarity = len(concepts1.intersection(concepts2)) / len(concepts1.union(concepts2))
        else:
            concept_similarity = 0.0
        
        # المتوسط المرجح
        return 0.6 * similarity + 0.4 * concept_similarity
    
    def evaluate_quality(self, text: str) -> Dict[str, float]:
        """تقييم جودة النص وفق المعايير المحددة"""
        quality_scores = self.quality_criteria.copy()
        
        # تقييم الوضوح (بناءً على طول الجمل ووضوح التعبير)
        sentences = re.split(r'[.!?]', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        quality_scores['clarity'] = max(0, min(1, 1 - (avg_sentence_length - 15) / 30))
        
        # تقييم الجمال الرياضي (وجود معادلات ورموز رياضية)
        math_patterns = len(re.findall(r'[=+\-*/∫∑√π]|\\[a-zA-Z]+', text))
        quality_scores['mathematical_beauty'] = min(1, math_patterns / 10)
        
        # تقييم المنطق العلمي (وجود كلمات منطقية)
        logic_words = len(re.findall(r'لذلك|إذن|بالتالي|نتيجة|استنتاج|برهان|therefore|thus|hence', text, re.IGNORECASE))
        quality_scores['scientific_logic'] = min(1, logic_words / 5)
        
        # تقييم القوة الرياضية (عمق المفاهيم)
        concepts = self.extract_key_concepts(text)
        quality_scores['mathematical_power'] = min(1, len(concepts) / 8)
        
        # تقييم الابتكار (وجود مصطلحات جديدة)
        innovation_indicators = len(re.findall(r'جديد|مبتكر|ثوري|novel|innovative|revolutionary', text, re.IGNORECASE))
        quality_scores['innovation'] = min(1, innovation_indicators / 3)
        
        # تقييم التماسك الأدبي (تدفق النص)
        transition_words = len(re.findall(r'أولاً|ثانياً|أخيراً|بالإضافة|علاوة|first|second|finally|moreover', text, re.IGNORECASE))
        quality_scores['literary_coherence'] = min(1, transition_words / 4)
        
        # تقييم القابلية للتطبيق (وجود أمثلة وتطبيقات)
        application_words = len(re.findall(r'مثال|تطبيق|نتيجة|example|application|result', text, re.IGNORECASE))
        quality_scores['applicability'] = min(1, application_words / 3)
        
        return quality_scores

class BookStructureManager:
    """مدير هيكل الكتاب"""
    
    def __init__(self, book_file: str = 'riemann_hypothesis_solution_book.md'):
        self.book_file = book_file
        self.structure = self._analyze_book_structure()
    
    def _analyze_book_structure(self) -> Dict:
        """تحليل هيكل الكتاب الحالي"""
        try:
            with open(self.book_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # استخراج العناوين والأقسام
            sections = {}
            current_section = None
            
            for line in content.split('\n'):
                if line.startswith('## '):
                    current_section = line[3:].strip()
                    sections[current_section] = {'content': '', 'subsections': {}}
                elif line.startswith('### '):
                    if current_section:
                        subsection = line[4:].strip()
                        sections[current_section]['subsections'][subsection] = ''
                elif current_section:
                    sections[current_section]['content'] += line + '\n'
            
            return sections
            
        except FileNotFoundError:
            return {}
    
    def find_best_section(self, idea_text: str, idea_concepts: List[str]) -> str:
        """العثور على أفضل قسم لوضع الفكرة"""
        best_section = "الفصل الأول: الأسس النظرية"  # القسم الافتراضي
        best_score = 0.0
        
        for section_name, section_data in self.structure.items():
            section_concepts = self._extract_concepts_from_section(section_data['content'])
            
            # حساب التطابق في المفاهيم
            common_concepts = set(idea_concepts).intersection(set(section_concepts))
            if section_concepts:
                score = len(common_concepts) / len(set(idea_concepts).union(set(section_concepts)))
            else:
                score = 0.0
            
            if score > best_score:
                best_score = score
                best_section = section_name
        
        return best_section
    
    def _extract_concepts_from_section(self, section_text: str) -> List[str]:
        """استخراج المفاهيم من قسم معين"""
        analyzer = IdeaAnalyzer()
        return analyzer.extract_key_concepts(section_text)

class IdeaIntegrationSystem:
    """نظام تكامل الأفكار الرئيسي"""
    
    def __init__(self):
        self.analyzer = IdeaAnalyzer()
        self.book_manager = BookStructureManager()
        self.existing_ideas = self._load_existing_ideas()
    
    def _load_existing_ideas(self) -> List[Dict]:
        """تحميل الأفكار الموجودة من الملف المرجعي"""
        try:
            with open('riemann_research_ideas.md', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # استخراج الأفكار المرقمة
            ideas = []
            idea_pattern = r'### .+? \((\d+)\)\n\*\*التاريخ:\*\* (.+?)\n\*\*(.+?)\n(.+?)(?=###|\n---|\Z)'
            
            matches = re.findall(idea_pattern, content, re.DOTALL)
            for match in matches:
                idea_id, date, title, description = match
                ideas.append({
                    'id': int(idea_id),
                    'date': date,
                    'title': title,
                    'description': description.strip()
                })
            
            return ideas
            
        except FileNotFoundError:
            return []
    
    def process_new_idea(self, new_idea_text: str) -> Dict:
        """معالجة فكرة جديدة"""
        result = {
            'status': 'unknown',
            'action': 'none',
            'similarity_scores': [],
            'quality_assessment': {},
            'recommended_section': '',
            'reasoning': ''
        }
        
        # استخراج المفاهيم من الفكرة الجديدة
        new_concepts = self.analyzer.extract_key_concepts(new_idea_text)
        
        # تقييم جودة الفكرة الجديدة
        new_quality = self.analyzer.evaluate_quality(new_idea_text)
        result['quality_assessment'] = new_quality
        
        # مقارنة مع الأفكار الموجودة
        max_similarity = 0.0
        most_similar_idea = None
        
        for existing_idea in self.existing_ideas:
            similarity = self.analyzer.calculate_similarity(new_idea_text, existing_idea['description'])
            result['similarity_scores'].append({
                'idea_id': existing_idea['id'],
                'similarity': similarity,
                'title': existing_idea['title']
            })
            
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_idea = existing_idea
        
        # تحديد الإجراء المطلوب
        if max_similarity > 0.95:
            result['status'] = 'duplicate'
            result['action'] = 'ignore'
            result['reasoning'] = f"مطابقة تماماً للفكرة ({most_similar_idea['id']}) - {most_similar_idea['title']}"
        
        elif max_similarity > 0.7:
            # مقارنة الجودة
            existing_quality = self.analyzer.evaluate_quality(most_similar_idea['description'])
            new_avg_quality = sum(new_quality.values()) / len(new_quality)
            existing_avg_quality = sum(existing_quality.values()) / len(existing_quality)
            
            if new_avg_quality > existing_avg_quality + 0.1:
                result['status'] = 'improvement'
                result['action'] = 'replace'
                result['reasoning'] = f"تحسين للفكرة ({most_similar_idea['id']}) - جودة أفضل"
            else:
                result['status'] = 'similar'
                result['action'] = 'consider'
                result['reasoning'] = f"مشابهة للفكرة ({most_similar_idea['id']}) - تحتاج مراجعة"
        
        else:
            result['status'] = 'new'
            result['action'] = 'add'
            result['reasoning'] = "فكرة جديدة - يُنصح بإضافتها"
        
        # تحديد القسم المناسب في الكتاب
        result['recommended_section'] = self.book_manager.find_best_section(new_idea_text, new_concepts)
        
        return result
    
    def generate_integration_report(self, new_idea_text: str) -> str:
        """إنتاج تقرير تكامل الفكرة الجديدة"""
        analysis = self.process_new_idea(new_idea_text)
        
        report = f"""
# تقرير تكامل الفكرة الجديدة
**التاريخ:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## النص المُحلل:
{new_idea_text[:200]}...

## نتائج التحليل:
- **الحالة:** {analysis['status']}
- **الإجراء المُوصى:** {analysis['action']}
- **السبب:** {analysis['reasoning']}
- **القسم المُوصى في الكتاب:** {analysis['recommended_section']}

## تقييم الجودة:
"""
        
        for criterion, score in analysis['quality_assessment'].items():
            report += f"- **{criterion}:** {score:.2f}\n"
        
        report += "\n## أعلى درجات التشابه:\n"
        
        # ترتيب حسب التشابه
        sorted_similarities = sorted(analysis['similarity_scores'], 
                                   key=lambda x: x['similarity'], reverse=True)[:5]
        
        for sim in sorted_similarities:
            report += f"- الفكرة ({sim['idea_id']}): {sim['similarity']:.2f} - {sim['title']}\n"
        
        return report

def main():
    """دالة اختبار النظام"""
    system = IdeaIntegrationSystem()
    
    # مثال على فكرة جديدة للاختبار
    test_idea = """
    الأعداد الأولية هي نغمات نقية في نسيج الزمكان، تُحدث رنيناً كونياً عند ترددات محددة.
    هذا الرنين يخلق موجات تداخل تؤدي إلى ظهور الأصفار غير التافهة في دالة زيتا ريمان.
    """
    
    report = system.generate_integration_report(test_idea)
    print(report)
    
    # حفظ التقرير
    with open('integration_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n✅ تم حفظ تقرير التكامل في: integration_report.md")

if __name__ == "__main__":
    main()

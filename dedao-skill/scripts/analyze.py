#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
得到课程内容分析器
用于分析课程内容并生成针对性的营销建议
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class CourseSection:
    """课程章节"""
    title: str
    content: str
    word_count: int
    key_points: List[str]


@dataclass
class CourseAnalysis:
    """课程分析结果"""
    title: str
    total_sections: int
    total_words: int
    sections: List[CourseSection]
    key_topics: List[str]
    actionable_insights: List[str]
    analysis_time: str


class DedaoCourseAnalyzer:
    """得到课程分析器"""
    
    def __init__(self, course_dir: str):
        self.course_dir = Path(course_dir)
        self.sections: List[CourseSection] = []
        
    def load_sections(self) -> None:
        """加载所有章节"""
        md_files = sorted(self.course_dir.glob("*.md"))
        
        for md_file in md_files:
            if md_file.name.startswith("00-"):
                continue  # 跳过已生成的建议文件
                
            content = md_file.read_text(encoding='utf-8')
            title = self._extract_title(content, md_file.stem)
            word_count = len(content)
            key_points = self._extract_key_points(content)
            
            section = CourseSection(
                title=title,
                content=content,
                word_count=word_count,
                key_points=key_points
            )
            self.sections.append(section)
    
    def _extract_title(self, content: str, fallback: str) -> str:
        """提取章节标题"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return fallback
    
    def _extract_key_points(self, content: str) -> List[str]:
        """提取关键点"""
        key_points = []
        
        # 查找划重点部分
        focus_match = re.search(r'##\s*划重点\s*\n(.*?)(?=\n---|\Z)', content, re.DOTALL)
        if focus_match:
            focus_content = focus_match.group(1)
            points = re.findall(r'\d+\s+(.+)', focus_content)
            key_points.extend(points)
        
        # 查找加粗内容作为关键点
        bold_points = re.findall(r'\*\*(.+?)\*\*', content)
        key_points.extend(bold_points[:5])
        
        return key_points[:10]
    
    def analyze(self) -> CourseAnalysis:
        """分析课程"""
        self.load_sections()
        
        total_words = sum(s.word_count for s in self.sections)
        key_topics = self._extract_key_topics()
        actionable_insights = self._extract_actionable_insights()
        
        return CourseAnalysis(
            title=self.course_dir.name,
            total_sections=len(self.sections),
            total_words=total_words,
            sections=self.sections,
            key_topics=key_topics,
            actionable_insights=actionable_insights,
            analysis_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    
    def _extract_key_topics(self) -> List[str]:
        """提取关键主题"""
        topics = set()
        
        for section in self.sections:
            title_words = re.findall(r'[\u4e00-\u9fa5]+', section.title)
            topics.update(title_words[:3])
            
            for point in section.key_points:
                words = re.findall(r'[\u4e00-\u9fa5]+', point)
                topics.update(words[:2])
        
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        topics = topics - stop_words
        
        return sorted(list(topics))[:20]
    
    def _extract_actionable_insights(self) -> List[str]:
        """提取可操作的洞察"""
        insights = []
        
        for section in self.sections:
            suggestions = re.findall(r'(?:建议|可以|应该|需要|能够)[^。\n]+', section.content)
            insights.extend(suggestions[:3])
        
        return insights[:10]


class SMTAdviceGenerator:
    """SMT外贸营销建议生成器"""
    
    def __init__(self, analysis: CourseAnalysis, industry_config: Dict[str, Any]):
        self.analysis = analysis
        self.industry_config = industry_config
    
    def generate_advice(self) -> str:
        """生成营销建议"""
        advice = []
        
        # 标题
        advice.append(f"# {self.industry_config.get('name', '营销建议')}")
        advice.append("")
        advice.append(f"> 基于课程《{self.analysis.title}》分析生成")
        advice.append(f"> 生成时间：{self.analysis.analysis_time}")
        advice.append(f"> 适用场景：{self.industry_config.get('description', '')}")
        advice.append("")
        advice.append("---")
        advice.append("")
        
        # 课程概览
        advice.append("## 课程概览")
        advice.append("")
        advice.append(f"- **总章节数**：{self.analysis.total_sections}")
        advice.append(f"- **总字数**：{self.analysis.total_words:,}")
        advice.append(f"- **关键主题**：{', '.join(self.analysis.key_topics[:10])}")
        advice.append("")
        advice.append("---")
        advice.append("")
        
        # 建议清单
        advice.append("## 建议清单")
        advice.append("")
        
        suggestions = self.industry_config.get('suggestions', [])
        for i, suggestion in enumerate(suggestions, 1):
            advice.append(f"### {i}. {suggestion['title']}")
            advice.append("")
            advice.append(f"**描述**：{suggestion['description']}")
            advice.append("")
            advice.append("**行动项**：")
            for action in suggestion.get('actions', []):
                advice.append(f"- {action}")
            advice.append("")
            advice.append(f"**理由**：{suggestion.get('reason', '')}")
            advice.append("")
        
        # 课程精华摘录
        advice.append("---")
        advice.append("")
        advice.append("## 课程精华摘录")
        advice.append("")
        
        quotes = [
            "深耕行业，能为客户提供附加价值的企业才能走得更远。",
            "人们往往高估了一年能做到的事，又低估了十年能做到的事。",
            "用一整个网络去对抗别人的几个节点，用全球组织去对抗别人给你带来的局部冲突。"
        ]
        
        for quote in quotes:
            advice.append(f"> {quote}")
            advice.append("")
        
        # 下一步行动计划
        advice.append("---")
        advice.append("")
        advice.append("## 下一步行动计划")
        advice.append("")
        advice.append("1. **立即执行**：完善阿里国际站店铺信息，上传产品视频")
        advice.append("2. **本周完成**：制作第一篇技术知识文章")
        advice.append("3. **本月目标**：建立LinkedIn行业社群，发布3篇技术文章")
        advice.append("4. **季度目标**：获得第一个海外客户询盘")
        advice.append("")
        
        return "\n".join(advice)


def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='得到课程内容分析器')
    parser.add_argument('course_dir', help='课程目录路径')
    parser.add_argument('--config', default='config/config.json', help='配置文件路径')
    parser.add_argument('--industry', default='SMT设备外贸', help='行业领域')
    parser.add_argument('--output', help='输出文件路径')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.course_dir):
        print(f"错误: 目录不存在: {args.course_dir}")
        exit(1)
    
    print(f"正在分析课程: {args.course_dir}")
    
    analyzer = DedaoCourseAnalyzer(args.course_dir)
    analysis = analyzer.analyze()
    
    print(f"课程包含 {analysis.total_sections} 个章节，共 {analysis.total_words:,} 字")
    
    # 加载行业配置
    config = load_config(args.config)
    industry_config = config.get('advice_templates', {}).get(args.industry, {})
    
    if not industry_config:
        print(f"警告: 未找到行业 '{args.industry}' 的配置，使用默认配置")
        industry_config = {
            'name': f'{args.industry}营销建议',
            'description': f'针对{args.industry}业务的实用建议',
            'suggestions': []
        }
    
    generator = SMTAdviceGenerator(analysis, industry_config)
    advice = generator.generate_advice()
    
    # 保存建议
    output_file = args.output or os.path.join(args.course_dir, "00-SMT外贸营销建议.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(advice)
    
    print(f"✓ 建议已生成: {output_file}")


if __name__ == "__main__":
    main()

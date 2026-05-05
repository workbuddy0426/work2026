#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分割Word文档中的公众号文章合集
作者: 小文 📄
"""

import re
import os
from datetime import datetime

def extract_text_from_doc(filepath):
    """从.doc文件中提取UTF-16 LE编码的文本"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    text_parts = []
    i = 0
    while i < len(data) - 1:
        high = data[i+1]
        # 中文字符范围
        if 0x4E <= high <= 0x9F:
            start = max(0, i - 50)
            end = min(len(data), i + 1000)
            chunk = data[start:end]
            try:
                text = chunk.decode('utf-16-le', errors='ignore')
                clean_text = ''.join(c for c in text if c.isprintable() or c in '\n\r')
                if len(clean_text.strip()) > 30:
                    text_parts.append(clean_text.strip())
            except:
                pass
            i += 200
        else:
            i += 2
    
    return text_parts

def merge_related_parts(text_parts):
    """合并相关的文本片段"""
    merged = []
    current = ''
    
    for part in text_parts:
        if len(current) < 10000:
            current += '\n' + part if current else part
        else:
            if len(current) > 200:
                merged.append(current)
            current = part
    
    if current and len(current) > 200:
        merged.append(current)
    
    return merged

def extract_filename(text):
    """从文本中提取文件名"""
    # 查找 .txt 文件名
    match = re.search(r'([^/\\]+\.txt)', text)
    if match:
        filename = match.group(1)
        # 清理文件名
        filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
        return filename.replace('.txt', '.md')
    return None

def extract_title(text):
    """提取文章标题"""
    lines = text.split('\n')
    for line in lines[:5]:
        line = line.strip()
        # 跳过文件名行
        if '.txt' in line:
            continue
        # 查找可能的标题（不含特殊字符的较长文本）
        if 10 < len(line) < 100 and '原创' not in line and '公众号' not in line:
            return line
    return "未命名文章"

def split_articles(input_file, output_dir):
    """分割文章并保存"""
    print(f"📄 正在读取文件: {input_file}")
    
    # 提取文本
    text_parts = extract_text_from_doc(input_file)
    print(f"✅ 提取到 {len(text_parts)} 个文本片段")
    
    # 合并
    merged = merge_related_parts(text_parts)
    print(f"✅ 合并为 {len(merged)} 个大段落")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 分析并分割文章
    articles = []
    current_article = None
    
    for i, text in enumerate(merged):
        filename = extract_filename(text)
        
        if filename:
            # 保存前一篇文章
            if current_article:
                articles.append(current_article)
            
            # 开始新文章
            title = extract_title(text)
            current_article = {
                'filename': filename,
                'title': title,
                'content': text,
                'index': len(articles) + 1
            }
        elif current_article:
            # 继续当前文章
            current_article['content'] += '\n\n' + text
    
    # 保存最后一篇
    if current_article:
        articles.append(current_article)
    
    print(f"✅ 识别到 {len(articles)} 篇文章")
    
    # 保存每篇文章
    saved_files = []
    for article in articles:
        filepath = os.path.join(output_dir, article['filename'])
        
        # 生成Markdown格式
        content = f"""# {article['title']}

> 来源: 记忆承载·碧树西风
> 提取时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

{article['content']}

---

*本文档由小文 📄 自动从Word合集中提取*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        saved_files.append({
            'filename': article['filename'],
            'title': article['title'],
            'size': len(content)
        })
        print(f"  ✓ {article['filename']} ({len(content)} 字符)")
    
    return saved_files

if __name__ == '__main__':
    input_file = 'C:/Users/user/Desktop/all20250228.doc'
    output_dir = 'C:/Users/user/Desktop/公众号文章'
    
    print("=" * 50)
    print("📚 公众号文章分割工具")
    print("=" * 50)
    
    try:
        files = split_articles(input_file, output_dir)
        
        print("\n" + "=" * 50)
        print(f"✅ 成功分割并保存 {len(files)} 篇文章")
        print(f"📁 保存位置: {output_dir}")
        print("=" * 50)
        
        # 生成索引文件
        index_path = os.path.join(output_dir, '_文章索引.md')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# 公众号文章索引\n\n")
            f.write(f"> 提取时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("| 序号 | 文件名 | 标题 | 大小 |\n")
            f.write("|------|--------|------|------|\n")
            for i, file in enumerate(files, 1):
                f.write(f"| {i} | [{file['filename']}](./{file['filename']}) | {file['title'][:30]}... | {file['size']} 字符 |\n")
        
        print(f"✅ 索引文件已生成: {index_path}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理文章 - 智能段落重组版本
"""

def extract_unique_content(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    
    # Step 1:  aggressively remove all garbage characters
    # Remove all non-Chinese, non-ASCII printable characters
    content = re.sub(r'[^\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef\w\s.,!?;:()""''【】《》（），。！？：；""''\-\n]', '', content)
    
    # Remove specific garbage patterns
    content = re.sub(r'h{2,}', '', content)
    content = re.sub(r'\u0000-\u001f', '', content)
    
    # Step 2: Remove metadata lines completely
    content = re.sub(r'记忆承载压缩/[^\n]*', '', content)
    content = re.sub(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2} 浙江', '', content)
    content = re.sub(r'已付费 原创 碧树西风 人间罗盘', '', content)
    content = re.sub(r'> 来源:[^\n]*', '', content)
    content = re.sub(r'> 提取时间:[^\n]*', '', content)
    content = re.sub(r'---', '', content)
    content = re.sub(r'# .*', '', content)  # Remove markdown headers
    
    # Step 3: Split into potential sentences
    # Chinese sentences end with 。！？
    raw_sentences = re.split(r'([。！？])', content)
    
    # Recombine sentences with their punctuation
    sentences = []
    i = 0
    while i < len(raw_sentences):
        if i + 1 < len(raw_sentences) and raw_sentences[i+1] in '。！？':
            sentences.append(raw_sentences[i] + raw_sentences[i+1])
            i += 2
        else:
            if raw_sentences[i].strip():
                sentences.append(raw_sentences[i])
            i += 1
    
    # Step 4: Advanced deduplication
    # Use a longer fingerprint (first 40 chars) to catch more duplicates
    unique_sentences = []
    seen = set()
    
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 15:  # Skip very short fragments
            continue
        
        # Create fingerprint from first 40 chars (ignoring spaces)
        fingerprint = sent[:40].replace(' ', '').replace('\n', '')
        
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_sentences.append(sent)
    
    # Step 5: Group sentences into coherent paragraphs
    # Group by topic/length
    paragraphs = []
    current_para = []
    
    for sent in unique_sentences:
        # Skip incomplete sentences (don't end with punctuation)
        if not sent[-1] in '。！？':
            continue
            
        current_para.append(sent)
        
        # Start new paragraph every 2-3 sentences or after long sentences
        if len(current_para) >= 3 or len(sent) > 80:
            paragraphs.append(''.join(current_para))
            current_para = []
    
    if current_para:
        paragraphs.append(''.join(current_para))
    
    # Step 6: Build final document
    output = f"""# 2024经济大戏的序幕，已经拉开

> **作者**：碧树西风（记忆承载·人间罗盘）
> **日期**：2024年03月09日
> **字数**：约2万字

---

## 文章导语

在这个风起云涌，全球各个投资品种跌宕起伏的时刻。应读者的要求，我对未来全球经济走势的各种可能，以及各种应对，进行一次全面梳理。

全文很长，两万两千字。文中多处有链接跳转部分如同画中画，文中文，你自己阅读时留心不要错过。

有问题，你可以发私信，阅读者的留言，我都能看见。

---

## 核心观点

**美国经济是处在一个即将面临阶段性调整的拐点前夜，还是处在一个即将迎来黄金周期爆发的起点？**

这个问题是理解当前全球经济形势的关键。

---

## 正文

"""
    
    # Add paragraphs with proper formatting
    for para in paragraphs:
        para = para.strip()
        if len(para) > 30:  # Only include substantial paragraphs
            output += para + '\n\n'
    
    output += """---

## 文章结语

从数据上看，当下明显不是散户做多美股的好时机。

作为散户，你一辈子，能认清大规律，踩住两到四次时机，完成一到两次向上置换，你妥妥的小区赢家。

---

*本文档由小文 📄 整理排版，去除重复内容，优化阅读体验*  
*原文来源：记忆承载·碧树西风*  
*原文日期：2024年03月09日*
"""
    
    # Clean up multiple newlines
    output = re.sub(r'\n{3,}', '\n\n', output)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"✅ 智能清理完成！")
    print(f"原始片段数: {len(sentences)}")
    print(f"去重后句子数: {len(unique_sentences)}")
    print(f"生成段落数: {len(paragraphs)}")
    print(f"输出文件: {output_file}")

if __name__ == '__main__':
    input_file = 'c:/Users/user/Desktop/公众号文章/202502112024经济大戏的序幕，已经拉开.md'
    output_file = 'c:/Users/user/Desktop/公众号文章/202502112024经济大戏的序幕_精排版.md'
    extract_unique_content(input_file, output_file)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理文章 - 最终版本：严格过滤，只保留干净内容
"""

def final_clean(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    import re
    
    # Step 1: Filter lines - remove any line with garbage characters
    clean_lines = []
    for line in lines:
        # Skip lines with Hebrew, special symbols, or control characters
        if re.search(r'[ꗬÁ袉¿ကƭלמɍʲӿ³ԩƁ\u0590-\u05ff\u00a0-\u00bf]', line):
            continue
        # Skip lines with too many non-Chinese/non-ASCII chars
        if re.search(r'[^\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef\w\s.,!?;:()""''【】《》（），。！？：；""''\-\n]', line):
            # Check if it's mostly garbage
            chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', line))
            if chinese_chars < 10:  # If less than 10 Chinese chars, skip
                continue
        clean_lines.append(line)
    
    # Step 2: Join and remove metadata
    content = ''.join(clean_lines)
    
    # Remove metadata patterns
    content = re.sub(r'记忆承载压缩/[^\n]*\.txt', '', content)
    content = re.sub(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2} 浙江', '', content)
    content = re.sub(r'已付费 原创 碧树西风 人间罗盘', '', content)
    content = re.sub(r'> 来源:[^\n]*', '', content)
    content = re.sub(r'> 提取时间:[^\n]*', '', content)
    content = re.sub(r'---', '', content)
    content = re.sub(r'^# .*$', '', content, flags=re.MULTILINE)
    
    # Step 3: Extract complete sentences
    # Find all sentences ending with Chinese punctuation
    sentences = re.findall(r'[^。！？]*[。！？]', content)
    
    # Step 4: Deduplication with longer fingerprint
    unique = []
    seen = set()
    
    for sent in sentences:
        sent = sent.strip()
        # Must be reasonable length and contain Chinese
        if len(sent) < 20:
            continue
        if not re.search(r'[\u4e00-\u9fa5]', sent):
            continue
        
        # Use longer fingerprint (50 chars)
        fp = sent[:50].replace(' ', '').replace('\n', '')
        if fp not in seen:
            seen.add(fp)
            unique.append(sent)
    
    # Step 5: Build paragraphs (3-4 sentences each)
    paragraphs = []
    current = []
    
    for sent in unique:
        current.append(sent)
        if len(current) >= 3:
            paragraphs.append(''.join(current))
            current = []
    
    if current:
        paragraphs.append(''.join(current))
    
    # Step 6: Write output
    output = f"""# 2024经济大戏的序幕，已经拉开

> **作者**：碧树西风（记忆承载）
> **日期**：2024年03月09日

---

## 文章导语

在这个风起云涌，全球各个投资品种跌宕起伏的时刻。应读者的要求，我对未来全球经济走势的各种可能，以及各种应对，进行一次全面梳理。

全文很长，两万两千字。文中多处有链接跳转部分如同画中画，文中文，你自己阅读时留心不要错过。

有问题，你可以发私信，阅读者的留言，我都能看见。

---

## 正文

"""
    
    for para in paragraphs:
        output += para + '\n\n'
    
    output += """---

*本文档由小文 📄 整理排版*  
*原文来源：记忆承载·碧树西风*
"""
    
    # Clean up
    output = re.sub(r'\n{3,}', '\n\n', output)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"✅ 最终清理完成！")
    print(f"清理前行数: {len(lines)}")
    print(f"有效句子数: {len(unique)}")
    print(f"生成段落数: {len(paragraphs)}")
    print(f"保存到: {output_file}")

if __name__ == '__main__':
    input_file = 'c:/Users/user/Desktop/公众号文章/202502112024经济大戏的序幕，已经拉开.md'
    output_file = 'c:/Users/user/Desktop/公众号文章/202502112024经济大戏的序幕_精排版.md'
    final_clean(input_file, output_file)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理文章 - 去除重复内容并重新排版
"""

def clean_article(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 去除开头的乱码和元信息
    lines = content.split('\n')
    
    # 找到真正的文章开始位置（跳过乱码和元信息）
    start_idx = 0
    for i, line in enumerate(lines):
        if '2024经济大戏的序幕' in line or '在这个风起云涌' in line:
            start_idx = i
            break
    
    # 提取有效内容
    content_lines = lines[start_idx:]
    
    # 合并所有行
    full_text = '\n'.join(content_lines)
    
    # 去除乱码字符
    import re
    # 去除UTF-16乱码
    full_text = re.sub(r'[\u0500-\u07ff]{2,}', '', full_text)
    # 去除特殊符号乱码
    full_text = re.sub(r'[ꗬÁ袉Љ倀¿က!卋卋¤ࠄᘂƭלמɍʲӿ³ԩ\x00-\x08\x0b\x0c\x0e-\x1f]', '', full_text)
    
    # 去除重复的元信息行
    full_text = re.sub(r'记忆承载压缩/[^\n]+\.txt', '', full_text)
    full_text = re.sub(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2} 浙江', '', full_text)
    full_text = re.sub(r'> 来源: 记忆承载·碧树西风[^<]*', '', full_text)
    full_text = re.sub(r'> 提取时间:[^\n]*', '', full_text)
    full_text = re.sub(r'---', '', full_text)
    
    # 去除明显的重复模式（同样的句子出现多次）
    # 将文本分成段落
    paragraphs = full_text.split('\n')
    
    # 去除完全重复的行
    seen = set()
    unique_lines = []
    for line in paragraphs:
        line = line.strip()
        if not line:
            continue
        # 检查是否是重复内容（使用前半部分作为指纹）
        fingerprint = line[:50] if len(line) > 50 else line
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_lines.append(line)
    
    # 智能合并句子
    result = []
    i = 0
    while i < len(unique_lines):
        line = unique_lines[i]
        
        # 如果这一行是合理的段落（以标点结尾或足够长）
        if len(line) > 20:
            result.append(line)
        i += 1
    
    # 重新组织成文章格式
    final_text = '\n\n'.join(result)
    
    # 添加标题和格式
    output = f"""# 2024经济大戏的序幕，已经拉开

> 作者：碧树西风（记忆承载）
> 日期：2024年03月09日
> 类型：付费文章

---

## 文章导语

在这个风起云涌，全球各个投资品种跌宕起伏的时刻。应读者的要求，我对未来全球经济走势的各种可能，以及各种应对，进行一次全面梳理。

全文很长，两万两千字。文中多处有链接跳转部分如同画中画，文中文，你自己阅读时留心不要错过。

---

## 正文

{final_text}

---

*本文档由小文 📄 整理排版*
*原文来源：记忆承载·碧树西风*
"""
    
    # 清理多余的空行
    output = re.sub(r'\n{3,}', '\n\n', output)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"✅ 清理完成！")
    print(f"原始行数: {len(lines)}")
    print(f"清理后行数: {len(result)}")
    print(f"保存到: {output_file}")

if __name__ == '__main__':
    input_file = 'c:/Users/user/Desktop/公众号文章/202502112024经济大戏的序幕，已经拉开.md'
    output_file = 'c:/Users/user/Desktop/公众号文章/202502112024经济大戏的序幕，已经拉开_整理版.md'
    clean_article(input_file, output_file)

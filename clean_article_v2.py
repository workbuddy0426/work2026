#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理文章 - 高级去重版本
"""

def clean_article_advanced(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    
    # Step 1: 去除所有乱码字符
    # 去除UTF-16乱码、希伯来文、特殊符号等
    content = re.sub(r'[ꗬÁ袉Љ倀¿က!卋卋¤ࠄᘂƭלמɍʲӿ³ԩƁ\x00-\x08\x0b\x0c\x0e-\x1f\u0500-\u06ff]+', '', content)
    
    # Step 2: 去除元信息行
    content = re.sub(r'记忆承载压缩/[^\n]+\.txt', '', content)
    content = re.sub(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2} 浙江', '', content)
    content = re.sub(r'> 来源:[^\n]*', '', content)
    content = re.sub(r'> 提取时间:[^\n]*', '', content)
    content = re.sub(r'---', '', content)
    content = re.sub(r'# [^\n]+', '', content)  # 移除原有标题
    
    # Step 3: 去除明显的前后缀
    content = re.sub(r'已付费 原创 碧树西风 人间罗盘', '', content)
    
    # Step 4: 分割成句子
    # 按句号、问号、感叹号分割，但保留标点
    sentences = re.split(r'([。！？])', content)
    
    # 合并句子和标点
    full_sentences = []
    for i in range(0, len(sentences)-1, 2):
        if i+1 < len(sentences):
            sentence = sentences[i] + sentences[i+1]
        else:
            sentence = sentences[i]
        full_sentences.append(sentence.strip())
    
    # Step 5: 去重 - 使用滑动窗口检测重复段落
    unique_sentences = []
    seen_windows = set()
    
    for sentence in full_sentences:
        if len(sentence) < 10:  # 跳过太短的句子
            continue
            
        # 创建滑动窗口指纹 (取前20个字符)
        fingerprint = sentence[:30].replace(' ', '').replace('\n', '')
        
        if fingerprint and fingerprint not in seen_windows:
            seen_windows.add(fingerprint)
            unique_sentences.append(sentence)
    
    # Step 6: 重新组合成段落
    # 按语义分组，每3-5个句子组成一个段落
    paragraphs = []
    current_para = []
    
    for i, sentence in enumerate(unique_sentences):
        current_para.append(sentence)
        # 每3-5个句子形成一个段落，或者在特定关键词后分段
        if len(current_para) >= 4 or any(keyword in sentence for keyword in ['。', '？', '！']):
            paragraphs.append(''.join(current_para))
            current_para = []
    
    if current_para:
        paragraphs.append(''.join(current_para))
    
    # Step 7: 格式化输出
    output_lines = [
        "# 2024经济大戏的序幕，已经拉开",
        "",
        "> **作者**：碧树西风（记忆承载）",
        "> **日期**：2024年03月09日",
        "> **类型**：付费文章",
        "",
        "---",
        "",
        "## 文章导语",
        "",
        "在这个风起云涌，全球各个投资品种跌宕起伏的时刻。应读者的要求，我对未来全球经济走势的各种可能，以及各种应对，进行一次全面梳理。",
        "",
        "全文很长，两万两千字。文中多处有链接跳转部分如同画中画，文中文，你自己阅读时留心不要错过。",
        "",
        "---",
        "",
        "## 正文",
        ""
    ]
    
    # 添加段落，确保每个段落之间有空白行
    for para in paragraphs:
        para = para.strip()
        if len(para) > 20:  # 只保留有意义的段落
            output_lines.append(para)
            output_lines.append("")  # 空行
    
    output_lines.extend([
        "---",
        "",
        "*本文档由小文 📄 整理排版*",
        "*原文来源：记忆承载·碧树西风*"
    ])
    
    # 清理多余的空行
    final_output = '\n'.join(output_lines)
    final_output = re.sub(r'\n{3,}', '\n\n', final_output)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_output)
    
    print(f"✅ 高级清理完成！")
    print(f"原始句子数: {len(full_sentences)}")
    print(f"去重后句子数: {len(unique_sentences)}")
    print(f"生成段落数: {len(paragraphs)}")
    print(f"保存到: {output_file}")

if __name__ == '__main__':
    input_file = 'c:/Users/user/Desktop/公众号文章/202502112024经济大戏的序幕，已经拉开.md'
    output_file = 'c:/Users/user/Desktop/公众号文章/202502112024经济大戏的序幕_精排版.md'
    clean_article_advanced(input_file, output_file)

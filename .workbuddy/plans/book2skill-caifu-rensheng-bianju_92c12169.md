---
name: book2skill-caifu-rensheng-bianju
overview: 将「记忆承载」付费长文《逆天改命的关键，在于学会如何做自己人生的编剧》通过 book2skill 方法论拆解为 5 个可执行 skills。
todos:
  - id: stage0-overview
    content: 阶段0：Adler四步分析全文，生成 BOOK_OVERVIEW.md 并汇报骨架
    status: completed
  - id: stage1-extract
    content: 阶段1：五维提取候选方法论（框架/原则/案例/反例/术语）写入 candidates/
    status: completed
    dependencies:
      - stage0-overview
  - id: stage1-5-verify
    content: 阶段1.5：三重验证筛选，通过的保留，淘汰的写入 rejected/ 附原因
    status: completed
    dependencies:
      - stage1-extract
  - id: stage2-ria
    content: 阶段2：RIA++构造5个skill，每个产出 SKILL.md（含R/I/A1/A2/E/B六段）
    status: completed
    dependencies:
      - stage1-5-verify
  - id: stage3-index
    content: 阶段3：建立skill间引用关系，生成 INDEX.md（含mermaid引用图）
    status: completed
    dependencies:
      - stage2-ria
  - id: stage4-test
    content: 阶段4：为每个skill设计test-prompts.json（含诱饵测试），本地验证通过后收尾
    status: completed
    dependencies:
      - stage3-index
---

## 产品概述

将公众号文章《逆天改命的关键，在于学会如何做自己人生的编剧》（记忆承载/碧树西风，约1.3万字）通过 book2skill RIA-TV++ 流水线蒸馏为5个可执行 skill。

## 核心特征

- 源文件：单篇长文（已完整读取），非整书，需按文章五幕结构提取
- 方法论浓度高：每部分对应一个完整决策框架
- 作者风格鲜明：精英实用主义，部分案例触及伦理灰色地带（如"讳败为胜"），边界需明确标注
- 产出要求：每个 skill 具备完整 R/I/A1/A2/E/B 六段、原文引用≤150字、description 含明确 trigger 条件、含诱饵测试

## 核心 Skill 清单（预估）

1. **成功者逆向拆解框架** — 不研究目标，研究达成目标的人（ Forbes 拆解法）
2. **终局视角自我设计系统** — 按终局形态反推当下行为，因果种因
3. **公开承诺倒逼执行法** — 利用"社死恐惧"突破舒适区与自毁程序
4. **高维视角决策模型** — 心眼/出离感/观影体验，用脑而非情绪决策
5. **人生叙事剪辑框架** — 主动剪辑记忆与叙事，控制幸福感与他人评价

## 质量红线

- 每个 skill 必须通过 V1跨域/V2预测力/V3独特性 三重验证
- 原文引用≤150字/段
- 必须包含 test-prompts.json（含应调用/不应调用/边界模糊三类测试）
- 保留 candidates/ 和 rejected/ 审计轨迹

## 技术方案

采用 book2skill RIA-TV++ 四阶段流水线，针对单篇长文做精简适配：

### 架构设计

```
阶段0: Adler 整文理解      → BOOK_OVERVIEW.md（给用户确认）
阶段1: 五维提取候选池       → candidates/{framework,principle,case,counter,glossary}.md
阶段1.5: 三重验证筛选       → 通过的进入阶段2，淘汰的写入 rejected/
阶段2: RIA++ 构造 skill     → 每个 skill 的 SKILL.md（R/I/A1/A2/E/B）
阶段3: Zettelkasten 链接    → INDEX.md + skill 间引用关系
阶段4: 压力测试             → test-prompts.json（darwin 兼容格式）
```

### 关键决策

1. **单篇文章 vs 整书适配**：源文件仅1.3万字，阶段1不强制 spawn 5个子 agent，由主 agent 基于全文记忆直接按五维提取，避免上下文碎片化
2. **质量基线**：严格遵循 SKILL.md.template 格式（frontmatter + 六段正文 + 相关 skills），test-prompts.json 遵循 darwin-skill 格式
3. **审计轨迹**：candidates/ 和 rejected/ 必须保留，允许用户事后捞回

### 输出目录结构

```
books/rensheng-bianju/
├── BOOK_OVERVIEW.md              # [NEW] 阶段0：Adler四步分析 + 批判 + 应用导向
├── INDEX.md                      # [NEW] 阶段3：skill总览 + 引用图 mermaid
├── candidates/                   # [NEW] 阶段1：原始候选池（framework/principle/case/counter/glossary）
├── rejected/                     # [NEW] 阶段1.5：淘汰单元 + 原因
├── reverse-engineer-success/     # [NEW] Skill 1：成功者逆向拆解框架
│   ├── SKILL.md
│   └── test-prompts.json
├── endgame-design/               # [NEW] Skill 2：终局视角自我设计系统
│   ├── SKILL.md
│   └── test-prompts.json
├── public-commitment/            # [NEW] Skill 3：公开承诺倒逼执行法
│   ├── SKILL.md
│   └── test-prompts.json
├── detached-perspective/         # [NEW] Skill 4：高维视角决策模型
│   ├── SKILL.md
│   └── test-prompts.json
└── life-editing/                 # [NEW] Skill 5：人生叙事剪辑框架
    ├── SKILL.md
    └── test-prompts.json
```

## Agent 扩展

### Skill

- **book2skill**
- 用途：指导整个蒸馏流程的 RIA-TV++ 流水线，确保阶段顺序、质量红线和输出格式符合规范
- 预期成果：按标准产出 BOOK_OVERVIEW.md、5个 SKILL.md、INDEX.md 及配套的 test-prompts.json
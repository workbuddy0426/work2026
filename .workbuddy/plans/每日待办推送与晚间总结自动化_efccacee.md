---
name: 每日待办推送与晚间总结自动化
overview: 创建两个每日定时自动化任务：1) 早上8:00推送今日待办事项和备忘录；2) 晚上20:00总结当天完成情况。任务会读取小戴skill的todos.json数据，生成摘要并推送给用户。
todos:
  - id: create-morning-push
    content: 使用 automation_update 创建每日早8点待办推送定时任务
    status: completed
  - id: create-evening-summary
    content: 使用 automation_update 创建每日晚8点完成情况总结定时任务
    status: completed
---

## Product Overview

为用户创建两个每日定时推送任务，由 WorkBuddy 的 automation 机制触发，利用 alarm-memo-assistant-pro skill 的数据文件生成摘要。

## Core Features

- 每天早上 8:00 读取待办和备忘录数据，推送今日任务摘要（含今日到期、高优先级、逾期未完成、备忘录提醒）
- 每天晚上 20:00 读取待办数据，推送今日完成情况总结（含已完成事项清单、未完成事项、完成率统计）
- 任务类型为 recurring（FREQ=DAILY），长期生效

## Tech Stack

- WorkBuddy automation_update 工具（recurring 定时任务）
- alarm-memo-assistant-pro skill 数据文件（todos.json, alarms.json, memos.md）

## Implementation Approach

通过 automation_update 创建两个 recurring 类型定时任务：

1. **早安推送**：scheduleType=recurring，schedule="FREQ=DAILY;BYHOUR=8;BYMINUTE=0"，prompt 指示 agent 读取 todos.json 筛选待办事项 + 读取 memos.md 展示备忘录，按格式输出
2. **晚间总结**：scheduleType=recurring，schedule="FREQ=DAILY;BYHOUR=20;BYMINUTE=0"，prompt 指示 agent 读取 todos.json 中当日完成的 completed 事项和未完成的 todos，统计完成率

两个任务的 cwds 设为 ["c:/Users/user/WorkBuddy/Claw"]，工作目录为 Claw，但 prompt 中会使用绝对路径读取 skill 数据文件。

## Implementation Notes

- 数据文件绝对路径：`C:\Users\user\.workbuddy\skills\alarm-memo-assistant-pro\data\todos.json`
- memos.md 路径：`C:\Users\user\.workbuddy\skills\alarm-memo-assistant-pro\data\memos.md`（需确认是否存在）
- prompt 中明确要求 agent 读取文件后生成结构化摘要，不要编造数据
- 任务状态设为 ACTIVE

## Agent Extensions

### Skill

- **alarm-memo-assistant-pro**
- Purpose: 定时任务触发时提供待办/备忘录管理上下文，确保数据读取和摘要格式与 skill 规范一致
- Expected outcome: 每日推送内容结构清晰，包含今日到期、高优先级、逾期、备忘录等分区，符合 skill 定义的标准输出模板
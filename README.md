# Lynx Skill Community

> The official community repository for sharing Lynx skill packages.

[English](#english) · [中文](#中文)

---

## English

### What is a Skill?

A **skill** is a small program that Lynx can call: it receives a context object (`ctx`) and returns a string or rich-text result. Skills extend what Lynx can do — text processing, code analysis, system operations, content generation, and more.

- **Import** — drop a skill file into Lynx's import dialog and it works instantly
- **Sandboxed** — every skill runs in a subprocess sandbox; first load requires user confirmation
- **Shareable** — publish your skill here for the global community

### Skill Formats

Lynx supports **5 single-file languages** plus **directory skills** (multi-file + manifest). Full specification: [`SKILL_FORMAT.md` in the main repo](https://github.com/ZeroDegree-Studio/LYNX/blob/main/SKILL_FORMAT.md).

| Type | File | Entry mechanism | Runtime |
|------|------|-----------------|---------|
| Python | `xxx.py` | `@skill` decorator | subprocess sandbox |
| JavaScript | `xxx.js` | `module.exports = fn` | Node.js subprocess |
| Bash | `xxx.sh` | reads ctx JSON from stdin | Bash subprocess |
| PowerShell | `xxx.ps1` | reads ctx JSON from `$input` | PowerShell subprocess |
| YAML | `xxx.yaml` | v1 template | prompt template |
| Directory | `my_skill/` + `manifest.yaml` | `manifest.entry` file | per manifest `language` |

Minimal Python skill:

```python
# my_skill.py
from agent.skills.decorator import skill

@skill(
    id="hello_world",
    name="打招呼",
    description="向选中的文本打招呼",
    trigger="selection",
    permission=["read_file"],
)
async def fn(ctx):
    return f"你好,我看到了:{ctx.selection}"
```

### Trigger Types

| Trigger | Meaning |
|---------|---------|
| `selection` | invoked on selected text (default) |
| `input` | invoked from the input box |
| `command` | invoked via `/skill_id` slash command |
| `file` | invoked when opening specific file types |
| `none` | manual, from the skill list only |

### Permission Model

Permissions (`read_file` / `write_file` / `execute` / `network` / `dangerous`) are soft hints injected into the LLM context to guide user consent. Lynx infers risk level from declared permissions; `dangerous: true` triggers a confirmation dialog before execution. **Declare what your skill actually does** — false declarations are grounds for PR rejection.

### Repository Structure

```
Lynx-Skill/
├── README.md                  # This file
├── CONTRIBUTING.md            # Submission guide
├── LICENSE                    # Repository license (MIT)
└── skills/
    └── <skill_id>/            # One directory per skill (directory skills)
        ├── manifest.yaml
        ├── main.py
        └── ...
    # or single-file skills:
    └── my_skill.py
```

### Contributing a Skill

1. Write your skill following [`SKILL_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/SKILL_FORMAT.md)
2. Fork this repository
3. Add your skill under `skills/` (single file or `<skill_id>/` directory)
4. Open a Pull Request — see [CONTRIBUTING.md](CONTRIBUTING.md) for review criteria

### Related

- **Lynx main repository**: [ZeroDegree-Studio/LYNX](https://github.com/ZeroDegree-Studio/LYNX)
- **Module system** ("everything is a module", `.lmp` packages): [`docs/MODULE_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/docs/MODULE_FORMAT.md)
- **Spore market** (experience sharing): [ZeroDegree-Studio/lynx-spore-market](https://github.com/ZeroDegree-Studio/lynx-spore-market)
- **ZeroDegree Studio**: [zerodegree.cc](https://zerodegree.cc)

---

## 中文

### 什么是技能？

**技能**（Skill）是一段可被 Lynx 桌面端调用的小程序：接收上下文 `ctx`，返回字符串或富文本结果。技能扩展 Lynx 的能力——文本处理、代码分析、系统运维、内容生成等等。

- **导入即用** — 把技能文件丢进 Lynx 的「导入」功能即可接入
- **沙箱隔离** — 每个技能运行在子进程沙盒中，首次加载需用户确认
- **社区共享** — 把你写的技能发布到这里，供全球用户使用

### 技能格式

Lynx 支持 **5 种单文件语言** + **目录技能**（多文件 + manifest）。完整规范见主仓库 [`SKILL_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/SKILL_FORMAT.md)。

| 类型 | 文件 | 入口机制 | 运行时 |
|------|------|---------|--------|
| Python | `xxx.py` | `@skill` 装饰器 | 子进程沙盒 |
| JavaScript | `xxx.js` | `module.exports = fn` | Node.js 子进程 |
| Bash | `xxx.sh` | stdin 读 ctx JSON | Bash 子进程 |
| PowerShell | `xxx.ps1` | `$input` 读 ctx JSON | PowerShell 子进程 |
| YAML | `xxx.yaml` | v1 模板 | 提示词模板 |
| 目录技能 | `my_skill/` + `manifest.yaml` | `manifest.entry` 文件 | 按 manifest `language` |

最小 Python 技能示例：

```python
# my_skill.py
from agent.skills.decorator import skill

@skill(
    id="hello_world",
    name="打招呼",
    description="向选中的文本打招呼",
    trigger="selection",
    permission=["read_file"],
)
async def fn(ctx):
    return f"你好,我看到了:{ctx.selection}"
```

### 触发方式

| 触发 | 含义 |
|------|------|
| `selection` | 选中文本触发（默认） |
| `input` | 输入框触发 |
| `command` | `/skill_id` 斜杠命令触发 |
| `file` | 打开特定类型文件时触发 |
| `none` | 仅从技能列表手动调用 |

### 权限模型

权限声明（`read_file` / `write_file` / `execute` / `network` / `dangerous`）是注入 LLM 上下文的"软提示"，引导 LLM 在调用工具前征得用户同意。Lynx 会根据声明推断风险等级；`dangerous: true` 执行前会弹二次确认。**声什么权就做什么事**——虚假声明是 PR 被拒的直接理由。

### 仓库结构

```
Lynx-Skill/
├── README.md                  # 本文件
├── CONTRIBUTING.md            # 提交指南
├── LICENSE                    # 仓库许可证（MIT）
└── skills/
    └── <skill_id>/            # 目录技能：一个技能一个目录
        ├── manifest.yaml
        ├── main.py
        └── ...
    # 单文件技能直接放 skills/ 下：
    └── my_skill.py
```

### 贡献技能

1. 按 [`SKILL_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/SKILL_FORMAT.md) 写你的技能
2. Fork 本仓库
3. 把技能放到 `skills/` 下（单文件或 `<skill_id>/` 目录）
4. 提交 Pull Request — 审核标准见 [CONTRIBUTING.md](CONTRIBUTING.md)

### 相关链接

- **Lynx 主仓库**：[ZeroDegree-Studio/LYNX](https://github.com/ZeroDegree-Studio/LYNX)
- **模块系统**（"一切皆模块"，`.lmp` 包）：[`docs/MODULE_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/docs/MODULE_FORMAT.md)
- **孢子市场**（经验共享）：[ZeroDegree-Studio/lynx-spore-market](https://github.com/ZeroDegree-Studio/lynx-spore-market)
- **零度工作室**：[zerodegree.cc](https://zerodegree.cc)

# Contributing to Lynx Skill Community

> How to submit a skill to the Lynx skill repository.

[English](#english) · [中文](#中文)

---

## English

### Quick Path

1. **Write the skill** following [`SKILL_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/SKILL_FORMAT.md) in the main repo
2. **Fork** this repository
3. **Add your skill** under `skills/`:
   - Single-file skill: `skills/my_skill.py` (or `.js` / `.sh` / `.ps1` / `.yaml`)
   - Directory skill: `skills/<skill_id>/` with `manifest.yaml` + entry file — directory name must equal `skill_id`
4. **Test locally** (see below)
5. **Open a Pull Request** — maintainers will review within 7 days

### Naming Conventions

| Item | Rule |
|------|------|
| `skill_id` | letters/digits/underscores, starts with a letter, 1–64 chars, globally unique |
| Directory name | must equal `skill_id` (directory skills) |
| `name` | display name, ≤12 chars recommended |
| `category` | free-form, used for grouping (e.g. `开发助手`, `文本处理`) |

### Review Criteria

Maintainers check:

1. ✅ Format valid per `SKILL_FORMAT.md` (entry mechanism, manifest fields, language rules)
2. ✅ Runs in the sandbox without errors
3. ✅ Permissions honestly declared — what the skill actually touches is what it declares
4. ✅ No malicious content (data exfiltration, destructive commands, credential harvesting)
5. ✅ No hardcoded local paths (`C:\Users\...`, `/home/user/...`) — read paths from `ctx`
6. ✅ No credentials, API keys, tokens, or personally identifiable information
7. ✅ Not a duplicate of an existing skill (same `skill_id` or near-identical function)
8. ✅ License compatible (default `MIT`; declare in `manifest.yaml` if different)

PRs that fail review will receive a comment explaining what to fix.

### Testing Before PR

1. Put the skill file / directory into Lynx's custom skills directory, or use the client's **Import** dialog
2. Invoke it via its trigger (`selection` / `input` / `/skill_id` command / skill list)
3. Verify the result and confirm it only touches what its `permission` declares

### PR Title Format

```
[skill] <skill_id> by <author>
```

Example: `[skill] git_commit_helper by alice`

### Updating an Existing Skill

1. **Do not** change the `skill_id`
2. Submit a PR replacing the old files, describe what changed in the PR body

### Removing a Skill

Open a PR deleting the skill, explain why in the description. Maintainers merge after confirming you're the original author.

### License

- **This repository** (docs, structure): [MIT License](LICENSE)
- **Each skill** may carry its own license (declare it in the skill header or `manifest.yaml`)

### Code of Conduct

- Be respectful in PR discussions
- No spam, no advertising, no malicious content
- Maintainers reserve the right to reject any PR

### Need Help?

- Open an issue with the `question` label
- Or read the full format spec: [`SKILL_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/SKILL_FORMAT.md)

---

## 中文

### 快速路径

1. **写技能** — 按主仓库 [`SKILL_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/SKILL_FORMAT.md) 规范编写
2. **Fork** 本仓库
3. **添加技能** 到 `skills/` 下：
   - 单文件技能：`skills/my_skill.py`（或 `.js` / `.sh` / `.ps1` / `.yaml`）
   - 目录技能：`skills/<skill_id>/` 含 `manifest.yaml` + 入口文件 — 目录名必须等于 `skill_id`
4. **本地测试**（见下）
5. **提交 Pull Request** — 维护者会在 7 天内审核

### 命名规范

| 项目 | 规则 |
|------|------|
| `skill_id` | 字母/数字/下划线，字母开头，1–64 字符，全局唯一 |
| 目录名 | 必须等于 `skill_id`（目录技能） |
| `name` | 显示名，建议 ≤12 字符 |
| `category` | 自由填写，用于分组（如 `开发助手`、`文本处理`） |

### 审核标准

维护者会检查：

1. ✅ 格式符合 `SKILL_FORMAT.md`（入口机制、manifest 字段、语言规则）
2. ✅ 沙箱内可正常运行
3. ✅ 权限如实声明 — 技能实际碰什么就声什么
4. ✅ 无恶意内容（数据外泄、破坏性命令、窃取凭证）
5. ✅ 无硬编码本地路径（`C:\Users\...`、`/home/user/...`）— 路径从 `ctx` 读
6. ✅ 无凭证、API 密钥、token 或个人隐私信息
7. ✅ 不是已有技能的重复（相同 `skill_id` 或功能高度雷同）
8. ✅ 许可证兼容（默认 `MIT`；不同的话在技能头或 `manifest.yaml` 声明）

审核未通过的 PR 会收到评论说明需要修改什么。

### 提 PR 前本地测试

1. 把技能文件/目录放进 Lynx 的自定义技能目录，或用客户端「导入」功能
2. 通过触发方式调用（`selection` / `input` / `/skill_id` 命令 / 技能列表）
3. 验证结果，确认它只碰了 `permission` 里声明的东西

### PR 标题格式

```
[skill] <skill_id> by <作者>
```

示例：`[skill] git_commit_helper by alice`

### 更新已有技能

1. **不要**改 `skill_id`
2. 提 PR 替换旧文件，在 PR 描述里写清改了什么

### 删除技能

提 PR 删除对应技能，在描述里说明原因。维护者确认你是原作者后合并。

### 许可证

- **本仓库**（文档、结构）：[MIT License](LICENSE)
- **每个技能**可自带许可证（在技能头或 `manifest.yaml` 里声明）

### 行为准则

- PR 讨论中保持尊重
- 不发垃圾信息、广告、恶意内容
- 维护者保留无理由拒绝任何 PR 的权利

### 需要帮助？

- 提 issue 并打 `question` 标签
- 或读完整格式规范：[`SKILL_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/SKILL_FORMAT.md)

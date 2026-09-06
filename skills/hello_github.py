# hello_github.py — 技能市场链路测试技能（下载安装后可通过 /hello_github 调用）
from agent.skills.decorator import skill


@skill(
    id="hello_github",
    name="GitHub 测试技能",
    description="验证技能市场下载链路的最小示例：返回一条问候",
    trigger="command",
    permission=[],
    category="测试",
)
async def fn(ctx):
    return "你好！这个技能来自 Lynx-Skill 仓库，下载安装成功 ✓"

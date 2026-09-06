# text_stats.py — 技能市场链路测试技能：统计选中文本（选中文本后触发）
from agent.skills.decorator import skill


@skill(
    id="text_stats",
    name="文本统计",
    description="统计选中文本的字符数、词数、行数",
    trigger="selection",
    permission=[],
    category="文本处理",
)
async def fn(ctx):
    text = getattr(ctx, "selection", "") or ctx.get("selection", "") if isinstance(ctx, dict) else str(getattr(ctx, "selection", "") or "")
    if not text:
        return "(没有选中文本)"
    lines = text.splitlines() or [""]
    words = len(text.split())
    return (
        f"字符数: {len(text)}\n"
        f"词数: {words}\n"
        f"行数: {len(lines)}"
    )

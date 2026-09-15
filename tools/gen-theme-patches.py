#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成各 Trime 主题的键盘补丁（<主题ID>.custom.yaml）。

背景
----
Trime 的主题补丁规则是「主题资源 ID + .custom.yaml」，而 `trime.custom.yaml` 只作用于内置主题 `trime`。
所以在设置里换成 mint / 单静 等第三方主题后，必须用同名补丁文件，否则 17/18/24 键键盘会消失。

本脚本以 `trime.custom.yaml` 为准（单一数据源），为每个主题生成一份补丁，内容包含：
  * 小鹤双拼 17/18/24 键键盘 + 英文 26 键键盘 + 切换键（`Trime_transcription` 等）
  * `preset_keys/Return1`（mint / 单静 主题缺少这个预设键）
  * 明暗配对（`light_scheme` / `dark_scheme`）：
      单静系 → 日间「谷歌白」/ 夜间「谷歌黑」（并把 default 也指向这对，选默认也能自动切换）
      单静·樱桃 → 日间「谷歌白」/ 夜间 cherry 本身（樱桃是深色方案，保留它的特色）
      mint   → 没有 google 配色，用主题自带 pair：蓝水鸭 ⇄ 黑水鸭
  * `"style/..."` 微调会被注释掉，保留主题自己的 keyboard_height / 字号

用法
----
    python3 tools/gen-theme-patches.py          # 在仓库根目录执行
然后重新部署 Trime。
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "trime.custom.yaml")

# 主题 ID -> (描述, 该主题必须一起部署的文件, 亮色方案, 暗色方案)
THEMES = {
    "mint.trime": (
        "薄荷 mint 主题（RimeTheme/ThemeForTrime）",
        ["mint.trime.yaml", "backgrounds/mint_light_blue/", "backgrounds/mint_dark_blue/"],
        "default",          # 蓝水鸭／Mint Light Blue
        "mint_dark_blue",   # 黑水鸭／Mint Dark Blue
    ),
    "单静.trime": (
        "单静主题（nopdan/danjing）",
        ["单静.trime.yaml", "danjing.yaml", "单静.patch.无障碍.yaml", "backgrounds/danjing.default/",
         "backgrounds/danjing.cherry/", "backgrounds/danjing.google_black/",
         "backgrounds/danjing.google_white/", "backgrounds/danjing.pink_blue/"],
        "google_white",     # 谷歌白
        "google_black",     # 谷歌黑
    ),
    "单静+.trime": (
        "单静+ 主题",
        ["单静+.trime.yaml", "单静.trime.yaml", "danjing.yaml", "单静.patch.无障碍.yaml", "backgrounds/（同单静）"],
        "google_white",
        "google_black",
    ),
    "单纯.trime": (
        "单纯主题",
        ["单纯.trime.yaml", "单静.trime.yaml", "danjing.yaml", "单静.patch.无障碍.yaml", "backgrounds/（同单静）"],
        "google_white",
        "google_black",
    ),
    "单纯+.trime": (
        "单纯+ 主题",
        ["单纯+.trime.yaml", "单纯.trime.yaml", "单静.trime.yaml", "danjing.yaml",
         "单静.patch.无障碍.yaml", "backgrounds/（同单静）"],
        "google_white",
        "google_black",
    ),
    "单静.cherry.trime": (
        "单静·樱桃主题（cherry 本身是深色方案）",
        ["单静.cherry.trime.yaml", "单静.trime.yaml", "danjing.yaml", "单静.patch.无障碍.yaml", "backgrounds/（同单静）"],
        "google_white",
        "default",          # 夜间就是 cherry 自己的配色
    ),
}


# 主题特有的「额外补丁」：少数主题的写法会让 Trime 解码主题时报错，必须在补丁里改掉。
# 每项是若干行 YAML（缩进与 patch 下其它键一致，即两个空格）。
EXTRA_PATCH = {
    "单静.cherry.trime": [
        "",
        "  # ==========================================================================",
        "  # cherry 主题的 preset_color_schemes/default 里带一个 `colors:` 列表",
        "  # （作者用 YAML 锚点在那里定义颜色；这个键对 Trime 本身没有意义）。",
        "  # Trime 解码配色时对每个值都做 `v.string!!`（data/theme/Theme.kt:79，3.3.12 与",
        "  # develop 一致）：列表不是标量 → 抛异常 → 整个主题被静默回退到内置 trime",
        "  # （现象就是「选了主题还是和默认一样」）。",
        "  # 锚点引用在 YAML 解析阶段就展开成字面值了，所以把这里置成空串不影响任何颜色。",
        "  # ==========================================================================",
        '  "preset_color_schemes/default/colors": ""',
    ],
}


def load_patch_body():
    """从 trime.custom.yaml 取出 patch 下的内容，并注释掉 style 微调。"""
    text = open(SRC, encoding="utf-8").read()
    lines = text.split("\n")
    start = next(i for i, l in enumerate(lines) if l.strip() == "patch:")
    body = "\n".join(lines[start + 1:])
    # 去掉「7. 深色模式」注释块（主题自带配对，见下方 pair block）
    marker = body.find("# 7. 可选：深色模式")
    if marker != -1:
        banner = body.rfind("  # ====", 0, marker)
        body = body[:banner].rstrip()
    # style 微调注释掉，保留主题自己的 style
    body = re.sub(r'(?m)^  ("style/[^\n]*)$', r"  # \1", body)
    return body


def pair_block(light, dark, theme_id):
    """生成明暗配对 + Return1 的补丁片段。"""
    night_is_self = (dark == "default")
    lines = [
        "",
        "  # ==========================================================================",
        "  # 主题缺少的预设键：内置 trime.yaml 有 Return1，mint / 单静 主题没有，",
        "  # 而我们的键盘用了 composing: Return1，所以在这里补上。",
        "  # ==========================================================================",
        '  "preset_keys/Return1":',
        "    label: Enter",
        "    send: Return",
        "",
        "  # ==========================================================================",
        "  # 明暗配对（「跟随系统夜间模式」用）",
        "  # --------------------------------------------------------------------------",
        "  # Trime 没有「分别选浅色/深色主题」的界面：它只看你当前选中的【配色】，",
        "  # 再按该配色里的 light_scheme / dark_scheme 两个链接决定另一模式用哪个配色。",
        "  # 这里显式写死配对，免得依赖主题（或主题变体的覆盖行为）：",
        f"  #   日间 -> {light}    夜间 -> {dark if not night_is_self else 'default（本主题配色）'}",
        "  # 想换别的：改这两行即可（值必须是对应主题里存在的配色 ID，见主题 yaml 的 preset_color_schemes）。",
        "  # ==========================================================================",
    ]
    # 明暗配对条目：用 dict 天然去重，并跳过自引用（如 default/light_scheme: default）
    links = {}
    links[(light, "dark_scheme")] = dark
    links[(dark, "light_scheme")] = light
    if night_is_self:
        # cherry：default 本身是夜间（深色）方案，只补一个日间亮色
        links[("default", "light_scheme")] = light
    else:
        # 让「默认」配色也走这一对：日间亮色、夜间暗色
        links[("default", "light_scheme")] = light
        links[("default", "dark_scheme")] = dark
    lines += [
        f'  "preset_color_schemes/{scheme}/{key}": {value}'
        for (scheme, key), value in links.items()
        if scheme != value
    ]
    lines += [
        "",
        "  # 上面的 style 微调（键盘高度/字号）已注释掉，保留主题自己的 style；",
        "  # 如果 17/18/24 键看起来太挤，把它们放开即可。",
        "",
    ]
    return "\n".join(lines)


def header(theme_id, desc, files):
    out = [
        f"# {theme_id}.custom.yaml —— 给「{desc}」补上小鹤双拼 17/18/24 键键盘 + 明暗配对",
        "# encoding: utf-8",
        "#",
        "# ⚠️ 本文件由 tools/gen-theme-patches.py 自动生成，请不要手改；",
        "#    要改键盘/配色配对，请改 trime.custom.yaml 或该脚本的表，然后重新生成。",
        "#",
        "# 为什么需要这个文件：",
        "#   Trime 的主题补丁规则是「主题资源 ID + .custom.yaml」，而 trime.custom.yaml 只作用于内置主题 trime。",
        f"#   一旦在设置里把主题切换为 {theme_id.split('.')[0]}，就必须用本文件，否则 17/18/24 键键盘与中英切换键都会消失",
        "#   （主题会按自己的预设键盘，如 qwerty / qwerty_ / qwertys 显示）。",
        "#",
        "# 使用：把主题文件与下面的文件都放到 Trime 用户目录**根部**，然后【部署】并在 设置 → 主题 里选择它：",
    ]
    out += [f"#   - {f}" for f in files]
    out += [
        "#",
        "# 明暗：本文件显式写了配色配对（见文件末尾），配合 设置 → 主题 → 打开「跟随系统夜间模式」即可自动切换；",
        "#       详见 README 第七、八节。",
        "patch:",
    ]
    return "\n".join(out)


def main():
    body = load_patch_body()
    written = []
    for theme_id, (desc, files, light, dark) in THEMES.items():
        extra = EXTRA_PATCH.get(theme_id, [])
        content = header(theme_id, desc, files) + "\n" + body + "\n" + pair_block(light, dark, theme_id)
        if extra:
            content += "\n" + "\n".join(extra) + "\n"
        path = os.path.join(ROOT, f"{theme_id}.custom.yaml")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        written.append(path)

    # 轻量自检：能解析、每个键盘每行宽度和为 100、配对键与 Return1 都在
    try:
        import yaml
    except ImportError:
        print("（未安装 PyYAML，跳过自检）")
    else:
        for path in written:
            data = yaml.safe_load(open(path, encoding="utf-8"))
            patch = data["patch"]
            bad = []
            for key, kb in patch.items():
                if not key.startswith("preset_keyboards/"):
                    continue
                default_w = kb.get("width", 10)
                acc = 0.0
                for k in kb["keys"]:
                    w = k.get("width", default_w)
                    if acc + w > 100.001 and acc > 0:
                        if abs(acc - 100) > 0.01:
                            bad.append(round(acc, 2))
                        acc = 0.0
                    acc += w
                if abs(acc - 100) > 0.01:
                    bad.append(round(acc, 2))
            pair = [k for k in patch if k.startswith("preset_color_schemes/")]
            print(f"✓ {os.path.basename(path):32s} patch 键={len(patch):3d} 明暗配对={len(pair)} 行宽异常={bad or '无'}")
    print(f"\n共生成 {len(written)} 个主题补丁。")


if __name__ == "__main__":
    main()

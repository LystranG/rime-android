# 薄荷 + 简纯+ Trime 组合包（Android 同文输入法）

**思路**：不再维护一整套自制补丁，改为——

* **方案/词库/lua**：手机上直接拉取 [oh-my-rime（薄荷）](https://github.com/Mintimate/oh-my-rime) 官方仓库（官方维护，升级 = git pull）；
* **键盘样式/布局**：直接用 [amzxyz/rime-wanxiang（万象）](https://github.com/amzxyz/rime-wanxiang) 官方维护的 Trime 主题 **简纯+**（26 键 / 18 键 / 14 键 + 英文键盘 + 功能键盘，万象官方本身就支持 Trime）；
* **本目录**：只放 4 个小补丁文件，把两者粘起来，并挂上 17/18 键共键映射；
* **词库同步**：两个方案的词典都是 `rime_mint`，与 macOS 端 `~/Library/Rime` 的方案**同词典名**
  → 三端共用同一个 `rime_mint.userdb`，Rime 的「同步用户数据」可以正确合并词频（Syncthing 只负责搬 `sync/` 目录）。

## 一、安卓用户目录结构

把下面所有内容平铺进 Trime 用户目录根部（**不要多套一层文件夹**）：

```text
<Trime用户目录>/                  ← /storage/emulated/0/rime 或「从外部存储同步」授权的目录
├── oh-my-rime 仓库的全部文件      ← git clone / 下载 zip 解压（default.yaml、dicts/、lua/、opencc/、*.schema.yaml …）
├── wanxiang-lts-zh-hans.gram     ← 万象语法模型（从万象 Releases 下载，Mac 端已有一份可直接拷）
├── 简纯+.trime.yaml              ← 本目录（万象官方主题）
├── backgrounds/                  ← 本目录（default / google_black / google_white 三套配色图）
├── fonts/                        ← 本目录（主题图标字体）
├── default.custom.yaml           ← 本目录（方案列表：小鹤双拼 + 薄荷全拼）
├── rime_mint.custom.yaml         ← 本目录（全拼：万象模型 + 18 键映射）
├── double_pinyin_flypy.custom.yaml ← 本目录（双拼：万象模型 + 17 键映射）
├── 简纯+.trime.yaml              ← 本目录（⚠️ 已把 17/18 键、func 按钮直接烘焙进主题源文件）
├── installation.yaml             ← installation_id: android（⚠️ 每台设备唯一，绝不参与 Syncthing 同步）
└── sync/                         ← Rime 同步导出目录（Syncthing 只共享这一层）
```

然后 Trime → 设置 → 主题 → 选 **简纯+** →【部署】。

## 二、键盘布局与方案的配对

17/18 键布局复刻四叶草官方「宇宙·十七键」（[forfudan/rime-clover-flypy](https://github.com/forfudan/rime-clover-flypy)，theme/cosmic17key）：左侧 18 宽功能键（简/123/符/Shift/英）+ 两侧留白，数字行下滑中文数字，字母键上滑标点；合并分组与官方方案完全一致（官方 `xlit/…/qqeettuiooaaddghjjlzzcvbbm/`）。四叶草官方只有 14/17 键，没有 18 键——「鹤18」是 17 键拆开 B/N 的同分组变体。

**切换方式**：主题里的「18键」**已经被直接替换为四叶草布局**（键盘 ID/名字都没变）——
你原来在设置里怎么切 18 键，现在切出来的就是四叶草 17/18 键，无需任何新习惯。
17 键（`小鹤双拼·17键`）也在同一个键盘列表里。功能键盘（长按回车）保持主题原样。

| 键盘 | 配合的方案 | 原理 |
| --- | --- | --- |
| 26 键（主题自带） | 全拼 / 双拼都能用 | 标准键盘 |
| 18 键（**已替换为四叶草布局**，名字仍叫「18键」） | **小鹤双拼 double_pinyin_flypy** | 四叶草分组拆开 B/N；`你好 = BN IO H C` 四键直出 |
| 17 键（本包新增「小鹤双拼·17键」） | **小鹤双拼 double_pinyin_flypy** | 四叶草 9 组合并（QW/ER/TY/OP/AS/DF/JK/ZX/BN），映射在 `double_pinyin_flypy.custom.yaml` |
| 14 键（主题自带） | 本包未启用 | 没加对应映射，忽略 |
| 26 键 + 全拼 | 薄荷全拼 rime_mint | 全拼没有共键映射（已移除，避免污染 26 键候选）；**全拼请用 26 键** |

> ⚠️ **万象官方 18 键不能用于双拼**：它的分组是按全拼设计的，小鹤里当韵母的
> `c/d/g/k/t/e/o/n` 都被合并掉、没有独立键（例：好 = 小鹤码 `hc`，`c` 在万象 18 键上
> 被并进 `X C` 键且发 `x`，只能打出 `hx`）。所以双拼请用 17 键或「鹤18」。
>
> ⚠️ 共键映射跟方案走：先切对方案，再切键盘（18键→全拼、17键/鹤18→双拼）。
>
> ✅ 映射用的是 `derive`（并集），**26 键永远可用**：开了 18/17 键映射后 26 键照常打字，
> 合并键上两类候选并存（比如 18 键的 `S D` 键 = s、d 的词都出）。这和万象原生的 `xlit`
> （替换式、切布局要改配置重部署）不同，是刻意选择的。
>
> 想让小鹤双拼默认就用 17 键：把主题文件里 `preset_keyboards/17jian` 改名为
> `preset_keyboards/double_pinyin_flypy` 即可（Trime 按「键盘 ID = 方案 ID」自动套用）。

## 三、词库同步（Syncthing + Rime 同步）

**原理**：Rime 的「同步用户数据」把 userdb 导出成 `sync/<installation_id>/*.userdb.txt`，
并把 `sync/` 里**其它 installation_id** 的快照合并回来。Syncthing 只负责把两端的 `sync/` 接起来。

1. **macOS（已配好）**：`~/Library/Rime/installation.yaml` 里 `installation_id: mac`、
   `sync_dir: /Users/lystran/data/rime`（该目录已是 Syncthing 共享文件夹，导出在 `sync/mac/`）。
2. **Android**：`installation.yaml` 写 `installation_id: android`（sync 默认在用户目录下 `sync/`，
   外部存储同步模式会在「同步用户数据」后导出回外部目录）。
3. **Syncthing**：两端共享**同一个文件夹**——Mac 端 `/Users/lystran/data/rime` ↔
   Android 端 `<Trime用户目录>/sync`。⚠️ 只共享 `sync/` 这一层！
4. 想同步时：两端各自点一次 Rime 的「同步用户数据」（Squirrel 菜单 / Trime 设置），Syncthing 负责搬运。

**绝对不要让 Syncthing 同步的东西**（会互相覆盖/损坏）：

* `installation.yaml` —— 每台设备必须唯一，被覆盖后合并逻辑失效；
* `build/`、`*.userdb/`（LevelDB 原始库）—— 只能由 Rime 自己的同步机制读写；
* 整个用户目录 —— Trime 外部同步模式会按外部目录删除内部多余文件，和 Syncthing 混用会互删。

## 四、已知差异 / 注意事项

* **简繁/其他开关**：主题不带简繁键，走候选栏菜单或方案菜单（空格上滑 Menu）。
* **英文键盘返回**：17 键上按`英`进入英文 26 键；英文键盘上长按原位返回键回到 26 键中文
  （主题自带行为），再从功能键盘切回 17 键。
* **万象的斜杠指令**（`/flypy`、`/zrm` 切输入类型）是万象方案的功能，薄荷方案没有，本包不依赖它。
* **14 键**：主题自带键盘保留但无映射，不可用。
* **重要：17/18 键是直接烘焙在 `简纯+.trime.yaml` 主题源文件里的**（不走 `.custom.yaml`
  补丁 —— 实测部分 Trime 版本对主题 custom 补丁的支持不稳定，直接改主题文件最可靠）。
  因此**升级万象、重新下载简纯+ 主题时，不要用官方原版覆盖本主题文件**；若要跟上游更新，
  用文件对比工具把本文件中「本组合包新增」注释标注的段落（两个键盘 + 5 个预设键 +
  func 按钮两处 + style/keyboards 两行 + 18jian 的 ascii_keyboard）搬到新版里。
* **更新**：oh-my-rime、万象主题各自 `git pull` / 重新下载即可，本目录 4 个补丁不用动；
  万象若把 `简纯+.trime.yaml` 结构改了，需对照检查本补丁。

## 五、部署后验证清单

1. 部署后在方案菜单里看到「小鹤双拼」「薄荷拼音」两个方案；
2. 切到「小鹤双拼」方案 → 键盘自动变成四叶草 18 键（`double_pinyin_flypy` 方案绑定）；
   键盘外观与主题自带 18 键完全同款（圆角图片键、数字行、功能行），只是字母排布为四叶草分组；
3. 双拼 + 17 键：按 `L` + `QW`（=lq）出「累/刘」；按 `BN` + `I`（=bi）出「你」；
   双拼 + 鹤18：按 `BN` `IO` `H` `C`（=ni hc）出「你好」；
   数字键下滑出中文数字（一/二/…），字母键上滑出标点（复刻官方手势）；
4. 全拼 + 18 键：按 `S D` 键出 s/d 两类候选，按 `B N` 键出 b/n 两类候选；
5. 切回 26 键照常精确输入（derive 并集不破坏 26 键）；
6. 密码框等强制英文场景自动变英文 26 键；
7. 两端各点一次「同步用户数据」后，检查 `sync/` 里出现 `android/` 和 `mac/` 两个子目录，
   且 `rime_mint.userdb.txt` 两边都在；再点一次同步，另一端的词频应出现对端学到的词。

# 同文输入法（Trime / Android）配置说明

这套文件是给 **Android 上「同文输入法 Trime」** 用的 oh-my-rime（薄荷）+ 万象词库配置，
基于 macOS 上 `~/Library/Rime` 的配置改写，新增了 **小鹤双拼 17 / 18 / 24 键** 三套共键键盘
（布局参考 [forfudan/rime-clover-flypy](https://github.com/forfudan/rime-clover-flypy) 的四叶草·宇宙十七键）。

## 一、文件清单

| 文件 | 作用 |
| --- | --- |
| `default.custom.yaml` | 全局补丁：方案列表（小鹤双拼 + 薄荷全拼）、外接键盘中英切换行为 |
| `double_pinyin_flypy.custom.yaml` | 小鹤双拼：候选个数、万象模型设置、**共键（17/18/24 键）拼写扩展 derive 规则** |
| `rime_mint.custom.yaml` | 薄荷全拼：候选个数、万象模型设置（全拼不使用共键，自动用 26 键） |
| `wanxiang.yaml` | 万象模型的 `grammar` / `translator` 调参片段。**目前只被全拼 `rime_mint.custom.yaml` 用 `__include` 引用**；小鹤双拼因为要与 `speller/algebra/+` 共存，已改为在 `double_pinyin_flypy.custom.yaml` 里**内联**（原因见第四节，重要）|
| `trime.custom.yaml` | **Trime 前端主题补丁**：17 / 18 / 24 键中文键盘 + 英文 26 键键盘 + 键盘切换按键 + 界面微调 |
| `installation.yaml` | 安装信息：`installation_id: android`，`sync_dir: "sync"`（= Trime 用户目录/sync） |
| `mint.trime.yaml` | 薄荷主题源文件。⚠️ **本仓库这份已补入上游漏掉的 `styl`/`conf` 定义，不要用上游原版直接覆盖**（否则 librime 编译失败、主题静默回退，见第八节）|
| `<主题>.trime.yaml` | 单静 / 单静+ / 单静·樱桃 / 单纯 / 单纯+ 各自的主题源文件（上游原样）|
| `danjing.yaml`、`单静.patch.无障碍.yaml` | 单静系主题的**硬依赖**（键盘库 + 无障碍补丁），必须和主题一起部署 |
| `backgrounds/` | 两套主题的背景图（`mint_*` / `danjing.*` 互不干扰）|
| `tools/gen-theme-patches.py` | 由 `trime.custom.yaml` 一键重新生成 6 个主题补丁（改键盘/改配色配对后跑一下）|
| `README-Trime-Android.md` | 本说明文件 |

> 主题的**源码仓库（`themes/`，约 22MB，含 PSD 模板/Demo）已删除** —— 部署不需要它，
> 根目录里已经放了真正要部署的主题文件与 `backgrounds/`。需要更新主题时再临时拉下来（具体命令见第八节末尾）。

> 这些文件是 **补丁（.custom.yaml）+ 说明**，不是完整配置。使用时请把它们和
> oh-my-rime 仓库的其它文件一起放到 **Trime 用户目录的根目录**（不要多套一层文件夹）。

## 二、部署步骤（推荐：Trime ≥3.3.12「从外部存储同步」模式）

Trime 新版的官方描述是：**「每次部署或同步用户数据前，从指定目录导入数据到内部存储，并在同步用户数据后导出到该目录。」**
所以要点是「先把文件准备到外部目录，再让 Trime 导入」。完整顺序：

1. **准备外部目录**：用手机存储根部的 `/storage/emulated/0/rime`（即 Trime 老版本的默认用户目录）。
2. **把文件全部放进这个目录的根部**（⚠️ 不要多套一层文件夹）：
   * oh-my-rime（薄荷）仓库的全部文件（`dicts/`、`lua/`、`*.schema.yaml` …）；
   * 本目录的文件（覆盖同名项）：`default.custom.yaml`、`double_pinyin_flypy.custom.yaml`、`rime_mint.custom.yaml`、`wanxiang.yaml`、`trime.custom.yaml`、`installation.yaml`；
   * `wanxiang-lts-zh-hans.gram`（约 400MB，建议直接从 mac 拷，见第五节）。
   * 用 `git clone` 拉仓库的话会带 `.git/`、`.github/` 等无关文件：无害，但会被一起导入内部存储，介意就只拷需要的文件。
3. **在 Trime 里设置**：设置 → 数据存储模式 → **从外部存储同步** → 选中上面那个文件夹（会弹系统文件夹选择器）。
4. **点【部署】**。部署前 Trime 会自动把外部目录导入内部存储，所以「部署 = 导入 + 编译」；首次要编译万象大词库，可能要几分钟，期间不要反复点。
5. **以后更新**：改外部目录里的文件（或在里面 `git pull`）→ 再点一次【部署】。导入是**增量**的（按大小/修改时间跳过），所以 400MB 模型只在首次拷一次。

⚠️ 两个必须记住的坑：

* **不要用 Trime 界面改方案列表/配置**：界面改的是**内部**文件（如 `default.custom.yaml`），下次部署导入时会被**外部**文件覆盖。要改就改外部目录里的 `default.custom.yaml`（本目录已提供）。
* **`.gram` 必须在外部目录里**：导入时 Trime 会以外部目录为基准，删掉内部多出来、外部没有的文件（`installation.yaml` 与本机 `sync/` 除外）。

### 如果你还在用 Trime ≤ 3.3.11

用户目录默认就是 `/storage/emulated/0/rime`（可自定义其他路径），**没有**导入/导出这一步：
把上面的文件直接放进去 → 点【部署】即可。`installation.yaml` 同样放根部。

### 如果选「使用应用专属存储空间」

文件要放到 `/storage/emulated/0/Android/data/com.osfans.trime/files/rime/`，不存在导入/覆盖问题（但 Android 11+
访问 `Android/data` 受限，需用 Trime 自带入口或支持该路径的文件管理器/Syncthing 写入）。不熟悉的话用外部同步模式更省事。

## 三、键盘布局

三套中文键盘都是「共键」布局：**一个键只发一个字母**（四叶草做法），被合并掉的两个字母
通过方案里的 `derive` 规则改写（见下一节），所以既能少按键、又能打出全部音节。

### 小鹤双拼 · 17 键（默认）
```
1    2    3    4    5    6    7    8    9    0    简
QW   ER   TY   U    I    OP
AS   DF   G    H    JK   L
Shift ZX  C    V    BN   M    ⌫
英   符   17   18   24   空格    ，。    ⏎
```
合并：`q←w`、`e←r`、`t←y`、`o←p`、`a←s`、`d←f`、`j←k`、`z←x`、`b←n`（四叶草全部 9 组）

### 小鹤双拼 · 18 键
```
1    2    3    4    5    6    7    8    9    0    简
QW   ER   TY   U    I    OP
AS   DF   G    H    JK   L
Shift ZX  C    V    B    N    M    ⌫
英   符   17   18   24   空格    ，。    ⏎
```
合并：17 键的 9 组里拆开 `b/n`，只保留 8 组（3 行 6+6+6，最整齐）

### 小鹤双拼 · 24 键
```
1    2    3    4    5    6    7    8    9    0    简
Q    W    E    R    T    Y    U    I    OP
A    S    D    F    G    H    JK   L
Shift Z X   C    V    B    N    M    ⌫
英   符   17   18   24   空格    ，。    ⏎
```
合并：只保留 `o←p`、`j←k` 两组（3 行 9+8+7，最接近全键盘，重码最少）

### 键盘上的功能键
| 键 | 功能 |
| --- | --- |
| `17` / `18` / `24` | 直接切换到对应布局（**默认是 17 键**） |
| `英` | 切到英文 26 键键盘（`flypy_en`）；英文键盘上的 `中` 键切回中文 |
| `符` | 符号键盘；**长按** = 数字键盘 |
| `空格` | 长按/上滑 = 方案菜单（也可在候选栏菜单里操作） |
| `简` | 简繁切换（薄荷的 `transcription` 开关） |
| 数字键上滑 | `!@#$%^&*()` |
| `，。` | 点按 `，`，上滑 `。` |

> 应用强制英文（如密码框）时，Trime 会按 `ascii_keyboard: flypy_en` 自动跳到英文 26 键，
> 不会因为共键键盘少字母而打不出英文。

### 17/18/24 键与默认方案绑定
Trime 的规则是：**键盘 ID 与方案 `schema_id` 同名时自动套用**（`KeyboardWindow.smartMatchKeyboard`）。
所以 `trime.custom.yaml` 里把 17 键布局直接命名为 `double_pinyin_flypy` ——
「小鹤双拼-薄荷定制」默认就是 17 键；薄荷全拼（`rime_mint`）的 alphabet 是 26 个字母，
会自动套用内置 `qwerty`（26 键）。

想换默认布局（例如默认 18 键），把 `trime.custom.yaml` 里
`"preset_keyboards/double_pinyin_flypy"` 的内容换成 `import_preset: flypy_18` 即可
（或把 `flypy_18` 的 `keys` 整段复制过去）。

### 小鹤双拼韵母助记（键盘上 hint 显示的内容）
| 键 | 韵母 | 键 | 韵母 | 键 | 韵母 |
| --- | --- | --- | --- | --- | --- |
| q | iu | w | ei | e | e |
| r | uan / er | t | ue / üe | y | un |
| u | u（也是 sh） | i | i（也是 ch） | o | uo / o |
| p | ie | a | a | s | ong / iong |
| d | ai | f | en | g | eng |
| h | ang | j | an | k | ing / uai |
| l | iang / uang | z | ou | x | ia / ua |
| c | ao | v | ui / ü（也是 zh） | b | in |
| n | iao | m | ian | | |

## 四、共键是怎么实现的（重要）

* **键盘侧**（`trime.custom.yaml`）：共键键只发送代表字母，例如 `{click: q, label: 'QW'}`。
* **方案侧**（`double_pinyin_flypy.custom.yaml` 里的 `"speller/algebra/+"`）：
  ```yaml
  - "derive/w/q/"   # q ← w
  - "derive/r/e/"   # e ← r
  ...（共 9 条，对应 9 组合并）
  ```
  用 `derive` 而不是 `xform`/`xlit`：`derive` 只**新增**拼写、保留原拼写，因此
  1. 24 键上单独的 `w / r / y / p / s / f / k / x / n` 键不会被废掉；
  2. 26 键全键盘（桌面端、Trime 内置 qwerty）依然能正常输入，不会出现「死键」。

举例：`累(lei)` 的小鹤码是 `lw`，加上 `derive/w/q/` 后 `lw` 与 `lq` 都能查到；
在 17/18/24 键上按 `L` + `QW`键（发 q）即可。

**副作用（可接受）**：同一个方案下，26 键全键盘输入代表字母时会多出一些「共键候选」
（例如打 `lq` 会同时出现「刘 / 累」）。若不需要共键，把 `"speller/algebra/+"` 整段删掉再部署即可。

**使用窍门**：共键键（代表字母）是「模糊」的，未合并的字母键是「精确」的 ——

* 18 键：`B` 键会同时给出 b- / n- 候选；要精确的 n 声母或 iao 韵母时用 `N` 键。
* 24 键：`OP` 键（发 o）同时给 uo/o 与 ie，`JK` 键（发 j）同时给 an 与 ing/uai；
  而 `W`(ei)、`R`(uan/er)、`Y`(un)、`S`(ong)、`F`(en)、`X`(ia/ua)、`N`(iao) 各只有一种读音，
  按 26 键的习惯直接按这些键即可得到精确候选。

### ⚠️ 必须避开的坑：`__include` 不能和 `speller/algebra/+` 同处一个补丁

本文件原来写的是 `__include: wanxiang:/settings`（薄荷/万象文档的推荐写法），但它和 `"speller/algebra/+"`
放在同一个补丁里时，**librime 会把方案编译坏**：部署提示成功，却**任何输入都没有候选**（输入框里只显示原始编码，打 `ni` 不出「你」），
而同一台设备上的全拼（`rime_mint`，也有 `__include` 但没有 algebra 追加）完全正常。

本机用 librime 1.16 + 真实薄荷方案/万象词库实测（每次清空 `build/double_pinyin_flypy.*` 后重建，可重复）：

| 补丁写法 | 结果 |
| --- | --- |
| `__include: wanxiang:/settings` + `speller/algebra/+` | ❌ 无候选（prism 104184，与顺序无关、与是否有 .gram 无关）|
| 把 `__include` 挪到最后一行 | ❌ 依旧无候选 |
| **内联全部万象设置 + `speller/algebra/+`** | ✅ `ni→你`、`bi→你/比`、`lq→累/刘`、`lw→累`、`nihc→你好` |

所以本文件把 `wanxiang.yaml` 的内容**内联**进来了；`wanxiang.yaml` 则保留给全拼（`rime_mint.custom.yaml`，它没有 algebra 追加，继续用 `__include` 没问题）。
改万象参数时记得两处一起改。

## 五、万象模型

* 词库：oh-my-rime 自带的 `dicts/rime_mint.*.dict.yaml`（2025-07-09 起为万象词库），无需额外下载。
* 参数：`wanxiang.yaml` 里的 `grammar`（`collocation_max_length` 等）与
  `translator/contextual_suggestions`、`max_homophones`、`max_homographs`，
  由两个方案的 custom 通过 `__include: wanxiang:/settings` 引入。
* **语法模型 `.gram`（约 400MB）未包含在配置里**：Trime 找不到该文件时会提示加载失败并按「无语言模型」
  继续工作，不影响输入。要启用见下面「模型下载 / 放置」。
* 注意：`menu/page_size`（候选个数）必须写在**方案**的 `.custom.yaml` 里（薄荷把 `menu` 冗余写进了每个方案），
  写在 `default.custom.yaml` 里对薄荷方案无效。

### 语法模型（.gram）该下载哪个、放哪里

官方只有两个语法模型，都在同一个 LTS release 里（长期维护、会不定期重建）：

| 文件 | 大小 | 说明 |
| --- | --- | --- |
| `wanxiang-lts-zh-hans.gram` | 400.5 MB | **简体，本配置用这个**（对应 `wanxiang.yaml` 里的 `grammar/language: wanxiang-lts-zh-hans`）|
| `wanxiang-lts-zh-hant.gram` | 402.2 MB | 繁体模型；薄荷的简繁转换走 OpenCC，一般**不需要**这个 |

* 下载页：<https://github.com/amzxyz/RIME-LMDG/releases/tag/LTS>
* 直链：<https://github.com/amzxyz/RIME-LMDG/releases/download/LTS/wanxiang-lts-zh-hans.gram>
* **省事做法：mac 上已经有同一份文件**（`~/Library/Rime/wanxiang-lts-zh-hans.gram`，419,910,700 字节），
  直接拷到 Android 即可 —— 既省一次 400MB 下载，又保证两端模型完全一致。
* 放置位置：Trime **用户目录根部**（与 `installation.yaml` 同级），然后【部署】。
* ⚠️ Trime ≥3.3.12 且「数据存储模式 = 从外部存储同步(SAF)」时：`.gram` 必须放在**你授权的那个外部目录**里。
  因为 Trime 导入时会拿外部目录当基准，**删掉内部目录里外部不存在的文件**（`installation.yaml` 与本机 `sync/` 除外），
  只放在内部目录的 `.gram` 会被当孤儿文件清掉。400MB 首次导入耗时较长，耐心等部署/导入结束。
* 另一种途径：万象官方发布包里有安卓一键更新 App（`Wanxiang-Updater-Android-v2.2.apk`，见 `tool` release），
  可一键下载并部署万象的**方案/词库/模型**到同文目录；但那是给「直接用万象方案」的人准备的，
  我们用的是薄荷方案 + 万象词库，手动只放 `.gram` 更干净。

### 用万象安卓更新器更新模型（可选，官方 APK）

官方 App：`Wanxiang-Updater-Android-v2.2.apk`（在 [RIME-LMDG releases 的 `tool` tag](https://github.com/amzxyz/RIME-LMDG/releases/tag/tool) 里；
源码在同仓库 `tool` 分支 `wanxiang-updater/`，Kotlin + Compose）。它把万象的**方案包 / 词库包 / 模型**解压覆盖到你指定的目录，
**不会整目录替换、也不会删除目标目录里多出来的文件**，但**没有备份 / 回滚**功能。

四个更新通道（源码 `MainActivity.kt`）：

| 按钮 | 下载内容 |
| --- | --- |
| 🧠 仅模型 | 只下 `wanxiang-lts-zh-hans.gram` ← **推荐：只动模型，不碰任何 oh-my-rime 文件** |
| 📖 仅词库 | 下 `base-dicts.zip`（dict-nightly 滚动版）解到 `<目标>/dicts/` |
| ⚙️ 仅方案 | 下 `rime-wanxiang-*.zip`（最新正式版方案包） |
| 🚀 全量更新 | 上面三样一起 |

**页面上的其它选项都是干什么的（结论：只用「仅模型」时全都不用管）**：

| 选项 | 影响范围 | 对「仅模型」有无影响 |
| --- | --- | --- |
| 📦 方案版本（Pro / Base / Lite / Pure，Pro 再选辅助类型）| 只决定**方案包**与**词库包**的文件名：`rime-wanxiang-{base,lite,pure,pro-<辅助>-fuzhu}.zip`、`{base,lite,pure,pro-<辅助>-fuzhu}-dicts.zip` | **无影响**（模型 URL 是固定的）|
| 🚀 更新通道（正式版 / 预览）| 只决定方案包取自最新 Release 还是 dict-nightly 滚动 tag（词库永远走 dict-nightly）| **无影响** |
| 🌐 下载源（CNB / GitHub，默认 CNB）| 只决定从哪个镜像下载；CNB 是万象官方国内镜像 | 都行，CNB 更快 |
| 📁 目标集 | 默认 `/rime`；也可加 SAF 授权目录 / Root 目录 | 保持默认 `/rime` |

模型的下载地址是写死的、与方案版本无关：
GitHub `RIME-LMDG/releases/download/LTS/wanxiang-lts-zh-hans.gram`、CNB `…/releases/download/model/wanxiang-lts-zh-hans.gram`。

> 唯一真正的「版本关系」：万象官方说**词库与模型紧耦合**（词库是上文）。而你的词库是 oh-my-rime 自带的
> `dicts/rime_mint.*`（由 oh-my-rime CI 从万象同步，可能比模型滞后一点）。这种「模型比词库新」的状态不会报错，
> 只是语言模型的收益小幅打折 —— 想严格一致就得改用万象自己的方案（会覆盖 `default.yaml`，不建议）。

**默认的防覆盖保护**（源码 `DEFAULT_EXCLUDE_RULES`，命中且本地文件已存在时强制跳过覆盖）：

```text
^custom_phrase\.txt$      .*userdb$        .*userdb\.txt     sequence.*txt
^(?!custom/).*\.custom\.yaml$               ^user\.yaml$      ^installation\.yaml$     ^sync/.*
```

→ 本目录的 4 个 `.custom.yaml` 与 `installation.yaml` **都在保护范围内**，即使误点全量更新也不会被改。

操作步骤（配合 Trime「从外部存储同步」模式）：

1. 安装 APK，授予**所有文件访问权限**（App 内写明：该权限仅用于写手机根目录的 `/rime`）。
2. 目标路径保持默认 `🎯 /rime`（= `/storage/emulated/0/rime`，即你在 Trime 里授权的那个外部目录）。
   ⚠️ **不要**指到 `/storage/emulated/0/Android/data/com.osfans.trime/files/rime`：那是 Trime 的**内部**目录，
   下次「部署 / 同步」的孤儿清理会把它删掉。
3. 选 **🧠 仅模型** → 点「立即更新」。
4. 回 Trime 点【部署】，让内部重新导入并加载新模型。

⚠️ **不要用「🚀 全量更新 / ⚙️ 仅方案」**，除非先做了备份：万象方案包根目录带有 `default.yaml`、`weasel.yaml`、`README.md`，
这三个与 oh-my-rime 同名且**不在**保护名单里。其中 `default.yaml` 被换掉的后果较重（薄荷方案里大量 `import_preset: default`
会改从万象版继承 key_binder / recognizer，schema_list 也会变成只剩 wanxiang）。确实要用的话，先在 App 的
「▶ 展开防覆盖保护配置 (高级)」里追加：

```text
^default\.yaml$
^weasel\.yaml$
^README\.md$
```

补充：更新器有 GitHub / CNB 双下载源（国内可走 CNB 镜像），可填 GitHub Token 提高 API 限额；
「仅词库」只会往 `dicts/` 里加万象自己的词库（`zi/jichu/en/…`），与薄荷的 `dicts/rime_mint.*` **不重名**，
但薄荷不会引用它们，只是多占空间与部署时间——用薄荷的话，只更新模型就够了。

### 模型 / 词库版本与多设备同步

* `.gram` **不参与 Rime 同步**：同步目录里只有 `*.userdb.txt`，加上用户目录根部 YAML/TXT 的单向备份
  （已在 mac 的 `sync/mac/` 里核实：没有任何非 yaml/txt 文件）。所以模型不会在两台设备之间传播，
  也就**不存在因模型版本不同而同步冲突**的问题。
* 因此同步层面**不要求**模型版本一致；但为了让断句与候选排序一致，建议各设备用**同一份 `.gram`**
  （从 mac 拷贝天然一致）。
* 真正要求一致的是**词库与方案版本**：万象文档明确「用户词编码必须与当前方案使用的编码体系保持一致」。
  薄荷下小鹤双拼（`double_pinyin_flypy`）与全拼（`rime_mint`）共用 `rime_mint` 词库，用户词库名都是
  `rime_mint.userdb`，所以两端 `sync/<设备ID>/rime_mint.userdb.txt` 能按 `db_name` 正确合并；
  若两端词库/方案版本不同，同步过来的用户词编码/词频可能与本地不匹配（轻则该词不参与调频，重则候选异常）。
* 建议的更新节奏：把 **模型 + 词库 + 方案** 当作一整套，**一次更新完所有设备**；更新前各设备先同步一次、
  更新后再同步一次。LTS 资产会被重建，不同时间下载可能拿到不同 build —— 从 mac 拷同一份文件最稳。

## 六、同步目录

`installation.yaml` 已配置好：

```yaml
installation_id: android
sync_dir: "sync"
```

* `sync_dir: "sync"` 是**相对路径**，即 **Trime 用户目录/sync**；同步后会在其中生成 `sync/android/*.userdb.txt`。
* 用 Trime 的【同步用户数据】或【后台定时同步】执行同步。
* **想让 mac 和 Android 真正互通**：两端得指向 Syncthing 文件夹里的**同一层**同步目录。

  现状：mac 的 `~/Library/Rime/installation.yaml` 里 `sync_dir = /Users/lystran/data/rime`，
  同步数据就落在该目录下的 `mac/`（它是 Syncthing 文件夹，有 `.stfolder`）；
  而 Android 是 `<外部目录>/sync/android/`（`sync_dir: "sync"` + 外部目录 `/storage/emulated/0/rime`）。
  两边的层级不一样，直接对拷合并不了。

  **最简单、不用改 mac 的做法**：在 Syncthing 里把两端配成同一个 folder：
  * Android 端：`/storage/emulated/0/rime/sync`
  * mac 端：`/Users/lystran/data/rime`

  这样 Android 的 `sync/android/` 与 mac 的 `mac/` 就成了同一目录下的兄弟目录，
  每端的 librime 同步时都会读取同层所有设备子目录并合并 ✓。
* 顺带：SAF 模式下同步是「内部 `<用户目录>/sync/android/` 写完 → 导出到 `<外部目录>/sync/android/`」，
  同步完可以直接在文件管理器里看到结果。
* 两端 `installation_id` 必须不同（mac 是 `mac`，Android 是 `android`），
  合并后结构就是 `sync/mac/…` + `sync/android/…`。
* 只同步 `sync` 目录，**不要**用网盘/Syncthing 直接同步整个用户目录（正在使用的 userdb 会坏）；
  也不要手动把两端设备子目录的内容互相覆盖。

## 七、深色模式 / 夜间配色自动切换

**支持**，但要分成两层来看（两层互不相干）：

| 层 | 在哪里开 | 机制（源码）|
| --- | --- | --- |
| App **界面**（设置页 / 候选栏 / 工具栏） | 设置 → 高级 → **用户界面模式** → 自动 / 亮色 / 暗色 | `AppPrefs.Advanced.UiMode` → `AppCompatDelegate.setDefaultNightMode(MODE_NIGHT_FOLLOW_SYSTEM / NO / YES)`（`AdvancedSettingsFragment.kt`）|
| **键盘配色** | 设置 → 主题 → **跟随系统夜间模式** 开关 | `ThemePrefs.follow_system_day_night` → `ColorManager.evaluateActiveColorScheme()`；系统切换夜/昼时会实时重算（`ColorManager.onSystemNightModeChange` ← `TrimeApplication` 监听 configuration 变化）|

关键：**键盘配色那层需要「明暗配对」才会生效**。Trime 内置默认主题 `trime.yaml` 里一个配对都没写（`light_scheme` / `dark_scheme` 出现 0 次；第三方主题如 `tongwenfeng.trime.yaml` 写了 2 处），而解析逻辑在没有配对时最终会**回退到 `default` 配色**（v3.3.12 源码：`?: colorScheme("default") ?: theme.colorSchemes.first()`），所以光打开开关看不出变化。

### 配对语义（v3.3.12 `ColorManager.evaluateActiveColorScheme`，develop 重构成 `ColorSchemeResolver`，行为一致）

在某个配色的 colors 里写 `light_scheme` / `dark_scheme`：

* **两个都写** → 按当前模式二选一（当它是「切换器」）；
* **只写 `light_scheme`** → 当前配色被当作**暗色**方案：夜间用它自己，白天切成 `light_scheme`；
* **只写 `dark_scheme`** → 当前配色被当作**亮色**方案：白天用它自己，夜间切成 `dark_scheme`；
* **都没写** → 用 `default` 配色的那对链接。

### 配置示例（推荐：一对内置配色互为配对）

内置配色里浅色的有 `default`/`aqua`/`luna`/`google`/`flypy`/`cool_breeze`/`so_young`…，深色的有 `dark_temple`(暗堂 `0x222222`)/`steam`/`ps4`/`starcraft_ii`/`solarized_rock`/`dota_2`/`modern_warfare`/`lost_temple`…

在 `trime.custom.yaml` 里加（文件末尾已附**注释版**，去掉注释即可用）：

```yaml
patch:
  # 白天用「小鹤飞扬」，夜间自动切到「暗堂」
  "preset_color_schemes/flypy/dark_scheme": dark_temple
  # 反向：如果选中的是「暗堂」，白天自动切回「小鹤飞扬」
  "preset_color_schemes/dark_temple/light_scheme": flypy
```

操作顺序：

1. 部署 → 在 Trime 里选「配色」为 **小鹤飞扬**（写 `dark_scheme` 的那个亮色方案）。
2. 打开「**跟随系统夜间模式**」开关。
3. 切换手机系统的深色模式，键盘背景应当面变化（无需重新部署）。

若想让**所有**配色都跟着系统变，也可以只给内置 `default` 加一对（未写链接的配色会回退到这对）：

```yaml
patch:
  "preset_color_schemes/default/dark_scheme": dark_temple
  "preset_color_schemes/default/light_scheme": default
```

> 注意：这样在白天时，任何“自身没写链接”的配色都会被切成 `default` 的亮色效果（而不是它自己）——这是源码里 `else -> defaultModeScheme` 的语义，所以更推荐「成对声明」。
>
> 另外：mac 上鼠须管的皮肤（`squirrel.custom.yaml` 里的 `style/color_scheme` / `color_scheme_dark`）**在 Trime 上不适用**，Trime 用的是自己的 `preset_color_schemes` + 上面这套配对机制。

## 八、主题（RimeTheme 的 mint / nopdan 的单静）

根目录里放的是**可部署文件**（主题源码仓库已删除，理由见下）：

| 主题 | 根目录需要一起部署的文件 | 说明 |
| --- | --- | --- |
| 薄荷 mint（`RimeTheme/ThemeForTrime`） | `mint.trime.yaml` + `backgrounds/mint_light_blue/` + `backgrounds/mint_dark_blue/` | 薄荷作者的 Trime 皮肤，基于单静主题精简制作 |
| 单静（`nopdan/danjing`） | `单静.trime.yaml`、`danjing.yaml`、`单静.patch.无障碍.yaml` + `backgrounds/danjing.*/` | 主主题。注意 `danjing.yaml` 是它的**键盘库**（被 `danjing:/keyboards` 引用）、`单静.patch.无障碍.yaml` 被 `__patch` 引用，两者都**必须有** |
| 单静+ / 单静·樱桃 / 单纯 / 单纯+ | 各自的 `*.trime.yaml` + 上面单静那三个文件 + backgrounds | 变体主题，都 `__include` 单静主主题 |

### ⚠️ 主题「失效」的机制与两个必修项（2026-09 已修）

**机制**：Trime 3.3.10 以后，主题是「先编译、再解码」两段式（`ThemeManager.loadThemeByIdOrNull`：
`Rime.deployRimeConfigFile()` 把 `<主题>.yaml` 编译成 `build/<主题>.yaml` → 读它 → `Theme.decode()`）。
**任何一步失败都会静默回退到内置 `trime` 主题** —— 界面没有任何提示，只有 logcat 里一行
`Theme 'X' is unavailable, fallback to default theme 'trime'`。所以「选了主题还是默认的样子」= 回退了。
判断方法：选完主题看【**配色**】列表是否变成该主题自己的配色（内置 trime 有 37 个，单静系只有几个）。

两个上游主题本身有问题，本仓库已修（用 Squirrel 自带 librime 1.16/1.17 + Trime 3.3.12 的解码规则实测）：

| 主题 | 问题 | 表现 | 修法 |
| --- | --- | --- | --- |
| 薄荷 mint | 源文件漏抄依赖：键盘里有 300+ 处 `__include: styl/...`、`__include: conf/sym`、`__patch: conf/bottom`，但它自己的 `styl` 只有 `key`/`off_key`/`off_func`，`conf` 也没有 `sym`/`bottom`（它其实是照 `danjing.yaml` 抄的键盘，却没把依赖抄全）| librime 报 `unresolved dependency: Include(mint.trime:styl/off_sym)` → `error building config: mint.trime` → **不产出** `build/mint.trime.yaml` → 回退 | 本仓库的 `mint.trime.yaml` 已在 `styl:` / `conf:` 末尾用 `# >>> 补入…块` 标出补入的节点（数据取自 `danjing.yaml`，`单静.trime:/conf/*` 已展开为字面量）。**上游原版不要直接覆盖本文件**；要跟上游更新就手工合并，或按此说明把缺的节点从 `danjing.yaml` 搬过来 |
| 单静·樱桃 | `preset_color_schemes/default` 里带一个 `colors:` **列表**（作者用 YAML 锚点在那里定义颜色）| 主题能编译，但 `Theme.decode` 对配色里每个值都做 `v.string!!`（`data/theme/Theme.kt:79`，3.3.12 与 develop 一致）→ 列表不是标量 → 抛异常 → 回退 | 主题补丁里加了一行 `"preset_color_schemes/default/colors": ""`（锚点在 YAML 解析阶段早已展开成字面值，置空不影响颜色）|

**两条通用规则（本次实测结论，踩着坑记下来）**：

1. **`.custom.yaml` 补丁无法满足主题源码里的 `__include`**：补丁是在 include 解析**之后**才合并进树的。
   实测 `styl/+`（值是字面量、带 `__include` 都试过）、把 `preset_keyboards` 整块换成
   `__include: danjing:/preset_keyboards` —— 全都仍然报同一个 unresolved 错误。所以这类问题**只能改主题源文件**
   （mint 就是这么修的）；反过来，补丁能做的是「覆盖数据」（键盘、预设键、配色链接）和「删掉坏值」（cherry 那行）。
2. **单静系主题的硬依赖（`danjing.yaml`，变体还要 `单静.patch.无障碍.yaml`）必须在 librime 编译时用的那个目录里**：
   Trime ≥3.3.12 的「从外部存储同步」模式下，运行时目录是 app 私有目录
   `Android/data/com.osfans.trime/files/rime`；而**在设置里点主题时，Trime 只会把 `<主题>.trime.yaml` 这一个文件**
   从外部目录拷进内部目录（`RimeDataSync.importThemeToLocal` 里只找 `"$configId.yaml"`）。
   所以：改完主题文件必须先【部署】（整树导入 + 编译）再选主题，否则 4 个单静系主题会**一起**编译失败 → 看起来「全都失效」。
   实测：内部目录里挑掉 `danjing.yaml`，`单静.trime` 必定 `error building config` 且没有产物。

### 与 17/18/24 键键盘的兼容性

* **不冲突**：两套主题只定义自己的 `preset_keyboards`（`default`/`letter`/`number`/`qwerty_`/`qwertys` 等），没有和我们的 `double_pinyin_flypy` / `flypy_18` / `flypy_24` / `flypy_en` 重名。
* 唯一缺的是预设键 `Return1`（我们键盘的 `composing: Return1` 用到）——已在生成的主题补丁里补上。
* ⚠️ **关键规则**：`trime.custom.yaml` 只作用于**内置主题 `trime`**。Trime 的补丁规则是「主题资源 ID + `.custom.yaml`」，所以在设置里换成 mint / 单静后，**必须用同名补丁文件**，否则 17/18/24 键键盘与中英切换键会消失（主题会按自己的 `qwerty_` 显示）。本目录已生成好 6 个（内容 = 三套键盘 + 切换键 + `Return1`；style 微调已注释，保留主题自己的 style）：

```text
mint.trime.custom.yaml              单静.trime.custom.yaml
单静+.trime.custom.yaml             单静.cherry.trime.custom.yaml
单纯.trime.custom.yaml              单纯+.trime.custom.yaml
```

### 操作步骤

1. 把表格里的主题文件/目录 + **你选中主题的那一个 `<主题>.trime.custom.yaml`** 放到 Trime 用户目录根部（本目录根目录已就绪，整体拷过去即可）；
2. 【部署】；
3. 设置 → 主题 → 选择 `mint` 或 `单静`（列表名来自主题的 `name` 字段）；
4. 设置 → 主题 → **配色** 里挑配色；打开「**跟随系统夜间模式**」即可日夜自动切换（详见下一小节）；
5. 键盘上的 `17 / 18 / 24 / 英` 切换键照旧可用。

### 明暗自动切换（已显式配好 Google 配色，但需在设置里开一次开关）

**Trime 为什么没有「分别选浅色/深色主题」的地方**：它的 UI 只有一个【主题】选择器 + 一个【配色】选择器，
自动明暗靠的是**当前选中配色里的两个链接键**：

```yaml
preset_color_schemes/<当前配色>/light_scheme: <日间用哪个配色>
preset_color_schemes/<当前配色>/dark_scheme:  <夜间用哪个配色>
```

解析逻辑（v3.3.12 `ColorManager.evaluateActiveColorScheme`，develop 重构为 `ColorSchemeResolver`，行为一致）：

* 两个链接都写 → 按当前夜/昼二选一（当它是“切换器”）；
* 只写 `light_scheme` → 当前配色当**深色**方案：夜间用它自己，日间切到 `light_scheme`；
* 只写 `dark_scheme` → 当前配色当**亮色**方案：日间用它自己，夜间切到 `dark_scheme`；
* 两个都没写 → 回退到 `default` 配色的链接；再都没有 → 用 `default`。

所以我在 6 个主题补丁末尾**显式写死了配对**（不依赖主题作者的写法，也不怕变体覆盖）：

| 主题 | 日间 | 夜间 | 备注 |
| --- | --- | --- | --- |
| 单静 / 单静+ / 单纯 / 单纯+ | **谷歌白** `google_white` | **谷歌黑** `google_black` | 一并给 `default` 也写上这对 → 保持默认的「默认」配色也能自动切换 |
| 单静·樱桃 | **谷歌白** `google_white` | `default`（樱桃本身，深色） | 保留樱桃的夜间观感 |
| 薄荷 mint | `default`（蓝水鸭） | `mint_dark_blue`（黑水鸭） | mint **没有** google 配色，只能用自带 pair |

**你要做的**：

1. 【部署】后，设置 → 主题 → **跟随系统夜间模式** = 开（默认关闭；这是 App 偏好，配置文件里写不了）；
2. 设置 → 高级 → **用户界面模式** = **自动**（否则界面部分不会跟随系统）；
3. 配色**不用改**：保持默认的 `默认` 就是「日间谷歌白 / 夜间谷歌黑」（单静系）；也可以在【配色】里直接选「**谷歌白**」或「**谷歌黑**」，两者都会自动切换到另一端。

想换成其它配对：改 `tools/gen-theme-patches.py` 顶部 `THEMES` 表里的 `light` / `dark` 两个值，重新生成并部署即可
（或直接改生成出来的 `<主题>.trime.custom.yaml` 末尾那几行）。

> 注：mac 鼠标管上的 `style/color_scheme` / `color_scheme_dark`（你的 `squirrel.custom.yaml` 用的机制）在 Trime 不适用。

### 注意事项 / 更新

* **主题源码仓库已不随仓库保留**（原来在 `themes/` 下，约 22MB，含 PSD/Demo；部署不需要它）。
  根目录里是真正要部署的东西：主题 `*.trime.yaml` + `danjing.yaml` + `单静.patch.无障碍.yaml` + `backgrounds/` + 6 个主题补丁。
  以后要更新主题（或重新拿源码/示例图）：

  ```bash
  git clone --depth 1 https://github.com/Mintimate/RimeTheme themes/RimeTheme
  git clone --depth 1 https://github.com/nopdan/danjing  themes/danjing
  # 再把有用的文件拷回根目录（★ 注意把新版的 *.trime.yaml / backgrounds/ 覆盖过来）：
  #   RimeTheme/ThemeForTrime/backgrounds/mint_*（mint.trime.yaml 见下！）
  #   danjing/{单静,单静+,单静.cherry,单纯,单纯+}.trime.yaml、danjing.yaml、单静.patch.无障碍.yaml、backgrounds/danjing.*
  # ★ mint.trime.yaml 例外：上游那版缺 styl/conf 依赖（编译必失败），
  #   要把它上游的改动手工合并进本仓库这份，别直接覆盖。
  # 拷完重新生成主题补丁：
  python3 tools/gen-theme-patches.py
  ```

  > ⚠️ 单静系（含樱桃）的主题文件、`danjing.yaml`、`backgrounds/` 可以直接用上游新版覆盖；
  > **只有 `mint.trime.yaml` 不能**（上游缺依赖 → 编译失败 → 静默回退，见上面的表）。

  产出的主题补丁已自检：YAML 可解析、每个键盘每行宽度和为 100。
* 根目录的 `backgrounds/` 是两套主题合并的（mint 用 `mint_*`，单静用 `danjing.*`，互不干扰，共约 292KB）。
* 主题只影响外观（配色 / 键盘底色 / 候选栏），不改方案拼写与词库，也不影响万象更新器的防覆盖名单。
* 若主题的键盘高度让你的 5 行 17 键显得太挤：把对应 `<主题>.trime.custom.yaml` 里已注释掉的 `"style/keyboard_height"` / `"style/key_long_text_size"` / `"style/symbol_text_size"` 放开即可。
* 主题补丁是从 `trime.custom.yaml` 生成的（附带 `Return1`、注释掉 style 行、显式明暗配对）。改了 `trime.custom.yaml` 的键盘或想换明暗配对后，跑一下就同步（在仓库根目录）：
  ```bash
  python3 tools/gen-theme-patches.py
  ```
  脚本会重新写出 6 个 `<主题>.trime.custom.yaml` 并自检（YAML 可解析、每个键盘每行宽度和为 100）。

## 九、已知限制 / 注意事项

1. **17/18/24 键只适用于小鹤双拼**（共键映射是小鹤键位）。全拼方案（`rime_mint`）请用 26 键。
2. **小鹤音形/辅助码**：形码码位会用到被合并的字母，共键后可能产生歧义；需要形码时建议用 26 键，
   或删掉 `speller/algebra/+` 那段 derive 规则。
3. **九宫格 `t9.schema.yaml` 在 Trime 上不可用**：它依赖 `t9_processor`（仓输入法/元书输入法的组件），
   Trime 没有；所以本配置的 `default.custom.yaml` 里没有启用 `t9`。
4. **Trime 版本差异**：`reset_ascii_mode` / `ascii_mode` 行为在 3.2.x~3.3.1x 之间修过多次
   （见 osfans/trime issue #1092 与 CHANGELOG）。如果「英 / 中」切换后中英状态不对，
   可改用内置 `Mode_switch` 键（把键盘第 5 行的 `Keyboard_flypy_en` 换成 `Mode_switch`）。
5. `style/keyboards` 列表在 Trime 3.3.x 已不再解析，所以本配置用「显式 select 的切换键」而不是
   `.next` 轮换（`.next` 会在含注音/仓颉等内置键盘的全量列表里乱跳）。
6. 未在真机上验证的部分：`installation.yaml` 的字段补全、`ascii_keyboard` 在各 Trime 版本的表现、
   共键键盘在你的具体机型上的手感 —— 部署后请按下面清单验证。

## 十、部署后验证清单

> **本地实测基准**（我在 mac 上用 Squirrel 自带的 librime 1.16 + 本目录的 algebra 规则搭了个最小方案跑出来的，可作对照）：
>
> | 键盘操作 | 双拼码 | 预期候选 |
> | --- | --- | --- |
> | 17 键：`BN` + `I` | bi | **你** 比（「你」靠 `derive/n/b/` 得到，且权重大排第一）|
> | 18 / 24 键：`N` + `I` | ni | 你 |
> | 17 键：`L` + `QW` | lq | 累 刘 |
> | 24 键：`L` + `W` | lw | 累（精确，不混入 iu 类）|
> | 17 键：`BN` `I` `H` `C` | ni hc | 你好 你 |

1. 候选栏出现候选，输入 `nihao`（小鹤：`ni` = `ni`，`hao` = `hc` → 打 `nihc`）能得到「你好」。
2. 按 `17 / 18 / 24` 键能切换布局，键盘外观随之变化（17 键应看到 QW ER TY…）。
3. 17 键下按 `L` + `QW`键 → 出现「刘 / 累」等候选（说明 derive 生效）。
4. 24 键下按 `W` 只出现 ei 类候选（`R/Y/S/F/X/N` 同理各自唯一）；
   按 `OP` 键（发 o）会同时出现 uo/o 与 ie 两类候选，按 `JK` 键（发 j）会同时出现 an 与 ing/uai 两类 —— 这是共键的预期行为。
5. 按 `英` 进入英文 26 键，能正常输入英文；按 `中` 回到小鹤 17 键且为中文状态。
6. 在密码框等强制英文的输入框里，键盘自动变成 26 键英文键盘。
7. 【同步用户数据】后，检查 `sync/android/` 下是否生成 `*.userdb.txt`。
8. 简繁切换（`简` 键）能生效。
9. 设置 → 主题：选完主题后看【**配色**】列表是否变成该主题自己的配色（内置 trime 37 个；单静系
   默认/谷歌白/谷歌黑/…）。若配色列表没变，就是主题编译/解码失败被静默回退到内置主题了（见下）。

### 如果「选了主题但外观没变化」（= 主题被静默回退）

Trime 不会报错，只会回退到内置 `trime` 主题（原因与两个必修项见第八节）。按顺序查：

1. **选完主题看【配色】列表**：没变成该主题的配色 → 确实在回退。
2. **确认内部目录里依赖齐全**（librime 编译用的就是这里，不是外部目录）：

   ```bash
   adb shell run-as com.osfans.trime ls -la /storage/emulated/0/Android/data/com.osfans.trime/files/rime/
   # 应有：单静.trime.yaml、danjing.yaml、单静.trime.custom.yaml、mint.trime.yaml（已修版）、backgrounds/
   adb shell run-as com.osfans.trime ls -la /storage/emulated/0/Android/data/com.osfans.trime/files/rime/build/ | grep trime
   # 每个主题应有一个 <主题>.yaml（没有 = 编译失败）
   ```

3. **抓一行日志**（最直接）：

   ```bash
   adb logcat -c        # 清空
   # 然后在手机上点一次主题
   adb logcat -d | grep -iE "fallback|error building config|unresolved dependency"
   ```

   看到 `Theme 'X' is unavailable, fallback to default theme 'trime'` 就是回退了；紧跟的 `E` 行会直接写明
   缺哪个引用/哪条配色。把这几行贴出来就能定位。
4. **最容易被路过的坑**：改完主题文件没重新【部署】，或者只把主题文件放进了外部目录还没导入 —— 见第八节规则 2。
5. mint 主题：本仓库这份 `mint.trime.yaml` 已补过依赖，**别用上游原版覆盖**（上游那版一定编译失败）。

### 如果「小鹤双拼没候选，但全拼正常」（本 repo 曾出现过，已修复）

这是 **`__include` 与 `speller/algebra/+` 同处一个补丁** 导致的方案被编译坏，与键盘/共键规则无关：

1. 确认你用的是**最新**的 `double_pinyin_flypy.custom.yaml`：里面**不应再有** `__include: wanxiang:/settings`，
   而是把 `grammar` / `contextual_suggestions` / `max_homophones` / `max_homographs` 直接写在该文件里（原因见第四节）。
2. 覆盖后重新【部署】。若依旧无候选，删掉内部目录里的 `build/double_pinyin_flypy.*` 再部署（清掉旧 prism）。
3. 用这几个输入验证（本机实测值，见第十节开头的对照表）：`ni→你`、`bi→你 比`、`lq→累 刘`、`lw→累`、`nihc→你好`。
4. 如果还是不行，把 Trime 的部署/运行日志发我。

### 如果「所有输入都没候选」（连全拼也没有）
这说明**不是键盘/共键规则的问题**（即使去掉 derive，`ni` 也必须能出「你」）——而是**词典或部署**环节出问题：

1. **先测全拼**：切到「薄荷拼音-全拼」，打 `ni`。
   * 也没候选 → 词库未到位或部署失败（继续往下查）；
   * 有候选 → 只有小鹤双拼方案有问题，请把 Trime 的部署/运行日志给我看。
2. **检查文件是否真的到位**（Trime 用户目录根部）：`double_pinyin_flypy.schema.yaml`、`rime_mint.dict.yaml`、
   **`dicts/rime_mint.chars/base/correlation/compatible/places/ext.dict.yaml` 这六个词库**、`lua/`。
   漏了 `dicts/` → 词典为空 → 所有方案都没有候选（症状与你描述的完全一致）。
3. **重新部署并等它跑完**：首次要编译万象大词库，可能要几分钟（万象官方也强调这一点）；中途反复点会留下不完整的 `build/`。
   必要时先删掉内部目录里的 `build/` 再部署（`build/` 不参与同步/导入，属内部缓存）。
4. **看 Trime 的部署结果**：重新部署后会有成功/失败提示，失败可点开看日志。
5. 若用「从外部存储同步」模式：确认 `dicts/` 在**你授权的外部目录**里（否则导入时带不过去）；
   `.userdb` 目录与 `build/` 不会被导入（源码行为，属正常）。

## 十一、参考来源

* 键盘布局：[forfudan/rime-clover-flypy](https://github.com/forfudan/rime-clover-flypy)（四叶草小鹤双拼 14/17 键，`theme/cosmic17key`）
* Trime 主题/键盘机制：[Trime wiki · trime.yaml 详解](https://github.com/osfans/trime/wiki/trime.yaml-%E8%A9%B3%E8%A7%A3)、
  [KeyboardWindow.kt](https://github.com/osfans/trime/blob/develop/app/src/main/java/com/osfans/trime/ime/keyboard/KeyboardWindow.kt)、
  [ThemeLoader.kt](https://github.com/osfans/trime/blob/develop/app/src/main/java/com/osfans/trime/data/theme/ThemeLoader.kt)
* 共键（双键）键盘案例：[五笔双键配置案例（四）](https://github.com/osfans/trime/wiki/%E4%BA%94%E7%AC%94%E5%8F%8C%E9%94%AE%E9%85%8D%E7%BD%AE%E6%A1%88%E4%BE%8B%E8%AF%A6%E8%A7%A3(%E5%9B%9B)-%E5%AE%9E%E7%8E%B0%E6%89%8B%E6%9C%BA%E4%B8%8A%E7%9A%84%E5%8F%8C%E9%94%AE%E9%94%AE%E7%9B%98)、
  [nextzhou/trime-dual-17keys](https://github.com/nextzhou/trime-dual-17keys)、
  [HXLH50K/trime-sharedkey-shuangpin](https://github.com/HXLH50K/trime-sharedkey-shuangpin)
* 薄荷配置覆写：<https://www.mintimate.cc/zh/guide/configurationOverride.html>
* 设备同步：<https://www.mintimate.cc/zh/guide/deviceSync.html>
* 万象词库/模型：<https://github.com/amzxyz/RIME-LMDG>、<https://amzxyz.github.io/rime-wanxiang/doc/trime/>

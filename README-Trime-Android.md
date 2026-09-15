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
| `wanxiang.yaml` | 万象模型的 `grammar` / `translator` 调参片段，被上面两个 custom 用 `__include: wanxiang:/settings` 引用 |
| `trime.custom.yaml` | **Trime 前端主题补丁**：17 / 18 / 24 键中文键盘 + 英文 26 键键盘 + 键盘切换按键 + 界面微调 |
| `installation.yaml` | 安装信息：`installation_id: android`，`sync_dir: "sync"`（= Trime 用户目录/sync） |
| `README-Trime-Android.md` | 本说明文件 |

> 这些文件是 **补丁（.custom.yaml）+ 说明**，不是完整配置。使用时请把它们和
> oh-my-rime 仓库的其它文件一起放到 **Trime 用户目录的根目录**（不要多套一层文件夹）。

## 二、部署步骤

1. 准备 oh-my-rime（薄荷）仓库的所有文件 + 本目录的文件，合并到一个文件夹里（本目录的文件直接覆盖同名文件）。
2. 找到 Trime 的**用户文件夹**（取决于 Trime 版本）：
   * Trime **≤ 3.3.11**：`/storage/emulated/0/rime/`
   * Trime **≥ 3.3.12**：`/storage/emulated/0/Android/data/com.osfans.trime/files/rime/`
     （若在「设置 → 数据存储模式」里选了**从外部存储同步**，则把你授权的外部目录当作数据源，Trime 会在部署/同步时导入）
3. 把第 1 步合并好的文件复制进该目录（`installation.yaml`、万字词库、`lua/`、`dicts/` 等全部放在根目录）。
4. Trime 里点【部署】。首次部署要编译万象大词库，可能需要几分钟，请耐心等待。
5. 部署完成后建议按下面的「验证清单」逐项测试。

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

## 五、万象模型

* 词库：oh-my-rime 自带的 `dicts/rime_mint.*.dict.yaml`（2025-07-09 起为万象词库），无需额外下载。
* 参数：`wanxiang.yaml` 里的 `grammar`（`collocation_max_length` 等）与
  `translator/contextual_suggestions`、`max_homophones`、`max_homographs`，
  由两个方案的 custom 通过 `__include: wanxiang:/settings` 引入。
* **语法模型 `.gram`（约 400MB）未包含**：Trime 找不到该文件时会提示加载失败并按「无语言模型」
  继续工作，不影响输入。想启用的话，把 `wanxiang-lts-zh-hans.gram` 放到 Trime 用户目录根部，
  然后重新部署（占内存/存储较大，建议旗舰机或平板再考虑）。
* 注意：`menu/page_size`（候选个数）必须写在**方案**的 `.custom.yaml` 里（薄荷把 `menu` 冗余写进了每个方案），
  写在 `default.custom.yaml` 里对薄荷方案无效。

## 六、同步目录

`installation.yaml` 已配置好：

```yaml
installation_id: android
sync_dir: "sync"
```

* `sync_dir: "sync"` 是**相对路径**，即 **Trime 用户目录/sync**；同步后会在其中生成 `sync/android/*.userdb.txt`。
* 用 Trime 的【同步用户数据】或【后台定时同步】执行同步。
* **想让 mac 和 Android 共用词库**：把 `sync_dir` 改成两端都能访问的同一个目录（Android 端建议用
  「数据存储模式 → 从外部存储同步」选一个 Syncthing/网盘的目录，mac 端已是 `/Users/lystran/data/rime`），
  两端 `installation_id` 必须不同（mac 是 `mac`，Android 是 `android`）。
* 只同步 `sync` 目录，**不要**用网盘直接同步整个用户目录（正在使用的 userdb 会坏）。

## 七、已知限制 / 注意事项

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

## 八、部署后验证清单

1. 候选栏出现候选，输入 `nihao`（小鹤：`ni` = `ni`，`hao` = `hc` → 打 `nihc`）能得到「你好」。
2. 按 `17 / 18 / 24` 键能切换布局，键盘外观随之变化（17 键应看到 QW ER TY…）。
3. 17 键下按 `L` + `QW`键 → 出现「刘 / 累」等候选（说明 derive 生效）。
4. 24 键下按 `W` 只出现 ei 类候选（`R/Y/S/F/X/N` 同理各自唯一）；
   按 `OP` 键（发 o）会同时出现 uo/o 与 ie 两类候选，按 `JK` 键（发 j）会同时出现 an 与 ing/uai 两类 —— 这是共键的预期行为。
5. 按 `英` 进入英文 26 键，能正常输入英文；按 `中` 回到小鹤 17 键且为中文状态。
6. 在密码框等强制英文的输入框里，键盘自动变成 26 键英文键盘。
7. 【同步用户数据】后，检查 `sync/android/` 下是否生成 `*.userdb.txt`。
8. 简繁切换（`简` 键）能生效。

## 九、参考来源

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

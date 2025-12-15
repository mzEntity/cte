# cte
*console-based text editor*

**windows platform only**

## usage

```shell
python main.py <file_path>
```

eg.
```shell
python main.py README.md
```


## MyVim 使用帮助

MyVim 是一个简化版的 Vim 编辑器，支持三种模式：插入模式（Insert）、普通模式（Normal） 和 命令模式（Command）。

### 模式说明

#### 普通模式（Normal Mode）

启动后默认进入此模式。在此模式下可使用快捷键执行编辑或切换模式。
按 `i/a/o` 进入 插入模式
按 `:` 进入 命令模式

#### 插入模式（Insert Mode）

可直接输入文本。按 `Esc` 键返回 普通模式。

使用上下左右箭头进行移动

#### 命令模式（Command Mode）

在普通模式下按 `:` 后进入。输入以下命令并回车执行：

| 命令 | 功能说明 |
| ---- | -------- |
|!w|保存当前文件|
|!q|退出（不保存）|
|!wq|保存并退出|

⚠️ 注意：所有命令必须以 ! 开头（例如 :!w），这是 MyVim 的设计约定。

示例流程

1. 启动 MyVim → 进入 普通模式
2. 按 i → 进入 插入模式，开始输入文字
3. 按 Esc → 返回 普通模式
4. 按 : → 输入 !wq → 回车 → 保存并退出

**支持使用上下箭头进行历史命令提取**


## MyVim User Guide

MyVim is a simplified Vim-like text editor that supports three modes: Insert Mode, Normal Mode, and Command Mode.
### Mode Description

#### Normal Mode

This is the default mode when MyVim starts. In this mode, you can use keyboard shortcuts to perform editing actions or switch to other modes.
Press `i`, `a`, or `o` to enter Insert Mode
Press `:` to enter Command Mode

#### Insert Mode

You can type text directly in this mode. Press the `Esc` key to return to Normal Mode.
Use the arrow keys (↑ ↓ ← →) to move the cursor.

#### Command Mode

Enter this mode by pressing `:` in Normal Mode. Type one of the following commands and press `Enter` to execute:

|Command| Action|
| ---- | -------- |
|!w|Save the current file|
|!q|Quit without saving|
|!wq|Save and quit|

⚠️ Note: All commands must start with ! (e.g., :!w). This is a design convention in MyVim.
Example Workflow

1. Launch MyVim → enters Normal Mode
2. Press i → enters Insert Mode, start typing text
3. Press Esc → returns to Normal Mode
4. Press : → type !wq → press Enter → save and exit

**Supports using the Up/Down arrow keys to navigate through command history.**





author: mzvltr
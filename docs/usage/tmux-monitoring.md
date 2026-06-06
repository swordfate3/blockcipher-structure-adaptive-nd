# tmux 监控使用教程

本文只覆盖本项目最常用的场景：远程 GPU 实验已经启动，本地用监控脚本每隔一段时间检查 GitHub 结果分支，并在结果门禁通过后自动拉回 `outputs/remote_results/`。

## 1. tmux 是什么

`tmux` 是终端会话管理器。可以把它理解成“后台终端窗口”：

- 你进入 tmux 会话时，可以看到里面程序的输出。
- 你离开 tmux 会话后，里面的程序仍然继续运行。
- 当前终端关闭后，tmux 会话通常仍然保留。

本项目用它来跑本地监控脚本，避免监控脚本占住当前终端，也避免会话断开后监控停止。

## 2. 当前创新一 MoE v5 监控

当前 MoE v5 PRESENT 远程实验的本地监控会话名是：

```bash
innovation1_moe_v5_monitor
```

监控脚本是：

```bash
./scripts/monitor_innovation1_moe_v5_present_results.sh
```

它每 30 分钟检查一次结果分支：

```text
results/innovation1-moe-v5-present-gpu1-20260606
```

当远程结果分支出现并且门禁满足：

```text
result_lines=10
expected_rows=10
```

它会自动把结果拉回：

```text
outputs/remote_results/innovation1-moe-v5-present-gpu1-20260606/
```

监控日志在：

```text
outputs/remote_results/monitor_logs/innovation1_moe_v5_present_monitor.log
```

## 3. 查看有哪些 tmux 会话

```bash
tmux list-sessions
```

如果监控正在运行，应该能看到类似：

```text
innovation1_moe_v5_monitor: 1 windows
```

## 4. 进入监控窗口

```bash
tmux attach -t innovation1_moe_v5_monitor
```

进入后可以看到监控输出。等待远程结果时常见输出：

```text
WAIT missing result branches: results/innovation1-moe-v5-present-gpu1-20260606
sleeping 1800s before next check
```

这不是报错，表示远程还没有推送结果分支，监控正在等待下一轮检查。

## 5. 离开窗口但不停止监控

进入 tmux 后，不要直接按 `Ctrl+C`，否则会中断里面的监控脚本。

正确离开方式：

```text
Ctrl+B
D
```

也就是先按住 `Ctrl` 再按 `B`，松开后再按 `D`。这个操作叫 detach，意思是“离开这个窗口，但让里面程序继续跑”。

## 6. 看监控日志

不进入 tmux，也可以直接看日志：

```bash
tail -f outputs/remote_results/monitor_logs/innovation1_moe_v5_present_monitor.log
```

如果只想看最后几十行：

```bash
tail -80 outputs/remote_results/monitor_logs/innovation1_moe_v5_present_monitor.log
```

## 7. 手动启动一个监控会话

以当前 MoE v5 监控为例：

```bash
tmux new-session -d -s innovation1_moe_v5_monitor \
  'cd /home/fate/gitproject/blockcipher-structure-adaptive-nd && PYTHONUNBUFFERED=1 ./scripts/monitor_innovation1_moe_v5_present_results.sh 2>&1 | tee -a outputs/remote_results/monitor_logs/innovation1_moe_v5_present_monitor.log'
```

说明：

- `new-session -d`：后台创建会话。
- `-s innovation1_moe_v5_monitor`：指定会话名。
- `PYTHONUNBUFFERED=1`：让 Python 监控输出实时刷新到日志。
- `tee -a ...log`：屏幕显示一份，同时追加写入日志。

## 8. 停止监控

只有确认不需要继续等结果时，再停止监控：

```bash
tmux kill-session -t innovation1_moe_v5_monitor
```

停止后，监控不会再自动检查远程结果分支，也不会自动拉回结果。

## 9. 重启监控

如果监控会话已停止，可以重新启动：

```bash
tmux new-session -d -s innovation1_moe_v5_monitor \
  'cd /home/fate/gitproject/blockcipher-structure-adaptive-nd && PYTHONUNBUFFERED=1 ./scripts/monitor_innovation1_moe_v5_present_results.sh 2>&1 | tee -a outputs/remote_results/monitor_logs/innovation1_moe_v5_present_monitor.log'
```

然后确认：

```bash
tmux list-sessions
tmux attach -t innovation1_moe_v5_monitor
```

## 10. 一次性检查，不启动长期监控

如果只想检查当前结果分支是否已经出现，不想进入 30 分钟循环：

```bash
uv run python scripts/monitor_remote_results.py \
  --once \
  --run-id innovation1-moe-v5-present-gpu1-20260606=10
```

可能结果：

```text
WAIT missing result branches: results/innovation1-moe-v5-present-gpu1-20260606
```

表示还没完成。

如果完成并通过门禁，会输出：

```text
RETRIEVED innovation1-moe-v5-present-gpu1-20260606 -> outputs/remote_results/innovation1-moe-v5-present-gpu1-20260606
DONE all remote results retrieved
```

## 11. 常见问题

### 进入 tmux 后如何退出？

按：

```text
Ctrl+B
D
```

不要按 `Ctrl+C`，除非你就是要停止监控。

### `WAIT missing result branches` 是失败吗？

不是。它表示远程实验还没推送结果分支。只要远程训练还在跑，就继续等。

### 监控完成后结果在哪里？

在：

```text
outputs/remote_results/<run-id>/
```

例如：

```text
outputs/remote_results/innovation1-moe-v5-present-gpu1-20260606/
```

### 怎么确认监控会话还活着？

```bash
tmux list-sessions
```

或者：

```bash
tmux capture-pane -pt innovation1_moe_v5_monitor -S -40
```

### 怎么确认远程实验本身还在跑？

远程实验状态不由 tmux 直接管理。tmux 只管本地结果监控。远程训练需要通过 SSH 检查 Task Scheduler、`nvidia-smi`、远程 logs 或 GitHub 结果分支。

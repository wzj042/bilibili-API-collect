---
name: bilibili-cli
description: 读取 B 站视频章节、进度条分段或复现 data.view_points 接口时使用此示例。
---

# Bilibili 章节 CLI

通过公开 HTTP 或 Kimi Browser Extension 的真实浏览器读取已发布章节，不提供修改章节功能。

## 要求

- Python 3.9+，无需第三方依赖。
- CLI 位于本技能目录向上两级的 `chapters.py`。当前检出绝对路径为 `C:/Users/XQH/Downloads/GPT/bilibili-API-collect/examples/video-chapters/chapters.py`；迁移后按实际仓库根目录解析。
- 使用 `--transport kimi` 时需要 kimi-webbridge skill 和已连接的浏览器扩展。daemon 不可达或扩展未连接时，按该 skill 的步骤恢复；可传 `--daemon-url` 指定地址。
- 本样本无需登录；`--credentials include` 仅供浏览器内使用既有登录态，不导出 Cookie。

## 用法

在仓库根目录执行：

```shell
python examples/video-chapters/chapters.py --help
python examples/video-chapters/chapters.py BV1vL411G7N7
python examples/video-chapters/chapters.py BV1vL411G7N7 --transport kimi --output chapters.json
python examples/video-chapters/chapters.py BV1vL411G7N7 --page 1
```

成功输出 `{"ok":true,"data":{...}}`，包含 aid/bvid/cid、分 P、时长和 view_points。失败输出 `{"ok":false,"error":{"code":"...","message":"..."}}`，退出码非零。

固定会话 `bilibili`，复用同域标签；页面保留供检查，不自动关闭。空章节只代表本次响应未提供章节，不能把字段缺失或接口错误视为空章节。遇到风控不自动重试、不回退旧接口。若用户需要安装本技能，再按其指定的智能体技能目录安装；仅保存于仓库不代表已全局安装。

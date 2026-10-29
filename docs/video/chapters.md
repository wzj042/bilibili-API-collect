# 视频章节（进度条分段）

## 获取章节

> https://api.bilibili.com/x/player/wbi/v2

*请求方式：GET*

章节来自 [web 播放器信息](player.md) 的 `data.view_points`，不是分 P 列表、字幕，也不是 [AI 摘要](summary.md) 的 `outline`。先通过 [视频基本信息](info.md) `/x/web-interface/view?bvid=...` 的 `data.pages` 选择分 P，再携带该分 P 的 `cid` 请求播放器信息。不能将第一 P 的章节用于其他 P。

**URL 参数：**

| 参数 | 类型 | 必要性 | 说明 |
| --- | --- | --- | --- |
| aid | num | 与 bvid 二选一 | 稿件 avid |
| bvid | str | 与 aid 二选一 | 稿件 BV 号 |
| cid | num | 必要 | 当前分 P 的 cid |

2026-10-29（Asia/Hong_Kong）通过 Kimi Browser Extension 在真实网页抓包并复现。网页主请求带有 `w_rid`、`wts` 等参数；本样本仅传 `aid + cid` 或 `bvid + cid`、不带 Cookie 和 WBI 签名也成功。该结果是指定样本及当前网络环境的观察，不保证所有视频或未来接口都免签名、免登录。

**响应：**

先检查 HTTP 状态和根对象 `code === 0`，再核对 `data.aid/bvid/cid` 与所选视频、分 P 一致。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| data.view_points | array | 本次响应提供的章节列表；`[]` 表示本次没有提供章节 |
| content | str | 章节标题 |
| from | num | 起始时间，单位秒 |
| to | num | 结束时间，单位秒 |
| type | num | 本样本六项均为 `2`；其他取值含义本次未验证 |
| imgUrl | str | 章节预览图；原响应可能使用 HTTP URL |
| logoUrl | str | 本样本为空字符串 |
| team_type | str | 本样本为空字符串 |
| team_name | str | 本样本为空字符串 |

章节 `from/to` 是同一分 P 内的时间点。绘制分段进度条时可按 `from / duration` 定位、按 `(to - from) / duration` 计算宽度，点击章节跳转到 `from` 秒。客户端可采用 `[from, to)` 判断当前章节，在视频终点单独处理最后一段；这是客户端约定，不是接口声明的区间规则。不要假设任意视频章节必然连续、覆盖全部时长或具有相同 `type`。

字段缺失、类型错误、身份不符、业务失败不能当成空章节。本次只验证读取已发布章节，没有验证创作者添加、修改或提交章节的接口。

## 指定视频实测

视频：[如何为你的B站视频添加进度条分段](https://www.bilibili.com/video/BV1vL411G7N7/)。

| bvid | aid | cid | 分 P | 时长 |
| --- | --- | --- | --- | --- |
| BV1vL411G7N7 | 463665680 | 427178148 | 1 | 670 秒 |

| 起始秒 | 结束秒 | 时间范围 | 标题 |
| --- | --- | --- | --- |
| 0 | 117 | 00:00–01:57 | 开头 |
| 117 | 257 | 01:57–04:17 | 分段章节的效果 |
| 257 | 326 | 04:17–05:26 | 为什么要使用分段章节 |
| 326 | 458 | 05:26–07:38 | 使用分段章节的要求和限制 |
| 458 | 633 | 07:38–10:33 | 如何为你的视频添加分段章节 |
| 633 | 670 | 10:33–11:10 | 结尾 |

对照结果：

| 请求环境 | 参数与凭据 | 结果 |
| --- | --- | --- |
| 网页主请求 `/x/player/wbi/v2` | aid、cid、WBI 签名、网页附加参数、浏览器 Cookie | HTTP 200，code 0，6 段 |
| 浏览器 fetch `/x/player/wbi/v2` | aid、cid；credentials include；无签名 | 同上，章节数组逐项一致 |
| 浏览器 fetch `/x/player/wbi/v2` | aid、cid；credentials omit；无签名 | 同上，章节数组逐项一致 |
| 浏览器 fetch `/x/player/wbi/v2` | bvid、cid；credentials omit；无签名 | 同上，章节数组逐项一致 |
| 浏览器 fetch `/x/player/v2` | aid、cid；credentials omit；无签名 | 同上，章节数组逐项一致 |
| Python 独立 HTTP `/x/player/wbi/v2` | aid、cid；无 Cookie、无签名 | HTTP 200，code 0，6 段 |

旧接口只作对照；复现脚本使用新接口，不自动回退。旧接口的字幕可靠性问题见 [播放器文档](player.md)。

抓包方式：打开目标页 → `network start` → 在同一标签重载 → 筛选 `/x/player/wbi/v2` → `network detail` → 提取章节及请求参数名 → `network stop` → 浏览器内 `evaluate` 重放并比对。保存的 [实测数据](../../examples/video-chapters/BV1vL411G7N7.json) 仅包含视频身份、章节、参数名称和对照摘要，未保留 Cookie、用户信息、IP、设备指纹及签名值。

## 复现

无需第三方 Python 依赖，要求 Python 3.9 或更高版本。在仓库根目录运行：

```shell
python examples/video-chapters/chapters.py BV1vL411G7N7
python examples/video-chapters/chapters.py BV1vL411G7N7 --transport kimi
python examples/video-chapters/chapters.py BV1vL411G7N7 --page 1 --output chapters.json
```

`http`（默认）直接访问公开接口；`kimi` 通过本地 Kimi daemon 在浏览器中执行 fetch，固定会话名 `bilibili`，复用同域标签。默认 `credentials: omit`，可用 `--credentials include` 在浏览器内使用登录态，Cookie 不导出。daemon 地址可以通过 `--daemon-url` 修改。新建的标签保留供检查，需要时由用户要求关闭。

脚本只导出章节相关数据，验证分 P、响应身份和时间范围；出错返回 `ok: false` 且退出码非零，不会把失败伪装成空列表。严格的时间范围校验属于本示例的客户端策略。请求遭风控或登录限制时保留错误，不进行自动重试或旧接口回退。

也可以在已打开的 B 站网页开发者控制台运行以下最小复现：

```javascript
(async () => {
  const response = await fetch(
    'https://api.bilibili.com/x/player/wbi/v2?aid=463665680&cid=427178148',
    { credentials: 'omit' }
  );
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const body = await response.json();
  if (body.code !== 0) throw new Error(`API ${body.code}: ${body.message}`);
  const { aid, bvid, cid, view_points } = body.data;
  if (aid !== 463665680 || bvid !== 'BV1vL411G7N7' || cid !== 427178148)
    throw new Error('视频或分 P 身份不符');
  if (!Array.isArray(view_points)) throw new Error('缺少章节数组');
  console.table(view_points);
})();
```

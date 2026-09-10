# 播放器

## web 播放器信息

web 播放器的信息接口，提供正常播放需要的元数据，包括：智能防挡弹幕、字幕、章节看点等。

> https://api.bilibili.com/x/player/wbi/v2  
> https://api.bilibili.com/x/player/v2

*请求方式：GET*

读取字幕时优先使用 `/x/player/wbi/v2`。2026-09-10 实测，旧 `/x/player/v2` 对 `BV1mgwezhEXX` 返回正确的 aid/bvid/cid，却附带其他视频的字幕；新接口与网页播放器均返回空字幕列表。该观察针对字幕来源可靠性，不代表旧接口的其他用途均已失效。

部分字幕需要认证：Cookie (SESSDATA)。该日期的网页请求及独立请求均可直接使用 `aid`、`cid`，未附加 `wts`、`w_rid`。

**URL参数:**

| 参数名 | 类型 | 内容      | 必要性      | 备注              |
| ------ | ---- | --------- | ----------- | ----------------- |
| aid    | num  | 稿件 avid | 必要 (可选) | aid 与 bvid 任选 |
| bvid   | str  | 稿件 bvid | 必要 (可选) | aid 与 bvid 任选 |
| cid    | num  | 稿件 cid | 必要 | |
| season_id | num | 番剧 season_id | 不必要 | |
| ep_id | num | 剧集 ep_id | 不必要 | |
| w_rid | str  | WBI 签名 | 不必要 |  |
| wts   | num  | 当前 unix 时间戳 | 不必要 |  |

**JSON回复:**

根对象:

| 字段    | 类型 | 内容     | 备注                        |
| ------- | ---- | -------- | --------------------------- |
| code    | num  | 返回值   | 0: 成功<br />-400: 请求错误 |
| message | str  | 错误信息 | 默认为 0                     |
| ttl     | num  | 1        |                             |
| data    | obj  | 数据本体 |                             |

`data` 对象:

| 字段      | 类型  | 内容     | 备注 |
| --------- | ----- | -------- | ---- |
| aid        | num  | 视频 aid   |      |
| bvid       | str  | 视频 bvid  |      |
| allow_bp   | bool |  |  |
| no_share   | bool | 禁止分享? |  |
| cid        | num  | 视频 cid   |      |
| dm_mask    | obj  | webmask 防挡字幕信息 | 若无则没有防挡功能 |
| subtitle   | obj  | 字幕信息 | 空列表需结合 `data.need_login_subtitle` 判断，不一定表示视频无字幕 |
| view_points | array  | 分段章节信息 |  |
| ip_info    | obj  | 请求 IP 信息 |      |
| login_mid  | num  | 登录用户 mid |      |
| login_mid_hash | str |  |  |
| is_owner | bool | 是否为该视频 UP 主 |  |
| name       | str  |  |  |
| permission | num  |  |  |
| level_info | obj  | 登录用户等级信息 |  |
| vip        | obj  | 登录用户 VIP 信息 |  |
| answer_status | num | 答题状态 |  |
| block_time | num | 封禁时间? |  |
| role | str |  |  |
| last_play_time | num | 上次观看时间? |  |
| last_play_cid | num | 上次观看 cid? |  |
| now_time | num | 当前 UNIX 秒级时间戳 |  |
| online_count | num | 在线人数 |  |
| need_login_subtitle | bool | 是否需要登录才能读取字幕 | 位于 `data` 顶层；为 `true` 且字幕列表为空时，应先登录或更新登录态 |
| preview_toast | str | `为创作付费，购买观看完整视频\|购买观看` |  |
| interaction | obj | 互动视频资讯 | 若非互动视频，则无该栏位（直接没有该键，而非栏位值为空）|
| options | obj |  |  |
| guide_attention | any |  |  |
| jump_card | any |  |  |
| operation_card | any |  |  |
| online_switch | obj |  |  |
| fawkes | obj | 播放器相关信息? |  |
| show_switch | obj |  |  |
| bgm_info | obj | 背景音乐信息 |  |
| toast_block | bool |  |  |
| is_upower_exclusive | bool | 是否为充电专属视频 |  |
| is_upower_play | bool |  |  |
| is_ugc_pay_preview | bool |  |  |
| elec_high_level | obj | 充电专属视频信息 |  |
| disable_show_up_info | bool |  |  |

`data` 对象中的 `options` 对象:

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | --- | --- |
| is_360 | bool | 是否 360 全景视频 |  |
| without_vip | bool |  |  |

`data` 对象中的 `bgm_info` 对象:

| 字段 | 类型 | 内容 | 备注 |
| --- | --- | --- | --- |
| music_id | str | 音乐 id |  |
| music_title | str | 音乐标题 |  |
| jump_url | str | 跳转 URL |  |

`data` 对象中的 `dm_mask` 对象 (如果有):

| 字段      | 类型  | 内容     | 备注 |
| --------- | ----- | -------- | ---- |
|cid        | num  |  视频 cid   |      |
|plat       | num  | 未知   |      |
|fps       | num  | webmask 取样 fps   |      |
|time       | num  | 未知   |      |
|mask_url   | str  |  webmask 资源 url |  |

解析 webmask 请看 [智能防挡弹幕](../danmaku/webmask.md)

`data` 对象中的 `subtitle` 对象:

| 字段      | 类型  | 内容     | 备注 |
| --------- | ----- | -------- | ---- |
|allow_submit|bool | true   |      |
|  lan      |  str | ""          |      |
|lan_doc | str | ""    | |
|subtitles| array | 字幕轨列表 | 无可用轨道或缺少所需登录态时可能为 `[]` |

`subtitle` 对象中的 `subtitles` 数组内的元素:

| 字段      | 类型  | 内容     | 备注 |
| --------- | ----- | -------- | ---- |
| ai_status | num  |    |      |
| ai_type   | num  |    |   |
| id  | num | 字幕 ID | 可能超过 JavaScript Number 的安全整数范围 |
|id_str | str| 字幕 ID 的字符串表示 | 保留字符串用于完整保存、比对，避免浮点精度损失 |
| is_lock | bool | | |
| lan | str | 语言类型英文字母缩写 ||
| lan_doc | str| 语言类型中文名称 | |
|subtitle_url|str| 字幕正文 JSON 地址 | `//` 开头时补 `https:`；URL 可能带有时效性签名 |
|type| num | 0 | |

`subtitle_url` 返回的 JSON 根对象（仅列字幕正文相关字段）:

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| body | array | 字幕条目列表 | 合法列表可以为空；字段缺失或类型错误不应视为空字幕 |

`body` 数组中的对象:

| 字段 | 类型 | 内容 | 备注 |
| ---- | ---- | ---- | ---- |
| from | num | 开始时间，单位秒 | 非负有限数值 |
| to | num | 结束时间，单位秒 | 不小于 `from` |
| content | str | 字幕文字 | |

下载正文时先检查 HTTP 状态，再验证 JSON 和上述字段。建议核对 player 响应的 aid/bvid/cid，并对照对应分 P 的时长检查字幕时间上界。例如客户端可容许 5 秒末尾误差，超过 `pages[].duration + 5` 秒时拒绝该轨正文并报告错误；这是异常检测策略，并非接口协议规定。身份和时长一致不能证明字幕语义正确，不应在新接口无字幕时自动回退到旧接口。

当 `data.need_login_subtitle=true` 且 `data.subtitle.subtitles=[]` 时，无法据此断言视频没有字幕；登录后再确认。标志为 `false` 且列表为空，也只表示本次响应未提供可用字幕轨。

`data`对象中的`view_point` 数组内的元素:

| 字段      | 类型  | 内容     | 备注 |
| --------- | ----- | -------- | ---- |
| content | str  |  分段章节名  |      |
| from | num  |  分段章节起始秒数  |      |
| to | num  |  分段章节结束秒数  |      |
| type | num  |    |      |
| imgUrl | str  |  图片资源地址  |      |
| logoUrl | str  |  ""  |      |
| team_type | str  |    |      |
| team_name | str  |    |      |

`data` 对象中的 `interaction` 对象 (如果有):

| 字段      | 类型  | 内容     | 备注 |
| --------- | ----- | -------- | ---- |
| graph_version | num | 剧情图id |   |
| msg | str |  | 未登入有机会返回 `登录后才能体验全部结局哦～` |
| error_toast | str | 错误信息？ | 所有互动视频皆返回 `剧情图被修改已失效`，不确定有没有例外 |
| mark | num | 0? |   |
| need_reload | num | 0? |   |

`data`对象中的`elec_high_level`对象：

| 字段           | 类型 | 内容                           | 备注             |
| -------------- | ---- | ------------------------------ | ---------------- |
| privilege_type | num  | 解锁视频所需最低定价档位的代码 | 见[充电档位代码与定价](../electric/monthly.md#充电档位代码privilege_type与定价) |
| title          | str  | 提示标题                       | `该视频为「{充电档位名称}」专属视频` |
| sub_title      | str  | 提示子标题                     | `开通「{充电档位定价}元档包月充电」即可观看` |
| show_button    | bool | 是否显示按钮                   |                  |
| button_text    | str  | 按钮文本                       | `去开通`         |
| jump_url       | obj  | 跳转url信息                    | 详细信息有待补充 |
| intro          | str  | 充电介绍语                     |                  |
| open           | bool | （？）                         |                  |
| new            | bool | （？）                         |                  |
| question_text  | str  | （？）                         |                  |
| qa_detail_link | str  | （？）                         |                  |

**示例:**

已登录读取 `BV1aD4y127GE` 的 AI 中文字幕。2026-09-10 网页播放器与独立请求返回同一条 `ai-zh` 字幕轨，正文共 512 条，最大结束时间 1087.18 秒。

```shell
curl -G 'https://api.bilibili.com/x/player/wbi/v2' \
  --data-urlencode 'aid=711776837' \
  --data-urlencode 'cid=234622982' \
  -b 'SESSDATA=xxx'
```

<details>
<summary>查看字幕元信息响应（仅保留相关字段，资源 URL 已脱敏）:</summary>

```json
{
  "code": 0,
  "data": {
    "aid": 711776837,
    "bvid": "BV1aD4y127GE",
    "cid": 234622982,
    "need_login_subtitle": false,
    "subtitle": {
      "subtitles": [
        {
          "id_str": "1082184109511715840",
          "lan": "ai-zh",
          "subtitle_url": "//aisubtitle.hdslb.com/bfs/subtitle/xxx.json"
        }
      ]
    }
  }
}
```

</details>

该轨的精确 `id_str` 为 `1082184109511715840`；浏览器将数值 ID 显示为 `1082184109511715800` 是 JavaScript Number 精度损失，不应据此判断为字幕错配。

未登录, `aid=1906473802`

```shell
curl -G 'https://api.bilibili.com/x/player/wbi/v2' \
--url-query 'bvid=BV1MU411S7iJ' \
--url-query 'aid=1906473802' \
--url-query 'cid=1625992822'
```

<details>
<summary>查看响应示例:</summary>

```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "aid": 1906473802,
    "bvid": "BV1MU411S7iJ",
    "allow_bp": false,
    "no_share": false,
    "cid": 1625992822,
    "max_limit": 1000,
    "page_no": 1,
    "has_next": false,
    "ip_info": {
      "ip": "104.28.152.138",
      "zone_ip": " 10.163.150.25",
      "zone_id": 29409280,
      "country": "美国",
      "province": "加利福尼亚州",
      "city": "东洛杉矶"
    },
    "login_mid": 0,
    "login_mid_hash": "",
    "is_owner": false,
    "name": "",
    "permission": "0",
    "level_info": {
      "current_level": 0,
      "current_min": 0,
      "current_exp": 0,
      "next_exp": 0,
      "level_up": 0
    },
    "vip": {
      "type": 0,
      "status": 0,
      "due_date": 0,
      "vip_pay_type": 0,
      "theme_type": 0,
      "label": {
        "path": "",
        "text": "",
        "label_theme": "",
        "text_color": "",
        "bg_style": 0,
        "bg_color": "",
        "border_color": "",
        "use_img_label": false,
        "img_label_uri_hans": "",
        "img_label_uri_hant": "",
        "img_label_uri_hans_static": "",
        "img_label_uri_hant_static": ""
      },
      "avatar_subscript": 0,
      "nickname_color": "",
      "role": 0,
      "avatar_subscript_url": "",
      "tv_vip_status": 0,
      "tv_vip_pay_type": 0,
      "tv_due_date": 0,
      "avatar_icon": {
        "icon_resource": {}
      }
    },
    "answer_status": 0,
    "block_time": 0,
    "role": "",
    "last_play_time": 0,
    "last_play_cid": 0,
    "now_time": 1725002188,
    "online_count": 1,
    "need_login_subtitle": false,
    "view_points": [],
    "preview_toast": "为创作付费，购买观看完整视频|购买观看",
    "options": {
      "is_360": false,
      "without_vip": false
    },
    "guide_attention": [],
    "jump_card": [],
    "operation_card": [],
    "online_switch": {
      "enable_gray_dash_playback": "500",
      "new_broadcast": "1",
      "realtime_dm": "1",
      "subtitle_submit_switch": "1"
    },
    "fawkes": {
      "config_version": 30787,
      "ff_version": 21289
    },
    "show_switch": {
      "long_progress": false
    },
    "bgm_info": {
      "music_id": "MA436038343856245020",
      "music_title": "Unwelcome school",
      "jump_url": "https://music.bilibili.com/h5/music-detail?music_id=MA436038343856245020&cid=1625992822&aid=1906473802"
    },
    "toast_block": false,
    "is_upower_exclusive": false,
    "is_upower_play": false,
    "is_ugc_pay_preview": false,
    "elec_high_level": {
      "privilege_type": 0,
      "title": "",
      "sub_title": "",
      "show_button": false,
      "button_text": "",
      "jump_url": "",
      "intro": "",
      "new": false
    },
    "disable_show_up_info": false
  }
}
```

</details>

旧接口历史示例：已登录, `aid=60977932`

```shell
curl -G 'https://api.bilibili.com/x/player/v2' \
--url-query 'aid=60977932' \
--url-query 'cid=106101299' \
-b 'SESSDATA=xxx'
```

<details>
<summary>查看响应示例:</summary>

```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "aid": 60977932,
    "bvid": "BV1Jt411P77c",
    "allow_bp": false,
    "no_share": false,
    "cid": 106101299,
    "max_limit": 1000,
    "page_no": 1,
    "has_next": true,
    "ip_info": {
      "ip": "108.181.22.55",
      "zone_ip": " 172.27.132.5",
      "zone_id": 29409296,
      "country": "美国",
      "province": "加利福尼亚州",
      "city": "洛杉矶"
    },
    "login_mid": 616368979,
    "login_mid_hash": "445e7035",
    "is_owner": false,
    "name": "淡紫玲儿",
    "permission": "10000,1001",
    "level_info": {
      "current_level": 3,
      "current_min": 1500,
      "current_exp": 2962,
      "next_exp": 4500,
      "level_up": -62135596800
    },
    "vip": {
      "type": 1,
      "status": 0,
      "due_date": 1665417600000,
      "vip_pay_type": 0,
      "theme_type": 0,
      "label": {
        "path": "",
        "text": "",
        "label_theme": "",
        "text_color": "",
        "bg_style": 0,
        "bg_color": "",
        "border_color": "",
        "use_img_label": true,
        "img_label_uri_hans": "",
        "img_label_uri_hant": "",
        "img_label_uri_hans_static": "https://i0.hdslb.com/bfs/vip/d7b702ef65a976b20ed854cbd04cb9e27341bb79.png",
        "img_label_uri_hant_static": "https://i0.hdslb.com/bfs/activity-plat/static/20220614/e369244d0b14644f5e1a06431e22a4d5/KJunwh19T5.png"
      },
      "avatar_subscript": 0,
      "nickname_color": "",
      "role": 0,
      "avatar_subscript_url": "",
      "tv_vip_status": 0,
      "tv_vip_pay_type": 0,
      "tv_due_date": 0,
      "avatar_icon": {
        "icon_resource": {}
      }
    },
    "answer_status": 0,
    "block_time": 0,
    "role": "0",
    "last_play_time": 0,
    "last_play_cid": 0,
    "now_time": 1725003260,
    "online_count": 1,
    "need_login_subtitle": false,
    "subtitle": {
      "allow_submit": true,
      "lan": "zh-CN",
      "lan_doc": "中文（中国）",
      "subtitles": [
        {
          "id": 13643112644608002,
          "lan": "zh-Hans",
          "lan_doc": "中文（简体）",
          "is_lock": true,
          "subtitle_url": "//aisubtitle.hdslb.com/bfs/subtitle/xxx-zh.json",
          "type": 0,
          "id_str": "13643112644608002",
          "ai_type": 0,
          "ai_status": 0
        },
        {
          "id": 13643200114196484,
          "lan": "en-US",
          "lan_doc": "英语（美国）",
          "is_lock": true,
          "subtitle_url": "//aisubtitle.hdslb.com/bfs/subtitle/xxx-en.json",
          "type": 0,
          "id_str": "13643200114196484",
          "ai_type": 0,
          "ai_status": 0
        }
      ]
    },
    "view_points": [],
    "preview_toast": "为创作付费，购买观看完整视频|购买观看",
    "options": {
      "is_360": false,
      "without_vip": false
    },
    "guide_attention": [],
    "jump_card": [],
    "operation_card": [],
    "online_switch": {
      "enable_gray_dash_playback": "500",
      "new_broadcast": "1",
      "realtime_dm": "1",
      "subtitle_submit_switch": "1"
    },
    "fawkes": {
      "config_version": 30787,
      "ff_version": 21289
    },
    "show_switch": {
      "long_progress": false
    },
    "bgm_info": null,
    "toast_block": false,
    "is_upower_exclusive": false,
    "is_upower_play": false,
    "is_ugc_pay_preview": false,
    "elec_high_level": {
      "privilege_type": 0,
      "title": "",
      "sub_title": "",
      "show_button": false,
      "button_text": "",
      "jump_url": "",
      "intro": "",
      "new": false
    },
    "disable_show_up_info": false
  }
}
```

</details>

## 播放反馈

> https://app.bilibili.com/x/resource/laser2

*请求方式: POST*

注: 该接口不传 Cookie

**URL参数:**

|参数名|类型|内容|必要性|备注|
|-|-|-|-|-|
|mid|num|当前用户 mid|不必要|未登录为空|
|buvid|str|BUVID (APP) 或 buvid3 (Web)|必要|可为任意非空字符串|
|app_key|str|APP 密钥|必要|Web: web_player<br />可为任意非空字符串|
|url|str|日志 URL|非必要|从 [上传接口](../creativecenter/upload.md#上传接口) 得到的 upos 协议 URL|
|task_type|num|任务类型|非必要|300: 播放卡顿<br />301: 进度条君无法调戏<br />354: 校园网无法访问<br />303: 弹幕无法显示<br />553: 跳过首尾时间有误<br />304: 出现浮窗广告<br />305: 无限小电视<br />302: 音画不同步<br />306: 黑屏<br />307: 其他|

**JSON回复:**

|字段|类型|内容|备注|
|-|-|-|-|
|code|num|返回值|0: 成功<br />-400: 请求错误|
|message|str|错误信息|默认为 0|
|ttl|num|1||
|data|obj|数据本体| |

`data` 对象:

|字段|类型|内容|备注|
|-|-|-|-|
|task_id|num|任务 ID?||

**示例:**

播放反馈无限小电视, 不登录, 不传文件, buvid 为 `chenrui-in-icu`

```shell
curl -X POST "https://app.bilibili.com/x/resource/laser2" \
--data-urlencode "buvid=chenrui-in-icu" \
--data-urlencode "app_key=web_player" \
--data-urlencode "task_type=305"
```

<details>
<summary>查看响应示例:</summary>

```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "task_id": 850448532
  }
}
```

</details>

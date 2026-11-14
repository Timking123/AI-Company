# 显式日志 Token 用量报告

`scripts/usage_report.py` 是本地只读工具，只打开用户明确提供的文件。
它不扫描目录、不联网、不安装依赖、不写日志，也不提取或展示消息正文、工具参数。
报告中的 Token 是日志计量，不能解释为净新增文字、任务质量、上下文容量或金额。
没有供应商账单、模型价格与计费契约时，金额保持 `unknown`。

## 使用

需要 Python 3.10 或更新版本，普通 JSONL 只使用标准库。
以下路径仅为虚构示例，请换成你授权读取的具体文件：

```sh
python -B scripts/usage_report.py --label worker=./example.jsonl
python -B scripts/usage_report.py --start 2026-01-01T00:00:00Z --end 2026-01-02T00:00:00Z --label worker=./part-1.jsonl --label worker=./part-2.jsonl --label lead=./lead.jsonl
```

时间必须是带时区的 ISO 时间，区间为 `[start, end)`，省略的边界不限制时间。
同一标签的文件必须是逻辑连续的日志，按参数顺序读取，共享累计 baseline 与重复检测；
标签不同则独立计量，不做跨标签去重。标签仅允许字母、数字、中文和 `_.-`，最多 64 个字符。
不要把互不相干的聊天当作同一标签的连续文件，也不要把同一聊天分到多个标签后相加。
路径可以带空格，在你的 shell 中对整个 `NAME=PATH` 参数加引号。
目录、UNC 网络路径与不存在的文件会报固定错误，不回显路径或原始异常。

`.zst` 仅在当前 Python 已安装 `zstandard` 时支持；缺少依赖会明确报错，工具不会安装包。
压缩读取失败也会留缺口，不会退回猜测。

## 计量与缺口

- 仅提取 `event_msg.payload.type=token_count` 的时间戳、
  `info.total_token_usage`、`info.last_token_usage`，以及 `session_meta` 的元数据时间。
  每组计数需要完整的 input、cached input、output、reasoning output 与 total 字段，
  必须是非负整数，且 `total=input+output`、`cached<=input`、`reasoning<=output`。
  `info:null` 是合法的限额更新，不含用量样本，直接忽略且保留 baseline；
  有非空 info 却缺计数、或缺少 info 字段，仍标记缺口。
- 使用相邻累计的差分；同一累计重复上报不重复相加，重叠文件中的相同时间戳及累计也去重。
  非重复倒序样本不纳入计量，并标记缺口。
- 首份正累计通常继承历史，只建立 baseline，不把整份累计算成本期。
  如果会话创建于区间内、创建时间不晚于首样本且 `total==last`，才计入首个请求。
  没有前序 baseline 时报告 `incomplete / unknown`；合法的首样本 last 会单列展示，
  因区间归属未证实而不混入已确认合计。首份零累计可建立已知 baseline。
- 累计下降时，仅在当前 `total==last` 时接受为一致 reset 并计入新累计。
  其它下降、差分子集不一致、缺字段与坏时间都会明确标记；缺口后重新建立 baseline，
  继续报告后续可确认的差分。无法解析的行可能隐藏 reset，因此会使前序 baseline 失效，
  下一合法样本只重建 baseline，不跨越未知记录计算差分。
  连续文件的 `session_meta` 可能有新的录制时间，只记段变化，不直接清空 baseline。
  后续相同累计去重，合法递增继续差分；倒序、子集不一致或无法证实的 reset 仍标缺口。
- 差分归属当前 token_count 的时间戳。这是日志事件口径，不证明请求的实际开始、结束或供应商计费时间。
  即便状态为 complete，也只代表显式文件内的日志证据自洽，不证明日志完整或等于供应商账单。
- cached 是 input 的子集，reasoning 是 output 的子集；报告展示它们但不会再次加入总数。
  未缓存 input 为 `input-cached`。金额始终未知，不填造单价或费用。
- 单行最多处理 1 MiB，超长行分块跳过并计一个缺口；坏 JSON、无效 UTF-8、读取/解压错误
  只显示固定诊断，不输出原行或异常正文。文件外的遗漏无法被工具发现。
  工具按流读取文件，重复快照索引会随合法样本数增长。
- 区间无可用样本标记 unknown；存在缺口时表内数字仅是可确认部分，不能当成完整用量。
  诊断采取整个显式文件范围的保守口径：区间外的坏行、缺字段等也可能使报告为 incomplete，
  当前不把这些异常精确归因到请求区间。complete 不代表精确全账。

默认输出可读 Markdown 表格。退出码 `0` 表示日志范围内自洽，`1` 表示存在计量缺口，
`2` 表示参数、文件或压缩依赖错误；错误时仍可展示其它文件的可确认部分。
请勿把含私有内容的原始日志提交到仓库。

## 合成测试

```sh
python -B -m unittest discover -s tests -p test_usage_report.py -v
```

测试针对累计重复、连续文件、区间边界、reset、继承 baseline、子集重复计数和隐私泄漏风险。
夹具均为合成数据，没有读取真实私有日志，也没有验证真实供应商计费。

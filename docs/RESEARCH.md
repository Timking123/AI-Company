# 3.1.0研究依据与适用边界

查阅日期为2026-11-13。以下一手资料用于方法选择，具体规则由本工作流结合实际失败模式独立编写。论文或厂商的单项结果只在其实验范围内成立。

3.1.0于2026-11-15根据后续实践补强可执行检查点，沿用这些方法依据，本次未重新联网核验资料。匿名回归聚焦正常组合接线、维护入口、首因保全、真实估时与状态、内部预算和版本加载；场景前提不构成外部项目已修复或长期效果的证据。

| 原始资料 | 本版采用的方法 | 适用限制 |
| --- | --- | --- |
| [Building effective agents](https://www.anthropic.com/research/building-effective-agents)，2024-12-19 | 从简单流程起步，按实际需要引入编排与代理 | 工程经验，无法保证所有项目使用同一组织方式 |
| [DORA小批量工作](https://dora.dev/capabilities/working-in-small-batches/) | 以独立、有用、可验证的行为组织批次 | 实际依赖决定边界，固定小时数不作为普遍硬限 |
| [Pact契约测试](https://docs.pact.io/getting_started/how_pact_works) | 真实consumer生成交互，再由provider验证 | 消息测试替代MQ，真实broker、适配器和正常入口仍有自身证据 |
| [SQLite测试方法](https://sqlite.org/testing.html) | 独立判定、差分和少量mutation识错检查 | 超大规模测试及覆盖目标依项目风险采用 |
| [Agent评测工程方法](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)，2026-01-09 | 判断实际结果、正负例及模型评委校准 | 任务成功仍受权限与过程约束 |
| [UK AISI Inspect日志](https://inspect.aisi.org.uk/eval-logs.html) | 运行状态、样本错误、评分与缺失分别保留 | 日志格式完整仍需语义和业务验证 |
| [HAL论文v1](https://arxiv.org/html/2510.11977v1)，2025-10-13 | 同时报质量、成本和失败，检查数据泄漏及环境影响 | 日志相关性无法独立证明干预因果或普遍收益 |
| [SWE-bench维护者讨论267](https://github.com/SWE-bench/SWE-bench/issues/267) | 用金标在真实评分环境校准，复读最终有效结果 | 历史已关闭问题只作方法依据 |
| [AWS超时、重试和退避](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) | 单一重试责任、幂等和副作用判断 | 原用户的一次启动及停止条件优先 |
| [gRPC deadlines](https://grpc.io/docs/guides/deadlines/) | 传播扣除已耗时的剩余期限 | 取消后的子活动仍由应用收口 |
| [Go context Cause](https://pkg.go.dev/context#Cause) | 首因、取消与完成状态分别处理 | 具体实现按语言与宿主能力核验 |
| [多代理研究系统](https://www.anthropic.com/research/multi-agent-research-system)，2025-06-13 | 并行收益应覆盖重复检索、协调和集成成本 | 厂商特定收益与Token倍数不外推为通用指标 |
| [Python subprocess](https://docs.python.org/3/library/subprocess.html) | 明确run/communicate、超时、流与回收语义 | 父子树和平台进程创建有各自限制 |
| [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | 分层入口、发现优先级与新运行加载 | 文本写入、宿主加载和行为证据分别报告 |
| [Codex Skills](https://learn.chatgpt.com/docs/build-skills) | 简短元数据和按需加载，避免无关指令注入上下文 | 技能目录和宿主当前可见性分别验证 |
| [OpenAI MCP安全](https://developers.openai.com/api/docs/guides/tools-connectors-mcp) | 限定工具、信任来源和数据外发，防提示注入 | 外部服务器有独立的数据保留与权限边界 |
| [MCP授权规范](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) | audience、resource、最小scope与禁止token passthrough | 具体服务授权能力须核实际实现 |
| [MCP工具信任](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | 工具描述与annotations作为不可信输入处理 | 提示字段无法作为强制权限保证 |
| [Invariant原研究](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)，2025-04-01 | 审工具描述及变化，隔离无关私有数据 | 具体攻击案例无法证明某个工具已安全或已受攻击 |

## 工具候选的固定证据

- Gitleaks [v8.30.1发布](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1)、[CLI参数源码](https://raw.githubusercontent.com/gitleaks/gitleaks/v8.30.1/cmd/root.go)、[脱敏讨论2296](https://github.com/gitleaks/gitleaks/issues/2296)。脱敏需显式CLI设置，可信配置与扫描边界也影响结果。
- OSV-Scanner [v2.7.1](https://github.com/google/osv-scanner/releases/tag/v2.7.1)、[离线模式](https://github.com/google/osv-scanner/blob/v2.7.1/docs/offline-mode.md)、[安装及来源验证](https://google.github.io/osv-scanner/installation/)。数据库时点和离线参数范围须说明。
- pip-audit [v2.10.1安全模型](https://raw.githubusercontent.com/pypa/pip-audit/v2.10.1/README.md)及[依赖声明](https://raw.githubusercontent.com/pypa/pip-audit/v2.10.1/pyproject.toml)。常规解析可能运行pip，不适合作为恶意包的隔离边界。
- Cisco skill-scanner [2.3.2说明](https://raw.githubusercontent.com/cisco-ai-defense/skill-scanner/2.3.2/README.md)、[构建与依赖](https://raw.githubusercontent.com/cisco-ai-defense/skill-scanner/2.3.2/pyproject.toml)、[维护者安全公告](https://github.com/cisco-ai-defense/skill-scanner/security/advisories/GHSA-ppfx-73j5-fhxc)。可选API旧版本存在未认证上传及资源消耗风险，后继修复不能替代其他风险核验。

以上链接是研究出处。采用、执行和数据发送仍受实际用户授权及工具准入结论约束。

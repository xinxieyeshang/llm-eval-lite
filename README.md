# llm-eval-lite

一个零依赖的 Python 小工具：读取 JSONL 格式的标准答案和模型输出，计算 exact_match 与 contains_match 两个指标，生成 Markdown 对比表。

输入：golden.jsonl 和 predictions.jsonl，每行一个 JSON 对象，含 id、question、answer、prediction 字段。

运行：python -m eval_lite.cli examples/golden.jsonl examples/predictions.jsonl
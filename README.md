# llm-eval-lite

一个零第三方依赖的 Python 小工具：读入标准答案和模型输出的 JSONL 文件，
计算 exact_match 与 contains_match 两个指标，生成一张 Markdown 对比表。

## 为什么做

评测大模型输出时，靠肉眼一条条比对不可靠，也不可复现——同一个人在不同时间
给出的判断都可能不一样。这个项目把评测变成一条命令：固定一份 golden set，
换不同的模型输出文件，就能跑出可以直接贴进报告的对比表。改了评测逻辑，
重跑一遍就能看到结果变化。

## 快速开始

需要 Python 3.10+，运行工具本身无需安装任何第三方依赖。

    git clone https://github.com/xinxieyeshang/llm-eval-lite.git
    cd llm-eval-lite
    python -m eval_lite.cli --golden examples/golden.jsonl --pred examples/model_a.jsonl examples/model_b.jsonl

如果要跑测试，再装 pytest：

    python -m pip install pytest
    python -m pytest -q

## 输入格式

两个文件都是 JSONL（每行一个 JSON 对象，UTF-8 编码）。

标准答案 golden.jsonl：
    {"id":"q1","question":"Python 中 len() 返回什么？","answer":"返回对象的长度"}

模型输出 model_a.jsonl：
    {"id":"q1","prediction":"返回对象的长度"}

两边通过 id 对齐：程序按 id 找到每条预测对应的标准答案，golden 里没有的 id 跳过。
answer 和 prediction 都是字符串。

## 输出示例

用仓库自带的 10 条评测集跑上面那条命令，输出如下（也保存在 demo_output.md）：

| 模型 | exact_match | contains_match | 样本数 |
| --- | --- | --- | --- |
| model_a | 8/10 | 9/10 | 10 |
| model_b | 4/10 | 6/10 | 10 |

两个指标的区别在这份数据里能看出来：model_a 第 9 条加了「答案：」前缀，
exact_match 不算命中、contains_match 算命中，所以两列差 1。

## 设计取舍

- 零第三方依赖：只用 Python 标准库（json / argparse / pathlib），clone 下来不用装
  环境就能跑。代价是分词、语义相似度这类能力都得自己实现，所以这里只做最基础的
  字符串匹配。
- exact_match 的局限：它去掉首尾空白后做全等比较，同义改写（「返回长度」和
  「返回对象的长度」）会被判错；contains_match 放宽成「标准答案去空格后是否为
  预测的子串」，能容忍前缀和多余空格，但也可能把包含正确答案却答了一堆无关内容
  的输出判为命中。
- 如果重做：会加归一化步骤（统一大小写、去标点），再按问题类别分组统计，
  看模型在哪类题上更容易错。

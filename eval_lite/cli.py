"""llm-eval-lite CLI: 读 JSONL，算指标，打印 Markdown 对比表。"""
import argparse
import json
from pathlib import Path

from eval_lite.metrics import exact_match, contains_match


def load_jsonl(path):
    """读 JSONL 文件：每行是一个 JSON 对象，返回一个列表。"""
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():                       # 跳过空行
                rows.append(json.loads(line))                # 填空1：把一行文本变成字典
    return rows


def main():
    parser = argparse.ArgumentParser(description="LLM output evaluator")
    parser.add_argument("--golden", required=True, help="标准答案 JSONL")
    parser.add_argument("--pred", nargs="+", required=True, help="模型输出 JSONL（可传多个）")
    args = parser.parse_args()

    # 第一步：把 golden 读成 {id: answer} 的字典，方便按 id 查
    gold_map = {}
    for row in load_jsonl(args.golden):
        gold_map[row["id"]] =row["answer"]                 # 填空2：值取 row 里的什么字段？

    # 第二步：打印 Markdown 表头
    print("| 模型 | exact_match | contains_match | 样本数 |")
    print("| --- | --- | --- | --- |")

    # 第三步：逐个模型算分
    for pred_path in args.pred:
        pred_rows = load_jsonl(pred_path)
        e_hit = 0
        c_hit = 0
        for p in pred_rows:
            gold_answer = gold_map.get(p["id"])     # 按 id 找标准答案；找不到返回 None
            if gold_answer is None:
                continue                             # golden 里没这个 id，跳过
            if exact_match(p["prediction"], gold_answer):
                e_hit += 1                               # 填空3：exact 命中，e_hit 加 1
            if contains_match(p["prediction"], gold_answer):
                c_hit += 1                              # 填空4：contains 命中，c_hit 加 1

        name = Path(pred_path).stem                  # 取文件名，如 model_a
        n = len(pred_rows)
        print(f"| {name} | {e_hit}/{n} | {c_hit}/{n} | {n} |")


if __name__ == "__main__":
    main()
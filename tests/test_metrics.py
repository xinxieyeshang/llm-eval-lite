from eval_lite.metrics import exact_match, contains_match

"""
函数约定：
exact_match(pred, gold)
    规则：pred 和 gold 分别 strip() 之后，内容完全相等返回 True，否则 False

contains_match(pred, gold)
    规则：gold 去掉全部空格之后的字符串，出现在 pred 里面时返回 True
"""

def test_exact_match_equal():
    # 完全相等
    assert exact_match("返回对象的长度", "返回对象的长度") is True

def test_exact_match_case_diff():
    # 大小写不同，exact_match 不匹配
    assert exact_match("Hello World", "hello world") is False

def test_exact_match_empty():
    # 空字符串场景
    assert exact_match("   ", "") is True

def test_contains_match_contained():
    # gold去空格后包含在pred中
    assert contains_match("模型输出：abc123结果", "abc 123") is True
def exact_match(pred, gold):
    """pred、gold 分别 strip() 后完全相等返回 True，否则 False"""
    pred_clean = pred.strip()
    gold_clean = gold.strip()
    return pred_clean == gold_clean

def contains_match(pred, gold):
    """gold 去掉全部空格后，是 pred 的子串返回 True"""
    gold_clean = gold.replace(" ", "")
    return gold_clean in pred
"""游戏逻辑 - 题目生成与判定"""
import random

DIFFICULTIES = ['10', '20', '50', '100']

DIFFICULTY_NAMES = {
    '10': '10以内加减法',
    '20': '20以内加减法',
    '50': '50以内加减法',
    '100': '100以内加减法',
}

MAX_VALUES = {
    '10': 10,
    '20': 20,
    '50': 50,
    '100': 100,
}


def generate_question(difficulty):
    """
    生成一道加减法题目。
    返回 dict:
      - op: '+' 或 '-'
      - a, b: 操作数 (int)
      - answer: 正确答案 (int)
      - display: 显示文本 如 '7 + 3 = '
    """
    max_val = MAX_VALUES.get(difficulty, 10)
    op = random.choice(['+', '-'])

    if op == '+':
        a = random.randint(0, max_val)
        b = random.randint(0, max_val - a)
        answer = a + b
    else:
        a = random.randint(0, max_val)
        b = random.randint(0, a)
        answer = a - b

    return {
        'op': op,
        'a': a,
        'b': b,
        'answer': answer,
        'display': f'{a} {op} {b} = ',
    }


def check_answer(question, user_answer):
    """检查用户答案是否正确"""
    return user_answer == question['answer']


def question_to_key(q):
    """题目转为唯一标识（用于错题去重）"""
    return f"{q['a']}{q['op']}{q['b']}"

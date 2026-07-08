"""用户数据管理 - JSON 文件存储"""
import json
import os
import sys

# 确保能找到 game_logic 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_logic import question_to_key

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _user_file(username):
    safe = ''.join(c for c in username if c.isalnum() or c in '_-')
    return os.path.join(DATA_DIR, f'{safe}.json')


def _load_user(username):
    _ensure_dir()
    path = _user_file(username)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'name': username,
        'stats': {},
        'wrong': {},
        'settings': {'timer_enabled': True, 'timer_seconds': 60},
    }


def _save_user(username, data):
    _ensure_dir()
    with open(_user_file(username), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_user_list():
    """返回所有用户名列表"""
    _ensure_dir()
    users = []
    for f in os.listdir(DATA_DIR):
        if f.endswith('.json'):
            users.append(f[:-5])
    return sorted(users)


def user_exists(username):
    return os.path.exists(_user_file(username))


def create_user(username):
    """创建新用户"""
    if user_exists(username):
        return False
    _save_user(username, _load_user(username))
    return True


def delete_user(username):
    """删除用户"""
    path = _user_file(username)
    if os.path.exists(path):
        os.remove(path)


def get_stats(username):
    """获取用户统计 {difficulty: {correct: N, wrong: N}}"""
    data = _load_user(username)
    return data.get('stats', {})


def record_result(username, difficulty, is_correct):
    """记录一次答题结果"""
    data = _load_user(username)
    stats = data.setdefault('stats', {})
    d = stats.setdefault(difficulty, {'correct': 0, 'wrong': 0})
    if is_correct:
        d['correct'] = d.get('correct', 0) + 1
    else:
        d['wrong'] = d.get('wrong', 0) + 1
    _save_user(username, data)


def add_wrong(username, difficulty, question):
    """添加错题"""
    data = _load_user(username)
    wrong = data.setdefault('wrong', {})
    dl = wrong.setdefault(difficulty, {})
    key = question_to_key(question)
    if key not in dl:
        dl[key] = {
            'a': question['a'],
            'op': question['op'],
            'b': question['b'],
            'answer': question['answer'],
        }
    _save_user(username, data)


def remove_wrong(username, difficulty, question):
    """移除错题"""
    data = _load_user(username)
    wrong = data.get('wrong', {})
    dl = wrong.get(difficulty, {})
    key = question_to_key(question)
    if key in dl:
        del dl[key]
        _save_user(username, data)


def get_wrong_list(username, difficulty):
    """获取某难度错题列表"""
    data = _load_user(username)
    wrong = data.get('wrong', {})
    dl = wrong.get(difficulty, {})
    return list(dl.values())


def clear_stats(username):
    """清除用户所有统计和错题"""
    data = _load_user(username)
    data['stats'] = {}
    data['wrong'] = {}
    _save_user(username, data)


def get_wrong_question(username, difficulty):
    """随机获取一道错题，无错题返回 None"""
    import random
    wrongs = get_wrong_list(username, difficulty)
    if not wrongs:
        return None
    q = random.choice(wrongs)
    q['display'] = f"{q['a']} {q['op']} {q['b']} = "
    return q


def get_settings(username):
    """获取用户设置"""
    data = _load_user(username)
    return data.get('settings', {'timer_enabled': True, 'timer_seconds': 60})


def save_settings(username, settings):
    """保存用户设置"""
    data = _load_user(username)
    data['settings'] = settings
    _save_user(username, data)

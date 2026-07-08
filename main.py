"""
加减法练习游戏 - 主入口
支持多用户、错题集、倒计时、多难度级别
"""
import os
os.environ['KIVY_LOG_LEVEL'] = 'warning'

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import platform
from kivy.metrics import dp, sp

import user_manager
import game_logic

# ─── 字体注册 ───
FONT_NAME = 'Roboto'  # 默认字体

def register_fonts():
    """注册中文字体 + emoji字体"""
    global FONT_NAME
    font_candidates = []
    emoji_candidates = []

    if platform == 'android':
        font_candidates = [
            '/system/fonts/NotoSansCJK-Regular.ttc',
            '/system/fonts/NotoSansSC-Regular.otf',
            '/system/fonts/DroidSansFallback.ttf',
            '/system/fonts/NotoSansCJKsc-Regular.otf',
        ]
        # Android 自带 NotoColorEmoji，无需额外注册
    elif platform == 'ios':
        font_candidates = [
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/System/Library/Fonts/PingFang.ttc',
        ]
    else:  # desktop
        import glob
        font_candidates = [
            'C:/Windows/Fonts/msyh.ttc',
            'C:/Windows/Fonts/msyhbd.ttc',
            'C:/Windows/Fonts/simhei.ttf',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/droid/DroidSansFallback.ttf',
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/wqy-microhei/wqy-microhei.ttc',
            '/System/Library/Fonts/PingFang.ttc',
        ]
        font_candidates += glob.glob('/usr/share/fonts/**/NotoSans*CJK*.ttc', recursive=True)
        font_candidates += glob.glob('/usr/share/fonts/**/NotoSans*SC*.otf', recursive=True)
        # Windows emoji 字体
        emoji_candidates = [
            'C:/Windows/Fonts/seguiemj.ttf',  # Segoe UI Emoji
        ]

    # 注册中文字体
    for font_path in font_candidates:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name='CJK', fn_regular=font_path)
                FONT_NAME = 'CJK'
                print(f'[字体] CJK已注册: {font_path}')
                break
            except Exception as e:
                print(f'[字体] 注册失败 {font_path}: {e}')
    else:
        local_font = os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSansSC-Regular.ttf')
        if os.path.exists(local_font):
            try:
                LabelBase.register(name='CJK', fn_regular=local_font)
                FONT_NAME = 'CJK'
                print(f'[字体] CJK已注册(本地): {local_font}')
            except Exception:
                pass
        else:
            print('[字体] 未找到中文字体，使用 Roboto')

    # 注册 emoji 字体 (Windows)
    for emoji_path in emoji_candidates:
        if os.path.exists(emoji_path):
            try:
                LabelBase.register(name='Emoji', fn_regular=emoji_path)
                print(f'[字体] Emoji已注册: {emoji_path}')
            except Exception:
                pass


# ─── 全局 ScreenManager ───
sm = ScreenManager(transition=SlideTransition(duration=0.3))


# ═══════════════════════ 屏幕类 ═══════════════════════

class MenuScreen(Screen):
    pass


class UserSelectScreen(Screen):
    users = ListProperty([])

    def on_enter(self):
        self.users = user_manager.get_user_list()

    def _rebuild_list(self):
        box = self.ids.user_list
        box.clear_widgets()
        self.users = user_manager.get_user_list()
        if not self.users:
            box.add_widget(Label(
                text='暂无用户，请先创建',
                font_size=sp(18),
                size_hint_y=None,
                height=dp(50),
                color=(0.6, 0.6, 0.7, 1),
            ))
            return
        for uname in self.users:
            btn = Button(
                text=f'{uname}',
                font_size=sp(20),
                size_hint_y=None,
                height=dp(52),
                background_normal='',
                background_color=(0.25, 0.35, 0.55, 1),
                color=(1, 1, 1, 1),
            )
            btn.bind(on_release=lambda b, u=uname: self._select_user(u))
            box.add_widget(btn)

    def _select_user(self, username):
        diff_screen = sm.get_screen('difficulty')
        diff_screen.username = username
        sm.current = 'difficulty'


class UserCreateScreen(Screen):
    def _do_create(self):
        name = self.ids.name_input.text.strip()
        if not name:
            self.ids.msg_label.text = '请输入用户名'
            return
        if len(name) > 20:
            self.ids.msg_label.text = '用户名不超过20个字符'
            return
        if user_manager.user_exists(name):
            self.ids.msg_label.text = f'用户 "{name}" 已存在'
            return
        user_manager.create_user(name)
        self.ids.name_input.text = ''
        self.ids.msg_label.text = ''
        # 跳转到难度选择
        diff_screen = sm.get_screen('difficulty')
        diff_screen.username = name
        sm.current = 'difficulty'


class DifficultyScreen(Screen):
    username = StringProperty('')

    def _start(self, difficulty):
        game = sm.get_screen('game')
        game.start_game(self.username, difficulty, from_wrong=False)
        sm.current = 'game'

    def _go_wrong(self):
        wrong = sm.get_screen('wrong')
        wrong.username = self.username
        sm.current = 'wrong'

    def _go_stats(self):
        stats = sm.get_screen('stats')
        stats.username = self.username
        sm.current = 'stats'

    def _go_settings(self):
        settings = sm.get_screen('settings')
        settings.username = self.username
        sm.current = 'settings'


class GameScreen(Screen):
    question_text = StringProperty('')
    difficulty_label = StringProperty('')
    timer_text = StringProperty('')
    feedback_text = StringProperty('')
    feedback_color = ListProperty([1, 1, 1, 1])
    answer_text = StringProperty('')
    show_next = BooleanProperty(False)
    timer_enabled = BooleanProperty(True)
    timer_seconds = NumericProperty(60)
    timer_remaining = NumericProperty(0)
    progress_value = NumericProperty(100)
    count_text = StringProperty('')

    _timer_event = None
    _current_q = None
    _username = ''
    _difficulty = ''
    _from_wrong = BooleanProperty(False)
    _total = NumericProperty(0)
    _correct = NumericProperty(0)
    _wrong = NumericProperty(0)

    def on_enter(self):
        self._load_next_question()

    def on_leave(self):
        self._cancel_timer()

    def start_game(self, username, difficulty, from_wrong=False):
        self._username = username
        self._difficulty = difficulty
        self._from_wrong = from_wrong
        self._total = 0
        self._correct = 0
        self._wrong = 0
        self.show_next = False
        self.feedback_text = ''
        self.answer_text = ''
        self.difficulty_label = game_logic.DIFFICULTY_NAMES.get(difficulty, difficulty)
        # 加载用户设置
        settings = user_manager.get_settings(self._username)
        self.timer_enabled = settings.get('timer_enabled', True)
        self.timer_seconds = settings.get('timer_seconds', 60)

    def _load_next_question(self):
        self._cancel_timer()
        self.answer_text = ''
        self.feedback_text = ''
        self.show_next = False
        self._update_count()

        if self._from_wrong:
            q = user_manager.get_wrong_question(self._username, self._difficulty)
            if q is None:
                self.feedback_text = '太棒了！错题全部答对了！'
                self.feedback_color = [0.2, 0.8, 0.2, 1]
                self.show_next = True
                self.question_text = ''
                return
            self._current_q = q
        else:
            self._current_q = game_logic.generate_question(self._difficulty)

        self.question_text = self._current_q['display']
        # 启动计时器
        if self.timer_enabled:
            self.timer_remaining = self.timer_seconds
            self.progress_value = 100
            self._timer_event = Clock.schedule_interval(self._tick, 1)

    def _tick(self, dt):
        self.timer_remaining -= 1
        self.progress_value = max(0, (self.timer_remaining / self.timer_seconds) * 100)
        if self.timer_remaining <= 10:
            self.timer_text = f'[color=ff3333]{int(self.timer_remaining)}s[/color]'
        else:
            self.timer_text = f'{int(self.timer_remaining)}s'
        if self.timer_remaining <= 0:
            self._cancel_timer()
            self._submit(timeout=True)

    def _cancel_timer(self):
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None

    def _update_count(self):
        self.count_text = f'第 {self._total + 1} 题  |  对 {self._correct}  错 {self._wrong}'

    def on_digit(self, digit):
        if self.show_next:
            return
        if len(self.answer_text) < 6:
            self.answer_text += digit

    def on_backspace(self):
        if self.show_next:
            return
        self.answer_text = self.answer_text[:-1]

    def on_clear(self):
        if self.show_next:
            return
        self.answer_text = ''

    def on_submit(self):
        if self.show_next:
            return
        self._submit(timeout=False)

    def _submit(self, timeout=False):
        self._cancel_timer()
        self._total += 1

        if timeout or self.answer_text.strip() == '':
            is_correct = False
            user_answer = '(未作答)'
        else:
            try:
                user_answer = int(self.answer_text.strip())
            except ValueError:
                user_answer = self.answer_text.strip()
            is_correct = game_logic.check_answer(self._current_q, user_answer)

        if is_correct:
            self._correct += 1
            self.feedback_text = '回答正确！'
            self.feedback_color = [0.2, 0.8, 0.2, 1]
            if self._from_wrong:
                user_manager.remove_wrong(self._username, self._difficulty, self._current_q)
            user_manager.record_result(self._username, self._difficulty, True)
        else:
            self._wrong += 1
            correct = self._current_q['answer']
            self.feedback_text = f'正确答案是: {correct}'
            self.feedback_color = [1, 0.3, 0.3, 1]
            if not self._from_wrong:
                user_manager.add_wrong(self._username, self._difficulty, self._current_q)
            user_manager.record_result(self._username, self._difficulty, False)

        self.show_next = True
        self._update_count()

    def on_next(self):
        self._load_next_question()

    def on_back(self):
        self._cancel_timer()
        sm.current = 'difficulty'


class WrongScreen(Screen):
    username = StringProperty('')
    difficulties = ListProperty([])
    count_10 = NumericProperty(0)
    count_20 = NumericProperty(0)
    count_50 = NumericProperty(0)
    count_100 = NumericProperty(0)

    def on_enter(self):
        self.difficulties = game_logic.DIFFICULTIES[:]
        self.count_10 = len(user_manager.get_wrong_list(self.username, '10'))
        self.count_20 = len(user_manager.get_wrong_list(self.username, '20'))
        self.count_50 = len(user_manager.get_wrong_list(self.username, '50'))
        self.count_100 = len(user_manager.get_wrong_list(self.username, '100'))

    def start_wrong(self, diff):
        game = sm.get_screen('game')
        game.start_game(self.username, diff, from_wrong=True)
        sm.current = 'game'


class StatsScreen(Screen):
    username = StringProperty('')
    stats_text = StringProperty('')

    def on_enter(self):
        stats = user_manager.get_stats(self.username)
        lines = [f'{self.username} 的练习统计\n']
        for diff in game_logic.DIFFICULTIES:
            name = game_logic.DIFFICULTY_NAMES.get(diff, diff)
            d = stats.get(diff, {})
            total = d.get('correct', 0) + d.get('wrong', 0)
            if total > 0:
                rate = d.get('correct', 0) / total * 100
                lines.append(f'【{name}】')
                lines.append(f'  总题数: {total}')
                lines.append(f'  正确: {d.get("correct", 0)}  错误: {d.get("wrong", 0)}')
                lines.append(f'  正确率: {rate:.1f}%\n')
        # 错题数
        wrong_count = 0
        for diff in game_logic.DIFFICULTIES:
            wrongs = user_manager.get_wrong_list(self.username, diff)
            wrong_count += len(wrongs)
        lines.append(f'当前错题数: {wrong_count}')
        self.stats_text = '\n'.join(lines)

    def clear_stats(self):
        user_manager.clear_stats(self.username)
        self.on_enter()  # 刷新显示


class SettingsScreen(Screen):
    username = StringProperty('')
    timer_enabled = BooleanProperty(True)
    timer_seconds = NumericProperty(60)

    def on_enter(self):
        settings = user_manager.get_settings(self.username)
        self.timer_enabled = settings.get('timer_enabled', True)
        self.timer_seconds = settings.get('timer_seconds', 60)

    def save_settings(self):
        user_manager.save_settings(self.username, {
            'timer_enabled': self.timer_enabled,
            'timer_seconds': int(self.timer_seconds),
        })


class UserManageScreen(Screen):
    users = ListProperty([])

    def on_enter(self):
        self.users = user_manager.get_user_list()

    def _rebuild_list(self):
        box = self.ids.manage_list
        box.clear_widgets()
        self.users = user_manager.get_user_list()
        if not self.users:
            box.add_widget(Label(
                text='暂无用户',
                font_size=sp(18),
                size_hint_y=None,
                height=dp(50),
                color=(0.6, 0.6, 0.7, 1),
            ))
            return
        for uname in self.users:
            row = BoxLayout(
                size_hint_y=None,
                height=dp(52),
                spacing=dp(10),
            )
            row.add_widget(Label(
                text=f'{uname}',
                font_size=sp(20),
            ))
            del_btn = Button(
                text='删除',
                font_size=sp(16),
                size_hint_x=0.3,
                background_normal='',
                background_color=(0.8, 0.2, 0.2, 1),
                color=(1, 1, 1, 1),
            )
            del_btn.bind(on_release=lambda b, u=uname: self._confirm_delete(u))
            row.add_widget(del_btn)
            box.add_widget(row)

    def _confirm_delete(self, username):
        user_manager.delete_user(username)
        self._rebuild_list()


# ═══════════════════════ App ═══════════════════════

class MathGameApp(App):
    title = '加减法练习'

    def build(self):
        register_fonts()
        if platform not in ('android', 'ios'):
            Window.size = (420, 750)
        # KV 文件由 Kivy 根据 App 类名自动加载 (MathGameApp -> mathgame.kv)
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(UserSelectScreen(name='user_select'))
        sm.add_widget(UserCreateScreen(name='user_create'))
        sm.add_widget(DifficultyScreen(name='difficulty'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(WrongScreen(name='wrong'))
        sm.add_widget(StatsScreen(name='stats'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(UserManageScreen(name='user_manage'))
        return sm


if __name__ == '__main__':
    MathGameApp().run()

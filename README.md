# 🧮 加减法练习游戏

一款专为小学生设计的加减法练习应用，支持 Android 手机和平板。

## ✨ 功能特性

### 🎯 四种难度级别
- 🟢 **10以内加减法** — 入门级
- 🟡 **20以内加减法** — 基础级
- 🟠 **50以内加减法** — 进阶级
- 🔴 **100以内加减法** — 挑战级

### 👤 用户管理
- 支持多用户，每个用户独立统计数据
- 创建、删除用户
- 查看每个难度的正确/错误数量和正确率

### 📝 错题集
- 答错的题目自动进入错题集
- 错题集按难度分类
- 重新答对后自动从错题集中移除

### ⌨️ 数字键盘输入
- 大按钮数字键盘，适合触屏操作
- ⌫ 退格 — 删除最后一位
- ✕ 清零 — 清空输入

### ⏱️ 倒计时功能
- 可开启/关闭倒计时
- 时间可调节（10秒 ~ 300秒）
- 倒计时进度条，最后10秒红色警告
- 超时自动提交（无输入默认提交错误答案）

### 📱 自适应界面
- 中文显示，深色主题
- 自适应不同分辨率手机和平板
- 每屏只显示一题，提交后显示对错
- 错误题目显示正确答案，必须提交才能进入下一题

## 🚀 快速开始

### 电脑运行（开发/测试）
```bash
pip install kivy
cd math-game
python main.py
```

### Android APK 构建

#### 方式一：GitHub Actions 自动构建（推荐）
1. Fork 或创建 GitHub 仓库
2. 将代码推送到 `main` 分支
3. GitHub Actions 自动构建 APK
4. 在 Actions → Artifacts 下载 APK
5. 同时会自动创建 Release

#### 方式二：本地构建
```bash
pip install buildozer cython
buildozer android debug
# APK 生成在 bin/ 目录
```

## 📁 项目结构
```
math-game/
├── main.py              # 主程序入口 + 界面逻辑
├── game_logic.py        # 游戏逻辑（出题、判题）
├── user_manager.py      # 用户数据管理
├── mathgame.kv          # Kivy UI 布局文件
├── buildozer.spec       # Android 打包配置
├── README.md
├── data/                # 用户数据（运行时自动生成）
│   └── <username>.json
└── .github/workflows/
    └── build-apk.yml    # GitHub Actions 自动构建
```

## 🛠️ 技术栈
- **Python 3** + **Kivy** 框架
- **Buildozer** Android 打包工具
- **GitHub Actions** CI/CD 自动构建
- JSON 文件存储用户数据

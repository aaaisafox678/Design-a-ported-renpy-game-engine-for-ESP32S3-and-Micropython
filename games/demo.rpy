# 定义角色
define e = Character("艾丽丝", color="#c8ffc8")
define d = Character("大卫", color="#ffc8c8")

# 背景音乐 (如果SD卡有音乐文件)
# play music "audio/bgm.mp3"

label start:
    # 显示背景
    scene bg default
    
    # 开场白
    e "欢迎来到 Micro-RenPy 视觉小说引擎！"
    e "这是为 JC3248W535CN 开发板定制的 RenPy 8.5.3 兼容版本。"
    
    # 显示角色
    show e happy at center
    e "我是一位虚拟角色，使用 RenPy 的角色系统管理。"
    
    # 对话
    d "你好，艾丽丝！我是大卫。"
    e "你好，大卫！让我们开始这段旅程吧。"
    
    # 分支选择
    menu:
        "继续故事":
            jump continue_story
        "查看引擎信息":
            jump engine_info
        "退出演示":
            jump end

label continue_story:
    with dissolve
    
    e "太棒了！让我们看看这个引擎能做什么。"
    d "它支持对话、角色显示、场景切换、分支选择等功能。"
    
    e "而且完全兼容 RenPy 的脚本语法！"
    
    menu:
        "再来一次":
            jump start
        "返回主菜单":
            jump start

label engine_info:
    with dissolve
    
    e "引擎信息:"
    e "平台: ESP32-S3"
    e "屏幕: 320x480 QSPI LCD"
    e "音频: NS4168 I2S 功放"
    e "版本: RenPy 8.5.3 兼容版"
    
    jump start

label end:
    e "感谢体验 Micro-RenPy！"
    e "开发者：新疆幻城网安科技有限责任公司"
    
    return
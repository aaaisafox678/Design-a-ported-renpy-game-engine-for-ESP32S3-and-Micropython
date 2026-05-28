import time

TRANSITIONS = {
    'dissolve': '溶解过渡',
    'fade': '淡入淡出',
    'push_up': '上推',
    'push_down': '下推',
    'None': '无过渡',
}


def transition(effect='dissolve', duration=0.5):
    """
    执行过渡效果
    
    Args:
        effect: 过渡效果名称
        duration: 持续时间 (秒)
    """
    if effect == 'fade':
        time.sleep(duration / 2)
        time.sleep(duration / 2)
    elif effect == 'dissolve':
        time.sleep(duration)
    # 其他过渡效果可扩展
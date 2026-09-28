# Script SOP: joints_sop

# 将下面内容粘贴到 TouchDesigner Script SOP 的 cook(scriptOP) 区

# Script SOP: 从 skeleton_smooth CHOP 读关节通道，生成每个关节点
def cook(scriptOP):
    joint_names = [
        'head','neck','torso',
        'left_shoulder','left_elbow','left_hand',
        'right_shoulder','right_elbow','right_hand',
        'left_hip','left_knee','left_foot',
        'right_hip','right_knee','right_foot'
    ]
    ch_op = op('skeleton_smooth')  # 确保与网络中 Null 名称一致
    if ch_op is None:
        scriptOP.clear()
        return

    scriptOP.clear()
    for j in joint_names:
        tx_name = f'{j}_tx'
        ty_name = f'{j}_ty'
        tz_name = f'{j}_tz'
        try:
            tx = ch_op[tx_name].eval()
            ty = ch_op[ty_name].eval()
            tz = ch_op[tz_name].eval()
        except Exception:
            tx = ty = tz = 0.0
        p = scriptOP.appendPoint()
        p.P = (tx, ty, tz)
    return

# CHOP Execute DAT: retarget 脚本
# 把下面内容粘到 CHOP Execute DAT（勾选 Every Frame/onFrameStart）
import math

# ---------- 配置区 ----------
# 把左边的源 joint 名（来自 skeleton_smooth，去掉 _tx/_ty/_tz 后缀）映射为 FBX 中对应骨骼 OP 路径
mapping = {
    ('neck','head'): '/project1/character/bone_head',
    ('torso','neck'): '/project1/character/bone_neck',
    ('left_shoulder','left_elbow'): '/project1/character/bone_l_upperarm',
    ('left_elbow','left_hand'): '/project1/character/bone_l_lowerarm',
    ('right_shoulder','right_elbow'): '/project1/character/bone_r_upperarm',
    ('right_elbow','right_hand'): '/project1/character/bone_r_lowerarm',
    ('left_hip','left_knee'): '/project1/character/bone_l_thigh',
    ('left_knee','left_foot'): '/project1/character/bone_l_shin',
    ('right_hip','right_knee'): '/project1/character/bone_r_thigh',
    ('right_knee','right_foot'): '/project1/character/bone_r_shin',
}

# 目标骨骼的默认朝向（在 bind pose 下）；如果你的骨骼在 bind 时朝向不是 Y，请修改
DEFAULT_BONE_DIR = (0.0, 1.0, 0.0)  # local +Y

# ----------------- 工具函数 -----------------
def dot(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def length(v):
    return math.sqrt(dot(v,v))

def normalize(v):
    l = length(v)
    if l == 0:
        return (0.0,0.0,0.0)
    return (v[0]/l, v[1]/l, v[2]/l)

def quat_from_two_vectors(v0, v1):
    v0n = normalize(v0)
    v1n = normalize(v1)
    d = dot(v0n, v1n)
    if d > 0.999999:
        return (0.0,0.0,0.0,1.0)
    if d < -0.999999:
        axis = (1.0,0.0,0.0)
        if abs(v0n[0]) > abs(v0n[2]):
            axis = (0.0,1.0,0.0)
        c = normalize(cross(v0n, axis))
        return (c[0], c[1], c[2], 0.0)
    c = cross(v0n, v1n)
    s = math.sqrt((1.0 + d) * 2.0)
    invs = 1.0 / s
    qx = c[0] * invs
    qy = c[1] * invs
    qz = c[2] * invs
    qw = s * 0.5
    return (qx, qy, qz, qw)

def quat_to_euler_deg(q):
    x,y,z,w = q
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    X = math.atan2(t0, t1)
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else (-1.0 if t2 < -1.0 else t2)
    Y = math.asin(t2)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    Z = math.atan2(t3, t4)
    return (math.degrees(X), math.degrees(Y), math.degrees(Z))

# ----------------- 主循环 -----------------
def onFrameStart(frame):
    ch = op('skeleton_smooth')
    if ch is None:
        return

    for (src_parent, src_child), target_path in mapping.items():
        txp = f'{src_parent}_tx'; typ = f'{src_parent}_ty'; tzp = f'{src_parent}_tz'
        txc = f'{src_child}_tx'; tyc = f'{src_child}_ty'; tzc = f'{src_child}_tz'
        try:
            p = (ch[txp].eval(), ch[typ].eval(), ch[tzp].eval())
            c = (ch[txc].eval(), ch[tyc].eval(), ch[tzc].eval())
        except Exception:
            continue

        src_vec = (c[0]-p[0], c[1]-p[1], c[2]-p[2])
        if length(src_vec) == 0:
            continue
        q = quat_from_two_vectors(DEFAULT_BONE_DIR, src_vec)
        euler = quat_to_euler_deg(q)

        bone_op = op(target_path)
        if bone_op is None:
            continue

        try:
            bone_op.par.rx = euler[0]
            bone_op.par.ry = euler[1]
            bone_op.par.rz = euler[2]
        except Exception:
            pass

    return

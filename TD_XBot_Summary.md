# TouchDesigner 项目 — X Bot Retargeting 总结

本文档总结了我们在本会话中完成的检查、发现与后续步骤，并记录了需要在 TouchDesigner 中修改的脚本位置与示例修改说明，便于你把成果保存到仓库并在本地完成导出 `.tox` 的工作。

---

## 一、仓库与文件位置

仓库: Nicajnor656/Nicajnor656.github.io

重要文件（td-nite2-tox 分支）:

- X Bot FBX (二进制): https://github.com/Nicajnor656/Nicajnor656.github.io/raw/td-nite2-tox/X%20Bot.fbx
- 脚本: scripts/script_sop_joints.py
  - 浏览: https://github.com/Nicajnor656/Nicajnor656.github.io/blob/td-nite2-tox/scripts/script_sop_joints.py
- 脚本: scripts/chop_execute_retarget.py
  - 浏览: https://github.com/Nicajnor656/Nicajnor656.github.io/blob/td-nite2-tox/scripts/chop_execute_retarget.py
- 模板 TOX（占位）: td-nite2-template.tox
  - 浏览: https://github.com/Nicajnor656/Nicajnor656.github.io/blob/td-nite2-tox/td-nite2-template.tox

---

## 二、我们已做的检查与结果

1. 我确认 `X Bot.fbx` 文件存在于 `td-nite2-tox` 分支根目录，大小约 1.75 MB。下载链接见上。
2. 我读取并检查了仓库中两个脚本：
   - `scripts/script_sop_joints.py`（生成 SOP 点，来自 `skeleton_smooth` CHOP）
   - `scripts/chop_execute_retarget.py`（将 CHOP 关节方向映射到目标 FBX 骨骼，执行 retarget）
3. 当前仓库中 `td-nite2-template.tox` 是一个占位文件，真正可用的 `.tox` 必须在本地的 TouchDesigner（例如 2025.32820）中打开 FBX、配置网络并执行 “Save Component” 导出，因此我无法在当前环境生成有效的二进制 `.tox` 文件。

---

## 三、需要你在本地 TouchDesigner 中完成的修改（详细）

### 1) 改动主要位置（必须改）

编辑： `scripts/chop_execute_retarget.py`

- 替换目标骨骼 OP 路径的行（示例位置）：

  在文件的 mapping 字典（原始文件为第 7–18 行附近）替换示例占位路径：

  ```python
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
  ```

  把 `'/project1/character/...'` 全部替换成你在 TouchDesigner 中从 FBX COMP 内部拷贝到的真实骨骼 OP 路径（请使用 Copy Path）。

  - 举例（假设你的 FBX COMP 路径/骨骼名）：

    ```python
    mapping = {
        ('torso','neck'): '/project1/xbot/mixamorig:Spine',
        ('neck','head'): '/project1/xbot/mixamorig:Head',
        ('left_shoulder','left_elbow'): '/project1/xbot/mixamorig:LeftArm',
        # ... 等等
    }
    ```

- 另请注意并根据需要调整：
  - 第 21 行的 `DEFAULT_BONE_DIR = (0.0, 1.0, 0.0)`（目标骨骼在 bind pose 下的朝向）。如果导入后出现旋转偏差，尝试改为 (1,0,0) 或 (0,0,1) 来匹配骨骼本地轴向。

### 2) `script_sop_joints.py` 中需要确认/可选修改点

通常不需要改 FBX 路径；它读取的是你的骨骼 CHOP（`skeleton_smooth`）。需要确认：

- 第 14 行 ch_op 名称：

  ```python
  ch_op = op('skeleton_smooth')
  ```

  如果你在网络里用的 CHOP 名称不是 `skeleton_smooth`（例如 `null_skeleton`），请改为实际名称。

- 第 7–13 行 `joint_names` 列表：该列表必须与来自你的人体追踪/骨骼 CHOP 输出的关节基名一致（这些是 CHOP 通道的 base 名，代码会查找 `name_tx/name_ty/name_tz`）。这不是 FBX 内的骨骼名，而是你的输入关节名集合。

---

## 四、导出并更新 `.tox` 的步骤（本地完成）

1. 在本地 TouchDesigner 中新建/打开网络。
2. 将 `X Bot.fbx` 导入到一个 FBX COMP，确认骨骼能看到（例如带 `mixamorig:` 前缀的骨骼）。
3. 根据上面说明修改 `scripts/chop_execute_retarget.py` 中的 mapping（Copy Path 获得每个骨骼的完整 OP 路径）。
4. 确认 `script_sop_joints.py` 的 `ch_op` 名称与 `joint_names` 匹配你的输入 CHOP。
5. 运行并调试：观察 FBX 骨骼的旋转是否正确应用，调整 `DEFAULT_BONE_DIR` 或 mapping（或检查是否需要对某些骨骼做额外偏移）。
6. 调整完成后，选中你要导出的 Component，右键 → Save Component，将 `.tox` 保存并命名（例如 `td-nite2-xbot.tox`）。
7. 上传导出的 `.tox` 到仓库的 `td-nite2-tox` 分支（或你指定的分支）。

---

## 五、后续我可以帮助的事

- 我可以把上面这份总结写入仓库（已为你生成并提交到默认分支）。
- 如果你把导出的 `.tox` 上传到 `td-nite2-tox` 分支，我会帮你验证骨骼 OP 路径、检查参数映射是否能在 TD 中直接使用，并修正 mapping 示例。
- 如果你把 TouchDesigner 网络的实际骨骼 OP 路径列表发给我，我可以直接帮你生成 `mapping` 字典的完整内容，供拷贝替换。

---

文件自动生成者：Copilot（在用户会话中整理）

时间：由会话创建（请查看提交历史以获取确切时间戳）

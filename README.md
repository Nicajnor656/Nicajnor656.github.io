# TouchDesigner NiTE2 / Astra Pro 骨骼 Retarget 模板（占位）

说明（中文版）

此分支包含一个 TouchDesigner retarget 模板的占位 .tox（文本形式）、用于可视化和 retarget 的脚本，以及示例 mapping 配置和使用说明。由于真实的 .tox 文件需要在本地由 TouchDesigner 导出（binary），本仓库以脚本 + README 的方式提供完整内容，方便你直接粘贴到 TD 或让我在获得 FBX 后生成真实 .tox 并上传。

快速上手：
1. 在 TouchDesigner（2025.32820）中新建项目。
2. 确保系统已安装 OpenNI2 + NiTE2，Astra Pro 驱动并能在 TD 中被识别（OpenNI CHOP 可列出 skeleton channels）。
3. 在网络中按 README 中的节点流程创建：OpenNI CHOP -> skeleton_in Null -> Rename -> Math -> Filter -> skeleton_smooth Null。
4. 新建 Script SOP，把 scripts/script_sop_joints.py 的内容粘入 cook(scriptOP) 并连接到 Copy SOP 与一个 Sphere SOP 以可视化关节。
5. 导入你的 FBX（FBX COMP），在网络中展开并复制目标骨骼的 OP 路径。
6. 编辑 scripts/chop_execute_retarget.py 中的 mapping 字典，把示例 target 路径替换为你的骨骼 OP 路径。
7. 把该脚本粘入 CHOP Execute DAT（勾选 Every Frame / onFrameStart），并确保 CHOP 名称 skeleton_smooth 与项目一致。
8. 运行并调试：调整 Math CHOP 的缩放、Filter CHOP 的平滑参数，或在脚本中修改 DEFAULT_BONE_DIR 与轴偏移来配合你的模型绑定方向。

如果你希望我把真实的 .tox 上传到仓库（非占位文本），请明确允许上传二进制文件并提供一个 FBX（或让我使用示例 FBX），我会在同一分支提交实际 .tox 文件。

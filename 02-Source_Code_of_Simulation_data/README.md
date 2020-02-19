100zxyzws:数据集中灵巧手的位姿数据，其中距离的单位为cm.
grasps:原始抓取数据。
models：训练好的模型文件。
new_depthes：里面是将原深度图的小部分区域设置为同一值,从而使得仿真图与实际图一致.使用picture_process.m文件。
noTh3dofs:graspIT中生成的抓取手势，未包含Th3关节值，因为实际灵巧手TH3关节是固定的，因此需要将graspIT中的关节值固定，并且将生成的抓取手势数据去掉TH3。
overall:物体的整体深度图。
patches:物体被抓取部位的深度图。
test1：仿真抓取实验。
test2：同一位姿，不同图像输入的仿真实验。
test3：同一图像，不同位姿输入的仿真实验。
相关程序：图像的裁剪等数据预处理程序。
100zxyzws: The pose data of the dexterous hand, where the unit of distance is cm.
grasp: raw grasp data.
models: trained model files.
new_depthes: It sets a small part of the original depth image to the same value, so that the simulation image is consistent with the actual image. Use the picture_process.m file.
noTh3dofs: the grasping posture generated in GraspIt, it does not include the value of TH3 joints. Because the TH3 joints of the dexterous hands are fixed, it is necessary to fix the joint values in grass IT and remove the TH3 from the grasping posture data.
overall: The overall depth image of the object.
patches: Depth image of the object's graspped area.
test1: Simulation grasping experiment.
test2: simulation experiment with the same pose and different image input.
test3: Simulation experiment with the same image and different pose input.
code:image preprocessing code, such as image cropping.
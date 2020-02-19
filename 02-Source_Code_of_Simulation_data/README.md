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
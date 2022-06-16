import os 
import numpy as np 
from pathlib import Path


def load_label_from_bfs(
    recon_env_name,
    mobile_pnp_dir
):
    # bfs stands for brute force sampling

    # Given a recon_env_name, this function returns a dictionary where:
    # the keys are the object names in the env_name
    # the values are the labels generated and saved by the file grasp_label_generation_with_brute_force_sampling_antipodal

    labels_for_env = mobile_pnp_dir / f'src/ArmGraspObjectClutterReconstruction-v0_antipodal_grasp_generation/{recon_env_name}_eval_results'

    list_obj_name = os.listdir(labels_for_env)

    obj_name_to_bfs_label = {}

    for obj_name in list_obj_name:

        path_to_label = labels_for_env / obj_name / 'grasp_pose_and_labels.npy'

        art_info = np.load(
            path_to_label,
            allow_pickle=True
        ).item()

        obj_name_to_bfs_label[obj_name] = art_info

    return obj_name_to_bfs_label



def get_path_to_recon_mesh(
    recon_env_name, 
    obj_name,
    mobile_pnp_dir
):

    test_env_name = recon_env_name.replace('Reconstruction', 'Test')

    return str(mobile_pnp_dir / 'mobile_pnp/current_reconstruction' / test_env_name / obj_name / 'model_vhacd.obj')

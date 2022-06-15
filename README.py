# Sequences of command to run finetuning 

# 1, Obtain the "label" from the reconstructed scenes:

# Example: python grasp_label_generation_with_brute_force_sampling_antipodal.py ArmGraspObjectClutterReconstruction_8-v0 --save-dir ArmGraspObjectClutterReconstruction-v0_antipodal_grasp_generation

# 2. Run the following two notebooks to obtain the correct data representation format

# Note that you need to change the path in these two files to point to the label generated in step 1

# reconstructed_create_contact_infos.ipynb

# reconstructed_create_table_top_scene.ipynb

# 3. Copy checkpoint of pretrained model to correct location to finetune on top op 

# cp -r <path_to_mobile_pnp_repo>/src/contact_graspnet/checkpoints .

# Then add these to checkpoints/scene_test_2048_bs3_hor_sigma_001/config.yaml, under DATA 

#   pc_augm:
#     occlusion_nclusters: 0
#     occlusion_dropout_rate: 0.0
#     sigma: 0.000
#     clip: 0.005
#   depth_augm:
#     sigma: 0.001
#     clip: 0.005
#     gaussian_kernel: 0

# 4. Run training

# /home/tele_mani_u20/anaconda3/envs/contact_graspnet_env/bin/python train.py --ckpt_dir checkpoints/scene_test_2048_bs3_hor_sigma_001 --data_path reconstructed/ --arg_configs DATA.num_test_scenes:0 OPTIMIZER.batch_size:2 OPTIMIZER.max_epoch:73001 DATA.scene_contacts_path:scene_contacts

# 5. Run inference on the fine-tuned model and evaluate the grasps 

# First, copy the checkpoint of the finetuned model and replaced the checkpoint of the pretrained cgn model
# which should be at <path_to_mobile_pnp_repo>/src/contact_graspnet/checkpoints 

# Then run inference to obtain grasp prediction with contact_graspnet/inference.py,
# and run contact_graspnet_policy.py to evaluate the grasp prediction.

# Example: python contact_graspnet/inference.py --np_path=eval_data/ArmGraspObjectClutterTest_8-v0.npy --local_regions --filter_grasps --forward_passes=10

# Example: python contact_graspnet_policy.py ArmGraspObjectClutterTest_8-v0 contact_graspnet/results --save-dir "ArmGraspObjectClutterTest-v0_ContactGraspNet_eval_results_${DATETIME}"

# Example command with tee: python contact_graspnet/inference.py --np_path=eval_data/ArmGraspObjectClutterTest_8-v0.npy --local_regions --filter_grasps --forward_passes=10 | tee inference_log_cgn_on_reconstructed_test_scene_8_June13.txt

# Example command with tee: python contact_graspnet_policy.py ArmGraspObjectClutterTest_8-v0 contact_graspnet/results --save-dir "ArmGraspObjectClutterTest-v0_ContactGraspNet_eval_results" 2>&1 | tee eval_log_finetune_cgn_on_reconstructed_test_scene_8_June13.txt

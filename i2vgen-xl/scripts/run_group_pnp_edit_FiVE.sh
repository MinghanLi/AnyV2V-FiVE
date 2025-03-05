#!/bin/bash
#source /home/YourName/miniconda3/etc/profile.d/conda.sh #<-- change this to your own miniconda path
conda activate anyv2v-i2vgen-xl

cd ..
while true; do
    python run_group_pnp_edit.py \
        --template_config "configs_FiVE/group_pnp_edit/template.yaml" \
        --configs_json "configs_FiVE/group_pnp_edit/group_config_edit1.json"

    python run_group_pnp_edit.py \
        --template_config "configs_FiVE/group_pnp_edit/template.yaml" \
        --configs_json "configs_FiVE/group_pnp_edit/group_config_edit2.json"

    python run_group_pnp_edit.py \
        --template_config "configs_FiVE/group_pnp_edit/template.yaml" \
        --configs_json "configs_FiVE/group_pnp_edit/group_config_edit5.json"
done
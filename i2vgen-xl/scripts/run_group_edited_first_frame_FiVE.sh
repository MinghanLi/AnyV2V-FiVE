#!/bin/bash
#source /home/YourName/miniconda3/etc/profile.d/conda.sh  #<-- change this to your own miniconda path
conda activate anyv2v-i2vgen-xl

cd ../..

python edit_image.py \
    --configs_json "i2vgen-xl/configs_FiVE/group_edited_first_frame/group_config_edit1.json"

python edit_image.py \
    --configs_json "i2vgen-xl/configs_FiVE/group_edited_first_frame/group_config_edit2.json"

python edit_image.py \
    --configs_json "i2vgen-xl/configs_FiVE/group_edited_first_frame/group_config_edit3.json"

python edit_image.py \
    --configs_json "i2vgen-xl/configs_FiVE/group_edited_first_frame/group_config_edit4.json"

python edit_image.py \
    --configs_json "i2vgen-xl/configs_FiVE/group_edited_first_frame/group_config_edit5.json"

python edit_image.py \
    --configs_json "i2vgen-xl/configs_FiVE/group_edited_first_frame/group_config_edit6.json"

# Run FiVE

Edited all videos in FiVE
```
cd i2vgen-xl/scripts
# bash run_group_edited_first_frame_FiVE.sh # （Done by Minghan）
bash run_group_ddim_inversion_FiVE.sh
bash run_group_pnp_edit_FiVE.sh
```


- Just test the code

Edited first frame for a single video in FiVE by using InstrcutPix2Pix
```
python edit_image.py --video_path "./data/car-turn16" \
    --input_dir "./data" \
    --output_dir "./data/car-turn16/edited_first_frame" \
    --prompt "Change the car to an elephant"
```
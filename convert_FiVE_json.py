import os
import json
from pathlib import Path


def main(first_frame_path, ddim_inv_path, pnp_edit_path):
    Path('/'.join(first_frame_path.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
    Path('/'.join(ddim_inv_path.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
    Path('/'.join(pnp_edit_path.split('/')[:-1])).mkdir(parents=True, exist_ok=True)


    with open(dataset_json, 'r') as json_file:
        data = json.load(json_file)

    # edited first frame
    edited_first_frame_list = []
    for entry in data:
        video_name = entry["video_name"]
        sample = {
            "video_path": f"./{edited_first_frame_dir}/{video_name}",     
            "input_dir": f"./{edited_first_frame_dir}",
            "output_dir": f"./{edited_first_frame_dir}/{video_name}/edited_first_frame",     
            "prompt": entry["instruction"],
        }
        edited_first_frame_list.append(sample)

    json_data = json.dumps(edited_first_frame_list, indent=2)
    with open(first_frame_path, 'w') as json_file:
        json_file.write(json_data)
    print(f"Processed first frame files: {len(edited_first_frame_list)}！")
    print(f"Save {first_frame_path}")

    # ddim inv
    ddim_inv_list = []

    video_names = []
    for entry in data:
        if entry["video_name"] in video_names:
            continue

        sample = {
            "active": True,
            "force_recompute_latents": False,
            "video_name": entry["video_name"],
            "recon_config":
            {
                "enable_recon": True
            }
        }
        ddim_inv_list.append(sample)
        video_names.append(entry["video_name"])

    json_data = json.dumps(ddim_inv_list, indent=2)
    with open(ddim_inv_path, 'w') as json_file:
        json_file.write(json_data)
    print(f"Processed ddim-inv files: {len(ddim_inv_list)}！")
    print(f"Save {ddim_inv_path}")

    # pnp edit
    pnp_edit_list = []

    for entry in data:
        video_name = entry["video_name"]
        instruction = entry["instruction"]
        sample = {
            "active": True,
            "task_name": "Prompt-Based-Editing",
            "video_name": entry["video_name"],
            "edited_first_frame_path": f"{edited_first_frame_dir}/{video_name}/edited_first_frame/{instruction}.png",
            "editing_prompt": entry["source_prompt"],
            "edited_video_name": entry["target_prompt"],
            "ddim_init_latents_t_idx": 0,
            "pnp_f_t": 1.0,
            "pnp_spatial_attn_t": 1.0,
            "pnp_temp_attn_t":1.0
        }
        pnp_edit_list.append(sample)

    json_data = json.dumps(pnp_edit_list, indent=2)
    with open(pnp_edit_path, 'w') as json_file:
        json_file.write(json_data)
    print(f"Processed pnp-edit files: {len(pnp_edit_list)}！")
    print(f"Save {pnp_edit_path}")


if __name__ == "__main__":

    for i in range(1, 7):
        dataset_json = f"data_FiVE/edit_prompt/edit{i}_FiVE_w_instruction.json"
        first_frame_path = f"i2vgen-xl/configs_FiVE/group_edited_first_frame/group_config_edit{i}.json"
        ddim_inv_path = f"i2vgen-xl/configs_FiVE/group_ddim_inversion/group_config_edit{i}.json"
        pnp_edit_path = f"i2vgen-xl/configs_FiVE/group_pnp_edit/group_config_edit{i}.json"
        edited_first_frame_dir = "data_FiVE"

        if not os.path.exists(dataset_json):
            print(f"Path does not exist, Skip {dataset_json}")
            continue

        main(first_frame_path, ddim_inv_path, pnp_edit_path)
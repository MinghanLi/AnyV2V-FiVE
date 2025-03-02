import os
import argparse
from PIL import Image
import json
from moviepy.editor import VideoFileClip, ImageSequenceClip
from pathlib import Path
import numpy as np

import black_box_image_edit as image_edit

def infer_video(model, video_path, output_dir, prompt, prompt_type="instruct", force_512=False, seed=42, negative_prompt="", overwrite=False):
    """
    Processes videos from the input directory, resizes them to 512x512 before feeding into the model by first frame,
    and saves the processed video back to its original size in the output directory.

    Args:
        model: The video editing model.
        input_dir (str): Path to the directory containing input videos.
        output_dir (str): Path to the directory where processed videos will be saved.
        prompt (str): Instruction prompt for video editing.
    """

    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if os.path.isfile(video_path):
        video_clip = VideoFileClip(video_path)
    elif os.path.isdir(video_path):
        print(f"Loading frames from directory: {video_path}")
        
        frame_files = sorted([
            os.path.join(video_path, f)
            for f in os.listdir(video_path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))
        ])
        if not frame_files:
            raise ValueError(f"No image files found in directory: {video_path}")
    else:
        raise ValueError(f"Invalid video_path: {video_path}")

    video_filename = os.path.basename(video_path)
    # filename_noext = os.path.splitext(video_filename)[0]
    
    # Create the output directory if it does not exist
    # final_output_dir = os.path.join(output_dir, filename_noext)
    final_output_dir = output_dir
    if not os.path.exists(final_output_dir):
        os.makedirs(final_output_dir)

    result_path = os.path.join(final_output_dir, prompt + ".png")

    # Check if result already exists
    if os.path.exists(result_path) and overwrite is False:
        print(f"Result already exists: {result_path}")
        return

    def process_frame(image, image_ori_size, is_array=True):
        if is_array:
            pil_image = Image.fromarray(image)
        else:
            pil_image = image
        if force_512:
            pil_image = pil_image.resize((512, 512), Image.LANCZOS)
        if prompt_type == "instruct":
            result = model.infer_one_image(pil_image, instruct_prompt=prompt, seed=seed, negative_prompt=negative_prompt)
        else:
            result = model.infer_one_image(pil_image, target_prompt=prompt, seed=seed, negative_prompt=negative_prompt)
        if force_512:
            result = result.resize(image_ori_size, Image.LANCZOS)
        return np.array(result)
    
    # Process only the first frame
    if os.path.isfile(video_path):
        first_frame = video_clip.get_frame(0)  # Get the first frame
        processed_frame = process_frame(first_frame, video_clip.size)  # Process the first frame
    elif os.path.isdir(video_path):
        first_frame = Image.open(frame_files[0])
        processed_frame = process_frame(first_frame, first_frame.size, is_array=False)
    else:
        raise ValueError(f"Invalid video_path: {video_path}")

    #Image.fromarray(first_frame).save(os.path.join(final_output_dir, "00000.png"))
    Image.fromarray(processed_frame).save(result_path)
    print(f"Processed and saved the first frame: {result_path}")
    return result_path


def main(args):
    if args.negative_prompt is None:
        negative_prompt = "worst quality, normal quality, low quality, low res, blurry, watermark, jpeg artifacts"
    else:
        negative_prompt = args.negative_prompt
        
    if args.dict_file:
        with open(args.dict_file, 'r') as json_file:
            folders_info = json.load(json_file)

        for video_name, video_infos in folders_info.items():
            input_dir = args.input_dir
            video_path = os.path.join(input_dir, video_name)

            for video_info in video_infos:
                model_name = video_info.get('image_model', None)
                instruction = video_info.get('instruction', None)
                target_caption = video_info.get('target_caption', None)

                if instruction is None and target_caption is None:
                    continue

                if model_name == 'magicbrush':
                    model = image_edit.MagicBrush()
                    prompt_type = "instruct"
                    prompt = instruction
                elif model_name == 'instructpix2pix':
                    model = image_edit.InstructPix2Pix()
                    prompt_type = "instruct"
                    prompt = instruction
                elif model_name == 'cosxl':
                    model = image_edit.CosXLEdit()
                    prompt_type = "instruct"
                    prompt = instruction
                else:
                    prompt_type = "target"
                    prompt = target_caption


                if args.output_dir is None:
                    video_filename = os.path.basename(video_path)
                    filename_noext = os.path.splitext(video_filename)[0]
                    output_dir = os.path.dirname(video_path)
                else:
                    output_dir = args.output_dir

                infer_video(model, video_path, output_dir, prompt, prompt_type, args.force_512, args.seed, negative_prompt)
    else:
        if args.model == 'magicbrush':
            model = image_edit.MagicBrush()
            prompt_type = "instruct"
        elif args.model == 'instructpix2pix':
            model = image_edit.InstructPix2Pix()
            prompt_type = "instruct"
        elif args.model == 'cosxl':
            model = image_edit.CosXLEdit()
            prompt_type = "instruct"

        video_path = args.video_path
        
        video_filename = os.path.basename(video_path)
        filename_noext = os.path.splitext(video_filename)[0]
        if args.output_dir is None:
            output_dir = os.path.dirname(video_path)
        else:
            output_dir = args.output_dir
        
        print("video_filename", video_filename)
        print("output_dir", output_dir)

        infer_video(model, video_path, output_dir, args.prompt, prompt_type, args.force_512, args.seed, negative_prompt)


if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Process some images.')
        parser.add_argument('--model', type=str, default='instructpix2pix', choices=['magicbrush','instructpix2pix', 'cosxl'], help='Name of the image editing model')
        parser.add_argument('--video_path', type=str, required=False, help='Name of the video', default=None)
        parser.add_argument('--input_dir', type=str, required=False, help='Directory containing the video', default="./demo/")
        parser.add_argument('--output_dir', type=str, required=False, help='Directory to save the processed images', default=None)
        parser.add_argument('--prompt', type=str, required=False, help='Instruction prompt for editing', default="turn the man into darth vader")
        parser.add_argument('--force_512', action='store_true', help='Force resize to 512x512 when feeding into image model')
        parser.add_argument('--dict_file', type=str, required=False, help='JSON file containing files, instructions etc.', default=None)
        parser.add_argument('--seed', type=int, required=False, help='Seed for random number generator', default=42)
        parser.add_argument('--negative_prompt', type=str, required=False, help='Negative prompt for editing', default=None)
        parser.add_argument(
            "--configs_json", type=str, default=None, help="./configs/group_edited_first_frame/group_config.json"
        )  # This is going to override the template_config
        args = parser.parse_args()

        if args.configs_json is None:
            main(args)
        else:
            # Load data jsonl into list
            configs_json = args.configs_json
            assert Path(configs_json).exists(), f'{configs_json}'
            with open(configs_json, "r") as file:
                configs_list = json.load(file)
            print(f"Loaded {len(configs_list)} configs from {configs_json}")

            for config_entry in configs_list:
                print(f'Processing {config_entry["video_path"]}')
                
                args.video_path = config_entry["video_path"]
                args.input_dir = config_entry["input_dir"]
                args.output_dir = config_entry["output_dir"] 
                args.prompt = config_entry["prompt"]

                main(args)

        print("Done!")
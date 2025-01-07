import os
import random
import gradio as gr
import cv2
from scripts.gradio.i2v_test_application import Image2Video

# Load the model once and reuse it
image2video = Image2Video('./tmp/', resolution='320_512')  # Initialize with appropriate parameters

def generate_multiple(image1, prompt, steps, cfg_scale, eta, motion, seed, image2, loop_count):
    video_paths = []

    for i in range(int(loop_count)):
        random_seed = random.randint(0, 50000)
        print(f"Generating video {i+1}/{loop_count} with seed {random_seed}")

        img1 = cv2.imread(image1) if isinstance(image1, str) else image1
        img2 = cv2.imread(image2) if isinstance(image2, str) else image2

        if img1 is None or img2 is None:
            print("Error: Could not load one or both images.")
            continue

        # Use the pre-loaded model to generate video
        output_path = image2video.get_image(img1, prompt, steps, cfg_scale, eta, motion, random_seed, img2)

        if os.path.exists(output_path):
            # Ensure the video is in .mp4 format
            if not output_path.endswith('.mp4'):
                new_output_path = output_path + '.mp4'
                os.rename(output_path, new_output_path)
                output_path = new_output_path

            video_paths.append(output_path)  # Collect video paths
            print(f"Video generated at: {output_path}")

            # Debugging: Check file type and path
            try:
                import magic  # Python-magic library, ensure it's installed
                mime_type = magic.from_file(output_path, mime=True)
                print(f"MIME type of the video: {mime_type}")
                if 'video' not in mime_type:
                    print(f"Warning: The file at {output_path} is not recognized as a video.")
            except ImportError:
                print("Warning: python-magic is not installed. Cannot check MIME type.")
        else:
            print(f"Error: Video file not found at {output_path}")

    print(f"Generated video paths: {video_paths}")
    return video_paths

def dynamicrafter_demo(result_dir='./tmp/', res=512):
    css = "#input_img {max-width: 512px !important} #output_vid {max-width: 512px; max-height: 320px}"

    with gr.Blocks(analytics_enabled=False, css=css) as dynamicrafter_iface:
        with gr.Tab(label='ToonCrafter_320x512'):
            with gr.Row():
                with gr.Column(scale=1):
                    i2v_input_image = gr.Image(label="Input Image1", elem_id="input_img")
                    i2v_input_text = gr.Textbox(label='Prompts')
                    i2v_seed = gr.Slider(label='Random Seed', minimum=0, maximum=50000, step=1, value=123)
                    i2v_eta = gr.Slider(minimum=0.0, maximum=1.0, step=0.1, label='ETA', value=1.0, elem_id="i2v_eta")
                    i2v_cfg_scale = gr.Slider(minimum=1.0, maximum=15.0, step=0.5, label='CFG Scale', value=7.5, elem_id="i2v_cfg_scale")
                    i2v_steps = gr.Slider(minimum=1, maximum=60, step=1, elem_id="i2v_steps", label="Sampling steps", value=50)
                    i2v_motion = gr.Slider(minimum=5, maximum=30, step=1, elem_id="i2v_motion", label="FPS", value=10)
                    i2v_loop_count = gr.Number(label="Number of Generations", value=1, precision=0)
                    i2v_generate_btn = gr.Button("Generate")
                with gr.Column(scale=1):
                    i2v_input_image2 = gr.Image(label="Input Image2", elem_id="input_img2")
                    video_gallery = gr.Gallery(label="Generated Videos", elem_id="output_gallery", type="video")

            i2v_generate_btn.click(fn=generate_multiple,
                                   inputs=[i2v_input_image, i2v_input_text, i2v_steps, i2v_cfg_scale, i2v_eta, i2v_motion, i2v_seed, i2v_input_image2, i2v_loop_count],
                                   outputs=video_gallery)

    return dynamicrafter_iface

if __name__ == "__main__":
    result_dir = os.path.join('./', 'results')
    dynamicrafter_iface = dynamicrafter_demo(result_dir)
    dynamicrafter_iface.queue(max_size=12)
    dynamicrafter_iface.launch(max_threads=1, share=True)

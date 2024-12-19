import os
import argparse
import random
import gradio as gr
from scripts.gradio.i2v_test_application import Image2Video  # Ensure this file exists and is correctly implemented

# Example inputs for demonstration
i2v_examples_interp_512 = [
    ['prompts/512_interp/74906_1462_frame1.png', 'walking man', 50, 7.5, 1.0, 10, 123, 'prompts/512_interp/74906_1462_frame3.png'],
    ['prompts/512_interp/Japan_v2_2_062266_s2_frame1.png', 'an anime scene', 50, 7.5, 1.0, 10, 789, 'prompts/512_interp/Japan_v2_2_062266_s2_frame3.png'],
    ['prompts/512_interp/Japan_v2_3_119235_s2_frame1.png', 'an anime scene', 50, 7.5, 1.0, 10, 123, 'prompts/512_interp/Japan_v2_3_119235_s2_frame3.png'],
]

def dynamicrafter_demo(result_dir='./tmp/', res=512):
    # Determine resolution and CSS styling based on the resolution
    resolution_css_map = {
        1024: ('576_1024', "#input_img {max-width: 1024px !important} #output_vid {max-width: 1024px; max-height:576px}"),
        512: ('320_512', "#input_img {max-width: 512px !important} #output_vid {max-width: 512px; max-height: 320px}"),
        256: ('256_256', "#input_img {max-width: 256px !important} #output_vid {max-width: 256px; max-height: 256px}")
    }

    if res not in resolution_css_map:
        raise NotImplementedError(f"Unsupported resolution: {res}")

    resolution, css = resolution_css_map[res]
    image2video = Image2Video(result_dir, resolution=resolution)

    # Function to generate multiple videos sequentially and update the gallery
    def generate_multiple(image1, prompt, steps, cfg_scale, eta, motion, seed, image2, loop_count):
        video_paths = []
        for _ in range(int(loop_count)):
            random_seed = random.randint(0, 50000)  # Generate a random seed for each iteration
            output_path = image2video.get_image(image1, prompt, steps, cfg_scale, eta, motion, random_seed, image2)
            if os.path.exists(output_path):
                video_paths.append(output_path)
            else:
                print(f"Error: Video file not found at {output_path}")
        return video_paths

    # Gradio interface setup
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
                    i2v_loop_count = gr.Number(label="Number of Generations", value=1, precision=0)  # New input for loop count
                    i2v_generate_btn = gr.Button("Generate")
                with gr.Column(scale=1):
                    i2v_input_image2 = gr.Image(label="Input Image2", elem_id="input_img2")
                    i2v_output_gallery = gr.Gallery(label="Generated Videos", elem_id="output_gallery")

            # Example demonstrations
            gr.Examples(examples=i2v_examples_interp_512,
                        inputs=[i2v_input_image, i2v_input_text, i2v_steps, i2v_cfg_scale, i2v_eta, i2v_motion, i2v_seed, i2v_input_image2],
                        outputs=[i2v_output_gallery],
                        fn=generate_multiple,
                        cache_examples=False)

            # Button click actions
            i2v_generate_btn.click(fn=generate_multiple,
                                   inputs=[i2v_input_image, i2v_input_text, i2v_steps, i2v_cfg_scale, i2v_eta, i2v_motion, i2v_seed, i2v_input_image2, i2v_loop_count],
                                   outputs=i2v_output_gallery)

    return dynamicrafter_iface

def get_parser():
    parser = argparse.ArgumentParser()
    return parser

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    result_dir = os.path.join('./', 'results')
    dynamicrafter_iface = dynamicrafter_demo(result_dir)
    dynamicrafter_iface.queue(max_size=12)
    dynamicrafter_iface.launch(max_threads=1, share=True)

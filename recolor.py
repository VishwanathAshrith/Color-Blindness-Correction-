import argparse
import os
import numpy as np
from PIL import Image
import cv2
from utils import Transforms, Utils

class Core:

    @staticmethod 
    # how an image look for coloublindness
    def simulate(input_path: str,
                 simulate_type: str = 'protanopia',
                 simulate_degree_primary: float = 1.0,
                 simulate_degree_sec: float = 1.0,
                 return_type: str = 'save',
                 save_path: str = None):

        assert simulate_type in ['protanopia', 'deutranopia', 'tritanopia', 'hybrid'], \
            'Invalid Simulate Type: {}'.format(simulate_type)

        try:
            # Load the image and convert to LMS
            img_lms = Utils.load_lms(input_path)

            if simulate_type == 'protanopia':
                transform = Transforms.lms_protanopia_sim(degree=simulate_degree_primary)
               # Depending on the type of color blindness, fetch the corresponding transformation matrix.
            elif simulate_type == 'deutranopia':
                transform = Transforms.lms_deutranopia_sim(degree=simulate_degree_primary)
            elif simulate_type == 'tritanopia':
                transform = Transforms.lms_tritanopia_sim(degree=simulate_degree_primary)
            else:
                transform = Transforms.hybrid_protanomaly_deuteranomaly_sim(
                    degree_p=simulate_degree_primary,
                    degree_d=simulate_degree_sec)

            # Apply simulation transform in LMS space
            img_sim_lms = np.dot(img_lms, transform)
#LMS stands for the Long, Medium, and Short wavelength cones in the human eye:
            # Convert LMS to RGB
            img_sim_rgb = np.clip(np.dot(img_sim_lms, Transforms.lms_to_rgb()), 0, 1)

            # Optional hue tweaks (for visual consistency)
            img_rgb_255 = (img_sim_rgb * 255).astype(np.uint8)
            img_hsv = cv2.cvtColor(img_rgb_255, cv2.COLOR_RGB2HSV).astype(np.float32)
            #Converts RGB to HSV (Hue, Saturation, Value) for easier color manipulation.
            #for eazy visuallization
            if simulate_type == 'protanopia':
                img_hsv[..., 0] = (img_hsv[..., 0] + 5) % 180
            elif simulate_type == 'deutranopia':
                img_hsv[..., 0] = (img_hsv[..., 0] + 8) % 180
            elif simulate_type == 'tritanopia':
                img_hsv[..., 0] = (img_hsv[..., 0] + 12) % 180
#converting back to rgb
            img_sim_final = cv2.cvtColor(img_hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

            if return_type == 'save':
                assert save_path is not None, 'No save path provided.'
                Image.fromarray(img_sim_final).save(save_path)
                return

            if return_type == 'np':
                return img_sim_final

            if return_type == 'pil':
                return Image.fromarray(img_sim_final)

        except Exception as e:
            print(f"Error during simulation: {e}")

    @staticmethod
    def correct(input_path: str,
                protanopia_degree: float = 1.0,
                deutranopia_degree: float = 1.0,
                return_type: str = 'save',
                save_path: str = None):

        try:
            img_rgb = Utils.load_rgb(input_path)
            transform = Transforms.correction_matrix(protanopia_degree=protanopia_degree,
                                                     deutranopia_degree=deutranopia_degree)
            corrected = np.clip(np.dot(img_rgb, transform) * 255, 0, 255).astype(np.uint8)

            if return_type == 'save':
                assert save_path is not None, 'No save path provided.'
                Image.fromarray(corrected).save(save_path)
                return

            if return_type == 'np':
                return corrected

            if return_type == 'pil':
                return Image.fromarray(corrected)

        except Exception as e:
            print(f"Error during correction: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description='Simulate and Correct Images for Color-Blindness')
    parser.add_argument('-input', type=str, required=True, help='Path to input image.')
    parser.add_argument('-output', type=str, required=True, help='Path to save output images.')
    parser.add_argument('-sim_protanopia', action='store_true', default=False)
    parser.add_argument('-sim_deutranopia', action='store_true', default=False)
    parser.add_argument('-sim_tritanopia', action='store_true', default=False)
    parser.add_argument('-sim_hybrid', action='store_true', default=False)
    parser.add_argument('-correct_colors', action='store_true', default=False)
    parser.add_argument('-run_all', action='store_true', default=False)
    parser.add_argument('-protanopia_degree', type=float, default=1.0)
    parser.add_argument('-deutranopia_degree', type=float, default=1.0)
    parser.add_argument('-tritanopia_degree', type=float, default=1.0)
    return parser.parse_args()

def main():
    args = parse_args()

    input_path = args.input
    output_path = args.output
    image_name = os.path.basename(input_path)

    assert os.path.isdir(output_path), 'Output path must be a directory.'

    if args.sim_protanopia or args.run_all:
        Core.simulate(input_path=input_path,
                      simulate_type='protanopia',
                      simulate_degree_primary=args.protanopia_degree,
                      return_type='save',
                      save_path=os.path.join(output_path, f'sim_protanopia_{image_name}'))

    if args.sim_deutranopia or args.run_all:
        Core.simulate(input_path=input_path,
                      simulate_type='deutranopia',
                      simulate_degree_primary=args.deutranopia_degree,
                      return_type='save',
                      save_path=os.path.join(output_path, f'sim_deutranopia_{image_name}'))

    if args.sim_tritanopia or args.run_all:
        Core.simulate(input_path=input_path,
                      simulate_type='tritanopia',
                      simulate_degree_primary=args.tritanopia_degree,
                      return_type='save',
                      save_path=os.path.join(output_path, f'sim_tritanopia_{image_name}'))

    if args.sim_hybrid or args.run_all:
        Core.simulate(input_path=input_path,
                      simulate_type='hybrid',
                      simulate_degree_primary=args.protanopia_degree,
                      simulate_degree_sec=args.deutranopia_degree,
                      return_type='save',
                      save_path=os.path.join(output_path, f'sim_hybrid_{image_name}'))

    if args.correct_colors or args.run_all:
        Core.correct(input_path=input_path,
                     protanopia_degree=args.protanopia_degree,
                     deutranopia_degree=args.deutranopia_degree,
                     return_type='save',
                     save_path=os.path.join(output_path, f'corrected_{image_name}'))

    print(f"All processing done. Check outputs in {output_path}")

if __name__ == '__main__':
    main()

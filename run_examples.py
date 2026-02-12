import sys
import os
from recolor import Core


def main():
    if len(sys.argv) < 4:
        print("Usage: python run_examples.py <input_path> <output_folder> <blindness_type>")
        return

    input_path = sys.argv[1]
    output_folder = sys.argv[2]
    blindness_type = sys.argv[3].lower()
    
    os.makedirs(output_folder, exist_ok=True)
    file_ext = os.path.splitext(input_path)[-1]

    if blindness_type == 'protanopia':
        Core.correct(input_path=input_path,
                     return_type='save',
                     save_path=os.path.join(output_folder, f'corrected_protanopia{file_ext}'),
                     protanopia_degree=0.9,
                     deutranopia_degree=0.0)
    
    elif blindness_type == 'deutranopia':
        Core.correct(input_path=input_path,
                     return_type='save',
                     save_path=os.path.join(output_folder, f'corrected_deutranopia{file_ext}'),
                     protanopia_degree=0.0,
                     deutranopia_degree=1.0)
    
    elif blindness_type == 'tritanopia':
        Core.correct(input_path=input_path,
                     return_type='save',
                     save_path=os.path.join(output_folder, f'corrected_tritanopia{file_ext}'),
                     protanopia_degree=0.0,
                     deutranopia_degree=0.0)
    
    elif blindness_type == 'hybrid':
        Core.correct(input_path=input_path,
                     return_type='save',
                     save_path=os.path.join(output_folder, f'corrected_hybrid{file_ext}'),
                     protanopia_degree=0.5,
                     deutranopia_degree=0.5)
    
    else:
        print(f"Unknown blindness type: {blindness_type}")
        return

    print(f"Successfully generated corrected_{blindness_type}{file_ext}")


if __name__ == '__main__':
    main()

import sys
import os
from recolor import Core


def main():
    if len(sys.argv) < 3:
        print("Usage: python run_examples.py <input_path> <output_folder>")
        return

    input_path = sys.argv[1]
    output_folder = sys.argv[2]
    os.makedirs(output_folder, exist_ok=True)#if output floder donot exit itv creates

    file_ext = os.path.splitext(input_path)[-1]

    # --- Simulate Color Blindness ---
    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_protanopia{file_ext}'),
                  simulate_type='protanopia',
                  simulate_degree_primary=0.9)

    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_deutranopia{file_ext}'),
                  simulate_type='deutranopia',
                  simulate_degree_primary=0.9)

    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_tritanopia{file_ext}'),
                  simulate_type='tritanopia',
                  simulate_degree_primary=0.9)

    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_hybrid{file_ext}'),
                  simulate_type='hybrid',
                  simulate_degree_primary=0.5,
                  simulate_degree_sec=0.5)

    # --- Correction: Protanopia ---
    Core.correct(input_path=input_path,
                 return_type='save',
                 save_path=os.path.join(output_folder, f'corrected_protanopia{file_ext}'),
                 protanopia_degree=0.9,
                 deutranopia_degree=0.0)

    Core.simulate(input_path=os.path.join(output_folder, f'corrected_protanopia{file_ext}'),
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_corrected_protanopia{file_ext}'),
                  simulate_type='protanopia',
                  simulate_degree_primary=0.9)

    # --- Correction: Deutranopia ---
    Core.correct(input_path=input_path,
                 return_type='save',
                 save_path=os.path.join(output_folder, f'corrected_deutranopia{file_ext}'),
                 protanopia_degree=0.0,
                 deutranopia_degree=1.0)

    Core.simulate(input_path=os.path.join(output_folder, f'corrected_deutranopia{file_ext}'),
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_corrected_deutranopia{file_ext}'),
                  simulate_type='deutranopia',
                  simulate_degree_primary=0.9)

    # --- Correction: Hybrid (Protanopia + Deutranopia) ---
    Core.correct(input_path=input_path,
                 return_type='save',
                 save_path=os.path.join(output_folder, f'corrected_hybrid{file_ext}'),
                 protanopia_degree=0.5,
                 deutranopia_degree=0.5)

    Core.simulate(input_path=os.path.join(output_folder, f'corrected_hybrid{file_ext}'),
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_corrected_hybrid{file_ext}'),
                  simulate_type='hybrid',
                  simulate_degree_primary=0.5,
                  simulate_degree_sec=0.5)

    # --- Correction: Tritanopia (Placeholder) ---
    # This is a placeholder since Core.correct() does not support tritanopia correction directly.
    Core.correct(input_path=input_path,
                 return_type='save',
                 save_path=os.path.join(output_folder, f'corrected_tritanopia{file_ext}'),
                 protanopia_degree=0.0,
                 deutranopia_degree=0.0)  # Placeholder correction

    Core.simulate(input_path=os.path.join(output_folder, f'corrected_tritanopia{file_ext}'),
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_corrected_tritanopia{file_ext}'),
                  simulate_type='tritanopia',
                  simulate_degree_primary=0.9)


if __name__ == '__main__':
    main()

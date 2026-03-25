import sys
import os
from recolor import Core


def run_protanopia(input_path, output_folder, file_ext):
    """Simulate + correct for Protanopia."""
    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_protanopia{file_ext}'),
                  simulate_type='protanopia',
                  simulate_degree_primary=0.9)

    Core.correct(input_path=input_path,
                 correction_type='protanopia',
                 return_type='save',
                 save_path=os.path.join(output_folder, f'corrected_protanopia{file_ext}'),
                 protanopia_degree=0.9,
                 deutranopia_degree=0.0)

    Core.simulate(input_path=os.path.join(output_folder, f'corrected_protanopia{file_ext}'),
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_corrected_protanopia{file_ext}'),
                  simulate_type='protanopia',
                  simulate_degree_primary=0.9)


def run_deutranopia(input_path, output_folder, file_ext):
    """Simulate + correct for Deutranopia."""
    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_deutranopia{file_ext}'),
                  simulate_type='deutranopia',
                  simulate_degree_primary=0.9)

    Core.correct(input_path=input_path,
                 correction_type='deutranopia',
                 return_type='save',
                 save_path=os.path.join(output_folder, f'corrected_deutranopia{file_ext}'),
                 protanopia_degree=0.0,
                 deutranopia_degree=1.0)

    Core.simulate(input_path=os.path.join(output_folder, f'corrected_deutranopia{file_ext}'),
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_corrected_deutranopia{file_ext}'),
                  simulate_type='deutranopia',
                  simulate_degree_primary=0.9)


def run_tritanopia(input_path, output_folder, file_ext):
    """
    Simulate + correct for Tritanopia.

    Correction uses the dedicated tritanopia_correction_matrix which redistributes
    the blue channel into red, shifting blues toward purple/violet so that
    individuals with tritanopia (who rely on intact red/green cones) can better
    distinguish blue-yellow colour pairs.
    """
    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_tritanopia{file_ext}'),
                  simulate_type='tritanopia',
                  simulate_degree_primary=0.9)

    # BUG FIX: was passing protanopia_degree=0.0, deutranopia_degree=0.0 which
    # produced an identity transform (corrected image == original). Now uses the
    # real tritanopia correction matrix via correction_type='tritanopia'.
    Core.correct(input_path=input_path,
                 correction_type='tritanopia',
                 degree=0.9,
                 return_type='save',
                 save_path=os.path.join(output_folder, f'corrected_tritanopia{file_ext}'))

    Core.simulate(input_path=os.path.join(output_folder, f'corrected_tritanopia{file_ext}'),
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_corrected_tritanopia{file_ext}'),
                  simulate_type='tritanopia',
                  simulate_degree_primary=0.9)


def run_hybrid(input_path, output_folder, file_ext):
    """Simulate + correct for Hybrid (Protanopia + Deutranopia)."""
    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, f'simulate_hybrid{file_ext}'),
                  simulate_type='hybrid',
                  simulate_degree_primary=0.5,
                  simulate_degree_sec=0.5)

    Core.correct(input_path=input_path,
                 correction_type='hybrid',
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


def main():
    if len(sys.argv) < 3:
        print("Usage: python run_examples.py <input_path> <output_folder> [blindness_type]")
        return

    input_path = sys.argv[1]
    output_folder = sys.argv[2]

    # BUG FIX: app.py passes blindness_type as sys.argv[3] but the old code
    # never read it — so all 4 types were always processed regardless of what
    # the user selected. Now we read it and only run the relevant pipeline,
    # making processing ~4x faster.
    blindness_type = sys.argv[3] if len(sys.argv) > 3 else 'protanopia'

    os.makedirs(output_folder, exist_ok=True)

    file_ext = os.path.splitext(input_path)[-1]

    dispatch = {
        'protanopia':  run_protanopia,
        'deutranopia': run_deutranopia,
        'tritanopia':  run_tritanopia,
        'hybrid':      run_hybrid,
    }

    if blindness_type not in dispatch:
        print(f"Unknown blindness type '{blindness_type}'. "
              f"Choose from: {', '.join(dispatch.keys())}")
        return

    dispatch[blindness_type](input_path, output_folder, file_ext)

    print(f"Processing complete for type='{blindness_type}'. "
          f"Outputs saved in: {output_folder}")


if __name__ == '__main__':
    main()
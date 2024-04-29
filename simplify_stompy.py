import os
from class_mesh_simplify import mesh_simplify

SIMPLIFICATION_RATIO: float = 0.5
THRESHOLD: float = 0
INPUT_STOMPY_FILEPATH: str = "./stompy"
OUTPUT_STOMPY_FILEPATH: str = "./stompy_simplified"
os.makedirs(OUTPUT_STOMPY_FILEPATH, exist_ok=True)
# Copy the .urdf file to the output directory
os.system(f"cp {INPUT_STOMPY_FILEPATH}/*.urdf {OUTPUT_STOMPY_FILEPATH}")
output_path = os.path.join(OUTPUT_STOMPY_FILEPATH, "meshes")
os.makedirs(output_path, exist_ok=True)
input_path = os.path.join(INPUT_STOMPY_FILEPATH, "meshes")
for filename in os.listdir(input_path):
    if filename.endswith(".obj"):
        input_filepath = os.path.join(input_path, filename)
        output_filepath = os.path.join(output_path, filename)
        original_size = os.path.getsize(input_filepath)
        try:
            model = mesh_simplify(input_filepath, THRESHOLD, SIMPLIFICATION_RATIO)
            model.generate_valid_pairs()
            model.calculate_optimal_contraction_pairs_and_cost()
            model.iteratively_remove_least_cost_valid_pairs()
            model.generate_new_3d_model()
            model.output(output_filepath)
        except Exception as e:
            print(f"Error simplifying {filename}: {e}")
            continue
        simplified_size = os.path.getsize(output_filepath)
        size_reduction = original_size - simplified_size
        reduction_percentage = (size_reduction / original_size) * 100
        print(f"File: {filename}")
        print(f"Original Size: {original_size} bytes")
        print(f"Simplified Size: {simplified_size} bytes")
        print(f"Reduction: {size_reduction} bytes ({reduction_percentage:.2f}%)")

print("Mesh simplification complete.")
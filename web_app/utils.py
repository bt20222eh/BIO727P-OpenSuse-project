import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os 

def save_matrix_to_csv(matrix, populations, filename='fst_matrix.csv'):
    """
    Save the FST matrix to a CSV file.
    """
    # Convert the FST matrix to a Pandas DataFrame
    df = pd.DataFrame(matrix, index=populations, columns=populations)
    
    # Get the path to the static directory
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    
    # Save the CSV file in the static directory
    csv_path = os.path.join(static_dir, filename)
    df.to_csv(csv_path)
    
    print(f"Matrix saved to {csv_path}")

def generate_heatmap(matrix, populations, filename='fst_heatmap.png'):
    """
    Generate a heatmap from the FST matrix and save it as an image.
    """
    # Convert the FST matrix to a Pandas DataFrame
    df = pd.DataFrame(matrix, index=populations, columns=populations)

    # Get the path to the static directory
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    
    # Save the heatmap image in the static directory
    heatmap_path = os.path.join(static_dir, filename)
    
    # Generate the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, annot=True, cmap='viridis')
    plt.title('Pairwise Population Genetic Differentiation (F_ST)')
    plt.savefig(heatmap_path)
    plt.close()
    
    print(f"Heatmap saved to {heatmap_path}")

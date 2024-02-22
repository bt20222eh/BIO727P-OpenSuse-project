import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os 
import time

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

def generate_heatmap(matrix, populations, filename=None):
    """
    Generate a heatmap from the FST matrix and save it as an image with a unique filename.
    """
    # Generate a timestamped filename if none is provided
    if filename is None:
        timestamp = int(time.time())
        filename = f'fst_heatmap_{timestamp}.png'
    
    # Define the path to the static directory (adjust as necessary)
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    heatmap_path = os.path.join(static_dir, filename)
    
    # Generate the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=False, cmap='viridis', xticklabels=populations, yticklabels=populations)
    plt.title('Pairwise Population Genetic Differentiation (F_ST)')
    plt.tight_layout()  # Adjust layout to fit the labels
    plt.savefig(heatmap_path)
    plt.close()
    
    print(f"Heatmap saved to {heatmap_path}")
    return heatmap_path  # Return the full path for further use

import os
import matplotlib.pyplot as plt
import pandas as pd

def save_assignments(assignments, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df = pd.DataFrame([{'Seeker_ID': i, 'Job_ID': j} for (i, j), val in assignments.items() if val > 0.5])
    df.to_csv(filename, index=False)

def plot_tradeoff(omega_values, dissimilarities, save_path=None):
    plt.plot(omega_values, dissimilarities, marker='o')
    plt.xlabel("ω (% of max priority weight)")
    plt.ylabel("Max Dissimilarity")
    plt.title("ω vs Max Dissimilarity Trade-off")
    plt.grid(True)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # <-- Add this line
        plt.savefig(save_path)
    
    plt.close()

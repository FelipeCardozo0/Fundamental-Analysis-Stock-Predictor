import pandas as pd
import matplotlib.pyplot as plt

# Load Piotroski Scores


def load_scores(file_path):
    return pd.read_csv(file_path)

# Plot score distribution


def plot_score_distribution(scores):
    plt.figure(figsize=(10, 6))
    scores['Piotroski Score'].hist(bins=10, edgecolor='black')
    plt.title('Distribution of Piotroski Scores', fontsize=16)
    plt.xlabel('Piotroski Score', fontsize=14)
    plt.ylabel('Number of Companies', fontsize=14)
    plt.grid(axis='y', alpha=0.75)
    plt.show()

# Display top and bottom companies


def display_extremes(scores, top_n=10):
    print("\nTop Companies by Piotroski Score:")
    print(scores.sort_values(by='Piotroski Score', ascending=False).head(top_n))

    print("\nBottom Companies by Piotroski Score:")
    print(scores.sort_values(by='Piotroski Score', ascending=True).head(top_n))

# Main function


def main():
    scores = load_scores('piotroski_scores.csv')
    plot_score_distribution(scores)
    display_extremes(scores)


# Run the script
if __name__ == "__main__":
    main()

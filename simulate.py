import numpy as np
import matplotlib.pyplot as plt

def simulate(initial, annual_return, volatility, years, n_sims=5000, seed=42):
    """Simulate many possible yearly growth paths for an investment."""
    rng = np.random.default_rng(seed)
    yearly_returns = rng.normal(annual_return, volatility, size=(n_sims, years))
    yearly_returns = np.maximum(yearly_returns, -1)
    growth = np.cumprod(1 + yearly_returns, axis=1)
    start = np.ones((n_sims, 1))
    return initial * np.hstack([start, growth])

def summarise(paths, initial):
    final = paths[:, -1]
    print(f"Simulations run: {len(final):,}")
    print(f"Worst 10% end below: GH₵{np.percentile(final, 10):,.0f}")
    print(f"Median outcome:      GH₵{np.percentile(final, 50):,.0f}")
    print(f"Best 10% end above:  GH₵{np.percentile(final, 90):,.0f}")
    print(f"Chance of losing money: {(final < initial).mean():.1%}")

def plot_paths(paths, initial):
    years = paths.shape[1] - 1
    plt.figure(figsize=(9, 5))
    for path in paths[:100]:
        plt.plot(path, color="steelblue", alpha=0.15)
    plt.plot(np.median(paths, axis=0), color="red", linewidth=2, label="Median")
    plt.axhline(initial, color="black", linestyle="--", label="Starting amount")
    plt.title(f"Monte Carlo simulation: GH₵{initial:,.0f} over {years} years")
    plt.xlabel("Years")
    plt.ylabel("Portfolio value (GH₵)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("monte_carlo.png", dpi=150, bbox_inches="tight")
    plt.show()

def ask_number(prompt, allow_negative=False):
    """Keep asking until the user types a valid number."""
    while True:
        try:
            value = float(input(prompt))
            if value > 0 or (allow_negative and value != 0):
                return value
            print("Please enter a number greater than 0.")
        except ValueError:
            print("That's not a number. Try again.")

def main():
    print("=== Monte Carlo Portfolio Simulator ===")
    initial = ask_number("Amount to invest (GH₵): ")
    annual_return = ask_number("Expected yearly return (%): ", allow_negative=True) / 100
    volatility = ask_number("Yearly volatility / risk (%): ") / 100
    years = int(ask_number("Years to invest: "))
    print()
    paths = simulate(initial, annual_return, volatility, years)
    summarise(paths, initial)
    plot_paths(paths, initial)

if __name__ == "__main__":
    main()
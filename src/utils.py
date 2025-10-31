import matplotlib.pyplot as plt

def convert_zscore(df, sym1, sym2, window_size=10):
    df['Spread_MA'] = df['Spread'].rolling(window_size).mean()
    df['Spread_std'] = df['Spread'].rolling(window_size).std()
    df['Zscore'] = (df['Spread'] - df['Spread_MA']) / df['Spread_std']

    df['Upper_Bound'] = df['Spread_MA'] + df['Spread_std']
    df['Lower_Bound'] = df['Spread_MA'] - df['Spread_std']

    plt.figure(figsize=(16, 8))
    plt.plot(df.index, df["Spread"], label="Spread", color="blue")
    plt.plot(df.index, df["Spread_MA"], label="Rolling Mean", color="black", linestyle="--")
    plt.plot(df.index, df["Upper_Bound"], label="+1 Std Dev", color="green", linestyle="--")
    plt.plot(df.index, df["Lower_Bound"], label="-1 Std Dev", color="red", linestyle="--")
    plt.title(f"Spread with ±1 Std Bounds (Window={window_size}): {sym1}, {sym2}")
    plt.legend()
    plt.show()

    plt.figure(figsize=(16, 8))
    plt.plot(df.index, df["Zscore"], label="Z-Score of Spread", color="purple")
    plt.axhline(0, color="black", linestyle="--", lw=1)
    plt.axhline(2.0, color="green", linestyle="--", lw=1, label="+2 Z")
    plt.axhline(1.0, color="green", linestyle="--", lw=1, label="+1 Z")
    plt.axhline(-1.0, color="red", linestyle="--", lw=1, label="-1 Z")
    plt.axhline(-2.0, color="red", linestyle="--", lw=1, label="-2 Z")
    plt.title(f"Z-Score of Spread (Window={window_size}): {sym1}, {sym2}")
    plt.legend()
    plt.show()

    return df

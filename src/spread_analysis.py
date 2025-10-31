import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd

def analyze_pair(data_dict, sym1, sym2):
    priceX = data_dict[sym1]['Close'].rename('X')
    priceY = data_dict[sym2]['Close'].rename('Y')
    df = pd.concat([priceX, priceY], axis=1, join='inner').dropna()

    X = sm.add_constant(df['X'])
    Y = df['Y']
    model = sm.OLS(Y, X).fit()

    df['Y_pred'] = model.predict(X)
    df['Spread'] = df['Y'] - df['Y_pred']

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["Y"], label=f"{sym2} (Actual)")
    plt.plot(df.index, df["Y_pred"], label=f"{sym2} (Predicted from {sym1})")
    plt.title(f"Pair: {sym1} (X) → {sym2} (Y)")
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df["Spread"], label="Spread (Y - Y_pred)")
    plt.axhline(df["Spread"].mean(), color='red', linestyle='--', label="Spread Mean")
    plt.title(f"Spread for {sym1} & {sym2}")
    plt.legend()
    plt.show()

    results_dict = {
        "model_params": model.params,
        "df": df,
        "summary": model.summary()
    }

    return results_dict
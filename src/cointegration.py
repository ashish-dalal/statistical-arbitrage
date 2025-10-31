import pandas as pd
from itertools import combinations
from statsmodels.tsa.stattools import coint

def generate_pairs(stocks):
    return list(combinations(stocks, 2))

def test_cointegration(data_dict, stock_pairs):
    results = []
    for pair in stock_pairs:
        sym1, sym2 = pair
        df1 = data_dict[sym1]['Close']
        df2 = data_dict[sym2]['Close']

        combined = pd.concat([df1, df2], axis=1, join='inner').dropna()
        combined.columns = ["Price1", "Price2"]

        coint_t, p_value, critical_values = coint(combined["Price1"], combined["Price2"])
        is_significant = (p_value < 0.05)
        results.append({
            "Symbol1": sym1,
            "Symbol2": sym2,
            "Test Statistic": coint_t,
            "p-value": p_value,
            "5% Critical Value": critical_values[1],
            "Is_Cointegrated_5pct": is_significant
        })

        for res in results:
            status = "Coinegrated" if res["Is_Cointegrated_5pct"] else "Not Cointegrated"
            print(
                f"{res['Symbol1']} & {res['Symbol2']} | "
                f"Test Statistic: {res['Test Statistic']:.3f} | "
                f"p-value: {res['p-value']:.3f} | "
                f"5% Crit. Value: {res['5% Critical Value']:.3f} | "
                f"Result: {status}"
            )

    results_df = pd.DataFrame(results)
    filtered_df = results_df[results_df['Is_Cointegrated_5pct'] == True]
    return filtered_df

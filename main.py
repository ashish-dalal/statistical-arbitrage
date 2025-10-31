from src.data_loader import fetch_data
from src.cointegration import generate_pairs, test_cointegration
from src.spread_analysis import analyze_pair
from src.utils import convert_zscore
from src.backtest import run_pair_trading

# Universe
stocks = [
    "DIS", "NFLX", "CMCSA", "FOX", "FOXA", "WBD", "ROKU", "SPOT", "LYV"
]

def main():
    # Pipeline
    data_dict = fetch_data(stocks)
    stock_pairs = generate_pairs(stocks)
    filtered_df = test_cointegration(data_dict, stock_pairs)

    cointegrated_pairs = [(row['Symbol1'], row['Symbol2']) for _, row in filtered_df.iterrows()]
    print("Cointegrated pairs @5%:")
    for cp in cointegrated_pairs:
        print(cp)

    sym1, sym2 = "FOX", "LYV"
    pair_results = analyze_pair(data_dict, sym1, sym2)
    df_zscore = convert_zscore(pair_results['df'], sym1, sym2, window_size=21)
    pair_trading = run_pair_trading(sym1, sym2, data_dict, df_zscore)

    for key, value in pair_trading['metrics'].items():
        print(f"{key} : {value}")


if __name__ == '__main__':
    main()
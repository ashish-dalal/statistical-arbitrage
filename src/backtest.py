import pandas as pd
import numpy as np

def run_pair_trading(sym1, sym2, data_dict, df_zscore, window_size=10, initial_equity=100_000.0):
    df1 = data_dict[sym1]["Close"].rename("X")
    df2 = data_dict[sym2]["Close"].rename("Y")
    df = pd.concat([df1, df2], axis=1, join="inner").dropna().sort_index()

    assert len(df) >= window_size, f"Not enough data for {sym1}-{sym2}"
    df = df.join(df_zscore, how="inner", rsuffix="_zscore")
    assert "Zscore" in df and not df["Zscore"].isna().all(), f"Missing or invalid Zscore data for {sym1}-{sym2}"

    df["x_position"] = np.nan
    df["y_position"] = np.nan

    df.loc[df["Zscore"] > 2, ["x_position", "y_position"]] = [-1, 1]
    df.loc[(df["Zscore"] > -1) & (df["Zscore"] < 1), ["x_position", "y_position"]] = [0, 0]
    df.loc[df["Zscore"] < -2, ["x_position", "y_position"]] = [1, -1]

    df["x_position"] = df["x_position"].ffill().fillna(0)
    df["y_position"] = df["y_position"].ffill().fillna(0)

    df["x_return"] = df["X"].pct_change().fillna(0.0)
    df["y_return"] = df["Y"].pct_change().fillna(0.0)

    df["x_notional"] = 0.02 * initial_equity
    df["y_notional"] = 0.02 * initial_equity

    df["daily_pnl_x"] = df["x_position"].shift(1) * df["x_notional"] * df["x_return"]
    df["daily_pnl_y"] = df["y_position"].shift(1) * df["y_notional"] * df["y_return"]
    df[["daily_pnl_x", "daily_pnl_y"]] = df[["daily_pnl_x", "daily_pnl_y"]].fillna(0.0)

    df["daily_pnl"] = df["daily_pnl_x"] + df["daily_pnl_y"]
    df["equity"] = initial_equity + df["daily_pnl"].cumsum()

    final_equity = df["equity"].iloc[-1]
    total_return_pct = (final_equity - initial_equity) / initial_equity

    df["equity_return"] = df["equity"].pct_change().fillna(0.0)
    ann_factor = 252
    mean_daily_ret = df["equity_return"].mean()
    std_daily_ret = df["equity_return"].std()
    sharpe_ratio = (mean_daily_ret / std_daily_ret) * np.sqrt(ann_factor) if std_daily_ret != 0 else np.nan

    neg_returns = df.loc[df["equity_return"] < 0, "equity_return"]
    std_downside = neg_returns.std() if not neg_returns.empty else np.nan
    sortino_ratio = (mean_daily_ret / std_downside) * np.sqrt(ann_factor) if std_downside and std_downside != 0 else np.nan

    df["running_max"] = df["equity"].cummax()
    df["drawdown"] = (df["equity"] / df["running_max"]) - 1
    max_drawdown = df["drawdown"].min()

    df["trade_signal"] = (df["x_position"].diff().abs() > 0) | (df["y_position"].diff().abs() > 0)
    trades = df[df["trade_signal"]].copy()
    trades["entry_date"] = trades.index
    trades["exit_date"] = trades["entry_date"].shift(-1)
    trades["pnl"] = trades["daily_pnl"]
    trades_df = trades[["entry_date", "exit_date", "x_position", "y_position", "pnl"]]
    num_trades = len(trades_df)
    win_rate = (trades_df[trades_df["pnl"] > 0].shape[0] / num_trades) if num_trades > 0 else np.nan

    metrics = {
        "sym1": sym1,
        "sym2": sym2,
        "final_equity": final_equity,
        "total_return_pct": total_return_pct,
        "sharpe_ratio": sharpe_ratio,
        "sortino_ratio": sortino_ratio,
        "max_drawdown_pct": max_drawdown,
        "num_trades": num_trades,
        "win_rate_pct": 100.0 * win_rate if not np.isnan(win_rate) else np.nan
    }

    return {"df": df, "metrics": metrics, "trades_df": trades_df}
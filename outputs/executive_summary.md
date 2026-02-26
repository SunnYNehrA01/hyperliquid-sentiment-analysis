# Executive Summary (1-page)

## Method
- Built an account-day panel by aligning Hyperliquid trades with Bitcoin sentiment regime labels (Fear/Greed).
- Engineered performance, behavior, and risk features: daily PnL, win flag, trade count, leverage proxy, long/short ratio, drawdown proxy, and volatility.
- Compared Fear vs Greed using Mann–Whitney U tests and segmented results by leverage/frequency/consistency.

## Key Evidence
- Daily PnL differs by regime (p-value: 0.0134).
- Leverage usage shifts by regime (p-value: 0.0018).
- Trade frequency shifts by regime (p-value: 0.0001).
- Merge alignment quality: 75.49%, unmatched trading days: 1.

## Actionable Rules
1. Reduce leverage ceilings for high-leverage traders during Fear windows.
2. Scale activity upward in Greed only for consistent + frequent segments.
3. Use long/short ratio and trade frequency as primary behavior monitors for daily risk gating.

## Limitations
- The aligned trade window is short; treat results as directional and revalidate on longer horizon.
- Leverage is a proxy estimate due to source-field constraints.

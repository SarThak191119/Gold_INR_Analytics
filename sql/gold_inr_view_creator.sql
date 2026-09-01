use GOLDTrackerDB
go

CREATE VIEW gold_inr_derived AS
SELECT
    g.date,
    g.close_price AS gold_usd_oz,
    u.close_price AS usdinr_rate,
    d.duty_pct,
    (g.close_price * u.close_price / 3.11035) AS gold_inr_per_10g_global,
    (g.close_price * u.close_price / 3.11035) * (1 + d.duty_pct / 100.0) AS gold_inr_per_10g_landed
FROM gold_prices g
JOIN usdinr_rate u ON g.date = u.date
CROSS APPLY (
    SELECT TOP 1 duty_pct
    FROM import_duty
    WHERE effective_date <= g.date
    ORDER BY effective_date DESC
) d;

SELECT TOP 10 * FROM gold_inr_derived ORDER BY date DESC;

SELECT date, duty_pct FROM gold_inr_derived
WHERE date BETWEEN '2022-06-25' AND '2022-07-05'
ORDER BY date;
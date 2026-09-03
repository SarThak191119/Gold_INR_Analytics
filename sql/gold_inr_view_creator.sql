CREATE VIEW gold_inr_derived AS
SELECT
    g.date,
    g.close_price AS gold_usd_oz,  
    u.close_price AS usdinr_rate,
    d.duty_pct, 
    (g.close_price * u.close_price / 3.11035) AS gold_inr_per_10g_global,
    CASE WHEN year(g.date) >2011 then (g.close_price * u.close_price / 3.11035) * (1 + d.duty_pct / 100.0) 
    else (g.close_price * u.close_price / 3.11035)+300
    END  AS gold_inr_per_10g_landed
FROM gold_prices g
JOIN usdinr_rate u ON g.date = u.date
CROSS APPLY (
    SELECT TOP 1 duty_pct
    FROM import_duty
    WHERE effective_date <= g.date
    ORDER BY effective_date DESC
) d;


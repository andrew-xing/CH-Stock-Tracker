# CH Stock Tracker v2

Crowdsourced Chrome Hearts global inventory tracker with ML-ready data schema.

## Setup

### 1. Supabase
- SQL Editor → run `migration.sql`
- Settings → API → copy **anon/public key**
- In `index.html`, replace `YOUR_SUPABASE_ANON_KEY_HERE`

### 2. Deploy
```bash
vercel --prod
```
Or connect GitHub repo to Vercel.

## Data Schema (ML-Ready)

Each report captures per-material nested data:

```
store_name: "Tokyo — Ginza"
silver_925_level: "GOOD"
silver_925_categories: ["pendant", "ring"]
gold_22k_level: "LOW"  
gold_22k_categories: ["chain"]
gold_18k_wg_level: "OOS"
gold_18k_wg_categories: []
```

Auto-generated columns for ML:
- `day_of_week` (0-6, extracted from report_date)
- `report_hour` (0-23, extracted from report_time)

### `latest_per_store` view
Returns the most recent report per store — useful for dashboard.

## ML Roadmap

With enough data, we can train models for:

1. **Restock prediction** — Given (store, material, day_of_week), predict P(restock).
   Features: day_of_week, report_hour, last_seen_level, days_since_OOS
   
2. **Category availability** — Which categories appear after a restock?
   Use the per-material category arrays to learn store-specific patterns.

3. **Temporal patterns** — Cluster stores by restock cadence.
   Some stores may restock weekly (e.g. Tokyo stores), others monthly.

4. **NLP on comments** — Extract specific item mentions, sizes, collabs.
   Build a structured product catalog from free-text notes.

Minimum viable dataset: ~200 reports across 10+ stores over 4+ weeks.

## Stack
- Pure HTML/CSS/JS (zero build)
- Cloister Black font (CH logo font)
- Supabase (Postgres + RLS + REST)
- Vercel (static hosting)

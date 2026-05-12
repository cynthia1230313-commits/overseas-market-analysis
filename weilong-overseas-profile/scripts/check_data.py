import pandas as pd
df = pd.read_csv("output/user_level_data.csv")
print("Total users:", len(df))
print()
for market in ["SEA", "NA", "EU"]:
    subset = df[df["market"] == market]
    print(f"{market}: {len(subset)} users")
    for ctype in ["海外华人", "本地消费者"]:
        ss = subset[subset["consumer_type"] == ctype]
        if len(ss) > 0:
            print(f"  {ctype}: {len(ss)} users, avg spend=${ss['annual_spend_usd'].mean():.0f}, avg aov=${ss['aov_usd'].mean():.1f}")
        else:
            print(f"  {ctype}: NO DATA")
    print()

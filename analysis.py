# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
df = pd.read_csv("./cleaned_data_science_job_posts_and_salaries_2025.csv")


# %% [markdown]
# How seniority level and role affect salary
# How much do skills cost

# %%
# filter with IQR by country and normalize salary using Z score
def iqr_filter(group):
    if len(group) < 4:
        return group
    Q1 = group["salary_avg"].quantile(0.25)
    Q3 = group["salary_avg"].quantile(0.75)
    IQR = Q3 - Q1
    filtered_group = group[(group["salary_avg"] >= Q1 - 1.5 * IQR) & (group["salary_avg"] <= Q3 + 1.5 * IQR)]
    return filtered_group

def normalize_salary(group):
    group["salary_avg_normalized"] = (group["salary_avg"] - group["salary_avg"].mean()) / group["salary_avg"].std()
    return group

df_unfiltered = df.copy()
df = df.groupby("country_code").apply(iqr_filter).reset_index(drop=True)
df = df.groupby("country_code").apply(normalize_salary).reset_index(drop=True)
df_unfiltered = df_unfiltered.groupby("country_code").apply(normalize_salary).reset_index(drop=True)

# %%
# Distribution is normal around 0 with thicker tail on right
plt.hist(df["salary_avg_normalized"], bins=50, density=True)
plt.show()

# %%
# Boxplot of salary by seniority level
df_unfiltered.boxplot(column="salary_avg_normalized", by="seniority_level_num")
plt.show()

# %%
# Obviously everyone wants seniors
df_unfiltered.groupby("seniority_level").salary.count().plot.bar()
plt.show()

# %%
# most variance is comming from small companies, large companies pay probably market salary (near 0 Z-score)
df.plot.scatter(x="company_size", y="salary_avg_normalized")
plt.show()

# %%
# retail pays more, education less
df_unfiltered.groupby("industry").salary_avg_normalized.median().sort_values(ascending=False).plot(kind="bar")
plt.show()

# %%
# most common roles
# hype bubble at its finest
df_unfiltered.groupby("job_title").salary.count().sort_values(ascending=False).plot(kind="bar")
plt.show()

# %%
# remote jobs pay more
df.boxplot(column="salary_avg_normalized", by="status")
plt.show()

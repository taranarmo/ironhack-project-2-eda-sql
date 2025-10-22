# %%
import numpy as np
import pandas as pd
import subprocess

# %%
data = pd.read_csv("./data_science_job_posts_and_salaries_2025.zip")

# %%
data.salary = data.salary.str.replace(",", "").str.replace("€", "")
data.revenue = data.revenue.str.replace(",", "").str.replace("€", "")
data.company_size[data.company_size.str.contains("€")] = None
data.company_size = data.company_size.str.replace(",", "")
data.company_size = pd.to_numeric(data["company_size"], errors="coerce")

# %%
data["revenue_category"] = np.where(
    data.revenue.str.contains(r"\d+.\d+[MBT]", regex=True).fillna(False),
    np.nan,
    data.revenue,
)
data["revenue"] = np.where(
    data.revenue.str.contains(r"\d+.\d+[MBT]", regex=True).fillna(False),
    data.revenue,
    np.nan,
)
data.revenue = [float(x[:-1]) * {"M":1e6, "B":1e9, "T":1e12}.get(x[-1], 1) if type(x)==str else None for x in data.revenue]

# %%
text_columns = ["job_title", "location", "company", "industry", "ownership", "seniority_level", "status"]
for col in text_columns:
    data[col] = data[col].str.lower().str.strip()

# %%
data.post_date = pd.to_datetime([
    subprocess.run(
        ("date", "-d", f"2025-10-02 + {datestr}", "+%F"),
        capture_output=True
    ).stdout.decode("utf-8").strip() for datestr in data.post_date
])

# %%
for idx, salary_str in data.salary.items():
    if '-' in salary_str:
        low, high = salary_str.split(' - ')
        low = float(low)
        high = float(high)
        salary = (low + high) / 2
    else:
        salary = float(salary_str)
        low = salary
        high = salary
    data.at[idx, 'salary_low'] = low
    data.at[idx, 'salary_avg'] = salary
    data.at[idx, 'salary_high'] = high

# %%
data.loc[(data.location == data.status), "location"] = None

# %%
data.to_csv("./cleaned_data_science_job_posts_and_salaries_2025.csv", index=False)

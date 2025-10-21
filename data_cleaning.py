# %%
import numpy as np
import pandas as pd

# %%
data = pd.read_csv("./data_science_job_posts_and_salaries_2025.zip")

# %%
data.salary = data.salary.str.replace(",", "").str.replace("€", "")
data.revenue = data.revenue.str.replace(",", "").str.replace("€", "")
data.company_size[data.company_size.str.contains("€")] = None
data.company_size = data.company_size.str.replace(",", "")

# %%
data.revenue = np.where(
    ~(data.revenue.str.contains(r"\d+.\d+[MBT]", regex=True).fillna(False)),
    np.nan,
    data.revenue
)
# %%
data.revenue = [float(x[:-1]) * {"M":1e6, "B":1e9, "T":1e12}.get(x[-1], 1) if type(x)==str else None for x in data.revenue]


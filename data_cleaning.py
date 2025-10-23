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
data.loc[(data.location == data.status) | (data.location == "fully remote"), "location"] = None

# %%
def extract_country_from_location(location):
    if pd.isna(location) or location is None:
        return None
    
    # US states abbreviations to identify US locations
    us_states = {
        'al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga', 'hi', 'id', 
        'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms', 
        'mo', 'mt', 'ne', 'nv', 'nh', 'nj', 'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 
        'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 
        'wi', 'wy',
        "california", "texas", "florida", "new york", "illinois", "pennsylvania",
    }
    
    # Check for US state codes in the location
    for state in us_states:
        if f', {state} ' in location or f', {state}.' in location or \
           f', {state},' in location or location.endswith(f', {state}') or \
           f' {state} .' in location:
            return 'US'
    
    # Check for full country names in location
    country_patterns = {
        'united states': 'US',
        'us': 'US',
        'usa': 'US',
        'washington': 'US',
        'san francisco': 'US',
        'new york': 'US',
        'birmingham, alabama': 'US',
        'raleigh-durham-chapel': 'US',
        'los angeles': 'US',
        'canada': 'CA',
        'ontario': 'CA',
        'quebec': 'CA',
        'salt lake city': 'US',
        'chicago': 'US',
        'british columbia': 'CA',
        'alberta': 'CA',
        'manitoba': 'CA',
        'saskatchewan': 'CA',
        'nova scotia': 'CA',
        'new brunswick': 'CA',
        'toronto': 'CA',
        'prince edward island': 'CA',
        'newfoundland': 'CA',
        'labrador': 'CA',
        'vancouver': 'CA',
        'uk': 'UK',
        'united kingdom': 'UK',
        'england': 'UK',
        'scotland': 'UK',
        'wales': 'UK',
        'germany': 'DE',
        'france': 'FR',
        'italy': 'IT',
        'spain': 'ES',
        'netherlands': 'NL',
        'japan': 'JP',
        'china': 'CN',
        'india': 'IN',
        'brazil': 'BR',
        'são paulo': 'BR',
        'mexico': 'MX',
        'australia': 'AU',
        'switzerland': 'CH',
        'poland': 'PL',
        'czechia': 'CZ',
        'ukraine': 'UA',
        'estonia': 'EE',
        'lithuania': 'LT',
        'romania': 'RO',
        'belgium': 'BE',
        'austria': 'AT',
        'sweden': 'SE',
        'thailand': 'TH',
        'singapore': 'SG',
        'south africa': 'ZA',
        'norway': 'NO',
        'denmark': 'DK',
        'ireland': 'IE',
        'portugal': 'PT',
        'hungary': 'HU',
        'greece': 'GR',
        'turkey': 'TR',
        'finland': 'FI',
        'chile': 'CL',
        'colombia': 'CO',
        'peru': 'PE',
        'venezuela': 'VE',
        'ecuador': 'EC',
        'dominican republic': 'DO',
        'sri lanka': 'LK',
        'new zealand': 'NZ',
        'philippines': 'PH',
        'malaysia': 'MY',
        'indonesia': 'ID',
        'vietnam': 'VN',
        'south korea': 'KR',
        'russia': 'RU',
        'belarus': 'BY',
        'serbia': 'RS',
        'croatia': 'HR',
        'slovenia': 'SI',
        'bulgaria': 'BG',
        'israel': 'IL',
        'uae': 'AE',
        'saudi arabia': 'SA',
        'kuwait': 'KW',
        'qatar': 'QA',
        'oman': 'OM',
        'jordan': 'JO',
        'lebanon': 'LB',
        'egypt': 'EG',
        'morocco': 'MA',
        'tunisia': 'TN',
        'kenya': 'KE',
        'nigeria': 'NG',
        'ghana': 'GH',
        'ethiopia': 'ET',
        'argentina': 'AR',
        'uruguay': 'UY',
        'paraguay': 'PY',
        'bolivia': 'BO',
        'suriname': 'SR',
        'guyana': 'GY',
        'panama': 'PA',
        'costa rica': 'CR',
        'honduras': 'HN',
        'belize': 'HN',
        'nicaragua': 'NI',
        'el salvador': 'SV',
        'elsalvador': 'SV',
        'guatemala': 'GT',
        'montenegro': 'ME',
        'taipei': 'TW',
        'taiwan': 'TW',
        'bangalore': 'IN',
        'antwerp': 'BE',
        'bengalaru': 'IN',
        'puerto rico': 'PR',
        'hyderabad': 'IN',
        'bengaluru': 'IN',
        'mumbai': 'IN',
    }
    
    for country_name, country_code in country_patterns.items():
        if country_name in location:
            return country_code
    
    return None

data['country_code'] = data['location'].apply(extract_country_from_location)

# %%
data.to_csv("./cleaned_data_science_job_posts_and_salaries_2025.csv", index=False)

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
#sns.set_palette("husl")

# %% 
# Load the data
df = pd.read_csv("./cleaned_data_science_job_posts_and_salaries_2025.csv")

# %%
# Define IQR filtering and normalization functions
def iqr_filter(group):
    if len(group) < 4:
        return group
    Q1 = group["salary_avg"].quantile(0.25)
    Q3 = group["salary_avg"].quantile(0.75)
    IQR = Q3 - Q1
    filtered_group = group[(group["salary_avg"] >= Q1 - 1.5 * IQR) & (group["salary_avg"] <= Q3 + 1.5 * IQR)]
    return filtered_group

def normalize_salary(group):
    mean_val = group["salary_avg"].mean()
    std_val = group["salary_avg"].std()
    
    # Handle case where standard deviation is 0 (or very close to 0)
    if std_val == 0 or pd.isna(std_val):
        group["salary_avg_normalized"] = 0  # If std is 0, all values are the same, so normalized value is 0
    else:
        group["salary_avg_normalized"] = (group["salary_avg"] - mean_val) / std_val
    return group

# %%
# Apply IQR filtering and normalization
df_unfiltered = df.copy()
df = df.groupby("country_code").apply(iqr_filter).reset_index(drop=True)
df = df.groupby("country_code").apply(normalize_salary).reset_index(drop=True)
df_unfiltered = df_unfiltered.groupby("country_code").apply(normalize_salary).reset_index(drop=True)

# %%
# Create salary distribution before filtering
plt.figure(figsize=(12, 8))
plt.hist(df_unfiltered["salary_avg"], bins=100, density=True, alpha=0.7, color='skyblue', edgecolor='black')
plt.xlabel("Salary", fontsize=14)
plt.ylabel("Density", fontsize=14)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("./salary_dist_before.png", dpi=150, bbox_inches='tight')
plt.close()

# %%
# Create salary distribution after filtering
plt.figure(figsize=(12, 8))
plt.hist(df["salary_avg_normalized"], bins=100, density=True, alpha=0.7, color='lightgreen', edgecolor='black')
plt.xlabel("Normalized Salary (Z-Score)", fontsize=14)
plt.ylabel("Density", fontsize=14)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("./salary_dist_after.png", dpi=150, bbox_inches='tight')
plt.close()

# %%
# number of job postings by seniority level
plt.figure(figsize=(12, 6))
df_unfiltered.groupby("seniority_level").salary.count().plot.bar()
plt.ylabel("Number of Job Postings", fontsize=14)
plt.xlabel("")
plt.xticks(rotation=0, fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("./job_postings_by_seniority.png", dpi=150, bbox_inches='tight')
plt.close()

# %%
# number of job postings by industry
plt.figure(figsize=(12, 6))
df_unfiltered.groupby("industry").salary.count().sort_values(ascending=False).head(10).plot.bar()
plt.xlabel("")
plt.ylabel("Number of Job Postings", fontsize=14)
plt.xticks(rotation=0, fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("./job_postings_by_industry.png", dpi=150, bbox_inches='tight')
plt.close()

# %%
# Create boxplot of salary by seniority level
plt.figure(figsize=(12, 6))
df_unfiltered.boxplot(column="salary_avg_normalized", by="seniority_level_num", ax=plt.gca())
plt.xlabel("Seniority Level", fontsize=14)
plt.ylabel("Normalized Salary", fontsize=14)
plt.suptitle("")  # Remove the automatic pandas suptitle
plt.tight_layout()
plt.savefig("./salary_by_seniority.png", dpi=150, bbox_inches='tight')
plt.close()

# %%
# Create scatter plot of company size vs salary
plt.figure(figsize=(12, 6))
plt.scatter(df["company_size"], df["salary_avg_normalized"], alpha=0.6)
plt.xlabel("Company Size", fontsize=14)
plt.ylabel("Normalized Salary", fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("./salary_by_company_size.png", dpi=150, bbox_inches='tight')
plt.close()

# %%
# Create bar chart of salary by industry
plt.figure(figsize=(14, 6))
df_unfiltered.groupby("industry").salary_avg_normalized.median().sort_values(ascending=False).plot(kind="bar")
plt.xlabel("Industry", fontsize=14)
plt.ylabel("Median Normalized Salary", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("./salary_by_industry.png", dpi=150, bbox_inches='tight')
plt.close()

# %%
# Create boxplot of salary by job status (remote/onsite)
plt.figure(figsize=(12, 6))
df.boxplot(column="salary_avg_normalized", by="status", ax=plt.gca())
plt.xlabel("Job Status", fontsize=14)
plt.ylabel("Normalized Salary", fontsize=14)
plt.suptitle("")
plt.tight_layout()
plt.savefig("./remote_vs_onsite_salary.png", dpi=150, bbox_inches='tight')
plt.close()

# %%
# Generate skill analysis graphs from skill_analysis.py
import ast  # To safely evaluate string representations of Python literals

def calculate_skill_prices(df, use_normalized=False):
    """
    Calculate the average salary for each skill by:
    1. Parsing the skills column (which contains string representations of lists)
    2. Creating a mapping from each skill to the salaries of jobs requiring that skill
    3. Calculating the average salary for each skill
    
    Args:
        df: DataFrame with job data
        use_normalized: Whether to use normalized salary instead of raw salary
    """
    # Create a dictionary to store skills and their associated salaries
    skill_salaries = {}
    
    # Determine which salary column to use
    salary_col = "salary_avg_normalized" if use_normalized else "salary_avg"
    
    # Iterate through each row in the dataframe
    for idx, row in df.iterrows():
        # Convert the string representation of the list to an actual list
        try:
            skills_list = ast.literal_eval(row['skills'])
            salary_avg = row[salary_col]
            
            # For each skill in the list, add the salary to that skill's list
            if isinstance(skills_list, list) and len(skills_list) > 0:
                for skill in skills_list:
                    skill = skill.lower().strip()  # Normalize the skill name
                    if skill not in skill_salaries:
                        skill_salaries[skill] = []
                    skill_salaries[skill].append(salary_avg)
        except (ValueError, SyntaxError):
            # If there's an error in parsing the skills, skip this row
            continue
    
    # Calculate the average salary for each skill
    skill_prices = {}
    for skill, salaries in skill_salaries.items():
        skill_prices[skill] = {
            'average_salary': np.mean(salaries),
            'count': len(salaries),
            'min_salary': np.min(salaries),
            'max_salary': np.max(salaries),
            'std_deviation': np.std(salaries)
        }
    
    return skill_prices

# %%
# Calculate skill prices with normalized salaries (filtered)
skill_analysis_filtered_normalized = calculate_skill_prices(df, use_normalized=True)

# Convert to DataFrame
skill_df_filtered_normalized = pd.DataFrame(skill_analysis_filtered_normalized).T
skill_df_filtered_normalized.index.name = 'skill'
skill_df_filtered_normalized = skill_df_filtered_normalized.sort_values(by='average_salary', ascending=False)

# %%
# Create top 10 highest paying skills plot
plt.figure(figsize=(14, 6))
top_10_highest = skill_df_filtered_normalized.head(10)
plt.barh(range(len(top_10_highest)), top_10_highest['average_salary'], color='coral')
plt.yticks(range(len(top_10_highest)), top_10_highest.index, fontsize=12)
plt.xlabel('Average Normalized Salary', fontsize=14)
plt.gca().invert_yaxis()  # Invert y-axis so highest salary is at top
plt.tight_layout()
plt.savefig("./top_10_highest_paying_skills.png", dpi=150, bbox_inches='tight')
plt.close()

# %%
# Create top 10 most common skills plot
plt.figure(figsize=(14, 6))
skill_df_by_count = skill_df_filtered_normalized.sort_values(by='count', ascending=False)
top_10_common = skill_df_by_count.head(10)
plt.barh(range(len(top_10_common)), top_10_common['count'], color='lightblue')
plt.yticks(range(len(top_10_common)), top_10_common.index, fontsize=12)
plt.xlabel('Number of Job Postings', fontsize=14)
plt.gca().invert_yaxis()  # Invert y-axis for consistency
plt.tight_layout()
plt.savefig("./top_10_most_common_skills.png", dpi=150, bbox_inches='tight')
plt.close()

print("All graphs have been generated successfully!")

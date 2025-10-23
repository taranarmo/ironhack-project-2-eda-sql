# %%
import numpy as np
import pandas as pd
import ast  # To safely evaluate string representations of Python literals

# %%
# Define IQR filtering and normalization functions similar to analysis.py
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
# Load the cleaned data
df = pd.read_csv("./cleaned_data_science_job_posts_and_salaries_2025.csv")

# %%
# Apply IQR filtering and normalization by country (similar to analysis.py)
df_filtered = df.copy()
df_filtered = df_filtered.groupby("country_code", group_keys=False).apply(iqr_filter).reset_index(drop=True)
df_filtered = df_filtered.groupby("country_code", group_keys=False).apply(normalize_salary).reset_index(drop=True)
df_unfiltered = df.copy()
df_unfiltered = df_unfiltered.groupby("country_code", group_keys=False).apply(normalize_salary).reset_index(drop=True)

# %%
# Calculate skill prices with raw salaries
skill_analysis = calculate_skill_prices(df, use_normalized=False)

# %%
# Calculate skill prices with normalized salaries (unfiltered)
skill_analysis_normalized = calculate_skill_prices(df_unfiltered, use_normalized=True)

# %%
# Calculate skill prices with normalized salaries (filtered to remove outliers)
skill_analysis_filtered_normalized = calculate_skill_prices(df_filtered, use_normalized=True)

# %%
# Convert the results to DataFrames for better visualization
skill_df = pd.DataFrame(skill_analysis).T
skill_df.index.name = 'skill'
skill_df = skill_df.sort_values(by='average_salary', ascending=False)

# Convert normalized results to DataFrame (unfiltered)
skill_df_normalized = pd.DataFrame(skill_analysis_normalized).T
skill_df_normalized.index.name = 'skill'
skill_df_normalized = skill_df_normalized.sort_values(by='average_salary', ascending=False)

# Convert filtered normalized results to DataFrame
skill_df_filtered_normalized = pd.DataFrame(skill_analysis_filtered_normalized).T
skill_df_filtered_normalized.index.name = 'skill'
skill_df_filtered_normalized = skill_df_filtered_normalized.sort_values(by='average_salary', ascending=False)

# %%
# Display the top 10 highest paying skills (raw salaries)
print("Top 10 Highest Paying Skills (Raw Salaries):")
print(skill_df.head(10))

# %%
print("\nTop 10 Highest Paying Skills (Normalized Salaries - Unfiltered):")
print(skill_df_normalized.head(10))

# %%
print("\nTop 10 Highest Paying Skills (Normalized Salaries - Filtered):")
print(skill_df_filtered_normalized.head(10))

# %%
print("\nTop 10 Skills by Job Count (Raw Salaries):")
skill_df_by_count = skill_df.sort_values(by='count', ascending=False)
print(skill_df_by_count.head(10))

# %%
print("\nTop 10 Skills by Job Count (Normalized Salaries - Unfiltered):")
skill_df_normalized_by_count = skill_df_normalized.sort_values(by='count', ascending=False)
print(skill_df_normalized_by_count.head(10))

# %%
print("\nTop 10 Skills by Job Count (Normalized Salaries - Filtered):")
skill_df_filtered_normalized_by_count = skill_df_filtered_normalized.sort_values(by='count', ascending=False)
print(skill_df_filtered_normalized_by_count.head(10))

# %%
# Save all analyses to CSV files
skill_df.to_csv("skill_price_analysis.csv")
skill_df_normalized.to_csv("skill_price_analysis_normalized_unfiltered.csv")
skill_df_filtered_normalized.to_csv("skill_price_analysis_normalized_filtered.csv")
print("\nSkill analysis (raw) saved to 'skill_price_analysis.csv'")
print("Skill analysis (normalized unfiltered) saved to 'skill_price_analysis_normalized_unfiltered.csv'")
print("Skill analysis (normalized filtered) saved to 'skill_price_analysis_normalized_filtered.csv'")

# %%
# Additional insights for raw salaries
print(f"\nTotal number of unique skills (Raw): {len(skill_df)}")
print(f"Skill with highest average salary (Raw): {skill_df.loc[skill_df['average_salary'].idxmax()].name} at €{skill_df['average_salary'].max():,.2f}")
print(f"Skill with lowest average salary (Raw): {skill_df.loc[skill_df['average_salary'].idxmin()].name} at €{skill_df['average_salary'].min():,.2f}")
print(f"Overall average salary across all skills (Raw): €{skill_df['average_salary'].mean():,.2f}")

# %%
# Additional insights for normalized salaries (unfiltered)
print(f"\nTotal number of unique skills (Normalized Unfiltered): {len(skill_df_normalized)}")
print(f"Skill with highest average normalized salary (Unfiltered): {skill_df_normalized.loc[skill_df_normalized['average_salary'].idxmax()].name} at {skill_df_normalized['average_salary'].max():.2f}")
print(f"Skill with lowest average normalized salary (Unfiltered): {skill_df_normalized.loc[skill_df_normalized['average_salary'].idxmin()].name} at {skill_df_normalized['average_salary'].min():.2f}")
print(f"Overall average normalized salary across all skills (Unfiltered): {skill_df_normalized['average_salary'].mean():.2f}")

# %%
# Additional insights for normalized salaries (filtered)
print(f"\nTotal number of unique skills (Normalized Filtered): {len(skill_df_filtered_normalized)}")
print(f"Skill with highest average normalized salary (Filtered): {skill_df_filtered_normalized.loc[skill_df_filtered_normalized['average_salary'].idxmax()].name} at {skill_df_filtered_normalized['average_salary'].max():.2f}")
print(f"Skill with lowest average normalized salary (Filtered): {skill_df_filtered_normalized.loc[skill_df_filtered_normalized['average_salary'].idxmin()].name} at {skill_df_filtered_normalized['average_salary'].min():.2f}")
print(f"Overall average normalized salary across all skills (Filtered): {skill_df_filtered_normalized['average_salary'].mean():.2f}")

# Ironhack EDA project

## Dataset

The initial dataset is [Data Science Careers & Salaries 2025](https://www.kaggle.com/datasets/nalisha/data-science-careers-and-salaries-2025) taken from Kaggle, data collected on Oct 2, 2025 (job posted field uses relative time thus we'll need this date as a reference).

Jobs collected from different locations thus salary variability is great, if possible this analysis will use relative salary refering to some base salary in the location.

## Preliminary questions

1. How seniority level and role affect salary
2. How much do different skills cost

## Project desctiption

- ./data_cleaning.py takes raw dataset ./data_science_job_posts_and_salaries_2025.zip and produces ./cleaned_data_science_job_posts_and_salaries_2025.csv
- ./analysis.py shows the analysis steps as they were done
- ./skill_analysis.py is responsible for skill analysis
- ./slides.md is a source file for presentation which is converted by [Marp](https://marp.app/) into pdf or html
- ./generate_presentation_graphs.py produces graphs for the slides
- ./flake.nix and ./flake.lock are responsible for local working environment, require [Nix](https://nixos.org/)
- SQL questions and queries are in ./questions.sql

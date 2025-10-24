-- we assume that dataset is called jobs, and fields are called like in ./cleaned_data_science_job_posts_and_salaries_2025.csv

-- 1. Count jobs per job title

SELECT
  job_title,
  COUNT(*) AS job_count
FROM 
  jobs
GROUP BY 
  job_title;

-- 2. Count jobs per seniority level

SELECT
  seniority_level,
  COUNT(*) AS job_count
FROM
  jobs
GROUP BY
  seniority_level;

-- 3. Apply IQR method to find outliers in the salary_usd field

SELECT
  salary_avg,
  CASE
    WHEN
      salary_avg < (Q1 - 1.5 * IQR) OR salary_avg > (Q3 + 1.5 * IQR)
      THEN TRUE
    ELSE FALSE
  END AS outlier_status
  FROM
    (
      SELECT
        salary_avg,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary_avg) AS Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary_avg) AS Q3,
        (PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary_avg) - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary_avg)) AS IQR
      FROM
        jobs
    ) AS stats;
  
-- 4. Average salary per job title

SELECT
  job_title,
  AVG(salary_avg) AS average_salary
FROM
  jobs
GROUP BY
  job_title;

-- 5. Average salary per seniority level

SELECT
  seniority_level,
  AVG(salary_avg) AS average_salary
FROM
  jobs
GROUP BY
  seniority_level;

-- 6. Count jobs per industry

SELECT
  industry,
  COUNT(*) AS job_count
FROM
  jobs
GROUP BY
  industry;

-- 7. Average salary per industry

SELECT
  industry,
  AVG(salary_avg) AS average_salary
FROM
  jobs
GROUP BY
  industry
ORDER BY
  average_salary DESC;

-- 8. Average salary per country

SELECT
  country_code,
  AVG(salary_avg) AS average_salary
FROM
  jobs
GROUP BY
  country_code
ORDER BY
  average_salary DESC;

-- 9. Count jobs per remote status

SELECT
  status,
  COUNT(*) AS job_count
FROM
  jobs
GROUP BY
  status
ORDER BY
  job_count DESC;

-- 10. Average salary per remote status

SELECT
  status,
  AVG(salary_avg) AS average_salary
FROM
  jobs
GROUP BY
  status
ORDER BY
  average_salary DESC;

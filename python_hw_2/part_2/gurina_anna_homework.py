"""
Orthopedic Patient Analysis
Student: Anna Gurina
Date: 1-Dec-2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Setup input/output paths
current_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(current_dir, 'input', 'column_3C_weka.csv')
output_dir = os.path.join(current_dir, 'output')

# Create output dur if it's absent
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load data
patients = pd.read_csv(input_path)

# ==================== Question 1 ====================
print("=" * 50)
print("QUESTION 1: Pandas - Data Exploration & Filtering")
print("=" * 50)

# Part A: Exploration
print("First 5 patients:")
print(patients.head())

print(f"\nDataset shape: {patients.shape}")
print(f"\nColumns: {patients.dtypes}")

# Part B: Filter severe cases
severe_cases = patients[
    (patients['degree_spondylolisthesis'] > 30) |
    (patients['pelvic_incidence'] > 70)
]

print(f"\nSevere cases found: {len(severe_cases)}")
print("\nClass distribution of severe cases:")
print(severe_cases['class'].value_counts())

# ==================== Question 2 ====================
print("\n" + "=" * 50)
print("QUESTION 2: Pandas - Group Analysis")
print("=" * 50)

# a) Group statistics
diagnosis_stats = patients.groupby('class').agg({
    'degree_spondylolisthesis': 'mean',
    'pelvic_incidence': 'mean',
    'lumbar_lordosis_angle': 'std',
    'class': 'count'
}).rename(columns={'class': 'count'})

diagnosis_stats_formatted = diagnosis_stats.round(2)

print("Statistics by Diagnosis:")
print(diagnosis_stats_formatted)

# b) Highest spondylolisthesis
highest_diagnosis = diagnosis_stats['degree_spondylolisthesis'].idxmax()
print(f"\nDiagnosis with highest spondylolisthesis: {highest_diagnosis}")

# Save results
output_path = os.path.join(output_dir, 'q2_diagnosis_statistics.csv')
diagnosis_stats_formatted.to_csv(output_path)
print(f"\nResults saved to: {output_path}")

# ==================== Question 3 ====================
print("\n" + "=" * 50)
print("QUESTION 3: NumPy - Statistical Analysis")
print("=" * 50)

# a) NumPy statistics for pelvic_incidence
pelvic_incidence_array = patients['pelvic_incidence'].to_numpy()

mean_pi = np.mean(pelvic_incidence_array)
median_pi = np.median(pelvic_incidence_array)
std_pi = np.std(pelvic_incidence_array)
p25 = np.percentile(pelvic_incidence_array, 25)
p75 = np.percentile(pelvic_incidence_array, 75)

print("Pelvic Incidence Statistics:")
print(f"Mean: {mean_pi:.2f}")
print(f"Median: {median_pi:.2f}")
print(f"Std Dev: {std_pi:.2f}")
print(f"25th percentile: {p25:.2f}")
print(f"75th percentile: {p75:.2f}")

# b) Z-score normalization using NumPy
spondylo_array = patients['degree_spondylolisthesis'].to_numpy()

# Calculate z-scores (vectorized operation)
spondylo_mean = np.mean(spondylo_array)
spondylo_std = np.std(spondylo_array)
spondylo_zscore = (spondylo_array - spondylo_mean) / spondylo_std

# Add to dataframe
patients['spondylo_zscore'] = spondylo_zscore

# Count outliers (|z-score| > 2)
outliers = np.abs(spondylo_zscore) > 2
num_outliers = np.sum(outliers)

print(f"\nNumber of outliers (|z-score| > 2): {num_outliers}")
print(f"Percentage of outliers: {(num_outliers/len(patients)*100):.1f}%")

# Save results
results_dict = {
    'Statistic': ['Mean', 'Median', 'Std Dev', '25th percentile', '75th percentile', 
                  'Number of outliers', 'Percentage of outliers'],
    'Value': [mean_pi, median_pi, std_pi, p25, p75, 
              num_outliers, (num_outliers/len(patients)*100)]
}
results_df = pd.DataFrame(results_dict)

analysis_output_path = os.path.join(output_dir, 'q3_statistical_analysis.csv')
results_df.to_csv(analysis_output_path, index=False)
print(f"\nResults saved to: {output_path}")

# Also save the updated patients dataframe with z-scores
patients_output_path = os.path.join(output_dir, 'q3_patients_with_zscores.csv')
patients.to_csv(patients_output_path, index=False)
print(f"Updated patient data saved to: {patients_output_path}")

# ==================== Question 4 ====================
print("\n" + "=" * 50)
print("QUESTION 4: Matplotlib - Visualization")
print("=" * 50)

# Create figure with 3 subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: Histogram
mean_spondylo = patients['degree_spondylolisthesis'].mean()
axes[0].hist(patients['degree_spondylolisthesis'], bins=30, 
             color='skyblue', edgecolor='black', alpha=0.7)
axes[0].axvline(mean_spondylo, color='red', linestyle='--', linewidth=2, 
                label=f'Mean: {mean_spondylo:.1f}')
axes[0].set_xlabel('Degree of Spondylolisthesis', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].set_title('Distribution of Spondylolisthesis', fontsize=14)
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# Plot 2: Box plot
# Prepare data for box plot
diagnosis_groups = [
    patients[patients['class'] == 'Normal']['pelvic_incidence'],
    patients[patients['class'] == 'Hernia']['pelvic_incidence'],
    patients[patients['class'] == 'Spondylolisthesis']['pelvic_incidence']
]

bp = axes[1].boxplot(diagnosis_groups, 
                    labels=['Normal', 'Hernia', 'Spondylolisthesis'],
                    patch_artist=True)
# Color the boxes
colors = ['lightgreen', 'orange', 'lightcoral']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

axes[1].set_ylabel('Pelvic Incidence (degrees)', fontsize=12)
axes[1].set_xlabel('Diagnosis', fontsize=12)
axes[1].set_title('Pelvic Incidence by Diagnosis', fontsize=14)
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(axis='y', alpha=0.3)

# Plot 3: Scatter plot
# Color by class
colors_map = {'Normal': 'green', 'Hernia': 'orange', 'Spondylolisthesis': 'red'}
for diagnosis in patients['class'].unique():
    diagnosis_data = patients[patients['class'] == diagnosis]
    axes[2].scatter(diagnosis_data['pelvic_incidence'], 
                   diagnosis_data['degree_spondylolisthesis'],
                   c=colors_map[diagnosis], 
                   label=diagnosis, 
                   alpha=0.6, 
                   s=50,
                   edgecolors='black',
                   linewidth=0.5)

axes[2].set_xlabel('Pelvic Incidence (degrees)', fontsize=12)
axes[2].set_ylabel('Degree of Spondylolisthesis', fontsize=12)
axes[2].set_title('Pelvic Incidence vs Spondylolisthesis', fontsize=14)
axes[2].legend(title='Diagnosis')
axes[2].grid(True, alpha=0.3)

#save figure
figure_path = os.path.join(output_dir, 'orthopedic_analysis.png')
plt.tight_layout()
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {figure_path}")

# ==================== Question 5 ====================
print("\n" + "=" * 50)
print("QUESTION 5: Pandas - Correlation & Complex Query")
print("=" * 50)

# Part A: Correlation Analysis
numeric_data = patients.select_dtypes(include=['number'])
correlation_matrix = numeric_data.corr()

print("Correlation Matrix:")
print(correlation_matrix.round(3))

# Find highest correlation (excluding diagonal)
# Hint: use .unstack() and filter out 1.0 values
correlations = correlation_matrix.unstack()
# Remove self-correlations and sort
sorted_correlations = correlations[correlations != 1.0].sort_values(ascending=False)

# Get the strongest positive correlation
strongest_correlation = sorted_correlations.iloc[0]
feature_pair = sorted_correlations.index[0]

print("\nStrongest Positive Correlation:")
print(f"Features: {feature_pair[0]} and {feature_pair[1]}")
print(f"Correlation: {strongest_correlation:.3f}")

# Part B: Complex Filtering
specific_patients = patients[
    (patients['pelvic_incidence'].between(50, 70)) &
    (patients['degree_spondylolisthesis'] > 20) &
    (patients['class'] == 'Spondylolisthesis')
]

total_count = len(patients)
specific_count = len(specific_patients)
percentage = (specific_count/total_count) * 100

print("\nComplex Query Results:")
print(f"Patients matching all criteria: {specific_count}")
print(f"Percentage of total: {percentage:.1f}%")

# Save results
results = {
    'Analysis': [
        'Strongest Correlation Features',
        'Correlation Value',
        'Matching Patients Count',
        'Matching Patients Percentage'
    ],
    'Value': [
        f"{feature_pair[0]} and {feature_pair[1]}",
        f"{strongest_correlation:.3f}",
        specific_count,
        f"{percentage:.1f}%"
    ]
}

# save correlation analysis to CSV
output_path = os.path.join(output_dir, 'q5_correlation_analysis.csv')
results_df = pd.DataFrame(results)
results_df.to_csv(output_path, index=False)
print(f"\nResults saved to: {output_path}")

# save correlation matrix
correlation_path = os.path.join(output_dir, 'q5_correlation_matrix.csv')
correlation_matrix.round(3).to_csv(correlation_path)
print(f"Correlation matrix saved to: {correlation_path}")

# ==================== Question 6 ====================
print("\n" + "=" * 50)
print("QUESTION 6: Pandas - Summary Report Creation")
print("=" * 50)

# a) Create abnormal flag
patients['abnormal'] = patients['class'].isin(['Hernia', 'Spondylolisthesis'])

# Print basic counts
normal_count = (~patients['abnormal']).sum()
abnormal_count = patients['abnormal'].sum()
print(f"Normal patients: {normal_count}")
print(f"Abnormal patients: {abnormal_count}")

# b) Compare groups
comparison = patients.groupby('abnormal').agg({
    'pelvic_incidence': 'mean',
    'pelvic_tilt': 'mean',
    'lumbar_lordosis_angle': 'mean',
    'sacral_slope': 'mean',
    'pelvic_radius': 'mean',
    'degree_spondylolisthesis': 'mean'
})

comparison['patient_count'] = patients.groupby('abnormal').size()

print("\nNormal vs Abnormal Comparison:")
print(comparison.round(2))

# Which features differ most?
differences = comparison.loc[True] - comparison.loc[False]
biggest_diff = differences.drop('patient_count').abs().idxmax()

print(f"\nFeature with biggest difference: {biggest_diff}")
print(f"Difference: {differences[biggest_diff]:.2f}")

# percentage differences
percent_diff = ((comparison.loc[True] - comparison.loc[False]) / 
               comparison.loc[False] * 100).round(2)
percent_diff = percent_diff.drop('patient_count')

print("Percentage differences (Abnormal vs Normal):")
print(percent_diff)

# Save results to CSV
output_path = os.path.join(output_dir, 'q6_normal_vs_abnormal_comparison.csv')
comparison.round(2).to_csv(output_path)
print(f"\nResults saved to: {output_path}")
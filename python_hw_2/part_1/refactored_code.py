# split the method into several ones to implement 1 function per method
# replaced the for .. in loops structures with several if-s with masks 
# self-descriptive method names added
# variables renamed to self-descriptive
# added usage comments where appropriate
# added errors handling
# added main entry point with error handling

"""
Clinical Trial Data Analysis Module

This module analyzes clinical trial data to identify responsive patients
and calculate survival statistics across treatment groups.
"""

import pandas as pd
from typing import List, Tuple, Dict

# Constants
AGE_THRESHOLD = 50
CANCER_TYPE_LUNG = 'Lung'
TREATMENT_A = 'Treatment_A'
CONTROL_GROUP = 'Control'

def load_clinical_data(file_path: str) -> pd.DataFrame: # input-output type hints are added
    # added methods description
    """
    Load clinical trial data from CSV file.

    Args:
        file_path (str): Path to the CSV file containing clinical trial data

    Returns:
        pd.DataFrame: DataFrame with clinical trial data
    
    Raises:
        FileNotFoundError: If the specified file doesn't exist
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Clinical trial data file not found: {file_path}")
    
def find_responsive_patients(data: pd.DataFrame) -> List[str]:
    """
    Identify patients who responded positively to treatment.

    Criteria:
    - Age >= AGE_THRESHOLD
    - Lung cancer type
    - Decreased tumor size from baseline

    Args:
        data (pd.DataFrame): Clinical trial data

    Returns:
        List[str]: List of responsive patient IDs
    """
    responsive_mask = (
        (data['age'] >= AGE_THRESHOLD) &
        (data['cancer_type'] == CANCER_TYPE_LUNG) &
        (data['final_tumor_size'] < data['baseline_tumor_size'])
    )
    return data.loc[responsive_mask, 'patient_id'].tolist()

def calculate_survival_statistics(data: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate average survival months for each treatment group.

    Args:
        data (pd.DataFrame): Clinical trial data

    Returns:
        Dict[str, float]: Dictionary containing average survival months 
                         for each treatment group
    """
    # Group by treatment and calculate mean survival months
    survival_stats = (data.groupby('treatment')['survival_months']
                     .mean()
                     .to_dict())
    
    # Ensure both treatment groups are in results
    survival_stats.setdefault(TREATMENT_A, 0.0)
    survival_stats.setdefault(CONTROL_GROUP, 0.0)
    
    return survival_stats

def print_analysis_results(survival_stats: Dict[str, float], 
                         responsive_count: int) -> None:
    """
    Print formatted results.

    Args:
        survival_stats (Dict[str, float]): Average survival months by treatment
        responsive_count (int): Number of responsive patients
    """
    print(f"Avg survival Treatment A: {survival_stats[TREATMENT_A]:.2f}")
    print(f"Avg survival Control: {survival_stats[CONTROL_GROUP]:.2f}")
    print(f"Responsive patients: {responsive_count}")

def analyze_clinical_trial_data(file_path: str) -> Tuple[List[str], Dict[str, float]]:
    """
    Clinical trial data analysis.

    Loads data, finds responsive patients, calculates survival statistics.

    Args:
        file_path (str): Path to the clinical trial data CSV file

    Returns:
        Tuple[List[str], Dict[str, float]]: Tuple containing:
            - List of responsive patient IDs
            - Dictionary of survival statistics by treatment group
    """
    # Load data
    clinical_data = load_clinical_data(file_path)
    
    # Find responsive patients
    responsive_patients = find_responsive_patients(clinical_data)
    
    # Calculate survival statistics
    survival_stats = calculate_survival_statistics(clinical_data)
    
    # Print results
    print_analysis_results(survival_stats, len(responsive_patients))
    
    return responsive_patients, survival_stats

# creating entry point - enabling handy importing and accessing the method from other classes
if __name__ == "__main__":
    try:
        responsive_ids, survival_statistics = analyze_clinical_trial_data(
            'clinical_trial_patients.csv'
        )
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
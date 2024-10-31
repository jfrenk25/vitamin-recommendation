#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st

# Define the Excel data directly in the script
biomarker_data = [
    {'biomarker': 'DHEA', 'relationship_ref_range': '<=', 'reference_range': 150, 'vitamin_supplement': 'DHEA 10 mg', 'times_day': 1},
    {'biomarker': 'DHEA', 'relationship_ref_range': '>=', 'reference_range': 300, 'vitamin_supplement': 'Mood Food', 'times_day': 2},
    {'biomarker': 'Cortisol', 'relationship_ref_range': '<=', 'reference_range': 4, 'vitamin_supplement': 'Adrenal Extra Strength', 'times_day': 1},
    {'biomarker': 'Cortisol', 'relationship_ref_range': 'between', 'reference_range': '5.0-9.0', 'vitamin_supplement': 'Adrenal Essence', 'times_day': 1},
    {'biomarker': 'Cortisol', 'relationship_ref_range': '>=', 'reference_range': 20, 'vitamin_supplement': 'Mood Food', 'times_day': 1},
    {'biomarker': 'Vitamin D', 'relationship_ref_range': '<=', 'reference_range': 30, 'vitamin_supplement': 'Vitamin D 10000 IU', 'times_day': 1},
    {'biomarker': 'Vitamin D', 'relationship_ref_range': 'between', 'reference_range': '31-80', 'vitamin_supplement': 'Vitamin D 5000 IU', 'times_day': 1},
    {'biomarker': 'Trigliceride', 'relationship_ref_range': '>=', 'reference_range': 110, 'vitamin_supplement': 'Liver Detox', 'times_day': 2},
    {'biomarker': 'Trigliceride', 'relationship_ref_range': '>=', 'reference_range': 110, 'vitamin_supplement': 'Glycemic Factors', 'times_day': 2},
    {'biomarker': 'A1c', 'relationship_ref_range': 'between', 'reference_range': '5.7-6.4', 'vitamin_supplement': 'Glycemic Factors', 'times_day': 2},
    {'biomarker': 'A1c', 'relationship_ref_range': '>=', 'reference_range': 6.5, 'vitamin_supplement': 'Glycemic Factors', 'times_day': 2},
    {'biomarker': 'Folate', 'relationship_ref_range': '<=', 'reference_range': 600, 'vitamin_supplement': 'Methyl Protect', 'times_day': 1},
    {'biomarker': 'Magnesium', 'relationship_ref_range': '<=', 'reference_range': 5, 'vitamin_supplement': 'Optimag', 'times_day': 2},
    # Add other rows here as per the entire content of your Excel file
]

def get_vitamin_recommendations(lab_values):
    recommendations = []
    would_have_been = []
    added_supplements = set()

    for row in biomarker_data:
        biomarker = row['biomarker']
        condition = row['relationship_ref_range']
        ref_range = row['reference_range']
        supplement = row['vitamin_supplement']
        times_day = row['times_day']

        if biomarker in lab_values:
            value = lab_values[biomarker]

            try:
                if condition == '<=' and value <= float(ref_range):
                    if supplement not in added_supplements:
                        recommendations.append({
                            'biomarker': biomarker,
                            'vitamin_supplement': supplement,
                            'times_day': times_day
                        })
                        added_supplements.add(supplement)
                    else:
                        would_have_been.append({
                            'biomarker': biomarker,
                            'vitamin_supplement': supplement,
                            'times_day': times_day
                        })
                elif condition == '>=' and value >= float(ref_range):
                    if supplement not in added_supplements:
                        recommendations.append({
                            'biomarker': biomarker,
                            'vitamin_supplement': supplement,
                            'times_day': times_day
                        })
                        added_supplements.add(supplement)
                    else:
                        would_have_been.append({
                            'biomarker': biomarker,
                            'vitamin_supplement': supplement,
                            'times_day': times_day
                        })
                elif condition == 'between':
                    low, high = map(float, ref_range.split('-'))
                    if low <= value <= high:
                        if supplement not in added_supplements:
                            recommendations.append({
                                'biomarker': biomarker,
                                'vitamin_supplement': supplement,
                                'times_day': times_day
                            })
                            added_supplements.add(supplement)
                        else:
                            would_have_been.append({
                                'biomarker': biomarker,
                                'vitamin_supplement': supplement,
                                'times_day': times_day
                            })
            except ValueError:
                pass

    return recommendations, would_have_been

# Streamlit App UI
st.title("Supplement Recommendation Tool")

# Input lab values
st.sidebar.header("Input Lab Values")
lab_values = {}
for biomarker in {row['biomarker'] for row in biomarker_data}:
    lab_values[biomarker] = st.sidebar.number_input(f"{biomarker} value", min_value=0.0, format="%.2f")

# Calculate recommendations
if st.sidebar.button("Get Recommendations"):
    recommendations, would_have_been = get_vitamin_recommendations(lab_values)

    st.subheader("Recommended Supplements")
    for rec in recommendations:
        st.write(f"{rec['biomarker']}: {rec['vitamin_supplement']} - {rec['times_day']} time(s) per day")

    st.subheader("Supplements That Would Have Been Recommended (but are already allocated)")
    for rec in would_have_been:
        st.write(f"{rec['biomarker']}: {rec['vitamin_supplement']} - {rec['times_day']} time(s) per day")


# In[ ]:





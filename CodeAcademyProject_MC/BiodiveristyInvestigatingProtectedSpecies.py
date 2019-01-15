import codecademylib
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency

species = pd.read_csv('species_info.csv')
print(species.head(10))

#Number of different species
print(species.scientific_name.nunique())
species_count = 5541

#Different values of category
species_type = species.category.unique()
print(species_type)

#Different values of conservation statuses
conservation_statuses = species.conservation_status.unique()
print(conservation_statuses)

#How many scientific names fall into each conservation status
conservation_counts = species.groupby(['conservation_status']).scientific_name.nunique().reset_index()
print(conservation_counts)

#Fill in the null values for conservation status
species.fillna('No Intervention', inplace = True)

#Check how many names for each status after fixing the null values
conservation_counts_fixed = species.groupby(['conservation_status']).scientific_name.nunique().reset_index()
print(conservation_counts_fixed)

protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')
    
plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)),protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
labels = [e.get_text() for e in ax.get_xticklabels()]
plt.show()

species['is_protected'] = species.conservation_status != 'No Intervention'

category_counts = species.groupby(['category', 'is_protected'])\
                         .scientific_name.count().reset_index()
  
# print category_counts.head()

category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()

category_pivot.columns = ['category', 'not_protected', 'protected']

category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)
print category_pivot.head()

contingency = [
  [30, 146],
  [75, 413]
]

_, pval, _, _ = chi2_contingency(contingency)

contingency2 = [
  [30, 146],
  [5, 73]
]

_, pval_reptile_mammal, _, _ = chi2_contingency(contingency2)

observations = pd.read_csv('observations.csv')

species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)

species_is_sheep = species[species.is_sheep]

sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]

sheep_observations = observations.merge(sheep_species)

print sheep_observations.head()

obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()

print obs_by_park

plt.figure(figsize=(16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)),obs_by_park.observations.values)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.show()

#Foot and Mouth Reduction Effort - Sample Size Determination
baseline = 15

minimum_detectable_effect = 100*5./15

sample_size_per_variant = 870

yellowstone_weeks_observing = sample_size_per_variant/507.

bryce_weeks_observing = sample_size_per_variant/250.




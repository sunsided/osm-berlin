from typing import Dict, List
import seaborn as sns
import matplotlib.pyplot as plt
from .queries import count_streets_per_area
sns.set_style('whitegrid')


def plot_street_counts(streets: Dict[str, List[str]], areas: Dict[str, float]):
    streets_per_area = count_streets_per_area(streets, areas)
    streets_by_value = sorted(streets_per_area.items(), key=lambda kv: -kv[1])
    streets = [kvp[0] for kvp in streets_by_value]
    values = [kvp[1] for kvp in streets_by_value]
    sizes = [areas[s] for s in streets]

    f, (ax0, ax1) = plt.subplots(1, 2, sharey=True, sharex=False, figsize=(10, 5))
    sns.barplot(values, streets, ax=ax0)
    sns.barplot(sizes, streets, ax=ax1)
    ax0.set_xlabel('Average number of streets per km²')
    ax1.set_xlabel('District area in km²')
    f.suptitle('District area vs. number of streets per km²')
    sns.despine()


def plot_street_counts_by_type(streets: Dict[str, List[str]], areas: Dict[str, float]):
    sorted_districts = sorted(areas.items(), key=lambda kv: kv[1])
    sorted_districts = [d[0] for d in sorted_districts]

    to_person = {}
    to_place = {}
    others = {}
    for district in streets:
        ds = streets[district]
        total = len(ds)
        to_person[district] = len([s for s in ds if s.endswith('straße')]) / total * 100
        to_place[district] = len([s for s in ds if s.endswith('Straße')]) / total * 100
        others[district] = len([s for s in ds if not s.endswith('traße')]) / total * 100

    f, (ax0, ax1, ax2) = plt.subplots(1, 3, sharey=True, sharex=True, figsize=(10, 5))

    values = [to_person[d] for d in sorted_districts]
    sns.barplot(values, sorted_districts, ax=ax0)

    values = [to_place[d] for d in sorted_districts]
    sns.barplot(values, sorted_districts, ax=ax1)

    values = [others[d] for d in sorted_districts]
    sns.barplot(values, sorted_districts, ax=ax2)

    ax0.set_xlabel('Percent related to persons')
    ax1.set_xlabel('Percent related to places')
    ax2.set_xlabel('Percent other street types')
    f.suptitle('Percentage of streets (Straße) related to persons and places by district (order by district area).')
    sns.despine()


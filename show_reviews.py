import pandas as pd
import matplotlib.pyplot as plt

# Load and clean dataset
df = pd.read_csv("Dataset.csv")
df.columns = df.columns.str.strip()
df['Restaurant Name'] = df['Restaurant Name'].astype(str)
df['Restaurant Name Lower'] = df['Restaurant Name'].str.lower()

# Get user input
search_name = input("Enter the restaurant name or keyword: ").strip().lower()

# Filter matches
matches = df[df['Restaurant Name Lower'].str.contains(search_name)]

if matches.empty:
    print("❌ No matching restaurant found.")
else:
    # Display matching restaurants with location and rating
    for idx, row in matches.iterrows():
        print(f"\n🍽️ {row['Restaurant Name']}")
        print(f"⭐ Rating: {row['Aggregate rating']} ({row['Rating text']})")
        print(f"📍 Location: {row.get('Locality', '')}, {row.get('City', '')}")
        print(f"🗳️ Votes: {row.get('Votes', 'N/A')}")
        print("-" * 50)

    # Use City as the location; you can switch to 'Locality' if needed
    matches['City'] = matches['City'].astype(str)

    # Pivot the data: each city as group, restaurants as x-labels
    pivot_data = matches[['Restaurant Name', 'City', 'Aggregate rating']]

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    cities = pivot_data['City'].unique()

    width = 0.8 / len(cities)  # width of each bar
    x_labels = pivot_data['Restaurant Name'].unique()
    x = range(len(x_labels))

    for i, city in enumerate(cities):
        city_data = pivot_data[pivot_data['City'] == city]
        city_ratings = []

        for name in x_labels:
            val = city_data[city_data['Restaurant Name'] == name]['Aggregate rating']
            city_ratings.append(val.values[0] if not val.empty else 0)

        ax.bar([pos + i * width for pos in x], city_ratings, width=width, label=city)

    ax.set_xticks([pos + width * (len(cities)-1) / 2 for pos in x])
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.set_ylabel("Aggregate Rating")
    ax.set_title(f"Restaurant Ratings Grouped by City for '{search_name}'")
    ax.legend(title="City")
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()

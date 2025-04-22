import streamlit as st
import polars as pl
import matplotlib.pyplot as plt

st.title("Global Cybersecurity Threats Dashboard")
st.write("Built using Polars and Matplotlib")

uploaded_file = st.file_uploader("Upload the Cybersecurity Threats (CSV)", type="csv")

if uploaded_file:
    df = pl.read_csv(uploaded_file)

    # Visualization selector
    selected_vis = st.selectbox(
        "Choose a visualisation",
        [
            "Top 10 countries by total financial loss",
            "Total affected users per year",
            "Top 5 most common attack types",
            "Scatter plot: users vs. financial loss",
            "Box plot: financial loss per attack type"
        ]
    )

    if selected_vis == "Top 10 countries by total financial loss":
        country_loss = (
            df.group_by("Country")
            .agg(pl.col("Financial Loss (in Million $)").sum().alias("Total Loss"))
            .sort("Total Loss", descending=True)
            .head(10)
        )
        countries = country_loss["Country"].to_list()
        losses = country_loss["Total Loss"].to_list()

        fig, ax = plt.subplots()
        ax.bar(countries, losses)
        ax.set_title("Top 10 Countries by Total Financial Loss")
        ax.set_ylabel("Loss (in Million $)")
        ax.set_xlabel("Country")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    elif selected_vis == "Total affected users per year":
        users_per_year = (
            df.group_by("Year")
            .agg(pl.col("Number of Affected Users").sum().alias("Total Users"))
            .sort("Year")
        )
        years = users_per_year["Year"].to_list()
        users = users_per_year["Total Users"].to_list()

        fig, ax = plt.subplots()
        ax.plot(years, users, marker="o")
        ax.set_title("Total Affected Users Per Year")
        ax.set_ylabel("Number of Users")
        ax.set_xlabel("Year")
        st.pyplot(fig)

    elif selected_vis == "Top 5 most common attack types":
        top_attacks = (
            df.group_by("Attack Type")
            .agg(pl.len().alias("Count"))
            .sort("Count", descending=True)
            .head(5)
        )
        attack_types = top_attacks["Attack Type"].to_list()
        counts = top_attacks["Count"].to_list()

        fig, ax = plt.subplots()
        ax.bar(attack_types, counts)
        ax.set_title("Top 5 Most Common Attack Types")
        ax.set_ylabel("Number of Incidents")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    elif selected_vis == "Scatter plot: users vs. financial loss":
        sample = df.sample(n=500, seed=42) if df.height > 500 else df
        x = sample["Number of Affected Users"].to_list()
        y = sample["Financial Loss (in Million $)"].to_list()
        types = sample["Attack Type"].to_list()

        unique_types = list(set(types))
        cmap = {t: i for i, t in enumerate(unique_types)}
        colors = [cmap[t] for t in types]

        fig, ax = plt.subplots()
        scatter = ax.scatter(x, y, c=colors, cmap="tab10", alpha=0.7)
        ax.set_title("Financial Loss vs. Affected Users (colored by Attack Type)")
        ax.set_xlabel("Affected Users")
        ax.set_ylabel("Financial Loss (in Million $)")
        ax.grid(True)

        handles = [
            plt.Line2D([0], [0], marker='o', color='w',
                       label=t, markersize=8,
                       markerfacecolor=plt.cm.tab10(i / len(unique_types)))
            for t, i in cmap.items()
        ]
        ax.legend(handles=handles, title="Attack Type", bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    elif selected_vis == "Box plot: financial loss per attack type":
        grouped = (
            df.group_by("Attack Type")
            .agg(pl.col("Financial Loss (in Million $)").alias("Losses"))
        )
        attack_types = grouped["Attack Type"].to_list()
        loss_lists = grouped["Losses"].to_list()

        fig, ax = plt.subplots()
        ax.boxplot(loss_lists, tick_labels=attack_types, patch_artist=True)
        ax.set_title("Financial Loss per Attack Type (Box Plot)")
        ax.set_ylabel("Loss (in Million $)")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

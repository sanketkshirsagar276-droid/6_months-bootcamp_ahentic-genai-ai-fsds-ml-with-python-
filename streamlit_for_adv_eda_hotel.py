import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data():
    df = pd.read_csv(r'C:\Users\Sanket kshirsagar\Downloads\hotel_bookings.csv')
    df['children'].fillna(0, inplace=True)
    df['total_guests'] = df['adults'] + df['children'] + df['babies']
    df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    return df

df = load_data()

st.title('Hotel Bookings - Interactive EDA')
st.sidebar.header('Filter Options')

# Filters
hotel_type = st.sidebar.multiselect("Select Hotel Type", df['hotel'].unique(), default=df['hotel'].unique())
year = st.sidebar.multiselect("Select Year", df['arrival_date_year'].unique(), default=df['arrival_date_year'].unique())

filtered_df = df[(df['hotel'].isin(hotel_type)) & (df['arrival_date_year'].isin(year))]

st.write('### Data Preview')
st.dataframe(filtered_df.head())

plot_type = st.sidebar.selectbox("Choose Plot Type", 
    ["Histogram", "Scatter", "Boxplot", "Heatmap", "Violin", "Correlation Heatmap"])

# Histogram
if plot_type == "Histogram":
    col = st.sidebar.selectbox("Select Column", filtered_df.select_dtypes("number").columns)
    fig, ax = plt.subplots()
    sns.histplot(filtered_df[col], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

# Scatter
elif plot_type == "Scatter":
    x_col = st.sidebar.selectbox("X-axis", filtered_df.select_dtypes("number").columns)
    y_col = st.sidebar.selectbox("Y-axis", filtered_df.select_dtypes("number").columns)
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df, x=x_col, y=y_col, hue="hotel", alpha=0.5, ax=ax)
    st.pyplot(fig)

# Boxplot
elif plot_type == "Boxplot":
    num_col = st.sidebar.selectbox("Select Numeric Column", filtered_df.select_dtypes("number").columns)
    cat_col = st.sidebar.selectbox("Select Category Column", filtered_df.select_dtypes("object").columns)
    fig, ax = plt.subplots()
    sns.boxplot(x=cat_col, y=num_col, data=filtered_df, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Heatmap (with month order fix)
elif plot_type == "Heatmap":
    month_order = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
    pivot = pd.crosstab(filtered_df['arrival_date_month'], filtered_df['hotel'], normalize="index")
    pivot = pivot.reindex(month_order)  # ensures proper month order
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(pivot, annot=True, cmap="YlGnBu", ax=ax)
    st.pyplot(fig)

# Violin (now user-selectable)
elif plot_type == "Violin":
    num_col = st.sidebar.selectbox("Select Numeric Column", filtered_df.select_dtypes("number").columns, index=list(filtered_df.select_dtypes("number").columns).index("adr") if "adr" in filtered_df.columns else 0)
    fig, ax = plt.subplots(figsize=(8,6))
    sns.violinplot(x="hotel", y=num_col, data=filtered_df, ax=ax)
    st.pyplot(fig)

# Correlation Heatmap
elif plot_type == "Correlation Heatmap":
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

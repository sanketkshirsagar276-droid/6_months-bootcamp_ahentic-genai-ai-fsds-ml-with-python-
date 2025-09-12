import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import io

sns.set_theme(style='whitegrid')


st.title('The Income & Expenditure Household Dataset')
st.write("""
         This app analyzes the **Income & Expenditure Household Dataset** which contains socio-economic
         information about families, including their income, expenses, education, occupation, living conditions.
         *Dataset created by Sanket Kshirsagar.*
            """)

df=pd.read_csv(r'C:\Users\Sanket kshirsagar\Downloads\Inc_Exp_Data.csv')

st.subheader("Dataset Shape")
st.write(f'Rows: {df.shape[0]}, Columns: {df.shape[1]}')

st.subheader('Dataset Descriptive Stats')
st.write(df.describe())

st.subheader('Information about Dataset')
buffer = io.StringIO()
df.info(buf=buffer)
s= buffer.getvalue()
st.text(s)

st.subheader('Top Rows of the Dataset')
st.write(df.head())

st.subheader('Descriptive stats (Transposed)')
st.write(df.describe().T)

st.subheader('Checking for Null Values')
st.write(df.isna().any())

# ---------------- Statistics ----------------
st.subheader('The Mean Expense of HOusehold')
st.write(df['Mthly_HH_Expense'].mean())

st.subheader('The Median Expense of Household')
st.write(df['Mthly_HH_Expense'].median())

st.subheader('Most Common Monthly Expense')
mth_exp_tmp = pd.crosstab(index=df['Mthly_HH_Expense'], columns='count')
mth_exp_tmp.reset_index(inplace=True)
most_common_exp = mth_exp_tmp[mth_exp_tmp['count'] == df['Mthly_HH_Expense'].value_counts().max()]
st.write(most_common_exp)

def display_plot(title, plot_func):
    st.subheader(title)
    fig, ax = plt.subplots(figsize=(8,6))
    plot_func(ax)
    st.pyplot(fig)
    plt.close(fig)

def bar_plot(ax):
    sns.barplot(
        x=df['Highest_Qualified_Member'].value_counts().index,
        y=df['Highest_Qualified_Member'].value_counts().values,
        ax=ax
    )
    ax.set_title('Bar Plot: Highest Qualified Member')

def line_plot(ax):
    sns.lineplot(data=df, x='Mthly_HH_Income', y='Mthly_HH_Expense', ax=ax)
    IQR = df['Mthly_HH_Expense'].quantile(0.75) - df['Mthly_HH_Expense'].quantile(0.25)
    ax.set_title(f"Line Plot: Income vs Expense (IQR = {IQR:.2f})")

def bar_plot2(ax):
    sns.barplot(
        x=df['No_of_Earning_Members'].value_counts().index,
        y=df['No_of_Earning_Members'].value_counts().values,
        ax=ax
    )
    ax.set_title('Bar Plot: Number of Earning Members')

display_plot('Bar Plot -  Qualified Members', bar_plot)
display_plot('Line Plot - Income vs Expense', line_plot)
display_plot('Bar Plot - Earning Members', bar_plot2)

st.subheader('Standard Deviation (first 5 numeric columns)')
st.write(df.select_dtypes(include='number').iloc[:,0:5].std())

st.subheader('Variance ( first 3 numeric columns)')
st.write(df.select_dtypes(include='number').iloc[:,0:3].var())

st.subheader('Count of Highest Qualified Member')
st.write(df['Highest_Qualified_Member'].value_counts())

st.success('Data Analysys of the Income & Expenditure Household Dataset Comleted!')

                                        


         
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ollama

def dataset_analysis(file_path):

    df = pd.read_csv(file_path)

    summary = df.describe(include='all').to_string()
    missing_values = df.isnull().sum().to_string()

    insights = generate_insights(summary)

    plot_paths = generate_visualization(df)

    report_text = (
        f"\n Data loaded successfully\n\n"
        f"{summary}\n\n"
        f"Missing Values:\n{missing_values}\n\n"
        f"Insights:\n{insights}\n"
    )

    return report_text, plot_paths

def generate_insights(df_summary):
    prompt = f"Analyze the dataset summary and provide insights:\n\n{df_summary}"
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

def generate_visualization(df):
    plot_paths = []

    if "Highest_Qualified_Member" in df.columns:
        plt.figure(figsize=(6,4))
        sns.barplot(
            x=df["Highest_QualifiedMember"].value_counts().index,
            y=df["Highest_Qualified_Member"].value_counts().values
        )
        plt.title("Bar graph of Highest Qualified Members")
        path = "Highest_Qualified_Member_dist.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    numeric_df = df.select_dtypes(inclide=["number"])
    if not numeric_df.empty:
        plt.figure(figsize=(8,5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Correlation Heatmap")
        path = "correlation_heatmap.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    return plot_paths

app = gr.Interface(
    fn=dataset_analysis,
    inputs=gr.File(type="filepath", label="Upload CSV"),
    outputs=[
        gr.Textbox(label="DATASET REPORT"),
        gr.Gallery(label="Data Visualization")
    ],
    title="Income &  Expenditure Household Dataset",
    description="Upload any dataset to view the EDA report and data visualization"
)
app.launch(share=True)


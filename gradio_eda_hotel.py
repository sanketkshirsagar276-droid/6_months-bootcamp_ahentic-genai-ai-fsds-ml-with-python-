import gradio as gr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r'C:\Users\Sanket kshirsagar\Downloads\hotel_bookings.csv')
df['children'].fillna(0, inplace=True)
df['total_guests'] = df['adults'] + df['children'] + df['babies']
df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']

def plot_graph(plot_type, x=None, y=None):
    plt.figure(figsize=(7,5))

    if plot_type == "Histogram":
        sns.histplot(df[x], bins=30, kde=True)

    elif plot_type == "Scatter":
        sns.scatterplot(data=df, x=x, y=y, hue="hotel", alpha=0.5)
    elif plot_type == "Boxplot":
        sns.boxplot(x=x, y=y, data=df)
        plt.xticks(rotation=45)
    elif plot_type == "Violin":
        sns.violinplot(x=x, y=y, data=df)
    elif plot_type == "Correlation Heatmap":
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")

    plt.tight_layout()
    return plt.gcf()

plot_types = ["Histogram", "Scatter", "Boxplot", "Violin", "Correlation Heatmap"]

with gr.Blocks() as demo:
    gr.Markdown(" Hotel Bookings EDA (Gradio)")
    
    plot_type = gr.Dropdown(plot_types, value="Histogram", label="Select Plot Type")
    x = gr.Dropdown(df.columns.tolist(), value="lead_time", label="X-axis")
    y = gr.Dropdown(df.columns.tolist(), value="adr", label="Y-axis (for Scatter/Boxplot/Violin)")
   
    plot_btn = gr.Button("Generate Plot")
    plot_out = gr.Plot()

    plot_btn.click(fn=plot_graph, inputs=[plot_type, x, y], outputs=plot_out)

demo.launch()
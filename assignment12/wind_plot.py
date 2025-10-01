import plotly.express as px
import plotly.data as pldata
import pandas as pd

def main():
    df = pldata.wind(return_type="pandas")
    print("=== FIRST 10 ROWS ===")
    print(df.head(10).to_string(index=False))
    print("\n=== LAST 10 ROWS ===")
    print(df.tail(10).to_string(index=False))
    if df['strength'].dtype == object or not pd.api.types.is_numeric_dtype(df['strength']):
        df['strength'] = df['strength'].astype(str).str.replace(r'[^0-9.\-]', '', regex=True)
        df['strength'] = pd.to_numeric(df['strength'], errors='coerce')
    df = df.dropna(subset=['strength', 'frequency', 'direction'])
    fig = px.scatter(
        df,
        x="frequency",
        y="strength",
        color="direction",
        title="Wind Strength vs Frequency (colored by direction)",
        labels={"frequency": "Frequency", "strength": "Strength"}
    )
    fig.write_html("wind.html")
    print("\nSaved interactive plot to wind.html")
    fig.show()

if __name__ == "__main__":
    main()

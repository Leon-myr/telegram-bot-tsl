import pandas as pd
import os

def load_basket():
    # Buduje ścieżkę do basket.csv w katalogu głównym projektu
    base = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(base, '..', 'basket.csv'))
    df = pd.read_csv(path)
    return df

if __name__ == '__main__':
    df = load_basket()
    print("=== Podsumowanie koszyka ===")
    print(df)
    print("Suma wartości:", df['value'].sum())
    perc = (df['value'] / df['limit'] * 100).round(2)
    print("Średnie wykorzystanie limitu (%):", perc.mean())


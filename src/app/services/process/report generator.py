from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from app.models.alerts_model import Alert
from app.models.event_model import Event


def plot_event_distribution(events: list[Event], output="reports/event_distribution.png"):
    df = pd.DataFrame([e.raw for e in events])
    df['level'] = df['level'].str.upper()
    counts = df['level'].value_counts()
    plt.figure(figsize=(8, 6))
    counts.plot(kind='bar', color='#3498db', edgecolor='black')
    plt.title("Distribution des niveaux d'événements")
    plt.xlabel("Niveau")
    plt.ylabel("Nombre")
    plt.xticks(rotation=0)
    plt.tight_layout()
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output)

def generate_pdf(events: list[Event], alerts: list[Alert], graph_path="reports/event_distribution.png", output="reports/report.pdf"):
    total = len(events)
    critical = sum(1 for e in events if e.level == "CRITICAL")

    plot_event_distribution(events, graph_path)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Rapport de Surveillance", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, f"Total événements : {total}", ln=True)
    pdf.cell(200, 10, f"Événements critiques : {critical}", ln=True)
    pdf.cell(200, 10, f"Alertes : {len(alerts)}", ln=True)
    pdf.ln(10)

    df = pd.DataFrame([e.raw for e in events])
    df['level'] = df['level'].str.upper()
    counts = df['level'].value_counts().reset_index()
    counts.columns = ["Niveau", "Nombre"]
    moyenne = round(counts["Nombre"].mean(), 2)

    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, f"Statistiques par niveau (moyenne: {moyenne})", ln=True, align="C")
    pdf.ln(5)

    # Table setup
    table_width = 140  # Reduced total width
    col_width = table_width / 2
    margin_left = (210 - table_width) / 2  # Center the table in A4 (210mm wide)

    pdf.set_x(margin_left)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(col_width, 8, "Niveau", border=1, fill=True, align="C")
    pdf.cell(col_width, 8, "Nombre", border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Arial", size=11)
    for _, row in counts.iterrows():
        pdf.set_x(margin_left)
        pdf.cell(col_width, 8, str(row["Niveau"]), border=1, align="C")
        pdf.cell(col_width, 8, str(row["Nombre"]), border=1, align="C")
        pdf.ln()

    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for alert in alerts:
        pdf.cell(200, 10, f"Alerte à {alert.triggered_at.isoformat()} ({len(alert.events)} événements)", ln=True)

    pdf.image(graph_path, w=180)
    pdf.output(output)
    print(f"[+] Rapport PDF généré : {output}")

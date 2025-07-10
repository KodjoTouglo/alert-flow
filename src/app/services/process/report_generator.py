import webbrowser
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

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

def generate_html(
    events: list[Event],
    alerts: list[Alert],
    image_path="reports/event_distribution.png",
    output="reports/report.html",
    interactive: bool = True
):
    total = len(events)
    critical = sum(1 for e in events if e.level == "CRITICAL")
    df = pd.DataFrame([e.raw for e in events])
    level_counts = df["level"].str.upper().value_counts()
    stats_df = level_counts.to_frame().reset_index()
    stats_df.columns = ["Niveau", "Nombre"]
    moyenne = round(stats_df["Nombre"].mean(), 2)
    stats_html = stats_df.to_html(index=False, classes="stats-table")

    plot_event_distribution(events, image_path)

    html = f"""
    <html>
    <head>
        <title>Rapport</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f8f9fa; color: #333; margin: 20px; }}
            h1 {{ color: #c0392b; }}
            .stats-table {{ border-collapse: collapse; width: 50%; margin-top: 20px; }}
            .stats-table th, .stats-table td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            .stats-table th {{ background-color: #f1f1f1; }}
            ul {{ background: #fff3cd; padding: 10px; border-radius: 5px; list-style-type: none; }}
            ul li {{ margin: 5px 0; padding: 5px; }}
            img {{ border: 1px solid #ccc; margin-top: 20px; display: block; margin-left: auto; margin-right: auto; max-height: 600px; }}
            select {{ padding: 5px; margin: 10px 0; border-radius: 4px; border: 1px solid #ccc; }}
            .fade-out {{ opacity: 0; transform: translateX(20px); transition: all 0.3s ease; }}
            .fade-in {{ opacity: 1; transform: translateX(0); transition: all 0.3s ease; }}
        </style>
    </head>
    <body>
        <h1>Rapport de Surveillance</h1>
        <p><b>Événements totaux :</b> {total}</p>
        <p><b>Critiques :</b> {critical}</p>
        <p><b>Alertes :</b> {len(alerts)}</p>

        {'''
        <h2>Filtrage interactif</h2>
        <label for="filter">Afficher uniquement les événements de niveau :</label>
        <select id="filter" onchange="filterTable()">
            <option value="ALL">Tous</option>
            <option value="INFO">INFO</option>
            <option value="WARNING">WARNING</option>
            <option value="ERROR">ERROR</option>
            <option value="CRITICAL">CRITICAL</option>
        </select>
        ''' if interactive else ''}

        <h2>Statistiques par niveau (Moyenne: {moyenne})</h2>
        {stats_html}

        <h2>Alertes détectées</h2>
        <ul id="alertList">
        {''.join(f"<li data-level='{e.level}'>{a.triggered_at.isoformat()} ({len(a.events)} événements)</li>" for a in alerts for e in a.events)}
        </ul>

        <h2>Graphique</h2>
        <div style="text-align: center;">
            <img src="{Path(image_path).name}" alt="Graphe"/>
        </div>

        {'''
        <script>
        function filterTable() {
            var select = document.getElementById("filter");
            var filter = select.value;

            var rows = document.querySelectorAll(".stats-table tbody tr");
            rows.forEach(function(row) {
                var cell = row.cells[0].textContent.toUpperCase();
                if (filter === "ALL" || cell === filter) {
                    row.classList.remove("fade-out");
                    row.classList.add("fade-in");
                    row.style.display = "";
                } else {
                    row.classList.add("fade-out");
                    setTimeout(() => { row.style.display = "none"; }, 300);
                }
            });

            var alerts = document.querySelectorAll("#alertList li");
            alerts.forEach(function(alert) {
                var level = alert.getAttribute("data-level");
                if (filter === "ALL" || level === filter) {
                    alert.classList.remove("fade-out");
                    alert.classList.add("fade-in");
                    alert.style.display = "";
                } else {
                    alert.classList.add("fade-out");
                    setTimeout(() => { alert.style.display = "none"; }, 300);
                }
            });
        }
        </script>
        ''' if interactive else ''}
    </body>
    </html>
    """
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as f:
        f.write(html)
    webbrowser.open(f"file://{Path(output).resolve()}")


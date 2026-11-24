import io
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def gerar_grafico(cidade, registros):
    rotulos = [datetime.fromisoformat(r["data"]).strftime("%d/%m") for r in registros]
    x = list(range(len(registros)))
    maximas = [r["temp_max"] for r in registros]
    minimas = [r["temp_min"] for r in registros]
    chuva = [r["chuva_mm"] or 0 for r in registros]
    cores = ["#f59e0b" if r["tipo"] == "hoje" else "#60a5fa" for r in registros]
    idx_hoje = next((i for i, r in enumerate(registros) if r["tipo"] == "hoje"), None)

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [2, 1]}
    )

    ax1.plot(x, maximas, marker="o", color="#ef4444", label="Máxima")
    ax1.plot(x, minimas, marker="o", color="#3b82f6", label="Mínima")
    ax1.fill_between(x, minimas, maximas, color="#fca5a5", alpha=0.25)
    for i in x:
        ax1.annotate(f"{maximas[i]:.0f}°", (i, maximas[i]), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
        ax1.annotate(f"{minimas[i]:.0f}°", (i, minimas[i]), textcoords="offset points", xytext=(0, -14), ha="center", fontsize=9)
    ax1.set_ylabel("Temperatura (°C)")
    ax1.set_title(f"Clima em {cidade}")
    ax1.grid(alpha=0.3)
    ax1.margins(x=0.08, y=0.2)
    ax1.legend(loc="upper right", ncol=2)

    ax2.bar(x, chuva, color=cores)
    ax2.set_ylabel("Chuva (mm)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(rotulos)
    ax2.grid(axis="y", alpha=0.3)

    if idx_hoje is not None:
        for ax in (ax1, ax2):
            ax.axvline(idx_hoje, color="#f59e0b", linestyle="--", alpha=0.7)
        ax1.text(idx_hoje, ax1.get_ylim()[1], " hoje", color="#f59e0b", va="top")

    fig.tight_layout()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=110)
    plt.close(fig)
    return buffer.getvalue()

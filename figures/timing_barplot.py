import numpy as np

from matplotlib.figure import Figure
import matplotlib
from matplotlib import rcParams

from pathlib import Path

rcParams.update({"font.size": 14})


def plot_times(
    analyses,
    mean_times,
    mean_uncertainties,
    single_node_times,
    machine_name,
    max_time,
    scale="linear",
):
    fig = Figure()
    fig.set_size_inches(7, 5)
    ax = fig.subplots()

    x = np.arange(len(analyses))
    width = 0.35

    ax.bar(x, mean_times, width=width, label="Wall time")
    bin_bottom = np.array(mean_times) - np.array(mean_uncertainties)
    ax.bar(
        x,
        height=2 * np.array(mean_uncertainties),
        width=width,
        bottom=bin_bottom,
        fill=False,
        linewidth=0,
        edgecolor="gray",
        hatch=3 * "/",
        label="Uncertainty",
    )
    ax.bar(x + width, single_node_times, width=width, label="Single node")

    text_left_edge = 0.66
    ax.text(
        text_left_edge, 0.68, "Nodes per block = 1", transform=ax.transAxes, size=10
    )
    ax.text(text_left_edge, 0.63, "Max blocks = 4", transform=ax.transAxes, size=10)

    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(analyses, rotation=10, size=10)
    ax.set_yscale(scale)
    if scale != "log":
        ax.set_ylim(top=max_time)

    ax.set_title(f"{machine_name}")
    ax.set_xlabel("Published analysis probability model")
    ax.set_ylabel("Evaluation time (seconds)")
    ax.legend(loc="best", frameon=False)
    fig.tight_layout()

    file_path = Path().cwd().joinpath("figures")
    image_name = f"timing_barplot_{machine_name.lower()}"
    if scale == "log":
        image_name += "_log"
    file_path = file_path.joinpath(image_name + ".png")
    fig.savefig(file_path)


if __name__ == "__main__":
    analyses = [
        "Eur. Phys. J. C 80 (2020) 691",
        "JHEP 06 (2020) 46",
        "Phys. Rev. D 101 (2020) 032009",
    ]
    mean_times = [156.2, 31.2, 57.4]
    mean_uncertainties = [9.5, 2.7, 5.2]
    single_node_times = [3842, 114, 612]
    machine_name = "RIVER"

    max_time = 4000

    plot_times(
        analyses,
        mean_times,
        mean_uncertainties,
        single_node_times,
        machine_name,
        max_time,
    )

    plot_times(
        analyses,
        mean_times,
        mean_uncertainties,
        single_node_times,
        machine_name,
        max_time,
        scale="log",
    )

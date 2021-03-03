from pathlib import Path
import numpy as np
import pandas as pd


def convert_to_seconds(time_str):
    minutes, seconds = time_str.split("m")
    total = 60 * int(minutes) + int(seconds.split(".")[0])
    return total


def main():
    mean_wall_time = []
    best_wall_time = []

    file_list = ["1Lbb", "InclSS3L", "staus"]
    for filename in file_list:
        file_path = Path("data").joinpath("river").joinpath(f"{filename}_times.txt")
        with open(file_path, "r") as readfile:
            lines = readfile.readlines()

        times = np.array([convert_to_seconds(line) for line in lines])
        mean_wall_time.append(f"${np.mean(times)}\pm{np.std(times):.1f}$")

    single_node_time = []
    file_list = ["1Lbb", "InclSS3L", "staus"]
    for filename in file_list:
        file_path = (
            Path("data").joinpath("river").joinpath(f"{filename}_single_node_time.txt")
        )
        with open(file_path, "r") as readfile:
            time = readfile.readlines()[0]
        single_node_time.append(convert_to_seconds(time))

    table_data = pd.DataFrame(
        dict(
            # analysis=["ATLAS SUSY 1Lbb", "ATLAS SUSY SS3L", "ATLAS SUSY staus"],
            analysis=[
                "Eur. Phys. J. C 80 (2020) 691",
                "JHEP 06 (2020) 46",
                "Phys. Rev. D 101 (2020) 032009",
            ],
            patches=[125, 76, 57],
            worker_nodes=[85, 85, 85],
            mean_wall_time=mean_wall_time,
            single_node_time=single_node_time,
        )
    )

    caption = (
        "Fit times for analyses using \pyhf{}'s NumPy backend and SciPy optimizer orchestrated with \\funcX{} on RIVER"
        + f" over {len(times)} trials compared to a single RIVER node."
        + " The reported wall fit time is the mean wall fit time of the trials."
        + " The uncertainty on the mean wall time corresponds to the standard deviation of the wall fit times."
        + " The number of worker nodes used is approximate as per-run reporting is not available."
    )
    performance_table_latex = table_data.to_latex(
        header=[
            "Analysis",
            "Patches",
            "Workers",
            "Wall time (sec)",
            "Single node (sec)",
        ],
        caption=caption,
        label="table:performance",
        index=False,
        escape=False,
        float_format="{:0.1f}".format,
        column_format="@{}lrrrr@{}",
        position="htpb",
    )

    with open("src/tables/performance_table.tex", "w") as table_file:
        table_file.write(performance_table_latex)


if __name__ == "__main__":
    main()

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

    file_list = ["1Lbb_times.txt"]
    for filename in file_list:
        file_path = Path("data").joinpath(filename)
        with open(file_path, "r") as readfile:
            lines = readfile.readlines()

        times = np.array([convert_to_seconds(line) for line in lines])
        mean_wall_time.append(f"${np.mean(times)}\pm{np.std(times):.1f}$")
        best_wall_time.append(np.min(times))

    # Remove later
    mean_wall_time.append("???")
    best_wall_time.append("???")

    table_data = pd.DataFrame(
        dict(
            analysis=["ATLAS SUSY 1Lbb", "ATLAS SUSY XXXX"],
            worker_nodes=[85, 85],
            mean_wall_time=mean_wall_time,
            best_wall_time=best_wall_time,
        )
    )

    caption = (
        f"Fitting performance on RIVER for analyses for {len(times)} trials."
        + " The uncertainty on the mean wall time corresponds to the standard deviation of the fit times."
    )
    performance_table_latex = table_data.to_latex(
        header=[
            "Analysis",
            "Worker nodes",
            "Mean wall time (sec)",
            "Best wall time (sec)",
        ],
        caption=caption,
        label="table:performance",
        index=False,
        escape=False,
        float_format="{:0.1f}".format,
        column_format="@{}lrrr@{}",
        position="htpb",
    )

    with open("src/tables/performance_table.tex", "w") as table_file:
        table_file.write(performance_table_latex)


if __name__ == "__main__":
    main()

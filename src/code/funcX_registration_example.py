import json
from pathlib import Path
from time import sleep

from funcx.sdk.client import FuncXClient
from pyhf.contrib.utils import download


def prepare_workspace(data):
    import pyhf

    return pyhf.Workspace(data)


if __name__ == "__main__":
    # locally get pyhf pallet for analysis
    if not Path("1Lbb-pallet").exists():
        download("https://doi.org/10.17182/hepdata.90607.v3/r3", "1Lbb-pallet")
    with open("1Lbb-pallet/BkgOnly.json") as bkgonly_json:
        bkgonly_workspace = json.load(bkgonly_json)

    # Use privately assigned endpoint id
    with open("endpoint_id.txt") as endpoint_file:
        pyhf_endpoint = str(endpoint_file.read().rstrip())

    fxc = FuncXClient()

    # Register function and execute on worker node
    prepare_func = fxc.register_function(prepare_workspace)
    prepare_task = fxc.run(
        bkgonly_workspace, endpoint_id=pyhf_endpoint, function_id=prepare_func
    )

    # Wait for worker to finish and retrieve results
    workspace = None
    while not workspace:
        try:
            workspace = fxc.get_result(prepare_task)
        except Exception as excep:
            print(f"prepare: {excep}")
            sleep(10)

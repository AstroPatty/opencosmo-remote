from enum import Enum
from pathlib import Path
from typing import Optional
from warnings import warn

from opencosmo_remote.messages.open_pb2 import DataType

"""
Basic organization of data is as follows:

analysis/                           snapshot data
    halos/
        step_##/                    step number
            haloproperties/         halo properties
            sodbighaloparticles/    halo particles
            sodpropertybins/        sod profiles
            # if hydro
            galaxyproperties/       galaxy properties
            galaxyparticles/        galaxy particles

analysis-lightcone                  lightcone data 
    maps/                           lightcone maps
    halos/                          lightcone halos
        step_##/
            haloproperties/         haloproperties
            sodbighaloparticles/    halo particles
            sodpropertybins/        sod profiles
            # if hydro
            galaxyproperties/       galaxy properties
            galaxyparticlces/       galaxy particles

If no analysis or analysis-lightcone directory is found, we assume that
this is a multi-simulation directory (e.g. the SCIDAC runs).
"""


class ProjectionType(Enum):
    SNAPSHOT = "snapshot"
    LIGHTCONE = "lightcone"


class DatasetType(Enum):
    HALOS = "halos"
    MAPS = "maps"


DataTypePaths = dict[DataType, Path]  # dictionary of data types and paths
DataSlicePaths = dict[int, DataTypePaths]  # dictionary of step numbers to data paths
DatasetPaths = dict[ProjectionType, DataSlicePaths]
SimulationPaths = dict[str, DatasetPaths]


def get_dataset_type_paths(path: Path):
    output = {}
    children = filter(lambda p: p.is_dir(), path.glob("*"))
    for child in children:
        match child.name:
            case "halos":
                output[DatasetType.HALOS] = child
            case "maps":
                output[DatasetType.MAPS] = child
            case _:
                warn(f"Unknown dataset type {child.name} found in {path}")
    if not output:
        raise ValueError(f"No dataset type directories found in {path}")
    return output


def get_projection_paths(path: Path):
    output = {}
    children = filter(lambda p: p.is_dir(), path.glob("*"))
    for child in children:
        match child.name:
            case "analysis":
                output[ProjectionType.SNAPSHOT] = child
            case "analysis-lightcone":
                output[ProjectionType.LIGHTCONE] = child
            case _:
                warn(f"Unknown dataset directory: {child}")
    if not output:
        raise ValueError(f"No dataset directories found in {path}")
    return output


def get_step_paths(path: Path):
    output = {}
    children = filter(
        lambda p: p.is_dir() and p.name.startswith("step_"), path.glob("*")
    )
    for child in children:
        step_number = int(child.name.split("_")[1])
        output[step_number] = child

    if not output:
        raise ValueError(f"Found no step folders at {path}")

    return output


def get_halo_datatype_paths(path: Path, step_number: int):
    output = {}
    children = filter(lambda p: p.is_dir(), path.glob("*"))
    for child in children:
        files = child.glob("*")
        file = list(
            filter(
                lambda p: p.name.endswith(child.name)
                or p.name.endswith(child.name + ".hdf5"),
                files,
            )
        )
        if len(file) != 1:
            raise ValueError(f"Unable to find a unique master file in {child}")
        match child.name:
            case "haloproperties":
                output[DataType.HALO_PROPERTIES] = file[0]
            case "sodpropertybins":
                output[DataType.HALO_PROFILES] = file[0]
            case "galaxypropertybins":
                output[DataType.GALAXY_PROFILES] = file[0]

            case "sodbighaloparticles":
                output[DataType.HALO_PARTICLES] = file[0]
            case "galaxyproperties":
                output[DataType.GALAXY_PROPERTIES] = file[0]

            case "galaxyparticles":
                output[DataType.GALAXY_PARTICLES] = file[0]
            case _:
                warn(
                    f"Unknown data type directory {child.name} found in directory {path}"
                )
    if not output:
        raise ValueError(f"Found no data type directories at path {path}")
    outputs = {}
    for dtype, dtype_path in output.items():
        hdf5_path = dtype_path.with_suffix(dtype_path.suffix + ".hdf5")
        if dtype_path.exists():  # genericio data
            outputs[dtype] = dtype_path
        elif hdf5_path.exists():  # hdf5 data
            outputs[dtype] = hdf5_path
        else:
            raise ValueError(
                f"Found a folder for data type {dtype.value}, but didn't find a root file at {dtype_path} or {hdf5_path}"
            )

    return outputs


def get_simulation_paths(
    path: Path,
    dataset_type: DatasetType,
    step_numbers: Optional[int | list[int]] = None,
    lightcone: bool = False,
) -> DatasetPaths:
    projection_type = ProjectionType.LIGHTCONE if lightcone else ProjectionType.SNAPSHOT

    projection_paths = get_projection_paths(path)
    projection_path = projection_paths.get(projection_type)
    if projection_path is None:
        raise ValueError(
            f"Unable to find path for {'lightcones' if lightcone else 'snapshots'} in {path}"
        )

    try:
        dataset_type_paths = get_dataset_type_paths(projection_path)
        dataset_type_path = dataset_type_paths.get(dataset_type)
    except ValueError:
        dataset_type_path = (
            projection_path  # Compatability with old organization scheme
        )

    if dataset_type_path is None:
        raise ValueError(
            f"Expected a {dataset_type.value} directory in {projection_path}"
        )

    if isinstance(step_numbers, int):
        step_numbers = [step_numbers]
    step_paths = get_step_paths(dataset_type_path)
    if step_numbers is not None:
        missing = set(step_numbers).difference(step_paths.keys())
        if missing:
            raise ValueError(f"Missing folders for requested steps {missing}")
    else:
        step_numbers = step_paths.keys()

    step_output = {}
    for step in step_numbers:
        datatype_paths = get_halo_datatype_paths(step_paths[step], step)
        step_output[step] = datatype_paths

    return {projection_type: step_output}


def get_halo_paths(
    base_path: Path,
    step_numbers: Optional[int | list[int]] = None,
    dtypes: Optional[list[str]] = None,
    lightcone: bool = False,
    flatten: bool = False,
) -> DatasetPaths | SimulationPaths:
    """
    Discover the paths available under the path provided by the SIMULATION_DATA_PATH
    environment variable. If this environment variable is not set, default to /data
    (which is where data will be mounted in containerized runs).
    """
    base_path = Path(base_path)
    children = list(filter(lambda p: p.is_dir(), base_path.glob("*")))
    child_names = [child.name for child in children]
    output = {}
    if "analysis" not in child_names and "analysis-lightcone" not in child_names:
        # working with multiple simulations
        for child in children:
            output[child.name] = get_simulation_paths(
                child, DatasetType.HALOS, step_numbers, lightcone
            )
        output
    output = get_simulation_paths(base_path, DatasetType.HALOS, step_numbers, lightcone)

    if dtypes is not None:
        dtypes_to_get = list(map(lambda dt: getattr(DataType, dt), dtypes))
        output = __filter_dtypes(output, dtypes_to_get)

    if flatten:
        return __flatten(output)
    return output


def __filter_dtypes(paths: dict, dtypes: list[int]):
    output = {}
    for name, item in paths.items():
        if isinstance(item, Path) and name in dtypes:
            output[name] = item
        elif isinstance(item, dict):
            output[name] = __filter_dtypes(item, dtypes)
    return output


def __flatten(paths: dict):
    output = []
    for key, val in paths.items():
        if isinstance(val, Path):
            output.append(val)
        else:
            output.extend(__flatten(val))
    return output

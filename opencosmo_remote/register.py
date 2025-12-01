from pathlib import Path

import click

from opencosmo_remote.paths import get_halo_paths
from opencosmo_remote.store import write


@click.group()
def cli():
    pass


@cli.command(name="register")
@click.argument("dataset_name", required=True)
@click.argument("dataset_path", type=click.Path(exists=True), required=True)
def register_dataset(dataset_name: str, dataset_path: Path):
    dataset_path = Path(dataset_path).resolve()
    # Verify this is a valid dataset
    _ = get_halo_paths(dataset_path)

    write(dataset_name, str(dataset_path))

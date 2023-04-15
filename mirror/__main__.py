import os
from functools import partial

import click
from hfmirror.storage import HuggingfaceStorage
from hfmirror.sync import SyncTask
from huggingface_hub import HfApi

from .plantuml import PlantumlMirrorResource
from .utils import GLOBAL_CONTEXT_SETTINGS, print_version

_RESOURCE_CLASS = {
    'plantuml': PlantumlMirrorResource,
}


@click.group(context_settings={**GLOBAL_CONTEXT_SETTINGS}, help='Utils for sync data.')
@click.option('-v', '--version', is_flag=True,
              callback=partial(print_version, 'mirror'), expose_value=False, is_eager=True,
              help="Show version information.")
def cli():
    pass  # pragma: no cover


@cli.command('sync', help="Transport files to huggingface",
             context_settings={**GLOBAL_CONTEXT_SETTINGS})
@click.option('--resource', '-R', 'resource', type=click.Choice(list(_RESOURCE_CLASS.keys())), required=True,
              help='Resource for sync.')
@click.option('--repo', '-r', 'repo', type=str, default='HansBug/opensource_mirror',
              help='Repository to upload.', show_default=True)
@click.option('--namespace', '-n', 'namespace', type=str, default=None,
              help="Namespace to upload. Resource will be used when not given.", show_default=True)
def sync(resource, repo, namespace):
    namespace = resource if namespace is None else namespace
    sync = _RESOURCE_CLASS[resource]()

    api = HfApi(token=os.environ.get('HF_TOKEN'))
    api.create_repo(repo, repo_type='dataset', exist_ok=True)
    storage = HuggingfaceStorage(repo, hf_client=api, namespace=namespace)

    task = SyncTask(sync, storage)
    task.sync()


if __name__ == '__main__':
    cli()

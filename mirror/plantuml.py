from typing import Optional

from hfmirror.resource import SourceForgeFilesResource


class PlantumlMirrorResource(SourceForgeFilesResource):
    def __init__(self):
        SourceForgeFilesResource.__init__(self, 'plantuml')

    def _get_version(self, type_, segments) -> Optional[str]:
        if len(segments) == 1 and type_ == 'directory':
            return segments[0]
        else:
            return None

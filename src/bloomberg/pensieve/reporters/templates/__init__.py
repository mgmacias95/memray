"""Templates to render reports in HTML."""
from functools import lru_cache
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Union

import jinja2

from bloomberg.pensieve import Metadata


@lru_cache(maxsize=1)
def get_render_environment() -> jinja2.Environment:
    return jinja2.Environment(
        loader=jinja2.PackageLoader("bloomberg.pensieve.reporters"),
    )


def get_report_title(*, kind: str, show_memory_leaks: bool) -> str:
    if show_memory_leaks:
        return f"{kind} report (memory leaks)"
    return f"{kind} report"


def render_report(
    *,
    kind: str,
    data: Union[Dict[str, Any], Iterable[Dict[str, Any]]],
    metadata: Metadata,
    show_memory_leaks: bool,
    merge_threads: bool,
) -> str:
    env = get_render_environment()
    template = env.get_template(kind + ".html")

    title = get_report_title(kind=kind, show_memory_leaks=show_memory_leaks)
    return template.render(
        kind=kind,
        title=title,
        data=data,
        metadata=metadata,
        show_memory_leaks=show_memory_leaks,
        merge_threads=merge_threads,
    )

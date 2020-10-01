"""baseline tools for working with repos"""

import ipywidgets as W
import traitlets as T

from ..repos.repo_base import Repo


class HeadPicker(W.VBox):
    """a simple dropdown-based picker of current DVCS heads"""

    # pylint: disable=no-self-use

    repo = T.Instance(Repo)
    picker = T.Instance(W.DOMWidget)
    refresh_btn = T.Instance(W.Button)

    _repo_link = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_btn.on_click(self.refresh)
        self.children = [self.picker, self.refresh_btn]

    def refresh(self, *args, **kwargs):
        """refresh the heads"""
        # pylint: disable=protected-access
        if self.repo is not None:
            self.repo._update_heads()

    @T.observe("repo")
    def _on_repo_changed(self, change):
        """react to the repo changing"""
        if self._repo_link is not None:
            self._repo_link.unlink()
            self._repo_link = None

        if change.new:
            self._repo_link = T.dlink((change.new, "heads"), (self.picker, "options"))

    @T.default("picker")
    def _default_picker(self):
        """a default picker"""
        return W.Dropdown()

    @T.default("refresh_btn")
    def _default_refresh_btn(self):
        """a default refresh button"""
        return W.Button(icon="refresh")

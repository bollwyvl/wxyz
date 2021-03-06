""" Full Screen widget
"""
# pylint: disable=too-many-ancestors
from .base import HTMLBase, T, W


@W.register
class Fullscreen(HTMLBase, W.Box):
    """ A full screen container
    """

    _model_name = T.Unicode("FullscreenModel").tag(sync=True)
    _view_name = T.Unicode("FullscreenView").tag(sync=True)

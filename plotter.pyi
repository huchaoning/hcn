from numpy.typing import ArrayLike

def plot(
    x: ArrayLike | tuple, 
    y: ArrayLike | function, 
    fmt: str, 
    dots: int, 
    alpha: float, 
    xerr: ArrayLike, 
    yerr: ArrayLike, 
    capsize: float,

    figsize: tuple, 
    axis: bool, 
    grid: bool, 
    xlabel: str, 
    ylabel: str, 
    title: str,
    xlim: tuple, 
    ylim: tuple, 
    legend: bool, 
    label: str, 
    save: bool | str, 
    override: bool, 
    show: bool
):  pass

def scatter(
    x: ArrayLike, 
    y: ArrayLike, 
    s: ArrayLike, 
    c: str, 
    marker: str, 
    alpha: float, 
    xerr: ArrayLike, 
    yerr: ArrayLike, 
    capsize: float,

    figsize: tuple, 
    axis: bool, 
    grid: bool, 
    xlabel: str, 
    ylabel: str, 
    title: str,
    xlim: tuple, 
    ylim: tuple, 
    legend: bool, 
    label: str, 
    save: bool | str, 
    override: bool, 
    show: bool
):  pass


def hist(
    x: ArrayLike, 
    bins: int, 
    histtype: str, 
    density: bool,

    figsize: tuple, 
    axis: bool, 
    grid: bool, 
    xlabel: str, 
    ylabel: str, 
    title: str,
    xlim: tuple, 
    ylim: tuple, 
    legend: bool, 
    label: str, 
    save: bool | str, 
    override: bool, 
    show: bool
):  pass


def imshow(
    x: ArrayLike, 
    cmap: str, 
    pillow: bool, 
    colorbar:bool,

    figsize: tuple, 
    axis: bool, 
    grid: bool, 
    xlabel: str, 
    ylabel: str, 
    title: str,
    xlim: tuple, 
    ylim: tuple, 
    legend: bool, 
    label: str, 
    save: bool | str, 
    override: bool, 
    show: bool
):  pass
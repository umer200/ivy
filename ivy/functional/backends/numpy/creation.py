# global
import numpy
import numpy as np
from typing import Union, Optional, List, Sequence

# local
import ivy
from .data_type import as_native_dtype
from ivy.functional.ivy import default_dtype
from ivy.functional.backends.numpy.device import _to_device


# Array API Standard #
# -------------------#


def arange(
    start,
    stop=None,
    step=1,
    *,
    dtype: np.dtype = None,
    device: str,
    out: Optional[np.ndarray] = None
):
    if dtype:
        dtype = as_native_dtype(dtype)
    res = _to_device(np.arange(start, stop, step=step, dtype=dtype), device=device)
    if not dtype:
        if res.dtype == np.float64:
            return res.astype(np.float32)
        elif res.dtype == np.int64:
            return res.astype(np.int32)
    return res


def asarray(
    object_in,
    *,
    copy=None,
    dtype: np.dtype = None,
    device: str,
    out: Optional[np.ndarray] = None
):
    # If copy=none then try using existing memory buffer
    if isinstance(object_in, np.ndarray) and dtype is None:
        dtype = object_in.dtype
    elif (
        isinstance(object_in, (list, tuple, dict))
        and len(object_in) != 0
        and dtype is None
    ):
        dtype = default_dtype(item=object_in, as_native=True)
        if copy is True:
            return _to_device(
                np.copy(np.asarray(object_in, dtype=dtype)), device=device
            )
        else:
            return _to_device(np.asarray(object_in, dtype=dtype), device=device)
    else:
        dtype = default_dtype(dtype, object_in)
    if copy is True:
        return _to_device(np.copy(np.asarray(object_in, dtype=dtype)), device=device)
    else:
        return _to_device(np.asarray(object_in, dtype=dtype), device=device)


def empty(
    shape: Union[ivy.NativeShape, Sequence[int]],
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    return _to_device(
        np.empty(shape, as_native_dtype(default_dtype(dtype))), device=device
    )


def empty_like(
    x: np.ndarray,
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    if dtype:
        dtype = "bool_" if dtype == "bool" else dtype
        dtype = np.dtype(dtype)
    else:
        dtype = x.dtype

    return _to_device(np.empty_like(x, dtype=dtype), device=device)


def eye(
    n_rows: int,
    n_cols: Optional[int] = None,
    k: Optional[int] = 0,
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    dtype = as_native_dtype(default_dtype(dtype))
    return _to_device(np.eye(n_rows, n_cols, k, dtype), device=device)


# noinspection PyShadowingNames
def from_dlpack(
    x,
    *,
    out: Optional[np.ndarray] = None
):
    return np.from_dlpack(x)


def full(
    shape: Union[ivy.NativeShape, Sequence[int]],
    fill_value: Union[int, float],
    *,
    dtype: np.dtype = None,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    return _to_device(
        np.full(shape, fill_value, as_native_dtype(default_dtype(dtype, fill_value))),
        device=device,
    )


def full_like(
    x: np.ndarray,
    fill_value: Union[int, float],
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    if dtype:
        dtype = "bool_" if dtype == "bool" else dtype
    else:
        dtype = x.dtype
    return _to_device(np.full_like(x, fill_value, dtype=dtype), device=device)


def linspace(
    start,
    stop,
    num,
    axis=None,
    endpoint=True,
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
):
    if axis is None:
        axis = -1
    ans = np.linspace(start, stop, num, endpoint, dtype=dtype, axis=axis)
    if dtype is None:
        ans = np.float32(ans)
    # Waiting for fix when start is -0.0: https://github.com/numpy/numpy/issues/21513
    if (
        ans.shape[0] >= 1
        and (not isinstance(start, numpy.ndarray))
        and (not isinstance(stop, numpy.ndarray))
    ):
        ans[0] = start
    return _to_device(ans, device=device)


def meshgrid(
    *arrays: np.ndarray,
    indexing: str = "xy"
) -> List[np.ndarray]:
    return np.meshgrid(*arrays, indexing=indexing)


def ones(
    shape: Union[ivy.NativeShape, Sequence[int]],
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    dtype = as_native_dtype(default_dtype(dtype))
    return _to_device(np.ones(shape, dtype), device=device)


def ones_like(
    x: np.ndarray,
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    if dtype:
        dtype = "bool_" if dtype == "bool" else dtype
        dtype = np.dtype(dtype)
    else:
        dtype = x.dtype

    return _to_device(np.ones_like(x, dtype=dtype), device=device)


def tril(
    x: np.ndarray,
    k: int = 0,
    *,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    return np.tril(x, k)


def triu(
    x: np.ndarray,
    k: int = 0,
    *,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    return np.triu(x, k)


def zeros(
    shape: Union[ivy.NativeShape, Sequence[int]],
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    return _to_device(np.zeros(shape, dtype), device=device)


def zeros_like(
    x: np.ndarray,
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    if dtype:
        dtype = "bool_" if dtype == "bool" else dtype
    else:
        dtype = x.dtype
    return _to_device(np.zeros_like(x, dtype=dtype), device=device)


# Extra #
# ------#


array = asarray


def logspace(
    start,
    stop,
    num,
    base=10.0,
    axis=None,
    *,
    device: str,
    out: Optional[np.ndarray] = None
):
    if axis is None:
        axis = -1
    return _to_device(
        np.logspace(start, stop, num, base=base, axis=axis), device=device
    )

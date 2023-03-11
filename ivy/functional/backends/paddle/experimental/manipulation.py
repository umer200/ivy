from typing import Optional, Union, Sequence, Tuple, NamedTuple, List
from numbers import Number
from .. import backend_version
from ivy.func_wrapper import with_unsupported_dtypes, with_unsupported_device_and_dtypes
import paddle
from ivy.utils.exceptions import IvyNotImplementedException
import ivy


@with_unsupported_dtypes(
    {"2.4.2 and below": ('int8', 'int16', 'uint8', 'uint16')},
    backend_version,
)
def moveaxis(
    a: paddle.Tensor,
    source: Union[int, Sequence[int]],
    destination: Union[int, Sequence[int]],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.moveaxis(a, source, destination)


@with_unsupported_dtypes(
    {"2.4.2 and below": ('int8', 'int16', 'uint8', 'uint16', 'bfloat16',
                         'float16', 'complex64', 'complex128', 'bool')},
    backend_version,
)
def heaviside(
    x1: paddle.Tensor,
    x2: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.heaviside(x1, x2)


def flipud(
    m: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def vstack(
    arrays: Sequence[paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def hstack(
    arrays: Sequence[paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def rot90(
    m: paddle.Tensor,
    /,
    *,
    k: Optional[int] = 1,
    axes: Optional[Tuple[int, int]] = (0, 1),
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


@with_unsupported_dtypes(
    {"2.4.2 and below": ("uint16", "bfloat16", "complex64", "complex128", "bool")},
    backend_version,
)
def top_k(
    x: paddle.Tensor,
    k: int,
    /,
    *,
    axis: Optional[int] = -1,
    largest: Optional[bool] = True,
    out: Optional[Tuple[paddle.Tensor, paddle.Tensor]] = None,
) -> Tuple[paddle.Tensor, paddle.Tensor]:
    topk_res = NamedTuple("top_k", [("values", paddle.Tensor), 
                                    ("indices", paddle.Tensor)])
    val, indices = paddle.topk(x, k, axis=axis, largest=largest)
    return topk_res(val, indices)
    

@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("int8", "int16", "uint8", "uint16", "bfloat16", "float16")}}, backend_version
)
def fliplr(
    m: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.flip(m, axis=1)


def i0(
    x: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def flatten(
    x: paddle.Tensor,
    /,
    *,
    start_dim: Optional[int] = 0,
    end_dim: Optional[int] = -1,
    order: Optional[str] = "C",
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def vsplit(
    ary: paddle.Tensor,
    indices_or_sections: Union[int, Tuple[int, ...]],
    /,
) -> List[paddle.Tensor]:
    raise IvyNotImplementedException()


def dsplit(
    ary: paddle.Tensor,
    indices_or_sections: Union[int, Tuple[int, ...]],
    /,
) -> List[paddle.Tensor]:
    raise IvyNotImplementedException()


def atleast_1d(*arys: paddle.Tensor) -> List[paddle.Tensor]:
    raise IvyNotImplementedException()


def dstack(
    arrays: Sequence[paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def atleast_2d(*arys: paddle.Tensor) -> List[paddle.Tensor]:
    raise IvyNotImplementedException()


def atleast_3d(*arys: Union[paddle.Tensor, bool, Number]) -> List[paddle.Tensor]:
    raise IvyNotImplementedException()


def take_along_axis(
    arr: paddle.Tensor,
    indices: paddle.Tensor,
    axis: int,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def hsplit(
    ary: paddle.Tensor,
    indices_or_sections: Union[int, Tuple[int, ...]],
    /,
) -> List[paddle.Tensor]:
    raise IvyNotImplementedException()


def broadcast_shapes(shapes: Union[List[int], List[Tuple]]) -> Tuple[int]:
    
    if len(shapes[0])==0 and len(shapes[1])==0:
        return shapes[0]
    elif len(shapes[0])==0 and not len(shapes[1])==0:
        return shapes[1]
    elif not len(shapes[0])==0 and len(shapes[1])==0:
        return shapes[0]
    else:
        return paddle.broadcast_shape(*shapes)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def expand(
    x: paddle.Tensor,
    shape: Union[List[int], List[Tuple]],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    shape = list(shape)
    
    for i, dim in enumerate(shape):
        if dim < 0:
            shape[i] = x.shape[i]
    if x.ndim == 0:
        if len(shape)==0:
            return x
        else:
            x = ivy.expand_dims(x,0)
    if x.ndim > len(shape):
        x = x.reshape([-1])
    
    if x.dtype in [paddle.int8, paddle.int16, paddle.uint8, paddle.float16,]:
        return paddle.expand(x.cast('float32'), shape).cast(x.dtype)
    elif x.dtype in [paddle.complex64, paddle.complex128]:
        x_real = paddle.expand(ivy.real(x).data,shape)
        x_imag = paddle.expand(ivy.imag(x).data,shape)
        return x_real + 1j * x_imag
    else:
        return paddle.expand(x, shape)

    

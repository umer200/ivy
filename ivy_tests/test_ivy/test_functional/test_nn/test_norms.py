"""Collection of tests for unified neural network layers."""

# global
import numpy as np
from hypothesis import given, strategies as st

# local
import ivy
import ivy.functional.backends.numpy as ivy_np
import ivy_tests.test_ivy.helpers as helpers


@given(
    dtype_x_normidxs=helpers.dtype_values_axis(
        available_dtypes=ivy_np.valid_float_dtypes,
        allow_inf=False,
        min_num_dims=1,
        min_axis=1,
        ret_shape=True,
    ),
    num_positional_args=helpers.num_positional_args(fn_name="layer_norm"),
    scale=st.floats(min_value=0.0),
    offset=st.floats(min_value=0.0),
    epsilon=st.floats(min_value=ivy._MIN_BASE, max_value=0.1),
    new_std=st.floats(min_value=0.0, exclude_min=True),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_layer_norm(
    dtype_x_normidxs,
    num_positional_args,
    scale,
    offset,
    epsilon,
    new_std,
    as_variable,
    with_out,
    native_array,
    container,
    instance_method,
    fw,
):
    dtype, x, normalized_idxs = dtype_x_normidxs
    helpers.test_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "layer_norm",
        x=np.asarray(x, dtype=dtype),
        normalized_idxs=normalized_idxs,
        epsilon=epsilon,
        scale=scale,
        offset=offset,
        new_std=new_std,
    )

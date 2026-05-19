# Fixes aplicados

## StreamlitAPIException: `_repr_html_()` is not a valid Streamlit command

Causa: se estaba usando una expresión ternaria con comandos Streamlit:

```python
st.success(msg) if ok else st.error(msg)
```

En Streamlit, una expresión suelta puede ser tratada como salida automática. Como `st.success()` / `st.error()` devuelven un objeto interno `DeltaGenerator`, Streamlit intentó renderizarlo y terminó invocando `_repr_html_`.

Solución aplicada:

```python
if ok:
    st.success(msg)
else:
    st.error(msg)
```


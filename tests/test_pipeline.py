import pytest
import pandas as pd
import requests

from unittest.mock import patch, MagicMock

from etl.pipeline_etl import (
    transformar_datos,
    extraer_datos
)


def test_transformar_datos_logica():
    """
    Verifica que los datos JSON se conviertan
    correctamente en un DataFrame.
    """

    datos_prueba = [
        {
            "id_usuario": 1,
            "pais": "Chile",
            "email": "user_1@ecommerce.com"
        },
        {
            "id_usuario": 2,
            "pais": "Perú",
            "email": "user_2@ecommerce.com"
        }
    ]

    df_resultado = transformar_datos(
        datos_prueba
    )

    assert isinstance(
        df_resultado,
        pd.DataFrame
    )

    assert len(df_resultado) == 2

    assert "pais" in df_resultado.columns


def test_transformar_datos_vacio():
    """
    Verifica que una lista vacía
    genere un DataFrame vacío.
    """

    datos_prueba = []

    df_resultado = transformar_datos(
        datos_prueba
    )

    assert isinstance(
        df_resultado,
        pd.DataFrame
    )

    assert df_resultado.empty


@patch("etl.pipeline_etl.requests.get")
def test_extraer_datos_error_api(mock_get):
    """
    Verifica que la función propague
    correctamente errores HTTP.
    """

    mock_respuesta = MagicMock()

    mock_respuesta.raise_for_status.side_effect = (
        requests.exceptions.HTTPError(
            "Error 500"
        )
    )

    mock_get.return_value = mock_respuesta

    with pytest.raises(
        requests.exceptions.HTTPError
    ):
        extraer_datos(
            "http://url-falsa/clientes"
        )
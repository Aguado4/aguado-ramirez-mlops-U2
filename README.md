# Predictor de Enfermedades — MLOps U2

Repositorio del proyecto de la Unidad 2 del curso de MLOps. Contiene el código fuente, la imagen Docker y el pipeline de CI/CD para un servicio que simula la predicción de enfermedades a partir de algunos síntomas reportados de un paciente.

## Problema

Dados los avances tecnológicos en medicina, existe abundante información de pacientes para enfermedades comunes, pero los datos escasean para enfermedades huérfanas. Se requiere construir un modelo capaz de predecir, a partir de los síntomas reportados, si un paciente podría sufrir alguna enfermedad, cubriendo tanto enfermedades comunes como huérfanas.

Para este ejercicio, el modelo se simula con una función determinística que clasifica al paciente en una de varias categorías según parámetros básicos (temperatura, nivel de dolor y días con síntomas).

## Propósito del repositorio

- Versionar el código fuente del servicio simulado.
- Mantener una imagen Docker reproducible que el médico pueda ejecutar localmente.
- Automatizar pruebas y publicación de la imagen mediante CI/CD con GitHub Actions.

## Estructura prevista

- Rama `main`: versión estable del proyecto.
- Rama `solución-inicial`: archivos iniciales heredados de la Unidad 1.
- Ramas posteriores: nuevos requerimientos y configuración del pipeline de CI/CD.

Este README se reemplazará por la versión combinada con el README técnico del servicio una vez se integre la `solución-inicial`.

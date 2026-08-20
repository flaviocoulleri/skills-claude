# Template — Matriz de integraciones

> Alcance y responsables de cada extremo, **incluidos los del cliente**. Validan: **PO + arquitecto**. Semana 2 del Sprint 0.

## Estructura mínima (una fila por integración)

| Columna | Contenido |
|---|---|
| ID | Identificador de la integración |
| Sistemas | Origen ↔ destino |
| Dirección | Uni/bidireccional |
| Datos | Entidades/campos intercambiados (referencia al diccionario de datos) |
| Mecanismo | API REST/SOAP, archivo, middleware, evento |
| Frecuencia | Tiempo real / batch / manual |
| Responsable extremo ProContacto | Nombre |
| Responsable extremo cliente | Nombre — **obligatorio**: cada extremo tiene dueño |
| Insumos del cliente | Credenciales, ambientes, documentación de la API, con **fecha límite** |
| Estado | Comprometida / fase 2 / excluida |

## Reglas

- Integraciones **no listadas acá están excluidas** (exclusión explícita estándar de toda propuesta).
- Comercial no vende integraciones sin pre-validación técnica de delivery (regla de F1).
- Insumos del cliente fuera de fecha → el cronograma se desplaza 1:1 (limitante 08).

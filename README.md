# Auction Project  
Sistema de Subastas Multiusuario con Archivos Compartidos  
UADE – Algoritmos y Estructuras de Datos I

---

## 📌 Introducción
**Auction Project** es una aplicación de consola desarrollada en Python que simula un sistema de subastas en línea.  
El objetivo del TP es implementar un entorno *cliente-servidor simulado* utilizando **archivos compartidos** para que múltiples usuarios puedan interactuar con la misma información de manera simultánea.

El proyecto aplica:
- Lectura y escritura de archivos JSON  
- Estructuras de datos  
- Validaciones  
- Persistencia  
- Manejo de tiempo en las subastas  
- Modularización  

---

## 🎯 Objetivos del Proyecto

- Simular un sistema distribuido utilizando archivos compartidos.
- Implementar la lógica completa de subastas: creación, puja, cierre y ganador.
- Incorporar roles (usuario y administrador).
- Controlar tiempos mediante `fecha_inicio` y `fecha_fin`.
- Actualizar automáticamente el estado de cada subasta.
- Generar informes completos a partir de datos reales de uso.

---

## 🧱 Arquitectura del Proyecto

### Estructura de carpetas (simplificada)
```
udae-auction-project/
│── config/
│ └── config.py
│
│── data/
│ ├── usuarios.py
│ ├── subastas.py
│ ├── pujas.py
│ └── JSONs.py
│
│── utilidades/
│ └── utils.py
│
│── validaciones/
│ └── validaciones.py
│
│── main.py
├── usuarios.json
├── subastas.json
└── pujas.json
```

### Archivos compartidos (base de datos del sistema)
Los JSON compartidos representan el “servidor” del proyecto:

- **usuarios.json** → registros de usuarios y roles  
- **subastas.json** → información activa/finalizada de subastas  
- **pujas.json** → historial de pujas agrupadas por ID de subasta  

Todos los clientes leen/escriben sobre los mismos archivos.

---

## 🌐 Funcionamiento Multiusuario  
Esto permite:

- Cada cliente ejecuta el programa desde su propia carpeta local.
- Todos leen/escriben en los mismos archivos compartidos sincronizados.
- Las subastas se actualizan automáticamente para todos los usuarios.

Esto simula un **sistema cliente-servidor real**, sin necesidad de sockets.

---

## 👤 Roles del Sistema

### Usuario común
- Registrarse / Iniciar sesión  
- Ver subastas  
- Realizar pujas  
- Ver estado de subastas  

### Administrador
- Crear nuevas subastas  
- Gestionar su duración  
- Cerrar subastas automáticamente  
- Generar informes completos  

---

## ⏱️ Lógica de Subastas y Control de Tiempo

Cada subasta contiene:

```json
{
  "fecha_inicio": "2025-11-24T21:05:00",
  "fecha_fin": "2025-11-24T21:40:00",
  "estado": "activa"
}

```
## El sistema:

- Calcula el tiempo restante dinámicamente.

- Cambia el estado de la subasta automáticamente cuando ahora >= fecha_fin.

- Determina ganador usando las pujas registradas.

- Actualiza el JSON compartido para todos los clientes.


## Diagrama de estados de subasta:
           ┌────────────────┐
           │   PROGRAMADA   │ (creada por admin)
           └───────┬────────┘
                   │ fecha_inicio
                   │ fecha_finalizacion
                   │
                   ▼
            ┌──────────────┐
            │    ACTIVA    │
            └───────┬──────┘
           tiempo   │ pujas
         expira     │
                   ▼
         ┌──────────────────┐
         │    FINALIZADA    │
         └──────────────────┘



## Estructura de los JSON
### usuarios.json
```
[
    {
        "id": 1,
        "nombre": "admin",
        "password": "123",
        "saldo": 0,
        "rol": "admin"
    }
]
```

### subastas.json
```
{
   "id": 101,
   "nombre": "iPhone 17 Pro Max - Titanium Edition",
   "categoria": "Tecnologia",
   "costo_inicial": 900000,
   "descripcion": "Edicion premium de Apple con cuerpo de titanio, triple camara y pantalla ProMotion OLED de 6.9 pulgadas.",
   "estado": "activa",
   "fecha_inicio": "2025-11-25T14:32:37",
   "fecha_fin": "2025-11-25T21:10:00",
   "monto_actual": 0,
   "ganador": null
},
  ```

### pujas.json
```
{
   "23": [
      {
         "id_usuario": 9864,
         "usuario": "Nico",
         "monto": 6000,
         "timestamp": "2025-11-24T18:39:36"
      },
      {
         "id_usuario": 9864,
         "usuario": "Nico",
         "monto": 6000,
         "timestamp": "2025-11-24T18:40:22"
      }
   ]
}
```
## Informe de cada subasta 
```
========== INFORME COMPLETO DE SUBASTAS ==========

Total de subastas registradas: 5

--- SUBASTA # 1 — Bora 1.8T ---
Categoría: Automotores
Estado: activa
Fecha inicio: 2025-11-25T12:48:22
Fecha fin: 2025-11-25T21:30:00
Duración total: 521 minutos
Precio inicial: $6000000
Ganador: Nadie

No hubo pujas en esta subasta.

--- SUBASTA # 104 — PlayStation 5 - The Last of Us Part II' ---
Categoría: Videojuegos
Estado: activa
Fecha inicio: 2025-11-25T12:48:22
Fecha fin: 2025-11-25T21:25:00
Duración total: 516 minutos
Precio inicial: $80000
Ganador: Nadie

No hubo pujas en esta subasta.

--- SUBASTA # 23 — Pastillas de cafeina ---
Categoría: Farmacos
Estado: activa
Fecha inicio: 2025-11-25T13:30:37
Fecha fin: 2025-11-25T21:15:00
Duración total: 464 minutos
Precio inicial: $5000
Ganador: Nadie

Estadísticas:
 - Cantidad de pujas: 2
 - Monto máximo: $6000
 - Monto mínimo: $6000
 - Promedio ofertado: $6000.0
 - Rentabilidad: 20.00%

Participantes:
 - Nico: 2 pujas, $12000 ofertados

 Historial de pujas:
 1) Nico | $6000 | 2025-11-24T18:39:36
 2) Nico | $6000 | 2025-11-24T18:40:22


--- SUBASTA # 101 — iPhone 17 Pro Max - Titanium Edition ---
Categoría: Tecnologia
Estado: activa
Fecha inicio: 2025-11-25T14:32:37
Fecha fin: 2025-11-25T21:10:00
Duración total: 397 minutos
Precio inicial: $900000
Ganador: Nadie

No hubo pujas en esta subasta.

--- SUBASTA # 256 — Scandal ---
Categoría: Perfumes
Estado: activa
Fecha inicio: 2025-11-25T14:32:37
Fecha fin: 2025-11-25T21:43:00
Duración total: 430 minutos
Precio inicial: $50000
Ganador: Nadie

No hubo pujas en esta subasta.
```




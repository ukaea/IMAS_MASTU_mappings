# PF Active Circuit Connections

This page describes how the MAST-U poloidal field coils are electrically connected to their power supply circuits.

## Overview

The PF active system consists of **13 power supplies** driving **25 coils** through various circuit topologies (series, parallel, and anti-series configurations).

## MAST-U Supplies and Coils

**Power Supplies:**
```python
supplies = [
    'D1PS', 'D2PS', 'D3PS', 'DPPS', 'D5PS', 'D6PS', 'D7PS',
    'P1PS', 'EFPS', 'PXPS', 'SFPS', 'MFPS', 'RFPS'
]
```

**Coils:**
```python
coils = [
    'D1U', 'D1L', 'D2U', 'D2L', 'D3U', 'D3L', 'DPU', 'DPL',
    'D5U', 'D5L', 'D6U', 'D6L', 'D7U', 'D7L', 'P1', 'PC',
    'PXU', 'PXL', 'P4U', 'P4L', 'P5U', 'P5L', 'P6U', 'P6L'
]
```



| Supply | Coil | Geometry | Circuit     | Notes                                                      |
| ------ | ---- |:-------- |:----------- |:---------------------------------------------------------- |
| D1PS   | D1U  | d1_upper | Series      |                                                            |
|        | D1L  | d1_lower |             |                                                            |
| D2PS   | D2U  | d2_upper | Series      |                                                            |
|        | D2L  | d2_lower |             |                                                            |
| D3PS   | D3U  | d3_upper | Series      |                                                            |
|        | D3L  | d3_lower |             |                                                            |
| DPPS   | DPU  | dp_upper | Series      |                                                            |
|        | DPL  | dp_lower |             |                                                            |
| D5PS   | D5U  | d5_upper | Series      |                                                            |
|        | D5L  | d5_lower |             |                                                            |
| D6PS   | D6U  | d6_upper | Series      |                                                            |
|        | D6L  | d6_lower |             |                                                            |
| D7PS   | D7U  | d7_upper | Series      |                                                            |
|        | D7L  | d7_lower |             |                                                            |
| P1PS   | P1   | p1_inner | Parallel    | 1 coil for current but two geometrically, central solenoid |
|        |      | p1_outer |             |                                                            |
| EFPS   | PC   | pc       | Parallel    | Not currently in use                                       |
| -      | -    | -        | -           |                                                            |
| PXPS   | PXU  | px_upper | Series      |                                                            |
|        | PXL  | px_lower |             |                                                            |
| SFPS   | P4U  | p4_upper | Series      |                                                            |
|        | P4L  | p4_lower |             |                                                            |
| MFPS   | P5U  | p5_upper | Series      |                                                            |
|        | P5L  | p5_lower |             |                                                            |
| RFPS   | P6U  | p6_upper | Anti-Series |                                                            |
|        | P6L  | p6_lower |             |                                                            |


## Circuit Topologies

### Series Circuit

In a series circuit, coils are connected end-to-end. The same current flows through all coils in the circuit.

![Series Circuit Diagram](https://hackmd.io/_uploads/HyQJg_CW6.png)

|       | S1(1) | S1(2) | C1(1) | C1(2) | C2(1) | C2(2) |
| ----- | ----- | ----- |:----- |:----- |:----- | ----- |
| **1** | 1     | 0     | 1     | 0     | 0     | 0     |
| **2** | 0     | 1     | 0     | 0     | 0     | 1     |
| **3** | 0     | 0     | 0     | 1     | 1     | 0     |


### Parallel Circuit

In a parallel circuit, coils share the same voltage. The current is divided between the parallel branches.

![Parallel Circuit Diagram](https://hackmd.io/_uploads/rJhQZOA-6.png)

|       | S1(1) | S1(2) | C1(1) | C1(2) | C2(1) | C2(2) |
| ----- | ----- | ----- |:----- |:----- |:----- | ----- |
| **1** | 1     | 0     | 1     | 0     | 1     | 0     |
| **2** | 0     | 1     | 0     | 1     | 0     | 1     |


### Anti-Series Circuit

In an anti-series circuit, coils are connected with opposite polarity. This configuration is used for coils that need to operate with reversed magnetic field direction.

![Anti-Series Circuit Diagram](https://hackmd.io/_uploads/BJeY-_Cba.png)

|       | S1(1) | S1(2) | C1(1) | C1(2) | C2(1) | C2(2) |
|:----- | ----- | ----- |:----- | ----- |:----- | ----- |
| **1** | 1     | 0     | 0     | 1     | 0     | 0     |
| **2** | 0     | 1     | 0     | 0     | 0     | 1     |
| **3** | 0     | 0     | 1     | 0     | 1     | 0     |

## Connection Matrices

The complete IMAS connection matrix encodes the electrical topology of all circuits:

- **13 circuits** = 13 connection matrices (one per power supply)
- **13 power supplies** driving the system
- **25 coils** in total across all circuits
- All coils and supplies appear in the matrix in the order defined in the IDS
- Approximately **~76 columns** in the full connection matrix

### Data Representation

The connection matrices are generated using the `pf_conn_matrix` custom function, which creates the appropriate circuit topology matrix for each power supply based on its configuration.

Each matrix row represents a circuit node, and columns represent:
- Supply connections (S columns)
- Coil connections (C columns)

Matrix values indicate electrical connectivity between nodes.

### Special Cases

**EFPS and PC (Central Coil):**

- The EFPS circuit and PC coil are **not currently operational**
- Connection matrix expected to be parallel topology but contains all zeroes (as of 26/10/23)
- These are maintained in the IDS structure for potential future use

### Full Connection Matrix Visualization

![Full IMAS Connection Matrix](https://hackmd.io/_uploads/Sy2hd7uzp.png)

## Data Sources

Circuit connection data is generated from:

- **Signal**: Power supply name (e.g., `D1PS`, `P1PS`)
- **Function**: `pf_conn_matrix` - Custom MAST-U function that generates the connection topology
- **Source**: `CUSTOM_MASTU` data source



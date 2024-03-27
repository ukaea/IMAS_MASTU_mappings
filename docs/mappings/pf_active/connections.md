# pf_active circuits

## MAST-U Supplies and Coils


```python
supplies = [
    'D1PS', 'D2PS', 'D3PS', 'DPPS', 'D5PS', 'D6PS', 'D7PS',
    'P1PS', 'EFPS', 'PXPS', 'SFPS', 'MFPS', 'RFPS'
]
```

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


## Series Circuit

![](https://hackmd.io/_uploads/HyQJg_CW6.png)



|       | S1(1) | S1(2) | C1(1) | C1(2) | C2(1) | C2(2) |
| ----- | ----- | ----- |:----- |:----- |:----- | ----- |
| **1** | 1     | 0     | 1     | 0     | 0     | 0     |
| **2** | 0     | 1     | 0     | 0     | 0     | 1     |
| **3** | 0     | 0     | 0     | 1     | 1     | 0     |


## Parallel Circuit

![](https://hackmd.io/_uploads/rJhQZOA-6.png)

|       | S1(1) | S1(2) | C1(1) | C1(2) | C2(1) | C2(2) |
| ----- | ----- | ----- |:----- |:----- |:----- | ----- |
| **1** | 1     | 0     | 1     | 0     | 1     | 0     |
| **2** | 0     | 1     | 0     | 1     | 0     | 1     |


## Anti-Series Circuit

![](https://hackmd.io/_uploads/BJeY-_Cba.png)

|       | S1(1) | S1(2) | C1(1) | C1(2) | C2(1) | C2(2) |
|:----- | ----- | ----- |:----- | ----- |:----- | ----- |
| **1** | 1     | 0     | 0     | 1     | 0     | 0     |
| **2** | 0     | 1     | 0     | 0     | 0     | 1     |
| **3** | 0     | 0     | 1     | 0     | 1     | 0     |

## Connections Matrix

13 circuits = 13 connection matrices
13 power supplies
25 coils
All coils and supplies within the matrix in order they appear in the IDS
~76 columns

EFPS and PC not operational
Expected to be parallel but all zeroes as of 26/10/23

![](https://hackmd.io/_uploads/Sy2hd7uzp.png)



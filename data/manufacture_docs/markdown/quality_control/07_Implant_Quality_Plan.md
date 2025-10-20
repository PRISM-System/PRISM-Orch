# Ion Implantation 품질 관리 계획서
## Quality Control Plan for Advanced Junction Formation

**문서번호:** QCP-IMP-JCT-007  
**개정일:** 2024.11.15  
**적용공정:** Source/Drain and Well Implantation  
**기술노드:** 5nm FinFET Technology  

---

## 1. 문서 개요

### 1.1 목적 및 범위
- **목적:** Ion implantation 공정의 품질 관리 체계 확립
- **장비:** Applied Materials VIISta Trident
- **공정:** S/D Extension, Halo, Deep S/D, Well
- **Critical Parameters:** Dose ±2%, Uniformity <1%, Angle ±0.5°
- **목표:** Zero defect, Yield >99.5%

### 1.2 Implant Species and Applications
| Species | Application | Energy Range | Dose Range |
|---------|-------------|--------------|------------|
| B/BF₂ | PMOS S/D | 0.5-35 keV | 1E13-5E15 |
| As | NMOS S/D | 2-80 keV | 1E14-5E15 |
| P | N-Well, NLDD | 10-500 keV | 1E12-1E14 |
| Ge | Pre-amorphization | 10-50 keV | 1E14-1E15 |
| C | Co-implant | 3-10 keV | 1E14-5E14 |

---

## 2. Critical Quality Parameters

### 2.1 Dose Control

| Parameter | Specification | Measurement | Control Limit |
|-----------|---------------|-------------|---------------|
| Dose Accuracy | ±2% | 4-point probe Rs | ±3% |
| Dose Uniformity | <1% (1σ) | 49-point map | <1.5% |
| Dose Repeatability | <0.5% | Run-to-run | <1% |
| Beam Current Stability | <2% variation | Real-time monitor | <3% |
| Charge Control | Neutralized | Surface voltage | <±10V |

### 2.2 Angular Control

```
Tilt and Rotation Specifications:
Standard Implant: 0° tilt, 0° rotation
Halo Implant: 15-30° tilt, quad rotation
Channel Stop: 7° tilt, 22° rotation

Tolerances:
- Tilt accuracy: ±0.5°
- Rotation accuracy: ±1°
- Twist: ±0.3°
```

### 2.3 Profile Control

| Metric | Target | Tolerance | Method |
|--------|--------|-----------|---------|
| Junction Depth (Xj) | Per design | ±2nm | SIMS |
| Lateral Straggle | Minimized | <2nm | SIMS |
| Peak Concentration | Per spec | ±5% | SIMS |
| Abruptness | <2nm/decade | - | SIMS |
| Activation | >80% | >70% | Rs/SIMS |

---

## 3. Process Control Methodology

### 3.1 Pre-Implant Requirements

```
Incoming Wafer Checks:
□ Screen oxide thickness: 50±5Å
□ Particle count: <10 @ 0.12µm
□ PR thickness: Per recipe ±10%
□ Pattern integrity: No defects
□ Queue time: <4 hours
```

### 3.2 Real-time Process Monitoring

| Parameter | Monitoring Method | Frequency | Action Limit |
|-----------|------------------|-----------|--------------|
| Beam Current | Faraday Cup | Continuous | ±2% |
| Beam Position | Beam scanner | Continuous | ±1mm |
| Dose Integration | Dose controller | Real-time | ±1% |
| Vacuum Level | Ion gauge | Continuous | <5E-6 Torr |
| Wafer Temperature | Thermocouple | Continuous | <100°C |

### 3.3 Post-Implant Verification

```
Immediate Checks (per lot):
- Visual inspection: No discoloration
- Charge damage: Test structures
- Particle adders: <5 adds

Within 2 hours:
- Sheet resistance: 5 points/wafer
- Uniformity calculation
- Dose verification

Daily Monitor:
- SIMS profile (monitor wafer)
- Junction depth
- Activation percentage
```

---

## 4. Contamination Control

### 4.1 Species Segregation Protocol

```
Implanter Dedication:
Tool A: Boron species only (B, BF2)
Tool B: N-type dopants (P, As)
Tool C: Special species (Ge, C, Xe)
Tool D: Development/Engineering

Cross-contamination Prevention:
- No species mixing
- Dedicated source materials
- Regular contamination monitoring
- Beam line conditioning after PM
```

### 4.2 Metal Contamination Control

| Element | Limit (atoms/cm²) | Detection | Frequency |
|---------|-------------------|-----------|-----------|
| Fe | <1E10 | TXRF | Weekly |
| Cu | <1E10 | TXRF | Weekly |
| Na | <5E10 | SIMS | Monthly |
| K | <5E10 | SIMS | Monthly |
| Heavy metals | <1E10 | ICP-MS | Monthly |

### 4.3 Particle Management

```
Source Flaking Prevention:
- Source life tracking: <200 hours
- Regular source inspection
- Optimized arc conditions
- Preventive replacement

Particle Monitoring:
- Pre/post measurement
- Adder limit: <5 @ >0.12µm
- Action: >10 particles → Source service
- Trend tracking daily
```

---

## 5. Statistical Process Control

### 5.1 Control Charts

| Parameter | Chart Type | Subgroup | Limits | Cpk Target |
|-----------|------------|----------|--------|------------|
| Dose (Rs) | X̄-R | 5 wafers | ±3σ | >2.00 |
| Uniformity | I-MR | Per wafer | UCL only | >1.67 |
| Beam Current | I-MR | Hourly | ±3σ | >1.67 |
| Angle | X̄-R | 3 samples | ±3σ | >2.00 |
| Contamination | C-chart | Weekly | UCL only | - |

### 5.2 Process Capability

```
Current Performance:
Parameter    Cp    Cpk   Ppk   Goal
Dose        2.25  2.18  2.05  >2.00
Uniformity  1.95  1.88  1.75  >1.67
Angle       2.35  2.28  2.15  >2.00
Energy      2.50  2.43  2.30  >2.00
```

### 5.3 Advanced SPC

```python
# Multivariate T² Control
parameters = ['dose', 'uniformity', 'beam_current', 'pressure']
covariance_matrix = calculate_covariance(historical_data)
mean_vector = calculate_mean(historical_data)

def detect_anomaly(current_data):
    T_squared = mahalanobis_distance(current_data, mean_vector, covariance_matrix)
    UCL = calculate_UCL(alpha=0.0027, dimensions=4)
    return T_squared > UCL
```

---

## 6. Sampling Plans

### 6.1 Production Sampling

| Lot Size | Rs Measurement | SIMS | Contamination |
|----------|---------------|------|---------------|
| 1-6 | 100% | 1 wafer | 1 wafer |
| 7-12 | 5 wafers | 1 wafer | 1 wafer |
| 13-25 | 3 + F/L | Monitor | Weekly pool |
| >25 | 20%, min 5 | Monitor | Weekly pool |

### 6.2 Measurement Strategy

```
Sheet Resistance Mapping:
5-point: Center + 4 @ r=100mm
9-point: + 4 @ r=60mm
49-point: Full uniformity map

Point Selection Algorithm:
- Avoid edge 3mm
- Avoid pattern features
- Consistent positioning
- Automated program
```

### 6.3 Skip Lot Qualification

**Eligibility Criteria:**
- 20 consecutive lots pass
- Cpk > 2.0 all parameters
- No equipment changes
- Stable beam current

**Skip Rate:** Maximum 75%
**Audit:** Random 10%

---

## 7. Thermal Budget Management

### 7.1 Anneal Process Control

| Anneal Type | Temperature | Time | Ambient | Purpose |
|-------------|-------------|------|---------|---------|
| Spike Anneal | 1050°C | <1s | N₂ | Activation |
| Flash Anneal | 1300°C | <1ms | N₂ | Ultra-shallow |
| Laser Anneal | 1350°C | <1µs | N₂ | Selective |
| Furnace | 800°C | 30min | N₂ | Drive-in |

### 7.2 Activation Monitoring

```
Sheet Resistance Targets:
B (1E15): 500 Ω/□ after anneal
As (3E15): 80 Ω/□ after anneal
P (1E13): 5000 Ω/□ after anneal

Activation Efficiency:
Target: >80% electrical activation
Measurement: Rs vs. SIMS dose
Frequency: Daily monitor
```

### 7.3 Diffusion Control

| Dopant | Diffusion Limit | Measurement | Control |
|--------|----------------|-------------|----------|
| B | <2nm lateral | SIMS 2D | Temp/time |
| As | <1nm lateral | SIMS 2D | Minimal |
| P | <3nm lateral | SIMS 2D | Temp/time |

---

## 8. Advanced Implant Techniques

### 8.1 Damage Engineering

```
Pre-Amorphization Implant (PAI):
Species: Ge or Si
Energy: 20-40 keV
Dose: 1E15 cm⁻²
Purpose: Reduce channeling
Benefit: 30% better activation
```

### 8.2 Co-implantation Strategy

| Primary | Co-implant | Purpose | Benefit |
|---------|------------|---------|---------|
| B | C | Reduce TED | 40% less diffusion |
| B | F | Reduce TED | 35% less diffusion |
| As | P | Activation | 10% lower Rs |
| P | C | Stress | +200 MPa |

### 8.3 Molecular Ion Advantages

```
BF₂ vs. B:
- Shallower junction (40% less Rp)
- Better amorphization
- Reduced channeling
- Higher throughput

B₁₈H₂₂ Cluster:
- Ultra-shallow (<5nm)
- High dose rate
- Minimal damage
- Better uniformity
```

---

## 9. Yield and Reliability Correlation

### 9.1 Electrical Parameter Impact

| Implant Parameter | Device Impact | Yield Sensitivity |
|------------------|---------------|-------------------|
| Dose ±5% | Vth ±30mV | -2% yield |
| Xj ±2nm | Ion ±10% | -1% yield |
| Uniformity >2% | Matching degradation | -3% yield |
| Contamination | Junction leakage | -5% yield |

### 9.2 Reliability Indicators

```
Hot Carrier Injection (HCI):
- Correlation: Halo dose
- Target: 10 year lifetime
- Monitor: Idsat degradation

Bias Temperature Instability (BTI):
- Correlation: Interface damage
- Target: <30mV shift
- Monitor: Vth shift

Junction Leakage:
- Specification: <1 nA/µm
- Correlation: Damage/contamination
- Monitor: Every lot
```

### 9.3 Defect Density Impact

| Defect Type | Critical Size | Yield Impact | Detection |
|-------------|--------------|--------------|-----------|
| Particles | >65nm | -0.1%/particle | Optical |
| Metal contamination | >1E10 | -5% | TXRF |
| Charge damage | Any | -2% | Antenna test |
| PR residue | >100nm | -1% | SEM review |

---

## 10. Continuous Improvement Program

### 10.1 Current Projects

| Project | Goal | Status | Benefit |
|---------|------|--------|---------|
| Beam current optimization | +20% | Testing | Throughput |
| Source life extension | 200→300hr | 60% done | Cost -30% |
| Uniformity improvement | <0.5% | Planning | Yield +1% |
| Contamination reduction | <1E9 | Ongoing | Reliability |

### 10.2 Technology Roadmap

```
3nm Node Requirements:
- Junction depth: <5nm
- Abruptness: <1nm/decade
- Activation: >90%
- Sheet resistance: <1000 Ω/□
- Uniformity: <0.5%

Enabling Technologies:
- Plasma doping
- Hot implantation
- Laser annealing
- Monolayer doping
```

### 10.3 Cost Optimization

```
Cost Reduction Initiatives:
                 Current  Target  Saving
Source gas usage  $2/wf    $1.5    25%
Throughput       100 wph  120 wph  20%
Source lifetime  200 hr   300 hr   33%
Energy reduction  -        -10%    15%
Total CoO        $5/wf    $3.5/wf  30%
```

---

## Appendix A: Implant Recipe Library

### NMOS Source/Drain Extension
```
Species: As
Energy: 2 keV
Dose: 8E14 cm⁻²
Tilt: 0°
Rotation: 0°
Temperature: 25°C
PAI: Ge 30keV, 5E14
```

### PMOS Halo
```
Species: As
Energy: 40 keV
Dose: 5E13 cm⁻²
Tilt: 25°
Rotation: Quad (0,90,180,270)
Temperature: 25°C
```

---

## Appendix B: Troubleshooting Matrix

| Issue | Probable Cause | Verification | Solution |
|-------|---------------|--------------|----------|
| High Rs | Low dose | Beam current | Recalibrate |
| Poor uniformity | Beam scanning | Scan waveform | Adjust scan |
| Contamination | Source/beamline | TXRF/SIMS | Clean/replace |
| Charge damage | Poor neutralization | Antenna test | Flood gun |
| Angle deviation | Stage calibration | Physical check | Recalibrate |

---

**Document Control:**
- Author: Implant Process Team
- Review: Quality Engineering
- Approval: Manufacturing Director
- Next Review: 2025-02-15
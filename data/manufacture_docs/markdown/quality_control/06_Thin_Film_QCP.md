# Thin Film Deposition 품질 관리 계획서
## Quality Control Plan for ALD High-k/Metal Gate Process

**문서번호:** QCP-TF-HKMG-006  
**개정일:** 2024.11.15  
**적용공정:** Atomic Layer Deposition (ALD)  
**제품:** 3nm FinFET High-k/Metal Gate Stack  

---

## 1. 문서 개요 및 범위

### 1.1 목적
본 문서는 3nm FinFET 공정의 High-k dielectric 및 Metal gate 증착 공정에 대한 품질 관리 체계를 정의하고, 박막 특성의 일관성과 신뢰성을 보증합니다.

### 1.2 적용 범위
- **공정 장비:** ASM Eagle XP8 ALD
- **박막 구조:** HfO2(1.5nm)/TiN(2nm)/TaN(3nm)/W(50nm)
- **Critical Parameters:** EOT < 0.8nm, Uniformity < 1%
- **목표 수율:** > 99.0%

### 1.3 품질 목표
| Parameter | Target | Current | Best in Class |
|-----------|--------|---------|---------------|
| EOT Control | ± 0.05nm | ± 0.06nm | ± 0.03nm |
| Uniformity (WiW) | < 1.0% | 1.1% | 0.8% |
| Leakage Current | < 1E-2 A/cm² | 8E-3 | 5E-3 |
| Interface Trap Density | < 1E11 /cm²-eV | 1.2E11 | 8E10 |

---

## 2. Critical Film Properties

### 2.1 Physical Properties

| Property | HfO2 | TiN | TaN | W | Measurement |
|----------|------|-----|-----|---|-------------|
| Thickness (nm) | 1.5±0.1 | 2.0±0.1 | 3.0±0.2 | 50±2 | XRR/Ellipsometer |
| Density (g/cm³) | >10.0 | >5.2 | >15.5 | >19.0 | XRR |
| Roughness (RMS) | <0.15 | <0.20 | <0.25 | <0.30 | AFM |
| Composition | Hf:O=1:2 | Ti:N=1:1 | Ta:N=1:1 | Pure W | XPS/RBS |
| Crystal Structure | Monoclinic | FCC | BCC | BCC | XRD |
| Grain Size (nm) | 5-10 | 10-15 | 15-20 | 20-30 | TEM |

### 2.2 Electrical Properties

| Parameter | Specification | Test Method | Frequency |
|-----------|---------------|-------------|-----------|
| EOT | 0.8±0.05nm | C-V @ 1MHz | Every wafer |
| Vfb (Flatband) | -0.2±0.1V | C-V sweep | Every wafer |
| Dit | <1E11 /cm²-eV | Hi-Lo method | Daily |
| Work Function | 4.6±0.1eV | C-V analysis | Daily |
| Breakdown Field | >10 MV/cm | I-V ramp | Sample |
| TDDB | t₅₀ >10 years | Stress test | Weekly |

### 2.3 Interface Quality

```
Interface Requirements:
SiO2/HfO2 Interface:
- Thickness: 0.3-0.5nm
- No Hf silicate formation
- Sharp transition < 0.2nm

HfO2/TiN Interface:
- No TiO2 formation
- N penetration < 0.1nm
- Stable after anneal

Metal/Metal Interface:
- No intermixing
- Low contact resistance
- Good adhesion
```

---

## 3. Process Control Parameters

### 3.1 ALD Process Windows

| Film | Precursor | Temperature | Pressure | Growth Rate |
|------|-----------|-------------|----------|-------------|
| HfO2 | HfCl4/H2O | 300±5°C | 1±0.1 Torr | 1.0Å/cycle |
| TiN | TiCl4/NH3 | 400±5°C | 2±0.2 Torr | 0.5Å/cycle |
| TaN | TaCl5/NH3 | 350±5°C | 1.5±0.1 Torr | 0.6Å/cycle |
| W | WF6/SiH4 | 350±10°C | 5±0.5 Torr | 2.0Å/cycle |

### 3.2 Critical Process Controls

```
Pre-deposition Controls:
□ Surface preparation (HF last)
□ Queue time < 2 hours
□ Moisture level < 1 ppm
□ Particle count < 5 @ 0.065µm
□ Native oxide < 8Å

In-situ Monitoring:
- Precursor flow stability ±1%
- Temperature uniformity ±2°C
- Pressure stability ±2%
- Purge efficiency >99.9%
- Growth rate per cycle ±2%

Post-deposition Checks:
□ Thickness mapping (49 points)
□ Composition analysis
□ Electrical test
□ Stress measurement
□ Adhesion test
```

### 3.3 Cycle Recipe Optimization

```
HfO2 ALD Cycle:
1. HfCl4 pulse: 0.1s
2. N2 purge: 2.0s
3. H2O pulse: 0.05s
4. N2 purge: 2.0s
Total cycle time: 4.15s
Cycles required: 15 (for 1.5nm)

Nucleation Enhancement:
- First 3 cycles: Extended pulse
- Plasma assist optional
- Temperature spike to 320°C
```

---

## 4. Measurement and Metrology

### 4.1 Inline Metrology Strategy

| Measurement | Tool | Frequency | Specification |
|-------------|------|-----------|---------------|
| Thickness | XRR | Every wafer | ±1Å |
| Uniformity | Ellipsometer | Every wafer | <1% (1σ) |
| Composition | XPS | Daily monitor | ±2 at% |
| Density | XRR | Daily monitor | >95% bulk |
| Roughness | AFM | Weekly | <2Å RMS |
| Crystallinity | XRD | Weekly | Per spec |

### 4.2 Measurement Sampling Plan

```
49-Point Wafer Map:
Radial Distribution:
- Center: 1 point
- R=30mm: 8 points
- R=60mm: 8 points  
- R=90mm: 16 points
- R=140mm: 16 points

Statistical Requirements:
- Capability: GR&R < 10%
- Precision: <3% of tolerance
- Accuracy: Traceable standards
```

### 4.3 Advanced Characterization

| Technique | Purpose | Frequency | Specification |
|-----------|---------|-----------|---------------|
| TEM | Interface analysis | Monthly | <2Å intermixing |
| SIMS | Impurity profile | Weekly | <1E18 atoms/cm³ |
| RBS | Stoichiometry | Monthly | ±1% accuracy |
| XAS | Chemical state | Quarterly | Oxidation state |
| ARXPS | Depth profile | Weekly | 0.1nm resolution |

---

## 5. Statistical Process Control

### 5.1 Control Chart Implementation

| Parameter | Chart Type | UCL | LCL | Cpk Target |
|-----------|------------|-----|-----|------------|
| HfO2 Thickness | X̄-R | 16Å | 14Å | >2.0 |
| EOT | X̄-R | 8.5Å | 7.5Å | >1.67 |
| Uniformity | I-MR | 1.5% | - | >1.67 |
| Leakage | I-chart | 1E-2 | - | >1.33 |
| Sheet Rs (TiN) | X̄-R | 110 Ω/□ | 90 Ω/□ | >1.67 |

### 5.2 Process Capability Analysis

```
Current Performance:
           Cp    Cpk   Ppk   Target
Thickness  2.15  1.98  1.85  >2.00
EOT       1.89  1.76  1.65  >1.67  
Uniformity 2.35  2.28  2.15  >2.00
Leakage   1.75  1.68  1.55  >1.33
```

### 5.3 Multivariate Control

```python
# Hotelling T² Control Chart
def calculate_T2(X, μ, Σ):
    """
    X: Current observation vector
    μ: Historical mean vector  
    Σ: Covariance matrix
    """
    diff = X - μ
    T2 = diff.T @ inv(Σ) @ diff
    UCL = ((p*(n-1)*(n+1))/(n*(n-p))) * F(α, p, n-p)
    return T2, UCL

Variables monitored:
- Thickness (all layers)
- Temperature profile
- Pressure profile
- Precursor consumption
```

---

## 6. Defectivity and Yield Management

### 6.1 Defect Specifications

| Defect Type | Size | Limit | Detection | Action |
|-------------|------|-------|-----------|---------|
| Particles | >45nm | <10/wafer | KLA SP3 | Review |
| Pinholes | Any | 0/cm² | Electrical | Hold |
| Delamination | Any | None | Optical | Scrap |
| Nodules | >100nm | <5/wafer | AFM | Monitor |
| Contamination | Metal | <1E10 at/cm² | TXRF | Hold |

### 6.2 Yield Loss Analysis

```
Yield Detractor Pareto:
1. Leakage (35%) - Interface quality
2. EOT shift (25%) - Process drift
3. Uniformity (20%) - Hardware
4. Defects (15%) - Particles
5. Other (5%) - Various

Improvement Actions:
- Interface engineering
- APC implementation
- Hardware upgrade
- Particle reduction
```

### 6.3 Electrical Yield Correlation

| Electrical Param | Correlation | Impact/Å | Action |
|-----------------|-------------|----------|---------|
| Vth | R=0.92 | 25mV/Å EOT | Critical |
| Gm (max) | R=0.88 | -5%/Å | Important |
| SS | R=0.75 | 2mV/dec/Å | Monitor |
| DIBL | R=0.71 | 3mV/V/Å | Monitor |
| Ig (gate leakage) | R=0.95 | 10×/Å | Critical |

---

## 7. Equipment Qualification

### 7.1 New Chamber Qualification

```
Qualification Flow (5 days):
Day 1: Hardware
- Leak check < 1E-9 Torr·L/s
- Temperature mapping ±1°C
- Gas flow calibration ±1%

Day 2: Process Baseline
- Blanket wafers (Si, SiO2)
- Growth rate determination
- Uniformity optimization

Day 3: Film Properties
- Full characterization
- Electrical testing
- Reliability screening

Day 4: Integration
- Pattern wafers
- Cross-contamination check
- Particle qualification

Day 5: Production Release
- Golden wafer correlation
- SPC limits setting
- Documentation complete
```

### 7.2 Preventive Maintenance Recovery

| PM Level | Downtime | Recovery | Qualification |
|----------|----------|----------|---------------|
| Daily | 30 min | None | Visual check |
| Weekly | 2 hours | 10 wafers | Uniformity |
| Monthly | 8 hours | 25 wafers | Full |
| Quarterly | 24 hours | 50 wafers | Complete |
| Annual | 48 hours | 100 wafers | Rebaseline |

### 7.3 Cross-Contamination Control

```
Chamber Dedication:
Chamber A: HfO2 only
Chamber B: TiN only  
Chamber C: TaN only
Chamber D: W nucleation
Chamber E: W bulk fill

Contamination Monitoring:
- TXRF: Weekly
- SIMS: Monthly  
- Cross-chamber: Never
- Purge between films: 30 cycles
```

---

## 8. Advanced Process Control

### 8.1 Run-to-Run Control

```python
# EOT Control Algorithm
def eot_control(target_eot, measured_eot, current_cycles):
    error = target_eot - measured_eot
    
    # Calculate cycle adjustment
    δ_cycles = error / GROWTH_RATE
    
    # Apply EWMA filter
    filtered_adjustment = α * δ_cycles + (1-α) * previous_adjustment
    
    # Calculate new recipe
    new_cycles = current_cycles + filtered_adjustment
    
    # Apply limits
    new_cycles = max(min(new_cycles, MAX_CYCLES), MIN_CYCLES)
    
    return int(new_cycles)

GROWTH_RATE = 1.0  # Å/cycle
α = 0.3  # EWMA constant
```

### 8.2 Virtual Metrology

| Input Parameters | Weight | Impact |
|-----------------|--------|---------|
| Temperature profile | 35% | Direct |
| Pressure profile | 25% | Direct |
| Precursor consumption | 20% | Indirect |
| Purge efficiency | 15% | Quality |
| Previous run | 5% | Drift |

**Model Performance:**
- R² = 0.96 for thickness
- RMSE = 0.3Å
- Update: Every 50 wafers

### 8.3 Predictive Maintenance

```
Monitored Parameters:
- Valve operation count
- MFC drift trend
- Heater power consumption
- Vacuum performance
- Particle generation rate

Predictive Models:
- Valve lifetime: Weibull distribution
- MFC calibration: Linear degradation
- Particle events: Poisson process
- Pump failure: Vibration analysis
```

---

## 9. Quality Improvement Initiatives

### 9.1 Six Sigma Projects

| Project | DPMO Current | Target | Timeline |
|---------|--------------|--------|----------|
| EOT Control | 1500 | 500 | Q1 2025 |
| Uniformity | 800 | 300 | Q2 2025 |
| Particle Reduction | 2000 | 1000 | Q1 2025 |
| Throughput | - | +15% | Q3 2025 |

### 9.2 Technology Development

```
Next Generation (2nm):
- EOT target: 0.6nm
- HfO2: 1.2nm (12 cycles)
- Interface: 0.2nm
- Leakage: <1E-3 A/cm²

Challenges:
- Thickness control ±0.3Å
- Interface engineering
- Reliability (BTI, TDDB)
- Integration complexity
```

### 9.3 Cost Reduction

| Initiative | Savings | Investment | ROI |
|-----------|---------|------------|-----|
| Precursor optimization | $50/wafer | $100k | 6 months |
| Cycle reduction | $20/wafer | $0 | Immediate |
| Throughput increase | $30/wafer | $200k | 8 months |
| Yield improvement | $100/wafer | $150k | 4 months |

---

## 10. Compliance and Documentation

### 10.1 Quality Records

| Document | Retention | Format | Location |
|----------|-----------|---------|----------|
| Lot travelers | 10 years | Electronic | MES |
| Metrology data | 5 years | Database | Server |
| SPC charts | 3 years | Electronic | Quality system |
| Qualification | Permanent | PDF | Document control |
| Customer COA | 7 years | PDF | Customer portal |

### 10.2 Change Control Process

```
Change Request Flow:
1. Engineering proposal
2. Risk assessment
3. DOE execution
4. Data review
5. Customer notification
6. Qualification lots
7. Implementation
8. Monitoring (30 days)
9. Closure
```

### 10.3 Audit Preparation

**Key Audit Points:**
- Process capability data current
- Calibration certificates valid
- Training matrix complete
- OCAP responses documented
- Change control tracked
- Customer specs available
- Trend charts accessible
- Corrective actions closed

---

## Appendix A: Test Methods

### C-V Measurement Procedure
1. Probe contact on MOS capacitor
2. Frequency: 1 MHz standard
3. Voltage sweep: -3V to +3V
4. Accumulation to inversion
5. Extract: EOT, Vfb, Dit
6. Temperature: 25°C

### Leakage Current Test
1. Apply gate voltage
2. Measure current density
3. Stress: Vg = ±1V
4. Duration: 100s
5. Pass: Ig < 1E-2 A/cm²

---

## Appendix B: Failure Analysis

| Failure Mode | Root Cause | Detection | Prevention |
|--------------|------------|-----------|------------|
| High leakage | Pinholes | Electrical | Particle control |
| EOT shift | Thickness variation | C-V | APC |
| Poor reliability | Interface | TDDB | Process optimization |
| Delamination | Stress | Visual | Temperature control |
| Contamination | Cross-talk | TXRF | Chamber dedication |

---

**Approval:**
- Process Engineering: ___________
- Quality Engineering: ___________
- Manufacturing: ___________
- Customer Representative: ___________

**Effective Date:** 2024-12-01
**Review Cycle:** Quarterly
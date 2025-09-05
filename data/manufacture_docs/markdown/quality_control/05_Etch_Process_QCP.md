# Plasma Etch 공정 품질 관리 계획서
## Quality Control Plan for Gate Etch Process

**문서번호:** QCP-ETCH-GATE-005  
**개정일:** 2024.11.15  
**적용공정:** Poly-Si/High-k Gate Stack Etch  
**기술노드:** 5nm FinFET Technology  

---

## 1. 문서 개요

### 1.1 목적 및 범위
- **목적:** 5nm FinFET gate stack etch 공정의 품질 관리 체계 수립
- **장비:** LAM Kiyo45 Conductor Etch
- **Materials:** Poly-Si/TiN/HfO2/SiO2 stack
- **Critical Parameters:** CD control < ±1nm, Profile 88°±2°
- **목표 수율:** > 99.5%

### 1.2 공정 구조
```
Gate Stack Structure:
┌─────────────┐ ← Hard Mask (SiN) 50nm
├─────────────┤ ← Poly-Si 80nm  
├─────────────┤ ← TiN 5nm
├─────────────┤ ← HfO2 2nm
├─────────────┤ ← SiO2 1nm
└─────────────┘ ← Si Substrate
```

---

## 2. Critical Quality Characteristics

### 2.1 Dimensional Control

| Parameter | Target | USL | LSL | Method | Frequency |
|-----------|--------|-----|-----|--------|-----------|
| Final Gate CD | 20nm | 21nm | 19nm | CD-SEM | 100% |
| CD Bias (Etch-Litho) | -5nm | -3nm | -7nm | Calculation | 100% |
| Gate Height | 80nm | 83nm | 77nm | Cross-section | Daily |
| Sidewall Angle | 88° | 90° | 86° | Cross-section | Daily |
| Footing | < 2nm | 3nm | 0nm | TEM | Weekly |
| Undercut | 0nm | 1nm | -1nm | Cross-section | Daily |
| LER (3σ) | < 1.5nm | 2.0nm | - | CD-SEM | Every lot |

### 2.2 Etch Performance Metrics

| Metric | Specification | Measurement | Control Limit |
|--------|---------------|-------------|---------------|
| Poly-Si Etch Rate | 1500±50 Å/min | Ellipsometer | ±5% |
| HfO2 Selectivity | > 50:1 | XPS analysis | > 40:1 |
| Si Substrate Loss | < 20Å | Ellipsometer | < 30Å |
| Uniformity (WiW) | < 2% (1σ) | 49-point map | < 3% |
| Uniformity (WtW) | < 1% | Wafer average | < 1.5% |
| Endpoint Accuracy | ± 2 seconds | OES signal | ± 3 seconds |

### 2.3 Material Quality

| Property | Specification | Test Method | Sampling |
|----------|---------------|-------------|----------|
| Polymer Residue | None visible | SEM inspection | 5 sites/wafer |
| Metal Contamination | < 1E10 atoms/cm² | TXRF | 1 wafer/lot |
| Surface Damage | < 10Å | TEM | Weekly |
| Gate Oxide Integrity | No degradation | GOI test | Sample |
| Interface Quality | Sharp < 1nm | HR-TEM | Monthly |

---

## 3. Process Control Strategy

### 3.1 Pre-Etch Controls

| Check Point | Specification | Action if OOS |
|-------------|---------------|---------------|
| Incoming CD | 25±1nm | Hold for review |
| PR Thickness | 500±20nm | Rework possible |
| Hard Mask Thickness | 50±2nm | Process adjust |
| Queue Time | < 4 hours | Priority processing |
| Particle Count | < 10 @ 0.12µm | Re-clean |

### 3.2 In-Situ Process Monitoring

```
Real-time Parameters:
┌──────────────┬────────────┬──────────┐
│ Parameter    │ Target     │ Tolerance │
├──────────────┼────────────┼──────────┤
│ Pressure     │ 4mT        │ ±0.2mT   │
│ RF Power     │ 400/100W   │ ±5W      │
│ Bias Voltage │ -250V      │ ±10V     │
│ Temperature  │ 60°C       │ ±2°C     │
│ Gas Flows    │ Per recipe │ ±2%      │
│ DC Bias      │ -180V      │ ±5V      │
└──────────────┴────────────┴──────────┘
```

### 3.3 Endpoint Detection Strategy

| Step | Material | Endpoint Method | Wavelength | Threshold |
|------|----------|-----------------|------------|-----------|
| Main Etch | Poly-Si | OES | 288nm (Si) | 80% drop |
| Over Etch 1 | Poly-Si | Time | - | 20% OE |
| TiN Clear | TiN | OES | 500nm (Ti) | Derivative |
| HfO2 Stop | HfO2 | Interferometry | Broadband | Min signal |
| Final OE | Residual | Time | - | Fixed 10s |

---

## 4. Statistical Process Control

### 4.1 SPC Chart Configuration

| Parameter | Chart Type | Subgroup | Control Limits | Run Rules |
|-----------|------------|----------|---------------|-----------|
| CD Mean | X̄-R | 5 wafers | μ ± 3σ | Western Electric |
| CD Range | R chart | 5 wafers | UCL = D₄R̄ | Trend detection |
| Etch Rate | I-MR | Individual | μ ± 3σ | Nelson rules |
| Profile Angle | X̄-R | 3 samples | μ ± 3σ | Zone rules |
| Uniformity | I-MR | Per wafer | UCL only | Trend rules |

### 4.2 Process Capability Targets

```
Current Performance vs. Targets:
                Current  Target  Action Plan
CD Cpk:         1.78     2.00   Reduce variation
Profile Cpk:    1.65     1.67   Monitor
Uniformity Cp:  2.10     2.00   Maintain
Rate Cpk:       1.82     1.67   Maintain
Defects Ppk:    2.35     2.00   Maintain
```

### 4.3 Multivariate Analysis

| Component | Variables | Method | Action Trigger |
|-----------|-----------|---------|----------------|
| PC1 (45%) | Pressure, Power | Hotelling T² | > UCL |
| PC2 (25%) | Temperature, Bias | EWMA | Trend |
| PC3 (15%) | Gas ratios | CUSUM | Shift |
| PC4 (10%) | Time, Rate | Correlation | R² < 0.9 |

---

## 5. Sampling and Inspection Plans

### 5.1 Measurement Sampling

```
Lot Size Based Sampling:
├─ Development (1-6 wafers)
│  └─ 100% inspection, all sites
├─ Pilot (7-12 wafers)
│  └─ 100% inspection, 17 sites/wafer
├─ Production (13-25 wafers)
│  └─ 3 wafers (F/M/L), 17 sites
└─ HVM (>25 wafers)
   └─ AQL sampling, 5 wafers minimum
```

### 5.2 Measurement Layout

```
17-Point Measurement Map:
        Edge (3mm exclusion)
     •     •     •     •     •
  •     •     •     •     •     •
     •     •  Center  •     •
  •     •     •     •     •     •
     •     •     •     •     •
```

### 5.3 Defect Inspection Strategy

| Inspection Type | Tool | Sampling | Threshold |
|----------------|------|----------|-----------|
| Macro defects | Optical | 100% | 0 allowed |
| Micro defects | E-beam | 20% | < 0.01/cm² |
| Particles | SP3 | 100% | < 20 adds |
| Residue | SEM review | Sample | None allowed |
| Electrical | WAT test | Sample | Meet spec |

---

## 6. Chamber Matching and Qualification

### 6.1 Multi-Chamber Matching Criteria

| Parameter | Chamber-to-Chamber | Method | Frequency |
|-----------|-------------------|--------|-----------|
| CD Offset | < ±0.5nm | Golden wafer | Weekly |
| Etch Rate | < ±3% | Monitor wafer | Daily |
| Uniformity | < ±0.5% absolute | 49-point | Weekly |
| Profile | < ±1° | Cross-section | Monthly |
| Selectivity | < ±10% | Blanket wafers | Weekly |

### 6.2 Qualification Protocol

```
New Chamber Qualification:
Day 1: Installation & Baseline
  ├─ Mechanical checks
  ├─ Leak rate < 1mT/min
  └─ RF calibration
  
Day 2: Process Qualification
  ├─ Season chamber (50 wafers)
  ├─ Rate & uniformity tests
  └─ Particle baseline
  
Day 3: Production Qualification
  ├─ Golden wafer correlation
  ├─ 30 wafer marathon
  └─ SPC limits establishment
  
Day 4: Release
  ├─ Customer notification
  └─ Production release
```

### 6.3 Preventive Maintenance Qualification

| PM Type | Duration | Requalification | Wafers |
|---------|----------|-----------------|---------|
| Daily | 30 min | None | 0 |
| Weekly | 2 hours | Particle check | 3 |
| Monthly | 8 hours | Full qual | 25 |
| Quarterly | 24 hours | Complete | 50 |

---

## 7. Yield Impact and Correlation

### 7.1 Parametric Yield Impact

| Parameter Deviation | Yield Loss | Device Impact | Recovery |
|--------------------|------------|---------------|----------|
| CD +1nm | -1.5% | Vth shift -20mV | Possible |
| CD -1nm | -2.0% | Vth shift +25mV | Limited |
| Profile < 86° | -3% | Short channel | None |
| Footing > 3nm | -5% | Reliability | None |
| Damage > 20Å | -2% | Junction leakage | None |

### 7.2 Defectivity Correlation

```
Defect Density to Yield Model:
Y = Y₀ × exp(-D₀ × A)

Where:
Y = Yield
Y₀ = Baseline yield (99.5%)
D₀ = Defect density (#/cm²)
A = Die area (100mm²)

Critical Defect Types:
- Bridges: -10% yield per defect
- Missing gate: Die kill
- Residue: -2% yield per 10 defects
- Particles: -0.5% per 100 defects
```

### 7.3 Electrical Correlation

| Electrical Parameter | Correlation to CD | Specification |
|---------------------|-------------------|---------------|
| Vth (Threshold) | -20mV/nm | 350±30mV |
| Ion (Drive current) | +2%/nm | >1200 µA/µm |
| Ioff (Leakage) | -15%/nm | <100 pA/µm |
| SS (Subthreshold) | -2mV/dec/nm | <65 mV/dec |
| DIBL | +5mV/V/nm | <50 mV/V |

---

## 8. Advanced Process Control (APC)

### 8.1 Feed-Forward Control

```python
# Incoming CD compensation
def etch_time_adjustment(incoming_cd, target_cd):
    cd_error = incoming_cd - (target_cd + 5)  # 5nm bias
    time_adjustment = cd_error * ETCH_RATE_SENSITIVITY
    new_time = base_time + time_adjustment
    return constrain(new_time, min_time, max_time)

ETCH_RATE_SENSITIVITY = 2.5 sec/nm
```

### 8.2 Feed-Back Control

| Measured Parameter | Control Action | Gain | Limits |
|-------------------|----------------|------|---------|
| CD too large | Increase OE time | 0.3 | ±10 sec |
| CD too small | Decrease OE time | 0.3 | ±10 sec |
| Poor uniformity | Adjust pressure | 0.4 | ±0.5mT |
| Profile deviation | Adjust bias | 0.2 | ±20V |

### 8.3 Virtual Metrology Model

```
Predictive Model Inputs:
- Incoming CD, thickness
- Chamber pressure profile
- RF forward/reflected power
- Endpoint time
- DC bias voltage
- Wafer temperature

Model Output:
- Predicted CD (±0.5nm accuracy)
- Predicted uniformity
- Confidence interval (95%)
- Anomaly score

Model Performance:
- R² = 0.94
- RMSE = 0.45nm
- Update frequency: Daily
```

---

## 9. Continuous Improvement Program

### 9.1 Current Improvement Projects

| Project | Goal | Status | Expected Benefit |
|---------|------|--------|------------------|
| CD Control Enhancement | Cpk > 2.0 | 70% | Yield +0.5% |
| Profile Optimization | < 1° variation | Testing | Reliability |
| Particle Reduction | < 10 adds | Ongoing | Yield +0.3% |
| Throughput Improvement | +10 WPH | Planning | CoO -5% |
| Chemistry Optimization | Selectivity > 100:1 | R&D | Process window |

### 9.2 Technology Roadmap

```
5nm → 3nm Migration Plan:
Q1 2025: Baseline 5nm process
Q2 2025: 3nm test mask
Q3 2025: Process development
Q4 2025: Qualification
Q1 2026: Production

Key Challenges:
- CD target: 14nm
- Aspect ratio: > 8:1
- Selectivity: > 200:1
- LER: < 1.0nm
```

### 9.3 Best Known Methods (BKM)

```
Current BKMs:
1. Chamber Seasoning
   - 20 wafers after wet clean
   - Specific season recipe
   - Particle < 10 adds

2. Endpoint Optimization
   - Multi-wavelength detection
   - Dynamic threshold
   - AI-based prediction

3. Profile Control
   - Dual-frequency pulsing
   - Bias pulsing
   - Temperature ramping

4. Defect Reduction
   - Optimized gas switching
   - Soft landing
   - Post-etch treatment
```

---

## 10. Documentation and Compliance

### 10.1 Required Documentation

| Document Type | Retention | Location | Access |
|--------------|-----------|----------|--------|
| Lot records | 7 years | MES database | Controlled |
| SPC charts | 5 years | Quality system | Open |
| Qualification | Permanent | Document control | Restricted |
| Customer data | 10 years | Secure server | Customer only |
| Equipment logs | 2 years | Tool PC | Engineering |

### 10.2 Audit Readiness

```
Audit Checklist:
□ SPC charts current (within 24 hours)
□ Calibrations valid
□ Training records complete
□ Change control documented
□ OCAP responses documented
□ PM compliance 100%
□ Customer specs available
□ Traceability demonstrated
```

### 10.3 Customer Requirements

| Customer | Special Requirement | Implementation |
|----------|-------------------|----------------|
| Customer A | Cpk > 2.0 all parameters | Enhanced sampling |
| Customer B | 100% CD measurement | No sampling |
| Customer C | Daily reporting | Automated report |
| Customer D | Witness qual runs | Schedule coordination |

---

## Appendix A: Recipe Parameters

### Standard Gate Etch Recipe
```
Step 1: Breakthrough
- Pressure: 10mT
- Source: 500W
- Bias: 50W
- CF4/O2: 50/10 sccm
- Time: 10 sec

Step 2: Main Etch
- Pressure: 4mT
- Source: 400W
- Bias: 100W
- HBr/Cl2/O2: 150/50/5 sccm
- Endpoint: 288nm OES

Step 3: Over Etch
- Pressure: 8mT
- Source: 300W
- Bias: 150W
- HBr/O2: 200/8 sccm
- Time: 20% of ME

Step 4: Soft Landing
- Pressure: 50mT
- Source: 200W
- Bias: 0W
- He/O2: 100/20 sccm
- Time: 5 sec
```

---

## Appendix B: Failure Mode Analysis

| Failure Mode | Probability | Severity | RPN | Mitigation |
|--------------|-------------|----------|-----|------------|
| CD out of spec | Medium | High | 6 | APC control |
| Profile deviation | Low | High | 4 | Recipe optimization |
| Particle excursion | Medium | Medium | 4 | PM schedule |
| Endpoint miss | Low | High | 4 | Multi-wavelength |
| Chamber drift | Medium | Low | 2 | Daily monitoring |

---

**Document Approval:**
- Author: Etch Process Team
- Reviewed: Quality Engineering
- Approved: Operations Director
- Customer Approval: Required for changes

**Next Review:** 2025-02-15
# Lithography Critical Dimension 품질 관리 계획서
## Quality Control Plan for ArF Immersion Lithography CD Control

**문서번호:** QCP-LITHO-CD-004  
**개정일:** 2024.11.15  
**적용공정:** ArF Immersion Lithography  
**기술노드:** 7nm FinFET Critical Layers  

---

## 1. 문서 정보 및 범위

### 1.1 목적
본 문서는 7nm FinFET 공정의 critical layer patterning에서 CD(Critical Dimension) 제어를 위한 품질 관리 체계를 정의하고, 공정 능력 확보 및 지속적 개선을 목표로 합니다.

### 1.2 적용 범위
- **Layers:** Fin, Gate, Contact, M1, Via1
- **Scanner:** ASML NXT:2100i
- **Target CD:** 20-30nm features
- **CD Uniformity:** < 1.5nm (3σ)
- **Overlay:** < 2.0nm (mean + 3σ)

### 1.3 핵심 성과 지표 (KPI)
| Metric | Target | Current | Goal |
|--------|--------|---------|------|
| CD Cpk | > 2.00 | 1.85 | 2.20 |
| CDU (3σ) | < 1.5nm | 1.6nm | 1.3nm |
| LCDU | < 2.0nm | 2.1nm | 1.8nm |
| Overlay | < 2.0nm | 1.9nm | 1.7nm |
| Defect Density | < 0.01/cm² | 0.012 | 0.008 |

---

## 2. CD Measurement Specifications

### 2.1 Measurement Parameters

| Parameter | Specification | Tolerance | Method |
|-----------|---------------|-----------|---------|
| Gate CD | 28nm | ± 1.5nm | CD-SEM |
| Fin Width | 7nm | ± 0.5nm | CD-SEM |
| Contact CD | 30nm | ± 2.0nm | CD-SEM |
| Line Edge Roughness | < 2.5nm (3σ) | - | CD-SEM |
| Sidewall Angle | 88° | ± 2° | Cross-section |
| Resist Height | 90nm | ± 3nm | CD-SEM |

### 2.2 Measurement Strategy

#### Sampling Plan
```
Within Wafer: 17 points
- Center: 1 point
- Middle radius: 8 points @ r=60mm
- Edge: 8 points @ r=140mm

Within Field: 5 points
- Center + 4 corners
- Total: 85 measurements/wafer

Frequency:
- Production: 3 wafers/lot (first, middle, last)
- Development: All wafers
- Qualification: 5 wafers minimum
```

### 2.3 Metrology Tool Requirements

| Tool | Model | Precision (3σ) | Accuracy | Calibration |
|------|-------|---------------|----------|-------------|
| CD-SEM | Hitachi CG6300 | 0.3nm | ± 0.5nm | Daily |
| Scatterometry | KLA SpectraCD | 0.2nm | ± 0.3nm | Weekly |
| AFM | Veeco D3100 | 0.5nm | ± 1.0nm | Monthly |
| Review SEM | AMAT SEMVision | - | - | As needed |

---

## 3. Process Window Qualification

### 3.1 Focus-Exposure Matrix (FEM)

```
Focus Range: -60nm to +60nm (20nm steps)
Dose Range: 26-30 mJ/cm² (0.5 mJ steps)

Process Window Criteria:
- CD Target ± 10%
- CD Uniformity < 2nm
- Profile angle > 86°
- Resist loss < 5%
- No pattern collapse

Overlapping Window:
- DOF: > 150nm
- EL: > 8%
- Window area: > 12 nm·%
```

### 3.2 Process Window Monitoring

| Check | Frequency | Sample | Pass Criteria |
|-------|-----------|--------|---------------|
| Daily FEM | Daily | 1 wafer | Window > baseline |
| Full FEM | Weekly | 3 wafers | DOF > 150nm |
| CD Linearity | Monthly | 5 doses | R² > 0.99 |
| MEEF | Monthly | Various | < 2.5 |
| PEB Sensitivity | Monthly | ± 2°C | < 0.5nm/°C |

### 3.3 Scanner Baseline Management

```
Weekly Baseline Tests:
1. Lens Aberration: < 5mλ RMS
2. Illumination Uniformity: < 0.5%
3. Stage Matching: < 2nm
4. Dose Reproducibility: < 0.3%
5. Focus Reproducibility: < 5nm
```

---

## 4. Statistical Process Control

### 4.1 Control Chart Architecture

| Parameter | Chart Type | Limits | Sampling | Update |
|-----------|------------|--------|----------|---------|
| CD Mean | X-bar R | ± 3σ | 17 pts/wafer | Real-time |
| CDU | R chart | UCL only | Per wafer | Real-time |
| Overlay X | X-bar R | ± 3σ | Per lot | Batch |
| Overlay Y | X-bar R | ± 3σ | Per lot | Batch |
| Dose | I-MR | ± 3σ | Per wafer | Real-time |
| Focus | I-MR | ± 3σ | Per wafer | Real-time |

### 4.2 Advanced Process Control (APC)

#### Feedback Control
```python
# CD Feedback Algorithm
def cd_correction(target, measured, gain=0.3):
    error = target - measured
    dose_correction = error * DOSE_SENSITIVITY
    new_dose = current_dose + (dose_correction * gain)
    return clip(new_dose, min_dose, max_dose)

# Parameters
DOSE_SENSITIVITY = 0.5 nm/(mJ/cm²)
FOCUS_SENSITIVITY = 0.03 nm/nm
PEB_SENSITIVITY = 0.4 nm/°C
```

#### Feedforward Control
- Previous layer overlay data
- Incoming film thickness
- Wafer shape data
- Tool matching offsets

### 4.3 Run-to-Run Control Limits

| Parameter | Adjustment Range | Max Step | Gain |
|-----------|-----------------|----------|------|
| Dose | ± 2 mJ/cm² | 0.5 mJ | 0.3 |
| Focus | ± 20nm | 5nm | 0.4 |
| PEB Temp | ± 2°C | 0.5°C | 0.5 |
| Develop Time | ± 3s | 1s | 0.3 |

---

## 5. Defectivity Control

### 5.1 Defect Specifications

| Defect Type | Size | Limit/cm² | Action Level |
|-------------|------|-----------|--------------|
| Particles | > 30nm | < 10 | Hold @ 20 |
| Pattern defects | Any | < 5 | Hold @ 10 |
| Bridging | Any | 0 | Immediate hold |
| Line collapse | Any | < 2 | Review required |
| Residue | > 50nm | < 5 | Clean review |

### 5.2 Defect Review Flow

```
Inspection → Classification → Review Decision
    ↓             ↓              ↓
KLA 2935    Auto-classify   SEM Review (>20%)
    ↓             ↓              ↓
Defect Map   Binning      Root Cause Analysis
    ↓             ↓              ↓
Database     Statistics    Corrective Action
```

### 5.3 Systematic Defect Analysis

| Pattern | Likely Cause | Verification | Action |
|---------|-------------|--------------|--------|
| Center cluster | Dispense issue | Video review | Nozzle check |
| Edge ring | EBR problem | Process check | EBR adjustment |
| Random | Particles | Filter check | Filter change |
| Repeating | Reticle defect | Reticle inspection | Clean/replace |
| Radial | Spin issue | RPM verify | Motor service |

---

## 6. Material Control

### 6.1 Photoresist Management

| Control Point | Specification | Frequency | Action |
|--------------|---------------|-----------|---------|
| Incoming QC | Vendor CoA | Every lot | Review |
| Viscosity | 2.5 ± 0.1 cP | Every bottle | Reject if OOS |
| Particle count | < 10/mL @ 0.1µm | Every bottle | Filter/reject |
| Thickness test | Target ± 1% | Every bottle | Adjust spin |
| Shelf life | < 6 months | Daily check | FIFO usage |
| Temperature | 23.0 ± 0.1°C | Continuous | Alarm |

### 6.2 Chemical Quality Monitoring

```
Developer (TMAH):
- Concentration: 2.38 ± 0.01%
- Temperature: 23.0 ± 0.1°C
- Normality check: Every 4 hours
- Metal content: < 1 ppb (weekly)
- Particle count: < 10/mL @ 0.2µm

BARC Material:
- Thickness uniformity: < 1%
- n, k values: ± 0.01
- Shelf life tracking: 3 months
- Contamination: < 10 ppb metals
```

### 6.3 Reticle Quality Control

| Check | Frequency | Specification | Tool |
|-------|-----------|---------------|------|
| CD bias | Monthly | ± 1nm from design | AIMS |
| Defects | Weekly | 0 printable | KLA Teron |
| Pellicle | Daily | No particles > 1µm | Visual |
| Phase (PSM) | Quarterly | 180° ± 2° | Interferometer |
| Registration | Monthly | < 5nm | Registration tool |

---

## 7. Equipment Qualification

### 7.1 Scanner Qualification Matrix

| Test | New Install | Post-PM | Periodic | Spec |
|------|-------------|---------|----------|------|
| Overlay | ✓ | ✓ | Monthly | < 2nm |
| CD Uniformity | ✓ | ✓ | Weekly | < 1.5nm |
| Focus Uniformity | ✓ | ✓ | Weekly | < 20nm |
| Dose Uniformity | ✓ | ✓ | Daily | < 0.5% |
| Illumination | ✓ | ✓ | Monthly | Pupil fill |
| Aberrations | ✓ | - | Quarterly | < 5mλ |

### 7.2 Track System Qualification

| Module | Parameter | Specification | Frequency |
|--------|-----------|---------------|-----------|
| Coater | Thickness uniformity | < 1% | Daily |
| Developer | Uniformity | < 2nm CD impact | Daily |
| Hot Plate | Temperature uniformity | ± 0.3°C | Weekly |
| Cool Plate | Temperature stability | ± 0.5°C | Monthly |

### 7.3 Metrology Qualification

```
CD-SEM Qualification:
1. Magnification calibration: ± 1%
2. Beam stability: < 0.5% drift
3. Stage accuracy: ± 0.5µm
4. Measurement precision: < 0.3nm (3σ)
5. Tool-to-tool matching: < 0.5nm offset
```

---

## 8. Yield Impact Analysis

### 8.1 CD Impact on Yield

| CD Deviation | Yield Impact | Device Impact | Recovery |
|-------------|--------------|---------------|----------|
| ± 1nm | -0.5% | Speed variation | Binning |
| ± 2nm | -2% | Leakage increase | Possible |
| ± 3nm | -5% | Functionality | Limited |
| > 3nm | -10% | Failure | None |

### 8.2 Correlation Studies

```
Correlation Matrix:
          CD    CDU   Overlay  Defect
Yield    0.85  0.72   0.68    -0.75
Speed    0.92  0.65   0.45    -0.35
Power   -0.78  -0.82  -0.55    0.45
Leakage -0.88  -0.75  -0.62    0.68
```

### 8.3 Yield Prediction Model

```python
def yield_prediction(cd_mean, cd_sigma, overlay, defects):
    cd_factor = exp(-((cd_mean - target) / tolerance)**2)
    uniformity_factor = exp(-(cd_sigma / spec_limit)**2)
    overlay_factor = exp(-(overlay / overlay_spec)**2)
    defect_factor = exp(-defects * die_area)
    
    predicted_yield = baseline_yield * cd_factor * 
                     uniformity_factor * overlay_factor * 
                     defect_factor
    return predicted_yield
```

---

## 9. Continuous Improvement

### 9.1 CD Reduction Roadmap

| Node | Current | Next Gen | Challenge | Solution |
|------|---------|----------|-----------|----------|
| Gate | 28nm | 20nm | Resolution | EUV |
| Fin | 7nm | 5nm | Roughness | Material |
| Contact | 30nm | 25nm | Aspect ratio | Hard mask |
| Metal | 32nm | 24nm | RC delay | Alternative |

### 9.2 Technology Enablers

```
Current Development:
1. DSA (Directed Self-Assembly)
   - Target: 3nm half-pitch
   - Status: Integration

2. Multi-patterning
   - SAQP for fin
   - LELE for metal
   - Status: Production

3. EUV Insertion
   - Single exposure
   - Simplified process
   - Status: Qualification

4. Advanced Materials
   - Metal oxide resist
   - Underlayer innovation
   - Status: Evaluation
```

### 9.3 Cost Reduction Initiatives

| Project | Saving/wafer | Implementation | ROI |
|---------|--------------|----------------|-----|
| Dose optimization | $0.05 | Q1 2025 | 3 months |
| Skip lot increase | $0.10 | Ongoing | Immediate |
| Resist consumption | $0.15 | Q2 2025 | 6 months |
| Rework reduction | $0.20 | Ongoing | 2 months |
| Throughput improve | $0.25 | Q3 2025 | 12 months |

---

## 10. Documentation and Reporting

### 10.1 Quality Reports

| Report | Frequency | Distribution | Content |
|--------|-----------|--------------|---------|
| CD Daily | Daily | Process team | SPC charts |
| Weekly Summary | Weekly | Management | Trends, issues |
| Monthly QBR | Monthly | All stakeholders | Full analysis |
| Customer Report | Monthly | Customer | Agreed metrics |

### 10.2 Data Management

```
Data Retention Policy:
- Raw measurements: 2 years
- SPC data: 5 years
- Images: 6 months
- Qualification: Permanent
- Customer data: 7 years

Data Format:
- Database: Oracle
- Analysis: JMP/Minitab
- Reporting: Tableau
- Archive: Secured NAS
```

### 10.3 Change Control

| Change Type | Approval Level | Validation | Customer Notice |
|-------------|---------------|------------|-----------------|
| Spec change | Director | Full qual | 30 days prior |
| Process change | Manager | 3 lots | 14 days prior |
| Material change | Manager | 5 lots | 14 days prior |
| Tool change | Engineer | 1 lot | Post-change |

---

## Appendix A: Calculation Methods

### CD Uniformity Calculation
```
CDU (3σ) = 3 × STDEV(all measurements)
CDU (Range) = MAX(CD) - MIN(CD)
CDU (%) = (CDU / Mean CD) × 100
```

### Process Capability
```
Cp = (USL - LSL) / (6 × σ)
Cpk = MIN[(USL - μ)/3σ, (μ - LSL)/3σ]
Ppk = MIN[(USL - μ)/3σ_lt, (μ - LSL)/3σ_lt]
```

---

## Appendix B: Troubleshooting Guide

| Issue | Check Points | Typical Cause | Solution |
|-------|-------------|---------------|----------|
| CD Large | Dose, Focus | Over-exposure | Reduce dose |
| CD Small | Dose, Focus | Under-exposure | Increase dose |
| CDU Poor | Scanner, Track | Non-uniformity | Calibration |
| LER High | Resist, Process | Material/Process | Optimization |
| Profile | PEB, Development | Temperature | Adjustment |

---

**Approval Signatures:**
- Process Engineering: ___________
- Quality Assurance: ___________
- Manufacturing: ___________
- Customer Quality: ___________

**Next Review Date:** 2025-02-15
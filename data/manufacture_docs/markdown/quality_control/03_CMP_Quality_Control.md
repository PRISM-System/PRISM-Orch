# CMP 공정 품질 관리 계획서
## Quality Control Plan for Cu/Barrier CMP Process

**문서번호:** QCP-CMP-CU-003  
**개정일:** 2024.11.15  
**적용제품:** 10nm FinFET Technology  
**공정단계:** Copper CMP (M1-M8 Layers)  

---

## 1. 문서 개요 및 적용 범위

### 1.1 목적
본 문서는 10nm FinFET 공정의 Cu damascene metallization을 위한 CMP 공정에서 품질 관리 기준, 측정 방법 및 개선 활동을 정의합니다.

### 1.2 적용 범위
- **공정:** Cu bulk removal, Barrier removal, Touch-up
- **장비:** Applied Materials Reflexion LK
- **Layer:** M1 through M8 metal layers
- **목표:** Dishing < 300Å, Erosion < 200Å
- **AQL:** 0.040%

### 1.3 참조 표준
- SEMI P38: CMP Planarity Metrics
- SEMI P40: Cu CMP Defectivity
- JEDEC JEP157: Copper Interconnect Reliability
- IPC-9701: CMP Process Characterization

---

## 2. Critical Quality Parameters

### 2.1 Dimensional Control

| Parameter | Target | USL | LSL | Measurement | Frequency |
|-----------|--------|-----|-----|-------------|-----------|
| Post-CMP Thickness | 3000Å | 3150Å | 2850Å | XRF/4-point | 100% |
| Within-Die Range | < 200Å | 250Å | - | Profilometer | 5 die/wafer |
| Wafer Uniformity | < 3% | 4% | - | 49-point map | Every wafer |
| Dishing (100µm line) | < 200Å | 300Å | - | AFM | Daily monitor |
| Erosion (50% density) | < 150Å | 200Å | - | Profilometer | Daily monitor |
| Edge Exclusion | 3mm | 3.5mm | 2.5mm | Visual | Every lot |

### 2.2 Surface Quality Metrics

| Parameter | Specification | Method | Sampling |
|-----------|---------------|---------|----------|
| Scratches | 0 counts > 0.25µm width | Optical inspection | 100% |
| Particles | < 30 adds @ 0.18µm | SP2 inspection | 100% |
| Residual Cu | < 1E10 atoms/cm² | TXRF | 1 wafer/lot |
| Corrosion | No visible defects | Optical | 100% |
| Surface Roughness | Ra < 2Å | AFM | Weekly |

### 2.3 Electrical Parameters

| Test | Specification | Method | Frequency |
|------|---------------|---------|-----------|
| Sheet Resistance | 1.8 ± 0.2 mΩ/□ | 4-point probe | Every wafer |
| Line Resistance | Target ± 10% | Electrical test | Sample |
| Via Resistance | < 2Ω | Kelvin structure | Sample |
| Leakage Current | < 1E-9 A/cm² | IV test | Sample |
| Breakdown Voltage | > 5 MV/cm | TDDB | Weekly |

---

## 3. Process Control Methodology

### 3.1 Pre-CMP Requirements

| Check Item | Specification | Action if OOS |
|------------|---------------|---------------|
| Incoming Cu Thickness | 8000 ± 200Å | Hold for review |
| Incoming Particles | < 20 @ 0.18µm | Re-clean |
| Surface Oxidation | < 20Å CuOx | Adjust queue time |
| Wafer Bow | < 50µm | Stress evaluation |
| Pattern Density | Per design rule | Design review |

### 3.2 In-Process Monitoring

#### Real-time Parameters
| Parameter | Target | Range | Control Action |
|-----------|--------|-------|----------------|
| Removal Rate | 6000 Å/min | ± 300 | Adjust time |
| Selectivity Cu:Ta | 100:1 | > 80:1 | Slurry check |
| Pad Temperature | 55°C | ± 3°C | Conditioning |
| Slurry Flow | 200 ml/min | ± 10 | MFC calibration |
| Endpoint Signal | Defined | ± 5% | Recipe update |

### 3.3 Post-CMP Quality Checks

```
Immediate (< 30 min):
□ Residual Cu inspection
□ Thickness measurement  
□ Defect inspection
□ Corrosion check

Within 2 hours:
□ Sheet resistance
□ Cross-section (sample)
□ Surface analysis
□ Particle count

End of Lot:
□ Yield correlation
□ Reliability sample
□ SPC update
□ Lot disposition
```

---

## 4. Sampling Plans

### 4.1 Production Sampling

| Lot Size | Measurement Sample | Defect Inspection | Reliability |
|----------|-------------------|------------------|-------------|
| 1-6 | 100% | 100% | 1 wafer |
| 7-12 | 5 wafers | 100% | 1 wafer |
| 13-25 | 3 wafers + first/last | 5 wafers | 2 wafers |
| >25 | 13 wafers | 20% min 5 | 3 wafers |

### 4.2 Measurement Locations

```
49-Point Map for Uniformity:
     R = 140mm (edge -10mm)
     R = 120mm  
     R = 100mm
     R = 80mm
     R = 60mm
     R = 40mm
     R = 20mm
     Center

5 sites/radius, 7 radii = 35 points
+ 14 edge points @ R=145mm
Total = 49 points
```

### 4.3 Skip Lot Criteria
**Eligible after:**
- 10 consecutive lots pass
- Cpk > 1.67 for all parameters
- No customer complaints
- Stable removal rate ± 5%

**Reduced inspection:**
- Measurement: 3 wafers/lot
- Defect: 2 wafers/lot
- Skip lot rate: Maximum 50%

---

## 5. Defectivity Control

### 5.1 Defect Classification

| Category | Size/Type | Limit | Action |
|----------|-----------|-------|---------|
| Micro-scratch | < 0.25µm width | < 10/wafer | Monitor |
| Macro-scratch | > 0.25µm width | 0/wafer | Hold lot |
| Particles | > 0.18µm | < 30 adds | Monitor |
| Residue | Any size | < 5/wafer | Re-polish |
| Corrosion | Any | 0/wafer | Immediate action |
| Missing pattern | Any | 0/die | Scrap |

### 5.2 Defect Source Analysis

| Defect Type | Common Sources | Detection | Prevention |
|-------------|---------------|-----------|------------|
| Scratches | Pad debris, Dried slurry | Brightfield | Pad conditioning |
| Particles | Slurry agglomeration | Darkfield | Filter change |
| Residue | Under-polish | SEM review | Process time |
| Corrosion | pH, Queue time | Optical | Rinse optimization |
| Fangs | Over-polish | Cross-section | Endpoint control |

### 5.3 Defect Reduction Strategy

```
PDCA Cycle Implementation:
Plan: Defect Pareto analysis
Do: Implement improvements
Check: Monitor 20 lots
Act: Standardize if successful

Current Projects:
1. Scratch reduction: Pad break-in optimization
2. Particle reduction: Slurry filtration upgrade  
3. Corrosion prevention: BTA concentration
4. Residue elimination: Megasonic clean
```

---

## 6. Statistical Process Control

### 6.1 Control Charts Configuration

| Parameter | Chart Type | Subgroup | Limits | Rules |
|-----------|------------|----------|--------|-------|
| Removal Rate | X-bar R | 5 wafers | ± 3σ | Western Electric |
| Uniformity | X-bar R | 3 wafers | ± 3σ | Nelson Rules |
| Dishing | I-MR | Daily average | ± 3σ | Zone Rules |
| Particles | C-chart | Per wafer | UCL only | Trend Rules |
| Sheet Rs | X-bar S | 5 sites | ± 3σ | All rules |

### 6.2 Process Capability Analysis

| Metric | Current Cp | Current Cpk | Target Cpk | Action Plan |
|--------|------------|-------------|------------|-------------|
| Thickness | 1.85 | 1.72 | > 1.67 | Maintain |
| Uniformity | 2.10 | 1.95 | > 1.67 | Maintain |
| Dishing | 1.45 | 1.38 | > 1.33 | Monitor |
| Erosion | 1.42 | 1.35 | > 1.33 | Monitor |
| Defects | 2.25 | 2.15 | > 2.00 | Maintain |

### 6.3 Out-of-Control Action Plan

| Violation | Response Time | Action | Escalation |
|-----------|--------------|---------|------------|
| 1 point > 3σ | Immediate | Hold lot | Engineer |
| 2/3 points > 2σ | < 1 hour | Investigate | Supervisor |
| 4/5 points > 1σ | < 2 hours | Check process | Engineer |
| 8 points same side | < 4 hours | Baseline check | Manager |
| 6 points trend | Next lot | Monitor closely | Engineer |

---

## 7. Equipment Qualification

### 7.1 Consumables Qualification

| Item | Qualification | Frequency | Criteria |
|------|--------------|-----------|----------|
| Polishing Pad | 25 dummy wafers | New pad | Rate ± 5%, Defects < 20 |
| Slurry Lot | 5 monitor wafers | New lot | Rate ± 3%, Selectivity |
| Conditioning Disk | 10 wafers | 500 hours | Pad cut rate |
| Retaining Ring | 5 wafers | New ring | Uniformity < 3% |
| Membrane | 3 wafers | Installation | No leaks |

### 7.2 Preventive Maintenance Impact

```
PM Qualification Requirements:
Minor PM (Weekly):
- 5 dummy wafers
- Particle check
- Rate verification

Major PM (Monthly):
- 25 dummy wafers
- Full qualification
- Correlation to reference
- Customer notification if needed
```

### 7.3 Multi-Tool Matching

| Parameter | Tool-to-Tool | Method | Frequency |
|-----------|-------------|---------|-----------|
| Removal Rate | ± 5% | Golden wafer | Weekly |
| Uniformity | ± 0.5% absolute | 49-point | Weekly |
| Dishing | ± 20Å | Test mask | Monthly |
| Defectivity | ± 5 counts | Split lot | Monthly |

---

## 8. Hold and Disposition Criteria

### 8.1 Automatic Hold Triggers

| Condition | Hold Type | Sample Required | Release Authority |
|-----------|-----------|-----------------|-------------------|
| Scratch detected | Quality | 100% inspection | Quality Engineer |
| Thickness OOS | Quality | 5 additional | Process Engineer |
| Uniformity > 5% | Process | 100% measurement | Process Engineer |
| Corrosion found | Quality | All wafers | Quality Manager |
| Rate shift > 10% | Equipment | None | Equipment Engineer |
| New consumable | Process | 5 wafers | Process Engineer |

### 8.2 Disposition Flow Chart

```
Lot On Hold
    ├── Spec Violation?
    │   ├── Major: Scrap/Rework Decision
    │   └── Minor: Engineering Review
    ├── Cosmetic Issue?
    │   ├── Customer Critical: Customer Review
    │   └── Non-critical: Document and Release
    └── Process Issue?
        ├── Correctable: Rework
        └── Non-correctable: Risk Assessment
```

### 8.3 Rework Criteria

| Condition | Rework Allowed | Method | Verification |
|-----------|---------------|---------|--------------|
| Under-polish | Yes | Additional polish | 100% measurement |
| Over-polish < 10% | No | - | Scrap |
| Residual Cu | Yes | Touch-up polish | Defect inspection |
| High particles | Yes | Megasonic clean | Re-inspect |
| Scratches | No | - | Customer decision |

---

## 9. Continuous Improvement Program

### 9.1 Key Performance Indicators

| KPI | Current | Target | Best in Class |
|-----|---------|---------|---------------|
| First Pass Yield | 97.5% | 98% | 99% |
| Defect Density | 0.02/cm² | 0.01/cm² | 0.005/cm² |
| Cpk Average | 1.65 | 1.67 | 2.00 |
| Tool Utilization | 85% | 88% | 92% |
| CoO ($/wafer) | $3.50 | $3.00 | $2.50 |

### 9.2 Improvement Projects

| Project | Goal | Status | Expected Benefit |
|---------|------|--------|------------------|
| APC Implementation | Reduce variation | 60% complete | Cpk +0.2 |
| Endpoint Optimization | Reduce dishing | Planning | Dishing -50Å |
| Slurry Reduction | Cost saving | Testing | -$0.30/wafer |
| Pad Life Extension | 2000→2500 wafers | Ongoing | -$0.20/wafer |

### 9.3 Innovation Initiatives

```
Next Generation Development:
1. Barrier-free Cu process
2. Alternative slurry chemistry
3. Pad-free CMP evaluation
4. ML-based process control
5. Predictive maintenance model
```

---

## 10. Training and Certification

### 10.1 Operator Certification Levels

| Level | Requirements | Privileges | Recertification |
|-------|--------------|------------|-----------------|
| Level 1 | Basic training + 40 hours | Lot processing | Annual |
| Level 2 | Level 1 + 200 hours | Minor PM | Annual |
| Level 3 | Level 2 + Advanced course | All operations | 2 years |
| Trainer | Level 3 + Teaching course | Train others | 2 years |

### 10.2 Critical Skills Matrix

| Skill | Level 1 | Level 2 | Level 3 |
|-------|---------|---------|---------|
| Lot processing | ✓ | ✓ | ✓ |
| Defect recognition | Basic | Advanced | Expert |
| SPC interpretation | View | Analyze | Action |
| Troubleshooting | Escalate | Basic | Advanced |
| PM activities | Assist | Perform | Lead |

---

## Appendix A: Measurement Procedures

### Thickness Measurement SOP
1. XRF Calibration check
2. 49-point automatic program
3. Data validation (remove outliers)
4. Calculate uniformity
5. Upload to SPC system

### AFM Dishing Measurement
1. Locate test structure
2. 10µm x 10µm scan
3. Average 5 locations
4. Calculate step height
5. Report maximum dishing

---

## Appendix B: Troubleshooting Matrix

| Symptom | Probable Cause | Verification | Corrective Action |
|---------|---------------|--------------|-------------------|
| High dishing | Over-polish | Time/removal | Reduce time |
| Poor uniformity | Pressure profile | Zone pressure | Adjust zones |
| Scratches | Pad contamination | Pad inspection | Conditioning |
| Residue | Under-polish | Optical check | Increase time |
| Corrosion | Chemistry | pH measurement | Adjust chemistry |

---

**Document Control:**
- Author: CMP Process Team
- Review: Quality Assurance
- Approval: Manufacturing Director
- Next Review: 2025-02-15

**Distribution:**
- CMP Process Engineering
- Quality Control
- Manufacturing
- Customer Quality (upon request)
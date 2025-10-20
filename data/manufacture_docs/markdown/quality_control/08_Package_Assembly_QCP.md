# Package Assembly 품질 관리 계획서
## Quality Control Plan for FC-BGA Package Assembly

**문서번호:** QCP-PKG-FCBGA-008  
**개정일:** 2024.11.15  
**적용제품:** High-Performance Computing Processor  
**패키지 유형:** Flip Chip Ball Grid Array (FC-BGA)  

---

## 1. 문서 개요 및 적용 범위

### 1.1 목적
본 문서는 고성능 프로세서의 FC-BGA 패키지 조립 공정에 대한 품질 관리 체계를 정의하고, 제품 신뢰성과 수율을 보증합니다.

### 1.2 패키지 사양
- **Package Size:** 45mm × 45mm
- **Ball Count:** 2397 balls
- **Ball Pitch:** 0.8mm
- **Substrate Layers:** 12L build-up
- **Die Size:** 400mm² (20mm × 20mm)
- **Target Yield:** > 98%

### 1.3 공정 흐름
```
Wafer Preparation → Bumping → Dicing → Die Attach
    ↓
Underfill → Lid Attach → Ball Attach → Singulation
    ↓
Final Test → Marking → Packing → Shipping
```

---

## 2. Critical Quality Parameters

### 2.1 Bump/UBM Quality

| Parameter | Specification | Method | Frequency |
|-----------|---------------|---------|-----------|
| Bump Height | 80±5µm | Laser profiler | 100% |
| Bump Diameter | 100±5µm | Optical | Sample |
| Coplanarity | <5µm | 3D measurement | 100% |
| Shear Strength | >80g | Shear test | Sample |
| IMC Thickness | 2-4µm | Cross-section | Daily |
| Void Content | <5% | X-ray | Sample |

### 2.2 Die Attach Process

```
Flip Chip Bonding Parameters:
- Placement Accuracy: ±10µm
- Bond Force: 50-100N
- Bond Temperature: 320°C
- Bond Time: 3-5 seconds
- Atmosphere: N₂ with 5% H₂

Quality Metrics:
- Alignment: <15µm deviation
- Standoff Height: 60±5µm
- Joint Resistance: <5mΩ
- Void: <10% per joint
```

### 2.3 Underfill Properties

| Property | Specification | Test Method |
|----------|---------------|-------------|
| Viscosity | 8,000±500 cP | Rheometer |
| Tg | >125°C | DSC |
| CTE (α1/α2) | 28/95 ppm/°C | TMA |
| Modulus | 8±1 GPa | DMA |
| Adhesion | >10 MPa | Die shear |
| Fillet Height | >50% die height | Optical |
| Void | <2% total area | C-SAM |

### 2.4 Ball Attach Quality

| Parameter | Specification | Control Limit |
|-----------|---------------|---------------|
| Ball Size | 0.45±0.02mm | ±0.03mm |
| Coplanarity | <0.08mm | <0.10mm |
| Position Accuracy | ±0.05mm | ±0.08mm |
| Shear Force | >500g | >400g |
| Missing Ball | 0 | 0 |
| Ball Void | <10% | <15% |

---

## 3. In-Process Quality Control

### 3.1 Wafer Level Inspection

```
Pre-Assembly Inspection:
□ Bump inspection (100% AOI)
□ Coplanarity measurement
□ Contamination check
□ Sawing quality
□ Die visual inspection

Acceptance Criteria:
- No missing bumps
- No bump damage
- Coplanarity <5µm
- No contamination
- Clean die edges
```

### 3.2 Assembly Process Monitoring

| Process Step | Control Parameters | Monitoring | SPC |
|--------------|-------------------|------------|-----|
| Die Placement | X,Y,θ accuracy | Vision system | X̄-R |
| Reflow | Temperature profile | Thermocouples | I-MR |
| Underfill | Flow time, coverage | Visual/Timer | X̄-R |
| Cure | Temperature, time | Data logger | I-MR |
| Ball Attach | Placement, reflow | AOI | p-chart |

### 3.3 Real-time Defect Detection

```python
# AOI Defect Classification
defect_categories = {
    'Critical': ['Missing die', 'Missing ball', 'Bridge'],
    'Major': ['Misalignment >20µm', 'Void >15%', 'Crack'],
    'Minor': ['Cosmetic', 'Marking', 'Surface']
}

def classify_defect(defect_type, size, location):
    if defect_type in defect_categories['Critical']:
        return 'REJECT'
    elif defect_type in defect_categories['Major']:
        return 'REWORK' if rework_possible else 'REJECT'
    else:
        return 'ACCEPT_WITH_NOTE'
```

---

## 4. Reliability Testing

### 4.1 Package Level Reliability

| Test | Condition | Duration | Criteria |
|------|-----------|----------|----------|
| TC (Thermal Cycling) | -55/125°C | 1000 cycles | No failure |
| HTSL (Storage Life) | 150°C | 1000 hrs | No failure |
| uHAST | 130°C/85%RH | 96 hrs | No failure |
| HTOL (Operating Life) | 125°C, Vmax | 1000 hrs | <1% fail |
| Drop Test | JESD22-B111 | 30 drops | No failure |
| Bend Test | JESD22-B113 | 2mm | No crack |

### 4.2 Board Level Reliability

```
Test Conditions and Requirements:
Temperature Cycling B (-55/125°C):
- Cycles: 500 minimum
- Dwell: 10 minutes
- Ramp: <15°C/min
- Failure: <1% at 500 cycles

Mechanical Shock:
- Peak: 1500G
- Duration: 0.5ms
- Direction: ±X, ±Y, ±Z
- Drops: 5 each direction
```

### 4.3 Failure Analysis Flow

```
Failure Detected
    ↓
Non-Destructive Analysis
- External Visual
- X-ray (2D/3D)
- C-SAM
- Electrical Test
    ↓
Destructive Analysis
- Cross-section
- Dye & Pry
- SEM/EDX
- FIB
    ↓
Root Cause & Corrective Action
```

---

## 5. Statistical Process Control

### 5.1 Key Process Indicators

| KPI | Target | Current | Cpk Goal |
|-----|--------|---------|----------|
| Assembly Yield | >98% | 97.8% | >1.67 |
| First Pass Yield | >95% | 94.5% | >1.67 |
| Defect Rate | <1000 PPM | 1200 PPM | >2.00 |
| Coplanarity | <80µm | 75µm | >1.67 |
| Ball Shear | >500g | 550g | >2.00 |

### 5.2 Control Chart Implementation

```
Control Chart Matrix:
Process         Parameter        Chart    Limits
Die Attach      Accuracy        X̄-R      ±10µm
Underfill       Flow Time       X̄-R      ±5 sec
Reflow          Peak Temp       I-MR     ±3°C
Ball Attach     Coplanarity     X̄-R      ±10µm
Warpage         Post-reflow     I-MR     <150µm
```

### 5.3 Process Capability Analysis

| Process | Cp | Cpk | Ppk | Action |
|---------|-----|-----|-----|---------|
| Die Placement | 2.10 | 1.95 | 1.82 | Monitor |
| Bump Joint | 1.85 | 1.72 | 1.65 | Improve |
| Ball Attach | 2.25 | 2.15 | 2.05 | Maintain |
| Warpage | 1.60 | 1.45 | 1.35 | Critical |

---

## 6. Sampling Plans and Inspection

### 6.1 Visual Inspection Criteria

```
AQL Sampling (MIL-STD-105E):
Lot Size: 500 units
Inspection Level: II
AQL: 0.65%

Sample Size: 50 units
Accept: 1 defect
Reject: 2 defects

Critical Defects (AQL 0.1%):
- Missing die/component
- Wrong die/component
- Functional failure

Major Defects (AQL 0.65%):
- Dimension out of spec
- Cosmetic major
- Marking error
```

### 6.2 Measurement Sampling Strategy

| Measurement | Sample Size | Frequency | Method |
|-------------|-------------|-----------|---------|
| Coplanarity | 5 units/lot | Every lot | Laser |
| Ball Shear | 5 balls × 3 units | Daily | Shear test |
| Warpage | 3 units/lot | Every lot | Shadow Moiré |
| Cross-section | 1 unit | Weekly | Microscopy |
| X-ray | 10% | Every lot | 2D X-ray |

### 6.3 Outgoing Quality Control

```
Final Inspection Checklist:
□ Visual inspection (100%)
□ Dimension check (Sample)
□ Marking verification (100%)
□ Moisture sensitivity level
□ Packing integrity
□ Documentation complete
□ CoC preparation
```

---

## 7. Material Control

### 7.1 Incoming Material Inspection

| Material | Key Parameters | Acceptance Criteria |
|----------|---------------|-------------------|
| Substrate | Warpage, dimension | <150µm, ±0.1mm |
| Solder Ball | Size, composition | ±20µm, Sn3.0Ag0.5Cu |
| Underfill | Viscosity, Tg | ±500cP, >125°C |
| Flux | Acid value, viscosity | 35±5, spec |
| Die | Bump quality, thickness | 100% KGD |

### 7.2 Material Storage and Handling

```
Storage Conditions:
Substrate: 20-25°C, <60%RH, N₂ cabinet
Solder Ball: 5-10°C, <12 months
Underfill: -40°C, <6 months
Flux: 5-10°C, <3 months

MSL (Moisture Sensitivity Level):
Level 3: Floor life 168 hours
Baking: 125°C for 24 hours if exceeded
Dry pack within 30 minutes after baking
```

### 7.3 Material Traceability

```
Lot Tracking System:
Raw Material Lot → Process Lot → Assembly Lot
                        ↓
                  Customer Lot Code
                        ↓
                  Field Returns

Information Tracked:
- Date code
- Operator ID
- Equipment ID
- Process parameters
- Test results
```

---

## 8. Yield Management

### 8.1 Yield Loss Analysis

```
Yield Loss Pareto (Current):
1. Ball defects (35%)
   - Missing ball: 15%
   - Ball bridge: 10%
   - Coplanarity: 10%

2. Die attach (25%)
   - Misalignment: 15%
   - Non-wet: 10%

3. Underfill (20%)
   - Voids: 12%
   - Delamination: 8%

4. Others (20%)
```

### 8.2 Yield Improvement Actions

| Issue | Root Cause | Action | Expected Gain |
|-------|------------|--------|---------------|
| Missing ball | Flux insufficient | Optimize flux volume | +0.5% |
| Misalignment | Vision calibration | Daily calibration | +0.3% |
| Underfill void | Dispense pattern | Pattern optimization | +0.4% |
| Warpage | Reflow profile | Profile optimization | +0.2% |

### 8.3 Scrap and Rework Management

```
Rework Decision Matrix:
Defect Type     Rework Possible    Success Rate
Ball missing    Yes               95%
Ball bridge     Yes               90%
Die misalign    No                -
Underfill void  Limited           70%
Crack          No                -

Scrap Categories:
- Process scrap: 1.5%
- Test reject: 0.3%
- Quality hold: 0.2%
- Customer return: <100 PPM
```

---

## 9. Equipment Qualification

### 9.1 New Equipment Qualification

```
Qualification Steps:
1. Installation Qualification (IQ)
   - Utilities connection
   - Safety verification
   - Software validation

2. Operational Qualification (OQ)
   - Process capability
   - Repeatability study
   - Correlation to reference

3. Performance Qualification (PQ)
   - Production lots (minimum 3)
   - Yield verification
   - Reliability testing
```

### 9.2 Preventive Maintenance

| Equipment | Daily | Weekly | Monthly | Quarterly |
|-----------|-------|--------|---------|-----------|
| Die Bonder | Clean | Calibrate | Full PM | Overhaul |
| Reflow Oven | Profile | Zone check | Clean | Calibration |
| Underfill | Nozzle | Weight cal | Pump service | Full service |
| Ball Mount | Vision | Flux check | Full clean | Major PM |

### 9.3 Equipment Performance Metrics

```
OEE Calculation:
Availability: 92% (Target: 95%)
Performance: 88% (Target: 90%)
Quality: 98% (Target: 99%)
OEE = 0.92 × 0.88 × 0.98 = 79.4%

Improvement Plan:
- Reduce setup time: +2% availability
- Optimize cycle time: +2% performance
- Reduce defects: +0.5% quality
```

---

## 10. Continuous Improvement

### 10.1 Six Sigma Projects

| Project | DMAIC Phase | Target | Status |
|---------|-------------|--------|--------|
| Reduce ball defects | Analyze | 50% reduction | In progress |
| Improve coplanarity | Improve | Cpk >2.0 | Planning |
| Optimize cycle time | Define | -10% | Initiated |
| Reduce material cost | Measure | -15% | Ongoing |

### 10.2 Technology Roadmap

```
Next Generation Package:
- 2.5D/3D Integration
- Finer pitch: 0.4mm
- Larger size: 55mm
- Higher I/O: >5000
- Embedded components

Challenges:
- Warpage control <100µm
- Ultra-fine pitch assembly
- Thermal management
- Reliability assurance
```

### 10.3 Cost Reduction Initiatives

```
Cost Breakdown (Current):
Material: 65%
Labor: 15%
Equipment: 10%
Overhead: 10%

Reduction Targets:
- Material: Supplier negotiation (-10%)
- Labor: Automation (+20% productivity)
- Yield: Improvement (+2%)
- Cycle time: Optimization (-15%)
Total CoO Reduction: -20%
```

---

## Appendix A: Defect Classification

### Visual Defect Criteria
| Defect | Critical | Major | Minor |
|--------|----------|-------|-------|
| Missing ball | Any | - | - |
| Ball offset | >0.2mm | 0.1-0.2mm | <0.1mm |
| Contamination | Functional area | Cosmetic | Marking |
| Crack | Any | - | - |
| Marking | Wrong/Missing | Unclear | Cosmetic |

---

## Appendix B: Test Methods

### Ball Shear Test Procedure
1. Sample preparation at room temperature
2. Shear speed: 100-500µm/s
3. Shear height: 50-100µm from substrate
4. Record peak force
5. Inspect failure mode
6. Pass criteria: >500g, ductile failure

---

**Document Approval:**
- Package Engineering: ___________
- Quality Assurance: ___________
- Manufacturing: ___________
- Customer: ___________

**Next Review Date:** 2025-02-15
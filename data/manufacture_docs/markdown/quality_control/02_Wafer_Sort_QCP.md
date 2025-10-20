# Wafer Sort 공정 품질 관리 계획서
## Quality Control Plan for 7nm FinFET Wafer Probing

**문서번호:** QCP-WS-7NM-002  
**개정일:** 2024.11.15  
**적용제품:** 7nm FinFET Logic Device  
**공정단계:** Wafer Sort (CP Test)  

---

## 1. 문서 정보 및 적용 범위

### 1.1 목적
본 문서는 7nm FinFET 공정으로 제조된 웨이퍼의 Probe Test 단계에서 품질 관리 기준과 절차를 정의하여 수율 향상 및 품질 보증을 목표로 합니다.

### 1.2 적용 범위
- **제품군:** High-Performance Computing Processor
- **웨이퍼 크기:** 300mm
- **Die Size:** 100mm²
- **Test Coverage:** Continuity, DC, AC, Functional, IDDQ
- **목표 수율:** Prime die > 85%
- **AQL:** 0.040%

### 1.3 책임과 권한
| 담당 | 책임사항 | 권한 |
|------|---------|------|
| Test Engineer | Probe program 개발/디버깅 | Program 수정 |
| Yield Engineer | 수율 분석 및 개선 | Process feedback |
| Quality Engineer | 품질 기준 관리 | Wafer disposition |
| PE Engineer | 공정 통합 관리 | Spec 조정 |

---

## 2. 검사 항목 및 Specification

### 2.1 Electrical Test Parameters

#### DC Parametric Test
| Parameter | Condition | Min | Typ | Max | Unit | Guardband |
|-----------|-----------|-----|-----|-----|------|-----------|
| VDD_CORE | Static, 25°C | 0.72 | 0.75 | 0.78 | V | 3% |
| IDD_Standby | VDD=0.75V | - | 10 | 50 | µA | 10% |
| IDD_Operating | 3GHz | - | 15 | 20 | W | 5% |
| IOL/IOH | 4mA load | 0.1 | - | 0.4 | V | - |
| Input Leakage | All pins | -1 | - | 1 | µA | 20% |
| Junction Leakage | 25°C | - | 0.1 | 1 | nA | 50% |

#### AC Timing Test
| Parameter | Condition | Min | Typ | Max | Unit |
|-----------|-----------|-----|-----|-----|------|
| Core Clock | Nominal V | 2.8 | 3.0 | 3.2 | GHz |
| Cache Access | L1/L2 | - | 1 | 2 | ns |
| Memory BW | DDR5 | 50 | - | - | GB/s |
| Setup Time | All inputs | 50 | - | - | ps |
| Hold Time | All inputs | 30 | - | - | ps |

### 2.2 Functional Test Coverage

| Test Block | Coverage | Test Time | Priority |
|------------|----------|-----------|----------|
| CPU Core | 99.5% | 500ms | Critical |
| Cache Memory | 100% | 300ms | Critical |
| I/O Interface | 95% | 200ms | High |
| Power Management | 98% | 150ms | High |
| Debug Interface | 90% | 100ms | Medium |
| Redundancy | 100% | 50ms | Critical |

### 2.3 Defect Classification Bins

| Bin | Category | Description | Action |
|-----|----------|-------------|---------|
| 1 | Good Die | All tests pass | Ship |
| 2-5 | Speed Bin | Frequency sorting | Downgrade |
| 10-19 | Continuity | Open/Short | Scrap |
| 20-29 | DC Fail | Voltage/Current | Scrap |
| 30-39 | AC Fail | Timing failure | Analysis |
| 40-49 | Functional | Logic failure | Scrap |
| 50-59 | IDDQ | Excess leakage | Scrap |
| 60-69 | Repair | Repairable | Repair |
| 90-99 | Retest | Marginal | Retest |

---

## 3. Probe Card Management

### 3.1 Probe Card Specification
| Parameter | Specification | Tolerance |
|-----------|---------------|-----------|
| Tip Material | BeCu with Rh coating | - |
| Contact Resistance | < 1Ω | ± 0.1Ω |
| Planarity | < 5µm | - |
| Overdrive | 75µm | ± 5µm |
| Leakage Current | < 100pA | @ 5V |
| Temperature Range | -40 to 125°C | - |

### 3.2 Maintenance Schedule
| Activity | Frequency | Specification |
|----------|-----------|---------------|
| Cleaning | Every 10K TD | IPA + DI water |
| Tip Inspection | Every 25K TD | SEM check |
| Planarity Check | Every 50K TD | < 5µm |
| CRES Measurement | Daily | < 2Ω |
| Full PM | 500K TD | Complete rebuild |

### 3.3 Probe Card Tracking
```
Card ID: PC-7NM-CPU-001
Total Touchdowns: 125,432
Last PM: 2024-11-01
Next PM Due: 375K TD
Current CRES: 0.85Ω
Status: Production
```

---

## 4. Sampling Plan and Statistical Control

### 4.1 Wafer Sampling Strategy
| Lot Size | Sample Size | Test Coverage | Notes |
|----------|-------------|---------------|-------|
| 1-5 wafers | 100% | Full test | Development |
| 6-12 wafers | 100% | Full test | Qualification |
| 13-25 wafers | 5 wafers | Full test | Production |
| > 25 wafers | 20% min 5 | Full test | HVM |

### 4.2 Die Sampling Pattern
```
Wafer Map Sampling:
[F][S][F][S][F]  F = Full Test
[S][F][S][F][S]  S = Sample Test
[F][S][F][S][F]  
[S][F][S][F][S]
[F][S][F][S][F]

Sample Test = 20% of die
Full Test = Critical parameters only
```

### 4.3 Statistical Process Control

#### Control Charts
| Parameter | Chart Type | UCL/LCL | Update |
|-----------|------------|---------|---------|
| Yield | P-chart | ± 3σ | Per lot |
| IDD | X-bar R | ± 3σ | Per wafer |
| Frequency | X-bar R | ± 3σ | Per wafer |
| Bin Distribution | Pareto | - | Daily |

#### Process Capability Requirements
| Metric | Target Cpk | Minimum | Action Level |
|--------|------------|---------|--------------|
| Yield | > 1.67 | 1.33 | < 1.00 |
| Speed Bin | > 1.50 | 1.33 | < 1.00 |
| Power | > 1.33 | 1.00 | < 0.67 |
| Leakage | > 1.33 | 1.00 | < 0.67 |

---

## 5. Yield Management

### 5.1 Yield Metrics and Targets
| Metric | Target | Min Acceptable | Action |
|--------|--------|----------------|---------|
| Probe Yield | 87% | 83% | Hold @ <80% |
| Prime Bin | 75% | 70% | Review @ <70% |
| Functional Yield | 95% | 92% | Analysis @ <90% |
| Parametric Yield | 98% | 96% | Check @ <95% |

### 5.2 Yield Loss Analysis

#### Systematic Yield Detractors
| Category | Typical Loss | Root Cause | Improvement |
|----------|-------------|------------|-------------|
| Edge Die | 3% | Process variation | Edge optimization |
| Defect Clusters | 2% | Particles | Clean improvement |
| Parametric | 1.5% | Process shift | APC enhancement |
| Random Defects | 1% | Various | Defect reduction |
| Test Escapes | 0.5% | Coverage | Program enhancement |

### 5.3 Wafer Map Analysis

#### Spatial Signature Recognition
- **Edge Effects:** Radial uniformity < 2%
- **Cluster Analysis:** Defect clustering index
- **Systematic Patterns:** Stepper shot analysis
- **Random Distribution:** Poisson model fit

#### Yield Prediction Model
```python
Predicted_Yield = Base_Yield × 
                  (1 - Defect_Density × Die_Area) × 
                  Process_Factor × 
                  Test_Coverage_Factor
```

---

## 6. Test Program Management

### 6.1 Program Version Control
| Version | Release Date | Changes | Status |
|---------|-------------|---------|--------|
| V1.0 | 2024-01-15 | Initial release | Obsolete |
| V1.1 | 2024-03-20 | Added SCAN | Obsolete |
| V1.2 | 2024-06-10 | Power optimization | Obsolete |
| V2.0 | 2024-09-01 | Full coverage | Production |
| V2.1 | 2024-11-15 | Bug fixes | Qualification |

### 6.2 Test Time Optimization
| Test Block | Original | Optimized | Method |
|------------|----------|-----------|--------|
| SCAN | 800ms | 500ms | Parallel |
| BIST | 400ms | 300ms | Concurrent |
| Functional | 600ms | 400ms | Smart skip |
| Parametric | 300ms | 200ms | Multi-site |
| Total | 2100ms | 1400ms | 33% reduction |

### 6.3 Multi-Site Testing
```
Configuration: Quad-site parallel
Sites: 4 die simultaneously
Efficiency: 85% (3.4X throughput)
Resource Sharing: Power supplies, PMU
Independent: Digital channels
```

---

## 7. Defect Dispositioning

### 7.1 Ink/Bin Map Rules
| Condition | Ink Color | Disposition |
|-----------|-----------|-------------|
| Pass all tests | No ink | Ship |
| Speed downgrade | Blue | Downgrade |
| Repairable | Yellow | Laser repair |
| Hard fail | Red | Scrap |
| Retest candidate | Green | Retest queue |

### 7.2 Repair Decision Matrix
| Defect Type | Repair Method | Success Rate | Decision |
|-------------|---------------|--------------|----------|
| Single bit fail | Redundancy | 95% | Auto repair |
| Column fail | Column repair | 85% | Repair if <2 |
| Row fail | Row repair | 85% | Repair if <2 |
| Block fail | - | 0% | Scrap |

### 7.3 Retest Criteria
- Contact resistance > 0.8Ω
- Marginal timing (within 5%)
- Single parameter fail
- Environmental factors
- Maximum retest: 2 times

---

## 8. Data Management and Traceability

### 8.1 Data Collection Architecture
```
Wafer Prober → Test System → Data Server
                    ↓            ↓
              Local Storage   MES Database
                    ↓            ↓
              Backup Server  Yield System
```

### 8.2 Data Retention Policy
| Data Type | Retention | Format | Location |
|-----------|-----------|---------|----------|
| Raw test data | 2 years | Binary | Server |
| Summary data | 5 years | Database | MES |
| Wafer maps | 5 years | Image | Archive |
| Program files | Permanent | Versioned | Repository |
| Correlation data | 3 years | CSV | Database |

### 8.3 Lot Genealogy
- Wafer lot number
- Fab lot history
- Process parameters
- Equipment history
- Test conditions
- Environmental data
- Operator information

---

## 9. Continuous Improvement

### 9.1 Weekly Yield Review
**Agenda Items:**
1. Yield trend analysis
2. Top bin Pareto
3. New failure modes
4. Spatial signatures
5. Equipment performance
6. Action item tracking

### 9.2 Test Coverage Enhancement
| Initiative | Current | Target | Timeline |
|------------|---------|--------|----------|
| Stuck-at fault | 99.2% | 99.5% | Q1 2025 |
| Transition fault | 94% | 96% | Q2 2025 |
| Path delay | 89% | 92% | Q2 2025 |
| Bridge coverage | 91% | 94% | Q3 2025 |

### 9.3 Cost Reduction Projects
| Project | Saving | Implementation |
|---------|--------|----------------|
| Test time reduction | $0.15/die | Parallel test |
| Multi-site increase | $0.10/die | Octal upgrade |
| Probe card life | $0.05/die | Better maintenance |
| Retest reduction | $0.03/die | Program optimization |

---

## 10. Quality Metrics Dashboard

### 10.1 Real-time KPIs
| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| Wafer Probe Yield | 86.5% | 87% | ↑ |
| Test Time | 1.42s | 1.40s | ↓ |
| First Pass Yield | 94.2% | 95% | ↔ |
| DPPM (predicted) | 45 | <50 | ↓ |
| Probe Card MTBF | 485K TD | 500K | ↑ |

### 10.2 Monthly Quality Report
```
Period: November 2024
Total Wafers Tested: 12,456
Total Die Tested: 4,234,521
Overall Yield: 86.3%
Prime Bin Yield: 74.8%
Test Escapes: 2 (under investigation)
Customer Returns: 0
Quality Index: 98.5
```

---

## Appendix A: Test Limit Calculations

### Guardband Formula
```
Test_Limit = Spec_Limit × (1 ± GB%)

Where GB% = √(Tester_Accuracy² + 
              Temperature_Variation² + 
              Voltage_Variation² + 
              Measurement_Noise²)
```

---

## Appendix B: Troubleshooting Guide

| Issue | Check Points | Solution |
|-------|-------------|----------|
| Low yield | Probe card, Test program | Clean/Replace, Debug |
| High retest | Contact, Temperature | Adjust overdrive |
| Spatial pattern | Process, Equipment | Feedback to fab |
| Bin shift | Calibration, Reference | Recalibrate |

---

**문서 승인:**
- 작성: 김태준 Test Engineer
- 검토: 이서연 Quality Manager
- 승인: 박정훈 Director

**개정 이력:**
| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2024.11.15 | Initial release |
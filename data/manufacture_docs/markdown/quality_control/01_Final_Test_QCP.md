# Final Test 공정 품질 관리 계획서
## Quality Control Plan for 28nm Mobile AP Package IC

**문서번호:** QCP-FT-PKG-001  
**개정일:** 2024.11.15  
**적용제품:** 28nm Mobile Application Processor  
**패키지:** FBGA 12x12mm, 896 balls  

---

## 1. 문서 정보 및 적용 범위

### 1.1 문서 목적
본 문서는 28nm 공정 모바일 AP 제품의 Final Test 단계에서의 품질 관리 기준, 검사 방법, 및 품질 보증 활동을 정의합니다.

### 1.2 적용 범위
- **제품:** Mobile AP (Model: MAP-2024-A1)
- **공정 단계:** Final Test (Package Test)
- **Test Coverage:** DC, AC, Functional, IDDQ, Burn-in
- **품질 목표:** AQL 0.065%, Yield > 98%

### 1.3 참조 문서
- JEDEC JESD47: Stress Test Qualification
- JEDEC JESD22: Reliability Test Methods
- AEC-Q100: Automotive Reliability Standard
- MIL-STD-1916: Sampling Procedures

### 1.4 책임과 권한
| 역할 | 책임 | 권한 |
|------|------|------|
| Test Engineer | Test program 개발/유지 | Program 수정 |
| Quality Engineer | 품질 기준 수립/관리 | Lot disposition |
| Production | Test 실행 | Hold 요청 |
| Customer Quality | Audit 및 승인 | Spec 변경 승인 |

---

## 2. 검사 항목 및 Specification

### 2.1 DC Parametric Test

| Parameter | Test Condition | Min | Typ | Max | Unit | Guardband |
|-----------|---------------|-----|-----|-----|------|-----------|
| VDD_CORE Operating | 25°C, Static | 0.95 | 1.00 | 1.05 | V | 5% |
| VDD_IO Operating | 25°C, Static | 1.71 | 1.80 | 1.89 | V | 5% |
| IDD_Sleep | VDD=1.0V, 25°C | - | 50 | 100 | µA | 10% |
| IDD_Active | f=1.8GHz, 25°C | - | 850 | 950 | mA | 3% |
| Input Leakage | VIN=0/VDD | -10 | - | 10 | µA | 20% |
| Output Drive High | IOH=8mA | 2.4 | - | - | V | - |
| Output Drive Low | IOL=8mA | - | - | 0.4 | V | - |

### 2.2 AC Timing Test

| Parameter | Test Condition | Min | Typ | Max | Unit | Guardband |
|-----------|---------------|-----|-----|-----|------|-----------|
| Core Frequency | Nominal voltage | 1.6 | 1.8 | 2.0 | GHz | 2% |
| Memory Interface | DDR4-3200 | - | 1.6 | - | GHz | 5% |
| Setup Time (tSU) | All inputs | 0.5 | - | - | ns | 10% |
| Hold Time (tH) | All inputs | 0.3 | - | - | ns | 10% |
| Propagation Delay | CL=50pF | - | 2.5 | 3.5 | ns | 10% |
| Rise Time | 10-90% | - | 0.8 | 1.2 | ns | 15% |
| Fall Time | 90-10% | - | 0.8 | 1.2 | ns | 15% |

### 2.3 Functional Test

| Test Category | Coverage | Pass Criteria | Test Time |
|--------------|----------|---------------|-----------|
| SCAN Test | 99.5% | All chains pass | 50ms |
| BIST Memory | 100% | No failures | 100ms |
| BIST Logic | 95% | All blocks pass | 80ms |
| At-Speed Test | Critical paths | Timing met | 150ms |
| Power Management | All modes | Transitions OK | 200ms |
| Interface Test | All I/Os | Protocol compliance | 300ms |

### 2.4 IDDQ Test

| Test Point | Current Limit | Temperature | Note |
|------------|--------------|-------------|------|
| All gates low | < 100µA | 25°C | Static |
| All gates high | < 100µA | 25°C | Static |
| Checkerboard | < 150µA | 25°C | Pattern |
| Random vectors | < 200µA | 25°C | 10 vectors |

---

## 3. Sampling Plan

### 3.1 Lot Acceptance Sampling (MIL-STD-1916)

| Lot Size | Sample Size | Accept | Reject | Inspection Level |
|----------|-------------|--------|--------|------------------|
| 1-90 | 13 | 0 | 1 | Level II |
| 91-150 | 20 | 0 | 1 | Level II |
| 151-280 | 32 | 1 | 2 | Level II |
| 281-500 | 50 | 1 | 2 | Level II |
| 501-1200 | 80 | 2 | 3 | Level II |
| > 1200 | 125 | 3 | 4 | Level II |

### 3.2 Skip Lot Criteria
**Qualification for Skip Lot:**
- 10 consecutive lots pass without rejection
- Process stable (Cpk > 1.67)
- No customer complaints
- Reduced sampling: 20% of normal

**Disqualification:**
- Any lot rejection
- Customer complaint
- Process change
- Return to normal sampling

### 3.3 Tightened Inspection
**Triggers:**
- 2 out of 5 consecutive lots rejected
- Customer complaint
- Critical defect found

**Requirements:**
- Double sample size
- 100% inspection for critical parameters
- Root cause analysis required
- 5 consecutive lots pass to return to normal

### 3.4 Customer Specific Requirements

| Customer | Requirement | Implementation |
|----------|-------------|----------------|
| Customer A | Zero defect for key params | 100% test |
| Customer B | Burn-in 100% | 48hr HTOL |
| Customer C | Statistical bin limits | Bin yield monitoring |
| Customer D | Cpk > 2.0 | Enhanced guardband |

---

## 4. Test Equipment 및 Calibration

### 4.1 ATE (Automatic Test Equipment)

#### Equipment Specification
- **Model:** Advantest V93000 PS1600
- **Channels:** 1024 digital, 256 analog
- **Frequency:** Up to 1.6 Gbps
- **Timing Accuracy:** ± 20ps
- **Voltage Accuracy:** ± 5mV
- **Current Measure:** 1nA to 2A

#### Test Program Control
- **Version Control:** Git repository
- **Change Management:** ECN required
- **Validation:** 30 device correlation
- **Release Approval:** Test & Quality sign-off

### 4.2 Test Hardware

#### Probe Card/Load Board
- **Vendor:** FormFactor/Xcerra
- **Maintenance:** 500k touchdowns
- **Cleaning:** Every 10k tests
- **Verification:** Daily continuity check

#### Socket Specification
- **Contact Resistance:** < 20mΩ
- **Lifetime:** 100k insertions
- **Temperature Range:** -40 to 125°C
- **Cleaning Cycle:** Every 5k insertions

### 4.3 Calibration Requirements

| Equipment | Parameter | Frequency | Specification | Standard |
|-----------|-----------|-----------|---------------|----------|
| ATE | Voltage | Monthly | ± 0.1% | NIST |
| ATE | Timing | Quarterly | ± 20ps | NIST |
| ATE | Current | Monthly | ± 0.5% | NIST |
| Handler | Temperature | Weekly | ± 2°C | NIST |
| Socket | Contact R | Daily | < 50mΩ | Internal |

### 4.4 Correlation Standards

#### Gage R&R Requirements
- **Repeatability:** < 5% of tolerance
- **Reproducibility:** < 5% of tolerance
- **Total GRR:** < 10% acceptable, < 30% marginal
- **Number of Parts:** 10 minimum
- **Number of Operators:** 3 minimum
- **Number of Trials:** 3 per operator

---

## 5. Data Collection 및 분석

### 5.1 Parameter Data Collection

#### Critical Parameters (100% monitoring)
| Parameter | Data Points | SPC Chart | Limit |
|-----------|-------------|-----------|-------|
| IDD_Active | Every device | X-bar R | ± 3σ |
| Core Frequency | Every device | X-bar R | ± 3σ |
| Standby Current | Every device | I-MR | UCL only |
| Key Timing | Every device | X-bar R | ± 3σ |

#### Non-Critical Parameters
- Sampling: 5 devices per lot
- Chart Type: X-bar R
- Review: Weekly
- Action: Investigation if OOC

### 5.2 Real-time SPC Monitoring

#### Control Chart Configuration
```
Control Limits Calculation:
- UCL = μ + 3σ
- LCL = μ - 3σ
- Warning Limits = μ ± 2σ

Update Frequency:
- Every lot completion
- Recalculation monthly
- Baseline: 20 lots minimum
```

#### Western Electric Rules
1. 1 point outside 3σ limits
2. 2 of 3 points outside 2σ
3. 4 of 5 points outside 1σ
4. 8 points on one side of center
5. 6 points trending up/down
6. 14 points alternating

### 5.3 Process Capability

#### Cpk Targets by Category
| Parameter Type | Cpk Target | Min Acceptable |
|---------------|------------|----------------|
| Key Electrical | > 1.67 | 1.33 |
| Timing Critical | > 1.67 | 1.33 |
| Power | > 1.50 | 1.00 |
| Non-critical | > 1.33 | 1.00 |

#### Capability Calculation
```
Cp = (USL - LSL) / 6σ
Cpk = min[(USL - μ)/3σ, (μ - LSL)/3σ]

Where:
- USL: Upper Specification Limit
- LSL: Lower Specification Limit
- μ: Process Mean
- σ: Process Standard Deviation
```

### 5.4 Out of Control (OOC) Action Plan

| Level | Trigger | Action | Responsibility |
|-------|---------|--------|----------------|
| Warning | 2σ violation | Monitor closely | Operator |
| Alert | Western Electric Rule | Investigate | Engineer |
| Hold | 3σ violation | Stop production | Engineer |
| Reject | Spec violation | Quarantine lot | Quality |

---

## 6. Yield 관리

### 6.1 Yield Targets and Monitoring

#### Baseline Yield Targets
| Test Category | Target | Min Acceptable | Action Level |
|--------------|--------|----------------|--------------|
| Overall Yield | 98.5% | 97.0% | < 96% |
| Bin 1 (Prime) | 95.0% | 93.0% | < 90% |
| Functional | 99.5% | 99.0% | < 98% |
| Parametric | 99.0% | 98.0% | < 97% |

### 6.2 Yield Loss Categories

#### Systematic Classification
| Category | Description | Typical % | Action |
|----------|-------------|-----------|--------|
| Functional Fail | Logic/memory failure | 0.5% | Design review |
| Parametric Fail | Speed/power out of spec | 0.8% | Process tune |
| IDDQ Fail | Excessive leakage | 0.2% | Defect analysis |
| ESD Fail | ESD damage | 0.1% | Handling review |
| Visual Defect | Physical damage | 0.1% | Inspection |
| Test Issue | False fail | 0.3% | Program debug |

### 6.3 Pareto Analysis

#### Analysis Schedule
- **Daily:** Top 5 failure bins
- **Weekly:** Detailed bin analysis
- **Monthly:** Trend analysis
- **Quarterly:** Comprehensive review

#### Pareto Chart Requirements
- 80/20 rule application
- Root cause for top 80%
- Action plan for improvement
- Effectiveness tracking

### 6.4 8D Report Process

#### Report Triggers
- Yield drop > 2% from baseline
- Customer complaint
- Systematic failure pattern
- New defect mechanism

#### 8D Report Timeline
| Step | Description | Timeline |
|------|-------------|----------|
| D1 | Team formation | 24 hours |
| D2 | Problem description | 48 hours |
| D3 | Containment action | 72 hours |
| D4 | Root cause analysis | 1 week |
| D5 | Corrective action | 2 weeks |
| D6 | Implementation | 3 weeks |
| D7 | Prevention | 4 weeks |
| D8 | Closure | 6 weeks |

---

## 7. Defect Classification

### 7.1 Bin Definition

#### Standard Bin Map (Bin 1-99)
| Bin Range | Category | Description |
|-----------|----------|-------------|
| 1 | Pass | All tests pass |
| 2-9 | Downgrade | Reduced spec pass |
| 10-19 | Continuity | Open/short |
| 20-29 | DC Fail | Voltage/current |
| 30-39 | AC Fail | Timing/frequency |
| 40-49 | Functional | Logic failure |
| 50-59 | Memory | BIST fail |
| 60-69 | IDDQ | Leakage fail |
| 70-79 | Interface | I/O failure |
| 80-89 | System | Retest candidates |
| 90-99 | Mechanical | Handler issues |

### 7.2 Major/Minor Defect Classification

#### Critical Defects (Customer Risk)
- Non-functional device
- Reliability risk
- Safety concern
- Specification violation

#### Major Defects (Quality Risk)
- Performance degradation
- Marginal pass
- Cosmetic major
- Documentation error

#### Minor Defects (Low Risk)
- Cosmetic minor
- Marking orientation
- Non-critical parameter
- Administrative error

### 7.3 Failure Analysis Process

#### FA Trigger Conditions
| Condition | Sample Size | Analysis Type |
|-----------|-------------|---------------|
| New failure mode | 5 units | Full analysis |
| Yield excursion | 10 units | Focused analysis |
| Customer return | All units | Comprehensive |
| Reliability fail | All units | Destructive |

#### FA Flow
1. **Non-Destructive**
   - External visual
   - X-ray inspection
   - SAM analysis
   - Electrical verification

2. **Destructive**
   - Decapsulation
   - SEM inspection
   - FIB cross-section
   - Material analysis

### 7.4 Customer Return Analysis

#### Return Rate Monitoring
- **Target:** < 100 DPPM
- **Measurement:** Monthly
- **Breakdown:** By failure mode
- **Action:** 8D for any return

#### RMA Process
1. Receipt and documentation
2. Failure verification
3. Root cause analysis
4. Corrective action
5. Customer report
6. Preventive action

---

## 8. Hold 및 Disposition 기준

### 8.1 Automatic Hold Criteria

| Condition | Hold Type | Release Authority |
|-----------|-----------|-------------------|
| Yield < Lower Limit | Immediate | Quality Manager |
| Cpk < 1.0 | Immediate | Quality Manager |
| 3 consecutive fails | Immediate | Test Engineer |
| New bin appearance | Review | Test Engineer |
| SPC violation | Review | Quality Engineer |
| Customer alert | Immediate | Customer Quality |

### 8.2 Engineering Review Process

#### Review Committee
- Test Engineering
- Quality Engineering
- Product Engineering
- Customer Quality (if required)

#### Review Checklist
- [ ] Test data analysis complete
- [ ] Retest performed if applicable
- [ ] Root cause identified
- [ ] Risk assessment completed
- [ ] Customer notification if required
- [ ] Corrective action defined

### 8.3 Disposition Decision Tree

```
Lot on Hold
    ├── Spec Violation?
    │   ├── Yes → Scrap/Downgrade
    │   └── No → Continue
    ├── Yield Issue?
    │   ├── Yes → Root Cause Analysis
    │   │   ├── Test Issue → Retest
    │   │   └── Real Issue → Evaluate Risk
    │   └── No → Continue
    └── Quality Risk?
        ├── High → Scrap
        ├── Medium → Sample Increase
        └── Low → Release with Monitoring
```

### 8.4 Special Release Conditions

| Condition | Requirement | Approval |
|-----------|-------------|----------|
| Marginal pass | 100% guardband test | Quality + Customer |
| Engineering sample | Full characterization | Product Engineering |
| Waiver request | Risk assessment | Customer |
| Retest pass | Root cause documented | Quality |

---

## 9. Traceability

### 9.1 Lot Genealogy System

#### Data Structure
```
Lot ID: YYWWDLLLL
├── Year/Week (YYWW)
├── Day (D)
├── Sequence (LLLL)
└── Full Traceability
    ├── Wafer lot
    ├── Assembly lot
    ├── Test program version
    ├── Equipment ID
    ├── Operator ID
    └── Time stamps
```

### 9.2 Test Data Retention

| Data Type | Retention Period | Storage Medium |
|-----------|-----------------|----------------|
| Parametric data | 10 years | Database |
| Datalog files | 5 years | Archive server |
| Test programs | Permanent | Version control |
| Calibration records | 3 years | Database |
| FA reports | Permanent | Document system |

### 9.3 Equipment History

#### Tracking Requirements
- Tester ID and configuration
- Handler/prober ID
- Socket/probe card ID
- Test program version
- Calibration status
- Maintenance history

### 9.4 Material Trace Code

#### Code Structure
- Raw material lot
- Date code
- Vendor code
- Process lot
- Location code

---

## 10. 개선 활동

### 10.1 Weekly Quality Review

#### Review Agenda
1. **Yield Summary**
   - Weekly yield trend
   - Pareto analysis
   - Action items status

2. **SPC Review**
   - OOC events
   - Capability indices
   - Trending parameters

3. **Customer Feedback**
   - Returns/complaints
   - Audit findings
   - Corrective actions

4. **Improvement Projects**
   - Test time reduction
   - Yield improvement
   - Cost reduction

### 10.2 Test Time Reduction

#### Optimization Targets
| Activity | Current | Target | Method |
|----------|---------|--------|--------|
| Index time | 1.5s | 1.0s | Handler optimization |
| Test time | 3.5s | 2.8s | Parallel test |
| Data log | 0.5s | 0.2s | Buffer optimization |
| Total | 5.5s | 4.0s | 27% reduction |

### 10.3 False Fail Analysis

#### Monitoring Metrics
- **Retest Recovery:** < 2%
- **Site-to-site:** < 0.5% delta
- **Shift-to-shift:** < 1% delta
- **Tester-to-tester:** < 1% delta

#### Reduction Strategy
1. Contact resistance monitoring
2. Temperature stability
3. Program optimization
4. Guardband review

### 10.4 Test Coverage Optimization

#### Coverage Analysis
- **Stuck-at Coverage:** > 99%
- **Transition Coverage:** > 95%
- **Path Delay:** > 90%
- **IDDQ Effectiveness:** Review quarterly

#### Enhancement Methods
- ATPG pattern improvement
- At-speed test expansion
- Adaptive test implementation
- Machine learning application

---

## 11. Quality Metrics Dashboard

### 11.1 Key Performance Indicators

| KPI | Target | Actual | Trend |
|-----|--------|--------|-------|
| Final Test Yield | > 98.5% | 98.7% | ↑ |
| DPPM | < 100 | 85 | ↔ |
| Test Escapes | 0 | 0 | ✓ |
| Cpk Average | > 1.67 | 1.75 | ↑ |
| OOC Events | < 5/week | 3 | ↓ |
| Test Time | < 4.0s | 4.2s | ↔ |

### 11.2 Quality Cost Tracking

| Category | Budget | Actual | Variance |
|----------|--------|--------|----------|
| Test Cost | $2.50/unit | $2.45 | -2% |
| Failure Cost | $0.50/unit | $0.48 | -4% |
| Prevention | $0.30/unit | $0.32 | +7% |
| Total CoQ | $3.30/unit | $3.25 | -1.5% |

---

## Appendix A: Test Limit Calculation

### Guardband Methodology
```
Test Limit = Spec Limit × (1 ± Guardband%)

Guardband factors:
- Tester accuracy
- Temperature variation
- Aging degradation
- Customer requirement
```

---

## Appendix B: Statistical Tables

### Sample Size Determination
- Confidence Level: 95%
- Confidence Interval: ± 3%
- Population: Lot size
- Formula: Modified for finite population

---

**문서 승인:**

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| 작성 | 김철수 Test Engineer | | |
| 검토 | 박영희 Quality Manager | | |
| 승인 | 이민호 Director | | |
| 고객 승인 | Customer Representative | | |

**개정 이력:**

| Rev | 날짜 | 변경 내용 | 작성자 |
|-----|------|-----------|--------|
| 1.0 | 2024.11.15 | 초기 배포 | 김철수 |
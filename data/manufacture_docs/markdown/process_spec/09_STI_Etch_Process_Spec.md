# STI (Shallow Trench Isolation) Etch 공정 사양서
## Advanced Device Isolation for Sub-5nm Technology

**문서번호:** PS-ETCH-STI-009-K  
**개정번호:** Rev. 2.7  
**작성일:** 2024년 11월 15일  
**보안등급:** Confidential  

---

## 1. 문서 헤더

### 승인 정보
| 역할 | 담당자 | 소속 | 서명 | 날짜 |
|------|--------|------|------|------|
| 작성 | 한상욱 수석 | Etch 공정팀 | | |
| 검토 | 조민지 책임 | 공정통합팀 | | |
| 승인 | 김진호 팀장 | 공정기술팀 | | |
| 승인 | 이유진 팀장 | 품질팀 | | |
| 승인 | 박상현 팀장 | 생산팀 | | |

---

## 2. 공정 개요

### 2.1 공정 목적
Active device 영역 간 전기적 isolation을 위한 shallow trench 형성

### 2.2 주요 사양
- **Trench Depth:** 3000 ± 50Å
- **CD (Critical Dimension):** 45 ± 2nm
- **Sidewall Angle:** 88 ± 1°
- **Aspect Ratio:** 6:1
- **Corner Rounding:** < 5nm radius
- **Uniformity:** < 2% (3σ, 49pt)
- **처리량:** 45 WPH

---

## 3. Process Integration Flow

```
STI Module Sequence:
1. Pad Oxide (100Å)
2. Si3N4 Deposition (1500Å)
3. Photolithography
4. Hardmask Open
5. Trench Etch (This Process)
6. Liner Oxidation
7. HDP Fill
8. CMP Planarization
```

---

## 4. 상세 Etch Recipe

### 4.1 Hardmask Open (Step 1)

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| Source Power | 800 | ± 20 | W |
| Bias Power | 150 | ± 10 | W |
| CHF3 Flow | 50 | ± 2 | sccm |
| O2 Flow | 10 | ± 1 | sccm |
| Pressure | 10 | ± 1 | mTorr |
| Time | Endpoint + 20% | - | sec |
| Temperature | 20 | ± 2 | °C |

### 4.2 Main Etch (Step 2)

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| Source Power | 1200 | ± 30 | W |
| Bias Power | 100 | ± 5 | W |
| Cl2 Flow | 80 | ± 3 | sccm |
| HBr Flow | 120 | ± 5 | sccm |
| O2 Flow | 5 | ± 0.5 | sccm |
| Pressure | 8 | ± 0.5 | mTorr |
| ESC Temperature | 60 | ± 2 | °C |
| He Backside | 10/30 | ± 2 | Torr |

### 4.3 Over Etch (Step 3)

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| Source Power | 1000 | ± 25 | W |
| Bias Power | 80 | ± 5 | W |
| HBr Flow | 150 | ± 5 | sccm |
| O2 Flow | 8 | ± 1 | sccm |
| Time | 15 | ± 2 | sec |
| Purpose | Corner rounding | - | - |

### 4.4 Passivation (Step 4)

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| Source Power | 600 | ± 20 | W |
| Bias Power | 0 | - | W |
| SiCl4 Flow | 20 | ± 2 | sccm |
| O2 Flow | 50 | ± 2 | sccm |
| Time | 10 | ± 1 | sec |
| Wall Thickness | ~20Å | - | - |

---

## 5. Critical Dimension Control

### 5.1 CD Budget Breakdown

| Component | Contribution | Control Method |
|-----------|-------------|----------------|
| Mask CD | 45nm ± 1nm | Lithography |
| Etch Bias | -2nm ± 1nm | Recipe optimization |
| Loading Effect | ± 0.5nm | Compensation table |
| Uniformity | ± 1nm | Chamber matching |

### 5.2 Profile Control Parameters

| Feature | Specification | Impact | Control |
|---------|--------------|---------|---------|
| Top CD | 45 ± 2nm | Device width | Bias power |
| Bottom CD | 40 ± 3nm | Isolation | Over etch |
| Sidewall Angle | 88 ± 1° | Fill capability | Gas ratio |
| Micro-loading | < 5% | Uniformity | Pressure |

---

## 6. Endpoint Detection

### 6.1 OES Configuration

| Wavelength | Species | Purpose | Action |
|------------|---------|---------|--------|
| 288nm | Si | Main etch | Endpoint |
| 704nm | F | Hardmask | Transition |
| 309nm | OH | Oxide clear | Stop |
| 656nm | H | Polymer | Monitor |

### 6.2 Endpoint Algorithm

```
Endpoint Logic:
1. Monitor Si signal (288nm)
2. Detect 80% drop from peak
3. Add fixed over-etch time
4. Verify with reflectometry
5. Stop on time if no endpoint
```

---

## 7. Process Control & Monitoring

### 7.1 SPC Parameters

| Parameter | Target | UCL | LCL | Cpk |
|-----------|--------|-----|-----|-----|
| Depth | 3000Å | 3050Å | 2950Å | >1.67 |
| Top CD | 45nm | 47nm | 43nm | >1.67 |
| Angle | 88° | 89° | 87° | >1.33 |
| Uniformity | 1.5% | 2.5% | - | >2.0 |

### 7.2 Metrology Plan

| Measurement | Tool | Frequency | Sites |
|-------------|------|-----------|-------|
| Depth | Profilometer | 100% | 5 |
| CD | CD-SEM | 100% | 9 |
| Profile | X-SEM | Daily | 1 |
| Uniformity | Auto | 100% | 49 |

---

## 8. 이상 발생 시 대응

### 8.1 Common Issues

| Issue | Root Cause | Detection | Solution |
|-------|------------|-----------|----------|
| Shallow trench | Low etch rate | Depth measurement | Increase time |
| CD shift | Bias drift | Inline CD-SEM | Adjust bias power |
| Poor profile | Gas ratio | Cross-section | Optimize chemistry |
| Micro-loading | Local effect | Pattern dependency | Pressure adjustment |
| Roughness | Polymer | SEM inspection | Reduce polymer gases |

### 8.2 Alarm Response

| Alarm Code | Description | Severity | Action |
|------------|-------------|----------|--------|
| EPD_001 | No endpoint | High | Check OES |
| PRE_001 | Pressure unstable | Medium | Check pump |
| RF_001 | Reflected power | High | Check matching |
| TEMP_001 | ESC temperature | Medium | Check chiller |

---

## 9. Chamber Maintenance

### 9.1 PM Schedule

| Item | Frequency | Duration | Action |
|------|-----------|----------|--------|
| Wet clean | 5000 wafers | 8 hrs | Full disassembly |
| Season | After wet clean | 2 hrs | Conditioning |
| Part replacement | 10000 wafers | 12 hrs | Critical parts |
| Calibration | Monthly | 4 hrs | Sensors |

### 9.2 Chamber Matching

| Parameter | Tolerance | Method | Frequency |
|-----------|-----------|--------|-----------|
| Etch rate | ± 3% | Monitor wafer | Daily |
| CD bias | ± 1nm | Product | Per lot |
| Profile | ± 1° | Cross-section | Weekly |
| Particles | < 5 adds | Bare wafer | Daily |

---

## 10. 참조 문서

- SOP-ETCH-002: LAM Etch Operation
- SPEC-STI-001: STI Module Specification  
- DOC-PROFILE-001: Profile Metrology
- MAN-ENDPOINT-001: OES Setup Guide

---

## Appendix: Troubleshooting Matrix

```
Quick Debug Guide:
Problem: Grass/residue
→ Check: HBr/O2 ratio
→ Action: Increase HBr to 150 sccm

Problem: Undercut
→ Check: Bias power
→ Action: Reduce to 80W

Problem: Loading effect
→ Check: Pattern density
→ Action: Adjust pressure to 10 mTorr
```

---

**문서 관리:**
- 다음 검토: 2025년 2월 15일
- 관리부서: Etch 공정팀
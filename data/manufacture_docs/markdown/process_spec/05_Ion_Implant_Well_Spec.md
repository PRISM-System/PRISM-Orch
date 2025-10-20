# Deep Well Ion Implantation 공정 사양서
## 5nm FinFET N-Well/P-Well Formation

**문서번호:** PS-IMP-WELL-005-K  
**개정번호:** Rev. 1.7  
**작성일:** 2024년 11월 15일  
**보안등급:** Confidential  

---

## 1. 문서 헤더

### 승인 정보
| 역할 | 담당자 | 소속 | 서명 | 날짜 |
|------|--------|------|------|------|
| 작성 | 신동욱 수석 | Implant 공정팀 | | |
| 검토 | 류현진 책임 | 공정통합팀 | | |
| 승인 | 오승환 팀장 | 공정기술팀 | | |
| 승인 | 박미경 팀장 | 품질팀 | | |
| 승인 | 김태성 팀장 | 생산팀 | | |

---

## 2. 공정 개요

### 2.1 공정 목적
CMOS device의 N-Well 및 P-Well 영역 형성을 위한 deep ion implantation 공정

### 2.2 주요 사양
- **N-Well Depth:** 2.5 ± 0.1 µm
- **P-Well Depth:** 2.0 ± 0.1 µm
- **Peak Concentration:** 5E17 ± 5E16 atoms/cm³
- **Junction Depth Uniformity:** < 3%
- **Sheet Resistance:** As specified per design
- **처리량:** 120 WPH

---

## 3. Implant Sequence

```
Multi-Step Well Formation:
1. Deep N-Well (Phosphorus, High Energy)
2. Medium N-Well (Phosphorus, Medium Energy)  
3. Shallow N-Well (Phosphorus, Low Energy)
4. Deep P-Well (Boron, High Energy)
5. Medium P-Well (Boron, Medium Energy)
6. Shallow P-Well (Boron, Low Energy)
```

---

## 4. 상세 공정 파라미터

### 4.1 N-Well Implantation

| Step | Ion | Energy (keV) | Dose (ions/cm²) | Tilt | Rotation |
|------|-----|-------------|-----------------|------|----------|
| Deep | P | 800 | 1.5E13 | 7° | 22° |
| Medium | P | 380 | 8E12 | 7° | 22° |
| Shallow | P | 180 | 5E12 | 7° | 22° |
| Channel Stop | P | 100 | 3E12 | 0° | 0° |

### 4.2 P-Well Implantation

| Step | Ion | Energy (keV) | Dose (ions/cm²) | Tilt | Rotation |
|------|-----|-------------|-----------------|------|----------|
| Deep | B | 320 | 2E13 | 7° | 22° |
| Medium | B | 160 | 1E13 | 7° | 22° |
| Shallow | B | 80 | 8E12 | 7° | 22° |
| Threshold Adjust | B | 30 | 5E12 | 0° | 0° |

### 4.3 Screen Oxide Requirements

| Parameter | Specification | Tolerance |
|-----------|--------------|-----------|
| Thickness | 150Å | ± 10Å |
| Quality | Thermal oxide | - |
| Uniformity | < 2% | - |
| Purpose | Channeling prevention | - |

---

## 5. Critical Control Parameters

### 5.1 Process Control Limits

| Parameter | N-Well | P-Well | Measurement |
|-----------|--------|--------|-------------|
| Junction Depth | 2.5±0.1 µm | 2.0±0.1 µm | SIMS |
| Peak Concentration | 5E17 cm⁻³ | 8E17 cm⁻³ | SIMS |
| Sheet Resistance | 800±50 Ω/□ | 600±50 Ω/□ | 4-point probe |
| Dose Accuracy | ±2% | ±2% | Thermawave |
| Angle Accuracy | ±0.5° | ±0.5° | Verification |

### 5.2 Contamination Control

| Contaminant | Limit | Detection Method |
|-------------|-------|------------------|
| Metals (Fe, Cu) | <1E10 atoms/cm² | TXRF |
| Carbon | <5E16 atoms/cm³ | SIMS |
| Oxygen | <1E17 atoms/cm³ | SIMS |
| Particles | <5 adds @ 0.12µm | Inspection |

---

## 6. 이상 발생 시 대응

### 6.1 Dose Deviation

| Issue | Cause | Action |
|-------|-------|--------|
| Low dose | Beam current drift | Recalibrate |
| High dose | Integration error | Check controller |
| Non-uniformity | Scanning issue | Adjust scan |

### 6.2 Depth Control

| Issue | Cause | Solution |
|-------|-------|----------|
| Shallow junction | Low energy | Verify energy |
| Deep junction | Channeling | Check tilt angle |
| Profile spread | Thermal budget | Reduce anneal |

---

## 7. Thermal Budget

### 7.1 Well Drive-in Anneal

| Parameter | Specification | Purpose |
|-----------|--------------|---------|
| Temperature | 1050°C | Dopant activation |
| Time | 30 seconds | Drive-in control |
| Ambient | N₂ | Oxidation prevention |
| Ramp Rate | 50°C/s | Stress management |

---

## 8. 참조 문서

- SOP-IMP-002: Well Implant Procedure
- SPEC-DEVICE-001: Device Specifications
- DOC-THERMAL-001: RTP Process Guide

---

## Appendix: SIMS Profile Target

```
Depth (µm)    N-Well Conc.    P-Well Conc.
0.0           1E16            1E16
0.5           5E17            8E17
1.0           5E17            8E17
1.5           3E17            5E17
2.0           1E17            2E17
2.5           5E16            5E16
3.0           1E16            1E16
```

---

**문서 관리:**
- 다음 검토: 2025년 2월 15일
- 관리부서: Implant 공정팀
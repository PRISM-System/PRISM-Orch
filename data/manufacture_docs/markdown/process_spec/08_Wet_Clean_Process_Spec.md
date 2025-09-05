# Wet Cleaning 공정 사양서
## Advanced RCA Clean & Surface Preparation

**문서번호:** PS-WET-CLN-008-K  
**개정번호:** Rev. 3.5  
**작성일:** 2024년 11월 15일  
**보안등급:** Confidential  

---

## 1. 문서 헤더

### 승인 정보
| 역할 | 담당자 | 소속 | 서명 | 날짜 |
|------|--------|------|------|------|
| 작성 | 윤재형 수석 | Wet 공정팀 | | |
| 검토 | 김하늘 책임 | 공정통합팀 | | |
| 승인 | 이동훈 팀장 | 공정기술팀 | | |
| 승인 | 박소영 팀장 | 품질팀 | | |
| 승인 | 정기훈 팀장 | 생산팀 | | |

---

## 2. 공정 개요

### 2.1 공정 목적
반도체 표면의 particle, metallic contamination, native oxide 및 organic residue 제거

### 2.2 주요 사양
- **Particle Removal Efficiency:** > 99% @ 45nm
- **Metal Contamination:** < 1E10 atoms/cm²
- **Surface Roughness:** < 0.2nm RMS
- **Native Oxide:** < 10Å (controlled)
- **Throughput:** 100 WPH
- **Chemical Consumption:** Optimized

---

## 3. Standard Clean Sequence

```
Modified RCA Clean Process:
1. Pre-rinse (DI Water)
2. APM (SC-1): Particle & organic removal
3. Rinse + Overflow
4. DHF: Oxide removal
5. Rinse + Overflow  
6. HPM (SC-2): Metallic contamination
7. Final rinse
8. IPA dry or Spin dry
```

---

## 4. 상세 공정 파라미터

### 4.1 APM (Ammonia Peroxide Mixture) - SC1

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| NH4OH:H2O2:H2O | 1:1:5 | ± 0.1 | ratio |
| Temperature | 70 | ± 2 | °C |
| Time | 10 | ± 0.5 | min |
| Megasonic Power | 600 | ± 50 | W |
| Frequency | 0.95 | ± 0.05 | MHz |
| Bath Volume | 150 | ± 5 | L |
| Circulation Rate | 30 | ± 2 | L/min |

### 4.2 DHF (Diluted HF)

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| HF:H2O | 1:100 | ± 1 | ratio |
| Temperature | 23 | ± 1 | °C |
| Time | 60 | ± 5 | sec |
| Etch Rate | 20 | ± 2 | Å/min |
| pH Monitor | 2.8 | ± 0.1 | - |

### 4.3 HPM (Hydrochloric Peroxide Mixture) - SC2

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| HCl:H2O2:H2O | 1:1:6 | ± 0.1 | ratio |
| Temperature | 75 | ± 2 | °C |
| Time | 10 | ± 0.5 | min |
| Bath Volume | 150 | ± 5 | L |
| Metal Removal | > 99.9 | - | % |

### 4.4 Final Rinse & Dry

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| DI Resistivity | > 18.0 | - | MΩ·cm |
| Rinse Time | 5 | ± 0.5 | min |
| Overflow Rate | 40 | ± 2 | L/min |
| Spin Speed | 1500 | ± 50 | RPM |
| N2 Flow (dry) | 100 | ± 5 | L/min |
| IPA Temperature | 82 | ± 1 | °C |

---

## 5. Chemical Management

### 5.1 Chemical Specifications

| Chemical | Grade | Purity | Metal Content |
|----------|-------|--------|---------------|
| NH4OH | VLSI | 29% | < 10ppb each |
| H2O2 | ULSI | 31% | < 1ppb each |
| HF | VLSI | 49% | < 10ppb each |
| HCl | VLSI | 37% | < 1ppb each |
| IPA | Electronic | 99.9% | < 1ppb each |

### 5.2 Bath Life Management

| Solution | Initial | Change Criteria | Frequency |
|----------|---------|-----------------|-----------|
| APM | Fresh | 500 wafers or 24hr | Monitor |
| DHF | Fresh | 1000 wafers or 48hr | Monitor |
| HPM | Fresh | 500 wafers or 24hr | Monitor |

---

## 6. Critical Control Parameters

| Parameter | Target | UCL | LCL | Method |
|-----------|--------|-----|-----|--------|
| Particles (>45nm) | < 5 | 10 | - | KLA SP5 |
| Fe contamination | < 5E9 | 1E10 | - | TXRF |
| Cu contamination | < 1E9 | 5E9 | - | TXRF |
| Surface carbon | < 2ML | 3ML | - | XPS |
| Watermark | 0 | 1 | - | Visual |

---

## 7. Process Monitoring

### 7.1 Inline Monitoring

| Test | Frequency | Specification | Tool |
|------|-----------|---------------|------|
| Particle count | Every lot | < 10 adds | SP5 |
| Metal contamination | Daily | < 1E10 at/cm² | TXRF |
| Chemical concentration | Every bath | ± 2% | Titration |
| DI water quality | Continuous | > 18 MΩ·cm | Online |
| Temperature | Continuous | ± 2°C | PLC |

### 7.2 Process Qualification

| Item | Method | Frequency | Limit |
|------|--------|-----------|-------|
| PRE (Particle Removal Efficiency) | Test wafer | Weekly | > 99% |
| Etch rate | Blanket oxide | Daily | ± 10% |
| Surface roughness | AFM | Weekly | < 0.2nm |
| Contact angle | Goniometer | Daily | < 5° |

---

## 8. 이상 발생 시 대응

### 8.1 Contamination Issues

| Issue | Probable Cause | Action |
|-------|---------------|--------|
| High particles | Filter failure | Replace filter |
| Metal contamination | Chemical quality | Check incoming |
| Watermarks | Poor drying | Check IPA/N2 |
| Residue | Incomplete clean | Extend time |

### 8.2 Equipment Issues  

| Alarm | Description | Impact | Response |
|-------|-------------|--------|----------|
| TEMP_01 | Bath temperature low | Clean efficiency | Check heater |
| FLOW_01 | Low circulation | Uniformity | Check pump |
| CHEM_01 | Concentration drift | Etch rate | Auto-spike |
| DI_01 | Low resistivity | Contamination | Check DI system |

---

## 9. Safety Requirements

### 9.1 Chemical Hazards

| Chemical | Hazard | PPE Required | Emergency |
|----------|--------|--------------|-----------|
| HF | Toxic, corrosive | Acid suit, gloves | Ca-gluconate |
| NH4OH | Corrosive | Face shield | Eye wash |
| H2O2 | Oxidizer | Chemical gloves | Shower |
| HCl | Corrosive | Acid suit | Neutralize |

### 9.2 Emergency Procedures

```
Chemical Spill Response:
1. Alert area personnel
2. Contain spill with kit
3. Neutralize if safe
4. Call ERT if > 1L
5. Complete incident report
```

---

## 10. 참조 문서

- SOP-WET-001: Wet Bench Operation
- SAFE-CHEM-002: Chemical Handling
- SPEC-CLEAN-001: Cleaning Specification
- MAN-FILTER-001: Filter Maintenance

---

## Appendix: Recipe Quick Reference

```
Standard Recipes:
PRE_GATE_CLEAN: Gate oxide preparation
POST_IMP_CLEAN: Post implant strip
PRE_SALI_CLEAN: Pre-salicide clean
POST_CMP_CLEAN: Post CMP clean
BACKSIDE_CLEAN: Wafer backside only
```

---

**문서 관리:**
- 다음 검토: 2025년 2월 15일
- 관리부서: Wet 공정팀
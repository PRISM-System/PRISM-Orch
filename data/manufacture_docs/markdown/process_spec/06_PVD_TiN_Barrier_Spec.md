# PVD TiN Barrier Layer 공정 사양서
## Advanced Cu Interconnect Barrier/Liner Deposition

**문서번호:** PS-PVD-TIN-006-K  
**개정번호:** Rev. 3.2  
**작성일:** 2024년 11월 15일  
**보안등급:** Confidential  

---

## 1. 문서 헤더

### 승인 정보
| 역할 | 담당자 | 소속 | 서명 | 날짜 |
|------|--------|------|------|------|
| 작성 | 이승준 수석 | PVD 공정팀 | | |
| 검토 | 박찬호 책임 | 장비기술팀 | | |
| 승인 | 김태영 팀장 | 공정기술팀 | | |
| 승인 | 정수연 팀장 | 품질팀 | | |
| 승인 | 한동규 팀장 | 생산팀 | | |

---

## 2. 공정 개요

### 2.1 공정 목적
Cu interconnect의 diffusion barrier 및 adhesion layer로서 TiN 박막 증착

### 2.2 주요 사양
- **TiN Thickness:** 100 ± 5Å
- **Resistivity:** < 200 µΩ·cm
- **Uniformity:** < 3% (1σ, 49pt)
- **Step Coverage:** > 70% @ AR 5:1
- **N/Ti Ratio:** 1.0 ± 0.1
- **처리량:** 35 WPH

---

## 3. 공정 Flow

```
Process Sequence:
1. Degas (250°C, 60s)
2. Pre-clean (Ar sputter)
3. Ti Wetting Layer (20Å)
4. TiN Barrier (100Å)
5. Cool Down
```

---

## 4. 상세 공정 파라미터

### 4.1 Pre-clean Step

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| RF Power | 200 | ± 10 | W |
| Ar Flow | 50 | ± 2 | sccm |
| Pressure | 5 | ± 0.5 | mTorr |
| Time | 15 | ± 1 | sec |
| Bias | -150 | ± 10 | V |

### 4.2 Ti Layer Deposition

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| DC Power | 8 | ± 0.5 | kW |
| Ar Flow | 40 | ± 2 | sccm |
| Pressure | 2 | ± 0.2 | mTorr |
| Temperature | 25 | ± 5 | °C |
| Time | 3 | ± 0.2 | sec |

### 4.3 TiN Deposition

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| DC Power | 12 | ± 0.5 | kW |
| Ar Flow | 40 | ± 2 | sccm |
| N₂ Flow | 60 | ± 2 | sccm |
| Pressure | 4 | ± 0.3 | mTorr |
| Temperature | 25 | ± 5 | °C |
| Deposition Time | 12 | ± 0.5 | sec |

---

## 5. Critical Control Parameters

| Parameter | Target | UCL | LCL | Method |
|-----------|--------|-----|-----|--------|
| Thickness | 100Å | 105Å | 95Å | XRF |
| Resistivity | 150 µΩ·cm | 200 | - | 4-point |
| Uniformity | 2.5% | 3.5% | - | 49-point |
| Stress | -500 MPa | -300 | -700 | Wafer bow |
| Composition | N/Ti=1.0 | 1.1 | 0.9 | XPS |

---

## 6. 품질 관리

### 6.1 Inline Monitoring

| Test | Frequency | Spec | Action |
|------|-----------|------|--------|
| Thickness | Every wafer | ±5Å | Hold if OOS |
| Resistivity | Every lot | <200 µΩ·cm | Recipe adjust |
| Particles | Every lot | <10 adds | PM if >20 |
| Adhesion | Daily | >10 MPa | Process check |

### 6.2 Contamination Control

| Element | Limit | Method |
|---------|-------|--------|
| Cu | <1E10 at/cm² | TXRF |
| Fe | <1E10 at/cm² | TXRF |
| Na | <5E10 at/cm² | SIMS |

---

## 7. 이상 발생 시 대응

| Issue | Probable Cause | Action |
|-------|---------------|--------|
| High resistivity | Low N₂ flow | Adjust N₂/Ar ratio |
| Poor uniformity | Target erosion | Target replacement |
| Peeling | Poor adhesion | Increase pre-clean |
| Particles | Target flaking | Target conditioning |

---

## 8. Target 관리

### 8.1 Target Specification

| Property | Specification |
|----------|--------------|
| Composition | Ti (99.995%) |
| Density | >99.5% theoretical |
| Grain Size | <100 µm |
| Bonding | Indium bonded |

### 8.2 Target Life Management

| Parameter | Limit | Action |
|-----------|-------|--------|
| kWh consumed | 400 kWh | Schedule replacement |
| Erosion depth | 8mm | Replace immediately |
| Voltage increase | >20% | Check target condition |

---

## 9. 참조 문서

- SOP-PVD-001: Endura Operation
- MAN-TARGET-001: Target Handling
- SPEC-BARRIER-001: Barrier Requirements

---

## Appendix: Recipe Quick Reference

```
Recipe Name: TIN_BARRIER_100A
Chamber: Endura TiN
Substrate: 300mm Si wafer

Key Settings:
- Base Pressure: <1E-8 Torr
- Ti: 8kW, 3 sec
- TiN: 12kW, 12 sec
- Total Process Time: 90 sec
```

---

**문서 관리:**
- 다음 검토: 2025년 2월 15일
- 관리부서: PVD 공정팀
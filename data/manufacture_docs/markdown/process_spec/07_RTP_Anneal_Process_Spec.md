# RTP (Rapid Thermal Processing) 공정 사양서
## Advanced Junction Activation & Silicidation

**문서번호:** PS-RTP-ANN-007-K  
**개정번호:** Rev. 2.3  
**작성일:** 2024년 11월 15일  
**보안등급:** Confidential  

---

## 1. 문서 헤더

### 승인 정보
| 역할 | 담당자 | 소속 | 서명 | 날짜 |
|------|--------|------|------|------|
| 작성 | 최성민 수석 | Thermal 공정팀 | | |
| 검토 | 강지훈 책임 | 공정통합팀 | | |
| 승인 | 송민수 팀장 | 공정기술팀 | | |
| 승인 | 임수정 팀장 | 품질팀 | | |
| 승인 | 권태경 팀장 | 생산팀 | | |

---

## 2. 공정 개요

### 2.1 공정 목적
Ultra-shallow junction의 dopant activation 및 NiSi/CoSi2 silicide 형성

### 2.2 주요 사양
- **Peak Temperature:** 1050°C ± 5°C
- **Ramp Rate:** 250°C/s (up), 100°C/s (down)
- **Process Time:** 1-5 seconds (spike anneal)
- **Temperature Uniformity:** < ±3°C @ 1050°C
- **Sheet Resistance:** Target ± 5%
- **Junction Depth:** < 30nm (USJ)
- **처리량:** 180 WPH

---

## 3. RTP Process Types

```
Application Matrix:
1. Spike Anneal: Dopant activation (1050°C, 1s)
2. Laser Anneal: USJ formation (1350°C, ms)
3. Soak Anneal: Silicidation (450°C, 30s)
4. Flash Anneal: Damage recovery (1200°C, ms)
```

---

## 4. 상세 공정 파라미터

### 4.1 Dopant Activation (Spike Anneal)

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| Peak Temperature | 1050 | ± 5 | °C |
| Ramp Up Rate | 250 | ± 10 | °C/s |
| Ramp Down Rate | 100 | ± 5 | °C/s |
| Dwell Time | 1.0 | ± 0.1 | sec |
| N2 Flow | 20 | ± 0.5 | slm |
| O2 Content | < 10 | - | ppm |
| Pressure | 760 | ± 5 | Torr |

### 4.2 Silicide Formation (First RTP)

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| Temperature | 450 | ± 5 | °C |
| Time | 30 | ± 2 | sec |
| Ramp Rate | 50 | ± 5 | °C/s |
| N2 Flow | 10 | ± 0.5 | slm |
| Forming Gas | 5% H2/N2 | - | - |

### 4.3 Silicide Transformation (Second RTP)

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| Temperature | 850 | ± 10 | °C |
| Time | 30 | ± 2 | sec |
| Ramp Rate | 100 | ± 10 | °C/s |
| Ambient | N2 | - | - |

---

## 5. Temperature Profile Control

### 5.1 Spike Anneal Profile

```
Temperature (°C)
1050 |      ___
     |     /   \
800  |    /     \
     |   /       \
400  |  /         \
     | /           \
25   |/_____________\___
     0   2   4   6   8  Time(s)

Key Points:
- Ramp start: 0.5s
- Peak reach: 4.0s
- Peak hold: 1.0s
- Cool down: 3.5s
```

### 5.2 Multi-Zone Temperature Control

| Zone | Location | Offset | Purpose |
|------|----------|--------|---------|
| Center | 0-100mm | 0°C | Reference |
| Middle | 100-130mm | +2°C | Edge compensation |
| Edge | 130-150mm | +5°C | Heat loss compensation |

---

## 6. Critical Control Parameters

| Parameter | Target | UCL | LCL | Method |
|-----------|--------|-----|-----|--------|
| Rs (n+) | 500 Ω/□ | 525 | 475 | 4-point probe |
| Rs (p+) | 800 Ω/□ | 840 | 760 | 4-point probe |
| Xj | 25nm | 30nm | 20nm | SIMS |
| Uniformity | < 2% | 3% | - | 49-point map |
| Activation | > 80% | - | 75% | Hall measurement |

---

## 7. Process Integration

### 7.1 Pre-RTP Requirements

| Check Item | Specification | Method |
|------------|---------------|--------|
| Native oxide | < 5Å | Ellipsometer |
| Moisture | < 10ppm | FTIR |
| Particles | < 5 @ 0.12µm | SP5 |
| Queue time | < 4 hours | MES tracking |

### 7.2 Post-RTP Monitoring

| Test | Frequency | Spec | Action |
|------|-----------|------|--------|
| Rs mapping | Every lot | ±5% | Hold if OOS |
| SIMS profile | Daily | Xj < 30nm | Recipe adjust |
| Silicide phase | Weekly | NiSi/CoSi2 | Process check |
| Leakage | Sample | < 1nA/cm² | Device check |

---

## 8. 이상 발생 시 대응

| Issue | Probable Cause | Verification | Action |
|-------|---------------|--------------|--------|
| High Rs | Low temperature | Pyrometer check | Calibration |
| Non-uniform | Lamp degradation | Power mapping | Lamp replacement |
| Deep junction | Slow ramp | Profile check | Controller tune |
| No activation | O2 contamination | Gas analysis | Purge system |
| Peeling | Stress | Visual inspection | Ramp rate adjust |

---

## 9. Lamp Management

### 9.1 Lamp Specification

| Property | Specification |
|----------|--------------|
| Type | Tungsten halogen |
| Power | 300kW total |
| Count | 198 lamps |
| Zones | 15 independent |
| Lifetime | 500k wafers |

### 9.2 Maintenance Schedule

| Item | Frequency | Action |
|------|-----------|--------|
| Power check | Daily | Log deviation |
| Uniformity | Weekly | Adjust zones |
| Replacement | 500k wafers | Full set change |
| Calibration | Monthly | Pyrometer cal |

---

## 10. 참조 문서

- SOP-RTP-001: RTP Tool Operation
- SPEC-ANNEAL-001: Thermal Budget Specification
- MAN-SAFETY-003: High Temperature Safety
- DOC-METROLOGY-002: Rs Measurement

---

## Appendix: Recipe Matrix

```
Recipe Library:
USJ_SPIKE_1050: Ultra-shallow junction
SILICIDE_450_30: NiSi formation
SALICIDE_850_30: CoSi2 transformation
DAMAGE_ANNEAL_950: Implant damage recovery
LASER_ANNEAL_USJ: Sub-20nm junction
```

---

**문서 관리:**
- 다음 검토: 2025년 2월 15일
- 관리부서: Thermal 공정팀
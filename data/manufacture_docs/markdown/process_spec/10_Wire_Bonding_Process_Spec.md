# Wire Bonding 공정 사양서
## Advanced Au/Cu Wire Bonding for FCBGA Package

**문서번호:** PS-ASM-WB-010-K  
**개정번호:** Rev. 1.2  
**작성일:** 2024년 11월 15일  
**보안등급:** Confidential  

---

## 1. 문서 헤더

### 승인 정보
| 역할 | 담당자 | 소속 | 서명 | 날짜 |
|------|--------|------|------|------|
| 작성 | 정민규 책임 | Assembly 공정팀 | | |
| 검토 | 오현주 수석 | Package 개발팀 | | |
| 승인 | 최동원 팀장 | 공정기술팀 | | |
| 승인 | 나영희 팀장 | 품질팀 | | |
| 승인 | 서준혁 팀장 | 생산팀 | | |

---

## 2. 공정 개요

### 2.1 공정 목적
Chip pad와 substrate/leadframe을 금속 wire로 전기적 연결

### 2.2 주요 사양
- **Wire Diameter:** 20 ± 0.5µm (Au), 25 ± 0.5µm (Cu)
- **Ball Size:** 45 ± 3µm (FAB), 65 ± 5µm (2nd bond)
- **Loop Height:** 75 ± 10µm
- **Pull Strength:** > 6.0g (Au), > 8.0g (Cu)
- **Shear Strength:** > 25g
- **IMC Thickness:** 0.5-1.5µm
- **처리량:** 8000 wires/hour

---

## 3. Wire Bonding Process Flow

```
Thermosonic Ball Bonding Sequence:
1. 1st Bond (Ball Bond on Pad)
   - EFO spark
   - Ball formation
   - Bond on chip pad
   
2. Loop Formation
   - Kink formation
   - Loop trajectory
   
3. 2nd Bond (Wedge Bond)
   - Stitch on substrate
   - Tail formation
   - Wire cut
```

---

## 4. 상세 공정 파라미터

### 4.1 Gold Wire Bonding Parameters

| Parameter | 1st Bond | 2nd Bond | Unit |
|-----------|----------|----------|------|
| Temperature | 175 ± 5 | 165 ± 5 | °C |
| Force | 45 ± 3 | 85 ± 5 | gf |
| Time | 15 ± 2 | 20 ± 2 | ms |
| Power | 120 ± 10 | 140 ± 10 | mW |
| US Frequency | 138 | 138 | kHz |
| Ball Size | 45 ± 3 | - | µm |

### 4.2 Copper Wire Bonding Parameters

| Parameter | 1st Bond | 2nd Bond | Unit |
|-----------|----------|----------|------|
| Temperature | 225 ± 5 | 215 ± 5 | °C |
| Force | 55 ± 3 | 100 ± 5 | gf |
| Time | 20 ± 2 | 25 ± 2 | ms |
| Power | 140 ± 10 | 160 ± 10 | mW |
| N2/H2 Flow | 0.5 | 0.5 | L/min |
| Ball Size | 48 ± 3 | - | µm |

### 4.3 EFO (Electronic Flame Off) Settings

| Parameter | Gold | Copper | Unit |
|-----------|------|--------|------|
| Current | 45 | 50 | mA |
| Time | 380 | 420 | µs |
| Tail Length | 200 | 220 | µm |
| Gas Type | N2 | Forming gas | - |
| Gas Flow | 0.3 | 0.5 | L/min |

### 4.4 Loop Profile Parameters

| Parameter | Specification | Tolerance | Unit |
|-----------|--------------|-----------|------|
| Loop Height | 75 | ± 10 | µm |
| Kink Height | 100 | ± 15 | µm |
| Span Length | 2000 | ± 50 | µm |
| Wire Sway | < 5 | - | % |
| Neck Height | 25 | ± 5 | µm |

---

## 5. Material Specifications

### 5.1 Wire Specifications

| Property | Gold Wire | Copper Wire |
|----------|-----------|-------------|
| Purity | > 99.99% | > 99.99% |
| Diameter | 20µm | 25µm |
| Elongation | 2-6% | 5-15% |
| Breaking Load | > 7g | > 10g |
| Tensile Strength | 250 MPa | 400 MPa |
| FAB Hardness | 45-65 Hv | 50-70 Hv |

### 5.2 Pad Metallization

| Layer | Thickness | Purpose |
|-------|-----------|---------|
| Al/Cu (Pad) | 8000Å | Base metal |
| TiN | 500Å | Barrier |
| Al Cap | 300Å | Protection |

---

## 6. Quality Control Parameters

### 6.1 Critical Quality Metrics

| Parameter | Target | USL | LSL | Test Method |
|-----------|--------|-----|-----|-------------|
| Ball Shear | > 30g | - | 25g | Shear test |
| Wire Pull | > 7g | - | 6g | Pull test |
| IMC Coverage | > 85% | 100% | 80% | Cross-section |
| Ball Height | 15µm | 20µm | 10µm | Optical |
| Stitch Width | 60µm | 70µm | 50µm | Optical |

### 6.2 Defect Criteria

| Defect Type | Classification | Limit |
|-------------|----------------|-------|
| Non-stick | Critical | 0% |
| Ball lift | Critical | 0% |
| Cratering | Critical | 0% |
| Wire sag | Major | < 0.1% |
| Loop inconsistency | Minor | < 1% |

---

## 7. Process Monitoring

### 7.1 Inline Monitoring

| Check Item | Frequency | Method | Limit |
|------------|-----------|--------|-------|
| Ball size | Every 2 hrs | Optical | ± 3µm |
| Loop height | Every lot | Profile check | ± 10µm |
| Wire pull | 5 pcs/lot | Destructive | > 6g |
| Ball shear | 5 pcs/lot | Destructive | > 25g |

### 7.2 Process Capability

```
Key Indices:
- Ball size Cpk > 1.67
- Loop height Cpk > 1.33
- Pull strength Cpk > 2.0
- Machine availability > 85%
```

---

## 8. 이상 발생 시 대응

### 8.1 Bonding Defects

| Issue | Cause | Verification | Solution |
|-------|-------|--------------|----------|
| Non-stick 1st | Low temp/force | Check parameters | Increase force |
| Ball lift | Over-bonding | Cross-section | Reduce power |
| Wire break | Neck damage | SEM check | Adjust trajectory |
| Short tail | Cutter wear | Visual check | Replace cutter |
| Contamination | Oxidation | EDX analysis | Clean or N2 purge |

### 8.2 Equipment Alarms

| Alarm | Description | Action |
|-------|-------------|--------|
| EFO_FAIL | No ball formation | Check electrode gap |
| BOND_ERR | Force deviation | Calibrate transducer |
| TEMP_LOW | Stage temperature | Check heater |
| WIRE_BREAK | Frequent break | Check wire spool |

---

## 9. Equipment Maintenance

### 9.1 Daily Maintenance

| Item | Action | Time |
|------|--------|------|
| Capillary | Clean with brush | 5 min |
| Wire clamp | Check tension | 2 min |
| EFO rod | Clean/align | 3 min |
| Stage | Clean debris | 5 min |

### 9.2 Periodic Maintenance

| Item | Frequency | Action |
|------|-----------|--------|
| Capillary | 1M wires | Replace |
| Transducer | 3 months | Calibrate |
| Wire guide | 1 month | Clean |
| Vision system | Weekly | Clean lens |

---

## 10. 참조 문서

- SOP-WB-001: Wire Bonder Operation
- SPEC-BOND-001: Wire Bond Specification
- QC-PULL-001: Pull Test Method
- MAN-CAPILLARY-001: Capillary Selection Guide

---

## Appendix A: Loop Types

```
Standard Loop Profiles:
1. Standard Loop - General purpose
2. Low Loop - Height constrained  
3. Long Loop - Extended span
4. M-Loop - EMI reduction
5. S-Loop - Fine pitch application
```

---

## Appendix B: Troubleshooting Guide

| Symptom | Check Points | Action |
|---------|--------------|--------|
| Inconsistent ball | EFO current | Adjust ± 5mA |
| Poor stitch | 2nd bond force | Increase 10gf |
| Wire sway | Loop trajectory | Reduce speed |
| Pad damage | 1st bond parameter | Reduce power |

---

**문서 관리:**
- 다음 검토: 2025년 2월 15일
- 관리부서: Assembly 공정팀
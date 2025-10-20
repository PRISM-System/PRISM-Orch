# Copper CMP 공정 사양서
## Dual Damascene Cu/Low-k Integration

**문서번호:** PS-CMP-CU-003-K  
**개정번호:** Rev. 1.8  
**작성일:** 2024년 11월 15일  
**보안등급:** Confidential  

---

## 1. 문서 헤더

### 승인 정보
| 역할 | 담당자 | 소속 | 서명 | 날짜 |
|------|--------|------|------|------|
| 작성 | 김동현 수석 | CMP 공정기술팀 | | |
| 검토 | 이서연 책임 | 통합공정팀 | | |
| 승인 | 정우진 팀장 | 공정기술팀 | | |
| 승인 | 한지민 팀장 | 품질팀 | | |
| 승인 | 박준영 팀장 | 생산팀 | | |

---

## 2. 공정 개요

### 2.1 목적
Dual damascene 구조의 Cu interconnect 형성을 위한 Cu overburden 및 barrier metal 제거

### 2.2 주요 사양
- **Cu Thickness Remaining:** 3000 ± 100Å
- **Dishing:** < 200Å (100µm line)
- **Erosion:** < 150Å (50% density)
- **Within-Die Non-Uniformity:** < 200Å
- **Within-Wafer Non-Uniformity:** < 3%
- **처리량:** 60 WPH

---

## 3. 공정 Flow

```
3-Step CMP Process:
Step 1: Cu Bulk Removal (Platen 1)
Step 2: Barrier Removal (Platen 2)  
Step 3: Buff/Touch-up (Platen 3)
```

---

## 4. 상세 공정 파라미터

### 4.1 Step 1: Cu Bulk Removal

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| Down Force | 3.0 | ± 0.1 | PSI |
| Platen Speed | 93 | ± 2 | RPM |
| Head Speed | 87 | ± 2 | RPM |
| Slurry Flow | 200 | ± 5 | ml/min |
| Pad Type | IC1010 | - | - |
| Slurry Type | Cu-CMP-A | - | - |
| Temperature | 55 | ± 2 | °C |
| Endpoint | Eddy current | - | - |

### 4.2 Step 2: Barrier Removal

| Parameter | Set Point | Tolerance | Unit |
|-----------|-----------|-----------|------|
| Down Force | 2.5 | ± 0.1 | PSI |
| Platen Speed | 63 | ± 2 | RPM |
| Head Speed | 57 | ± 2 | RPM |
| Slurry Flow | 150 | ± 5 | ml/min |
| Pad Type | Politex | - | - |
| Over-polish | 20 | ± 2 | % |

---

## 5. Critical Control Parameters

| Parameter | Target | UCL | LCL |
|-----------|--------|-----|-----|
| Removal Rate | 6000 Å/min | 6300 | 5700 |
| Selectivity Cu:Ta | 100:1 | - | 80:1 |
| Dishing | < 200Å | 250Å | - |
| Erosion | < 150Å | 200Å | - |

---

**다음 검토일:** 2025년 2월 15일
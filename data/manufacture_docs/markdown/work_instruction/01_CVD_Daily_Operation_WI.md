# Chemical Vapor Deposition (CVD) 장비 일일 점검 및 운전 작업 지시서
## AMAT Producer SE CVD 장비 기준

**문서번호:** WI-CVD-DAILY-002  
**효력발생일:** 2024년 12월 1일  
**개정번호:** Rev 2.1  

---

## 1. 문서 정보

### 1.1 승인 정보
| 구분 | 담당자 | 소속 | 직책 | 서명 | 날짜 |
|------|--------|------|------|------|------|
| 작성 | 김상훈 | 장비기술팀 | 책임 | | |
| 검토 | 이정민 | 생산팀 | 수석 | | |
| 승인 | 최윤석 | 제조부문 | 이사 | | |

### 1.2 교육 이수자 서명란
| 이름 | 사번 | 소속 | 교육일 | 서명 | 인증 |
|------|------|------|--------|------|------|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |

### 1.3 개정 이력
| Rev | 날짜 | 변경 내용 | 작성자 |
|-----|------|-----------|--------|
| 1.0 | 2024.06.01 | 최초 작성 | 김상훈 |
| 2.0 | 2024.09.15 | 안전 절차 강화 | 김상훈 |
| 2.1 | 2024.11.15 | Particle 기준 update | 이정민 |

---

## 2. 목적 및 적용 범위

### 2.1 목적
본 작업 지시서는 AMAT Producer SE CVD 장비의 일일 점검 및 운전 절차를 표준화하여 장비 가동률을 극대화하고 공정 품질을 안정적으로 유지하는 것을 목적으로 합니다.

### 2.2 적용 범위
- **적용 장비:** AMAT Producer SE CVD Systems (P1, P2, P3)
- **적용 공정:** TEOS oxide, Silicon nitride deposition
- **적용 대상:** 3교대 작업자 및 장비 엔지니어
- **작업 주기:** 매 shift 시작 시 및 lot 처리 전

### 2.3 관련 문서
- Equipment Manual: AMAT Producer SE
- Process Specification: PS-CVD-001
- Safety Guideline: SG-FAB-001
- Emergency Response: ER-CVD-001

---

## 3. 안전 주의사항 ⚠️

### 3.1 Chemical Hazards

#### 위험 물질 정보
| Chemical | 위험성 | TLV | 증상 | 응급처치 |
|----------|--------|-----|------|----------|
| TEOS | 자극성 | 10 ppm | 호흡곤란, 눈 자극 | 신선한 공기, 의료진 호출 |
| NH3 | 부식성/독성 | 25 ppm | 화상, 호흡곤란 | 즉시 물로 세척, 응급실 |
| SiH4 | 발화성/독성 | 5 ppm | 화상, 질식 | 대피, 소방대 호출 |
| NF3 | 산화성/독성 | 10 ppm | 호흡곤란 | 대피, 의료진 호출 |

### 3.2 필수 개인보호장비 (PPE)

#### 기본 PPE
- ✓ Chemical resistant gloves (Nitrile)
- ✓ Safety goggles (Chemical splash type)
- ✓ Cleanroom suit (Anti-static)
- ✓ Safety shoes (ESD safe)
- ✓ Face shield (PM 작업 시)

### 3.3 비상 대응

#### Emergency Shower/Eyewash Station
- **위치:** Bay 3-A, 3-B 양 끝단
- **점검:** 매주 월요일 flow test
- **사용법:** 
  1. 즉시 station으로 이동
  2. 레버를 당겨 작동
  3. 최소 15분간 세척
  4. 의료진 호출

#### Gas Leak 시 대피 경로
```
CVD Bay Layout:
[P1] [P2] [P3]
  ↓    ↓    ↓
[━━━━━━━━━━━] Main Corridor
  ↓         ↓
Exit A    Exit B
```
**대피 순서:**
1. 가장 가까운 출구로 신속히 대피
2. Gas alarm 작동 확인
3. 집결지: Sub-fab 주차장
4. 인원 점검 및 보고

### 3.4 Lockout/Tagout Procedure
작업 전 반드시:
1. 장비 전원 차단
2. Lock 설치 및 Tag 부착
3. 에너지 0 상태 확인
4. 작업 완료 후 제거

---

## 4. 사전 준비사항

### 4.1 MES System 로그인 및 Lot 확인

#### Step-by-Step 절차:
1. **MES Terminal 접속**
   - ID/Password 입력
   - Equipment P1/P2/P3 선택
   
2. **대기 Lot 확인**
   ```
   화면 경로: [Main] → [Lot Status] → [Queue]
   확인 사항:
   - Lot ID
   - Product type
   - Layer
   - Priority
   - Recipe name
   ```

3. **Recipe 확인**
   - Recipe가 등록되어 있는지 확인
   - Version이 최신인지 체크
   - Process time 확인

### 4.2 이전 Shift Pass-down 확인

#### 인수인계 체크리스트:
- [ ] 장비 상태 (Idle/Production/Down)
- [ ] 진행 중인 PM 항목
- [ ] Particle trend (마지막 3 lot)
- [ ] 특이사항 또는 주의사항
- [ ] 완료된 작업 내역
- [ ] 다음 shift 요청사항

### 4.3 Tool Status 확인

#### System Status Check:
| Module | Normal State | Check Point | ✓ |
|--------|-------------|-------------|---|
| Chamber A | Idle/Ready | Pressure < 1mT | □ |
| Chamber B | Idle/Ready | Pressure < 1mT | □ |
| Transfer | Ready | Robot initialized | □ |
| Load Lock | Atmosphere | Door closed | □ |
| Gas Panel | Normal | No alarms | □ |
| Vacuum | Normal | Foreline < 100mT | □ |

### 4.4 Consumable Parts 수명 체크

#### Parts Life Monitor:
| Part | Current | Limit | Action | ✓ |
|------|---------|-------|--------|---|
| Showerhead | 8,234 wafers | 10,000 | Monitor | □ |
| Chamber liner | 15,632 wafers | 20,000 | OK | □ |
| O-ring (lid) | 4,521 wafers | 5,000 | Prepare | □ |
| Remote plasma kit | 2,456 hours | 3,000 | OK | □ |

**💡 현장 Tip:** Parts life가 90% 도달 시 미리 부품 준비하고 엔지니어에게 통보할 것!

---

## 5. 단계별 작업 절차

### 5.1 시작 전 점검 (소요시간: 10분)

#### Step 1: Chamber Pressure 확인 (2분)
**조작 방법:**
1. Main panel에서 [Process] → [Chamber Status] 선택
2. 각 chamber별 pressure 확인

**정상 범위:**
- Base pressure: < 1.0E-6 Torr ✓
- Leak rate: < 5 mTorr/min ✓

**Check Point:**
- [ ] Chamber A pressure 정상
- [ ] Chamber B pressure 정상
- [ ] Leak rate 정상

⚠️ **이상 시:** Troubleshooting guide TS-CVD-001 참조

#### Step 2: Gas Flow 확인 (2분)
**조작 방법:**
1. [Utility] → [Gas System] 선택
2. 각 MFC별 0 point 확인

**확인 항목:**
| Gas | MFC# | Zero Reading | Status | ✓ |
|-----|------|-------------|--------|---|
| TEOS | MFC1 | 0.0 ± 0.1 sccm | | □ |
| O2 | MFC2 | 0.0 ± 0.5 sccm | | □ |
| NH3 | MFC3 | 0.0 ± 0.5 sccm | | □ |
| SiH4 | MFC4 | 0.0 ± 0.1 sccm | | □ |

#### Step 3: Temperature 확인 (2분)
**조작 방법:**
1. [Process] → [Temperature Monitor] 선택
2. 각 zone별 온도 확인

**정상 온도:**
- Susceptor: 380 ± 2°C
- Wall: 65 ± 2°C
- Lid: 65 ± 2°C
- Foreline: < 50°C

**온도 안정화 확인:**
- 최근 1시간 drift < 1°C
- Set point 도달 확인

#### Step 4: Robot 초기화 확인 (2분)
**조작 방법:**
1. [Transfer] → [Robot Status] 확인
2. Home position 확인
3. Wafer mapping sensor test

**Test 절차:**
1. Dummy wafer load
2. [Utility] → [Robot Test] → [Mapping Test]
3. Pass/Fail 확인

#### Step 5: Exhaust System 확인 (2분)
**확인 항목:**
- Scrubber 정상 작동 (녹색등)
- Exhaust pressure: -2.0 ± 0.5" H2O
- Pump 소음 정상
- Foreline filter ΔP < 10 Torr

---

### 5.2 Dummy Wafer Run (소요시간: 15분)

#### Particle Qualification Run
**목적:** Chamber condition 및 particle 성능 확인

**절차:**
1. **Dummy Wafer Loading**
   - Cassette position 1-3: Particle monitor wafer
   - Position 4-5: Thickness monitor wafer
   
2. **Recipe 선택**
   ```
   [Recipe] → [Qual] → [PARTICLE_QUAL_001]
   Parameters:
   - TEOS: 400 sccm
   - O2: 800 sccm
   - Pressure: 600 mTorr
   - Power: 400W
   - Temperature: 380°C
   - Time: 60 seconds
   ```

3. **Run 실행**
   - [Start] 버튼 클릭
   - Process 진행 모니터링
   - End point 확인

4. **결과 확인**
   - Particle count: < 10 ea @ 0.16μm ✓
   - Thickness: 1000 ± 50Å ✓
   - Uniformity: < 2% (1σ) ✓

**💡 현장 Tip:** Particle이 spec out일 경우 한 번 더 dummy run 실시. 그래도 fail이면 seasoning 필요.

---

### 5.3 Production Recipe 실행 (소요시간: Variable)

#### Step 1: Lot 정보 입력
1. **FOUP Load**
   - Load port에 FOUP 안착
   - Clamp 동작 확인
   - Purge 시작 (N2 flow)

2. **Lot ID Scan**
   ```
   화면: [Lot] → [Scan ID]
   - Barcode scanner로 lot ID 읽기
   - MES와 정보 일치 확인
   - Recipe auto-download
   ```

3. **Recipe 확인**
   | 항목 | 확인 내용 | ✓ |
   |------|----------|---|
   | Recipe name | Product와 일치 | □ |
   | Thickness target | Spec 확인 | □ |
   | Process time | 예상 시간 | □ |
   | Wafer count | 실제 수량 일치 | □ |

#### Step 2: Process 실행
1. **Start 조건 확인**
   - Chamber ready
   - Recipe loaded
   - No alarms
   - Vacuum OK

2. **Process Start**
   ```
   [Process] → [Start]
   확인 메시지: "Start lot XXXXX?" → [Yes]
   ```

3. **실시간 모니터링**
   **Critical Parameters:**
   | Parameter | Target | Actual | Deviation | Status |
   |-----------|--------|--------|-----------|--------|
   | Pressure | 600 mT | | ± 10 mT | |
   | RF Power | 400W | | ± 5W | |
   | TEOS Flow | 400 sccm | | ± 5 sccm | |
   | Temperature | 380°C | | ± 2°C | |

#### Step 3: In-situ Monitoring
**Monitoring Points:**
- Chamber pressure stability
- RF power reflected < 5W
- Temperature deviation < 1°C
- Gas flow stability
- End point signal (if applicable)

**Alarm 발생 시:**
1. Alarm 내용 확인
2. Pause 또는 Abort 판단
3. Troubleshooting 실시
4. Engineer call (필요시)

---

### 5.4 Process 완료 후 확인

#### Wafer Unloading
1. **Cool Down 확인**
   - Chamber 온도 < 100°C
   - Wafer 온도 적정

2. **Transfer 확인**
   - Robot speed normal
   - No wafer sliding
   - Centering OK

3. **FOUP Purge**
   - N2 purge 30초
   - Humidity < 30%

#### Data Recording
**Lot History 기록:**
| 항목 | 기록 내용 |
|------|----------|
| Lot completion time | |
| Total process time | |
| Wafer count | |
| Particle performance | |
| Thickness average | |
| Any issues | |

---

## 6. 품질 확인 항목

### 6.1 Inline Metrology

#### Thickness Measurement
**Sampling:** Wafer #1, #13, #25

**Measurement Points:** 49 points/wafer
```
Wafer Map:
     1  2  3  4  5  6  7
     8  9 10 11 12 13 14
    15 16 17 18 19 20 21
    22 23 24 25 26 27 28
    29 30 31 32 33 34 35
    36 37 38 39 40 41 42
    43 44 45 46 47 48 49
```

**Specifications:**
| Parameter | Spec | Measured | Pass/Fail |
|-----------|------|----------|-----------|
| Thickness mean | 5000 ± 100Å | | |
| Uniformity (1σ) | < 1.5% | | |
| Range | < 150Å | | |

### 6.2 Particle Performance

#### Particle Count Specification
- **Spec:** < 10 ea @ 0.16μm
- **Action Level:** > 20 ea
- **Control Level:** > 30 ea

**Particle Trend Chart:**
```
30 |           
25 |         x  <- Control Limit
20 |       x    <- Action Limit
15 |     x
10 | - - - - - - <- Spec Limit
 5 | x x 
 0 |___________
   1 2 3 4 5 <- Lot Number
```

### 6.3 Film Properties

#### Critical Properties Check
| Property | Target | Tolerance | Method |
|----------|--------|-----------|---------|
| RI (Refractive Index) | 1.46 | ± 0.01 | Ellipsometer |
| Stress | -250 MPa | ± 50 MPa | Wafer bow |
| Wet Etch Rate | 800 Å/min | ± 50 | BOE 6:1 |
| Composition | Stoichiometric | ± 2% | FTIR |

---

## 7. 작업 완료 후 조치

### 7.1 Logbook 기록

#### 기록 필수 항목:
```
Date: ____/____/____  Shift: ____  Operator: ________

Equipment Status:
□ Production  □ Idle  □ Down  □ PM

Lots Processed:
Lot ID: ________ Product: ________ Qty: ____ Result: ____
Lot ID: ________ Product: ________ Qty: ____ Result: ____

Issues/Comments:
_________________________________________________
_________________________________________________

Parts Life Status:
Showerhead: ______ wafers remaining
Chamber Kit: ______ wafers remaining

Next Shift Action Items:
_________________________________________________
```

### 7.2 MES Data Entry

#### Data Input Procedure:
1. **[MES] → [Lot Complete]**
2. 입력 항목:
   - Actual quantity processed
   - Scrap quantity (if any)
   - Process time
   - Any holds or issues

3. **SPC Data Upload**
   - Thickness data
   - Particle data
   - Film properties

### 7.3 다음 Shift 인수인계

#### Pass-down Sheet 작성:
| 항목 | 내용 |
|------|------|
| 완료 lot | |
| 진행 중 lot | |
| 장비 상태 | |
| 특이사항 | |
| 잔여 PM 항목 | |
| 부품 교체 필요 | |
| 주의사항 | |

**💡 현장 Tip:** 사소한 것도 빠짐없이 기록! 다음 shift가 고생하지 않도록.

---

## 8. 비정상 상황 대응

### 8.1 Alarm Code별 1차 조치

#### Critical Alarms (즉시 정지)
| Alarm Code | Description | 1차 조치 | Engineer Call |
|------------|-------------|----------|---------------|
| E001 | Chamber pressure high | Check exhaust valve | Yes |
| E002 | RF no power | Check RF generator | Yes |
| E003 | Over temperature | Check heater/TC | Yes |
| E004 | Gas leak detected | Evacuate area | Emergency |

#### Warning Alarms (주의 필요)
| Alarm Code | Description | 1차 조치 | Engineer Call |
|------------|-------------|----------|---------------|
| W001 | Particle trending high | Run seasoning | Monitor |
| W002 | MFC deviation | Reset MFC | If persist |
| W003 | Robot position error | Re-initialize | If persist |
| W004 | Exhaust pressure low | Check scrubber | Monitor |

### 8.2 엔지니어 호출 기준

#### 즉시 호출 상황:
1. Safety 관련 alarm
2. Chamber pressure 이상
3. Repeated failure (3회 이상)
4. Unknown error
5. Wafer breakage

#### 호출 시 준비 정보:
- Alarm code & message
- 발생 시간
- 진행 중이던 recipe/step
- 시도한 조치 사항
- Current equipment status

### 8.3 Lot Hold 기준 및 절차

#### Hold 기준:
| 상황 | Hold Type | Release Authority |
|------|-----------|-------------------|
| Thickness OOS | Quality hold | QA Engineer |
| Particle > 30 | Quality hold | QA Engineer |
| Recipe mismatch | Process hold | Process Engineer |
| Equipment alarm | Equipment hold | Equipment Engineer |

#### Hold Procedure:
1. **MES에서 lot hold**
   ```
   [Lot] → [Hold] → [Select Reason] → [Comments]
   ```

2. **Physical 표시**
   - Hold tag 부착
   - FOUP에 hold sticker

3. **통보**
   - Owner engineer
   - Shift supervisor
   - QA (if quality hold)

---

## 9. 관련 양식

### 9.1 일일 점검 체크시트

```
CVD Daily Check Sheet         Date: ___/___/___

Equipment: Producer SE #___    Shift: ___

[System Check]
□ Chamber pressure < 1E-6 Torr
□ Leak rate < 5 mTorr/min
□ Gas system normal
□ Temperature stable
□ Robot initialized
□ Exhaust normal

[Dummy Run Result]
Particle: _____ ea @ 0.16μm  (Spec < 10)
Thickness: _____ Å  (Target 1000 ± 50)
Uniformity: _____ %  (Spec < 2%)

[Production Summary]
Total lots: _____
Total wafers: _____
Uptime: _____ %

Operator: _____________ Sign: _____________
```

### 9.2 Particle Trend Chart

```
Date: ___/___/___ to ___/___/___

40 |
35 |
30 |---------------------------- Control
25 |---------------------------- Action  
20 |
15 |
10 |---------------------------- Spec
 5 |
 0 |_________________________
   Mon Tue Wed Thu Fri Sat Sun
```

### 9.3 Downtime Report Form

```
DOWNTIME REPORT

Date: ___/___/___  Time: ___:___
Equipment: ____________
Module: ______________

Problem Description:
________________________________
________________________________

Root Cause:
________________________________
________________________________

Action Taken:
________________________________
________________________________

Parts Replaced: _________________
Down Time: _____ minutes
Wafer Loss: _____ ea

Engineer: __________ Sign: __________
```

---

## 10. FAQ 및 현장 팁

### 10.1 자주 발생하는 문제와 해결

#### Q1: Particle이 갑자기 증가했어요.
**A:** 
1. 먼저 dummy wafer 3장 추가 run
2. Seasoning recipe 30분 실행
3. 그래도 높으면 wet clean 필요
4. Showerhead 육안 검사

#### Q2: Thickness가 target보다 계속 두꺼워요.
**A:**
1. MFC calibration 확인
2. Process time 확인
3. Temperature 확인
4. RF power 확인
보통 MFC drift가 원인입니다.

#### Q3: Wafer가 깨졌어요. 어떻게 하죠?
**A:**
1. 즉시 공정 중단
2. Chamber를 vent하지 마세요
3. Engineer 호출
4. 파편 위치 기록
5. 절대 혼자 처리하지 마세요

### 10.2 효율적인 작업 팁

#### 💡 Pro Tips:
1. **Morning Shift**
   - 장비가 idle 상태였다면 warm-up run 필수
   - 월요일은 extended PM check

2. **Day Shift**
   - Peak 시간대 - 빠른 lot 처리 중요
   - PM window 활용

3. **Night Shift**
   - Qual wafer run 하기 좋은 시간
   - 다음날 준비 철저히

4. **Common Sense**
   - 의심스러우면 확인하고 진행
   - 기록은 자세히
   - 안전이 최우선

### 10.3 Emergency Contacts

| 구분 | 담당 | 연락처 | 비고 |
|------|------|--------|------|
| Equipment Engineer | 김엔지 | #8234 | 24/7 |
| Process Engineer | 박프로 | #8235 | 주간 |
| Safety Officer | 이안전 | #8119 | 24/7 |
| Facility | 시설팀 | #8888 | 24/7 |
| Emergency | | 119 | |

---

## Appendix A: Recipe Parameters Reference

### Standard TEOS Oxide
```
Recipe: TEOS_5000A_STD
Thickness: 5000Å
TEOS: 400 sccm
O2: 800 sccm  
Pressure: 600 mTorr
Power: 400W
Temperature: 380°C
Time: 125 seconds
```

### Silicon Nitride
```
Recipe: SIN_2000A_STD
Thickness: 2000Å
SiH4: 100 sccm
NH3: 400 sccm
N2: 2000 sccm
Pressure: 900 mTorr
Power: 350W
Temperature: 400°C
Time: 85 seconds
```

---

## Appendix B: Troubleshooting Quick Guide

| 증상 | 확인사항 | 조치 |
|------|----------|------|
| Pressure 불안정 | Throttle valve | Calibration |
| Thickness 불균일 | Showerhead | Cleaning |
| Particle 높음 | Chamber wall | Wet clean |
| Peel-off | Temperature | Ramp rate 조정 |
| Haze | Gas ratio | Recipe 조정 |

---

**교육 문의:** Training@company.com  
**문서 관리:** 장비기술팀  
**최종 수정일:** 2024.11.15  
**다음 개정 예정:** 2025.03.01

**⚠️ 주의: 본 문서는 회사 기밀이므로 외부 유출을 금합니다.**
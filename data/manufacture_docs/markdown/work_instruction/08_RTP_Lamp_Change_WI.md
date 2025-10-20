# RTP Lamp 교체 작업 지시서
## Applied Materials RTP Centura Lamp Module Replacement

**문서번호:** WI-RTP-LAMP-009  
**효력발생일:** 2024년 12월 1일  
**개정번호:** Rev 2.0  

---

## 1. 문서 정보

### 1.1 승인 정보
| 구분 | 담당자 | 소속 | 직책 | 서명 |
|------|--------|------|------|------|
| 작성 | 이준혁 | RTP 기술팀 | 수석 | |
| 검토 | 김나영 | 장비보전팀 | 책임 | |
| 승인 | 최병철 | 제조부문 | 부장 | |

### 1.2 적용 범위
- **장비:** Applied Materials RTP Centura
- **작업자:** Certified RTP Engineers
- **교체 주기:** 500k wafers 또는 lamp failure
- **소요시간:** 4시간 (Full set), 1시간 (Single lamp)

---

## 2. 안전 주의사항 ⚠️

### 2.1 고온 위험
- **Lamp 온도:** 최대 1200°C 도달
- **Cool down:** 최소 2시간 필수
- **화상 위험:** 보호 장구 착용

### 2.2 전기 위험
- **전압:** 480V 3-phase
- **전류:** 최대 600A per zone
- **감전 주의:** LOTO 필수

### 2.3 취급 주의
- **Lamp 재질:** Tungsten-halogen (깨지기 쉬움)
- **오염 금지:** 맨손 접촉 시 hot spot
- **파손 위험:** 2인 1조 작업

---

## 3. 작업 준비

### 3.1 필수 장비 및 부품
- [ ] Replacement lamps (Type: ______)
- [ ] Lamp puller tool
- [ ] Torque wrench (5 N·m)
- [ ] Contact cleaner
- [ ] Lint-free gloves
- [ ] IPA wipes
- [ ] Multimeter
- [ ] IR thermometer
- [ ] Lamp map sheet

### 3.2 Lamp 사양 확인
```
Lamp Specifications:
- Type: Tungsten-halogen
- Power: 1.5kW per lamp
- Voltage: 24V DC
- Total quantity: 198 ea
- Zone configuration: 15 zones
```

---

## 4. Lamp 교체 절차

### 4.1 Step 1: 시스템 Shutdown (30분)

**작업 내용:**
1. Process 중단
   ```
   [System] → [Abort Process]
   Wafer 확인: Chamber 내 wafer 없음
   Cool down recipe 실행
   ```

2. Power isolation
   ```
   차단 순서:
   1) Recipe 정지
   2) Lamp power OFF
   3) Main breaker OFF (Panel LP-01)
   4) LOTO 설치
   
   Lock #: __________
   Tag 시간: __________
   ```

3. 온도 확인
   ```
   IR Thermometer 측정:
   - Chamber top: _____°C (< 50°C)
   - Lamp house: _____°C (< 40°C)
   - Reflector: _____°C (< 40°C)
   ```

**💡 Tip:** Lamp house 팬 계속 작동 유지

### 4.2 Step 2: Lamp Module Access (20분)

**작업 내용:**
1. Chamber 상부 개방
   ```
   개방 순서:
   1) Safety interlock 해제
   2) Lift mechanism 작동
   3) Chamber top 상승
   4) Support bar 설치
   ```

2. Reflector plate 제거
   ```
   주의사항:
   - Reflector 오염 방지
   - 표면 손상 금지
   - 보관 위치 확보
   
   볼트 제거: 8개 (M6)
   Lift handle 사용
   ```

3. Lamp array 노출
   - Zone 구분 확인
   - Lamp 배열 사진 촬영
   - 이상 lamp marking

### 4.3 Step 3: Lamp Mapping (15분)

**작업 내용:**
1. 불량 lamp 확인
   ```
   육안 검사:
   □ Filament 단선
   □ 흑화 (blackening)
   □ 변형 (deformation)
   □ 접점 부식
   ```

2. Lamp position 기록
   ```
   Zone Map:
   [Center Zone 1-12]
   1: ___ 2: ___ 3: ___
   4: ___ 5: ___ 6: ___
   7: ___ 8: ___ 9: ___
   10:___ 11:___ 12:___
   
   [Middle Zone 13-15]
   ...
   
   교체 대상: Zone ___, Position ___
   ```

### 4.4 Step 4: Lamp 제거 (30분/lamp)

**작업 내용:**
1. 전기 연결 분리
   ```
   작업 순서:
   1) Connector 위치 확인
   2) Locking tab 해제
   3) Connector 분리
   4) 접점 상태 확인
   ```

2. Lamp 제거
   ```
   Lamp puller 사용:
   1) Tool을 lamp base에 체결
   2) 수직으로 당기기
   3) 좌우 흔들기 금지
   4) 제거된 lamp 안전 보관
   ```

3. Socket 청소
   ```
   청소 절차:
   - Contact cleaner 도포
   - 부식 제거
   - IPA wipe
   - 건조 확인
   ```

**⚠️ 주의:** Lamp 유리 부분 접촉 금지

### 4.5 Step 5: 신규 Lamp 설치 (30분/lamp)

**작업 내용:**
1. Lamp 검수
   ```
   확인 사항:
   □ Model 일치: __________
   □ 외관 이상 없음
   □ Filament 정상
   □ Base contact 깨끗함
   ```

2. Lamp 삽입
   ```
   설치 순서:
   1) Lint-free glove 착용
   2) Lamp base만 잡기
   3) Socket에 수직 삽입
   4) 완전 삽입 확인 (click 소리)
   5) 흔들림 없음 확인
   ```

3. 전기 연결
   ```
   연결 작업:
   1) Connector 정렬
   2) 확실히 체결
   3) Locking tab 잠금
   4) 저항 측정: _____ Ω
   ```

### 4.6 Step 6: Zone Balancing (45분)

**작업 내용:**
1. 초기 저항 측정
   ```
   각 Zone 저항 측정:
   Zone 1: _____ Ω
   Zone 2: _____ Ω
   ...
   Zone 15: _____ Ω
   
   허용 편차: ± 5%
   ```

2. Power distribution 확인
   ```
   Test 조건:
   - Low power test (10%)
   - 각 zone 개별 점등
   - Current 측정
   - 균일도 확인
   ```

### 4.7 Step 7: System 재조립 (30분)

**작업 내용:**
1. Reflector 재설치
   ```
   설치 절차:
   1) Reflector 표면 청소
   2) 정렬 pin 맞춤
   3) 볼트 체결 (대각선)
   4) Torque: 5 N·m
   ```

2. Chamber top 닫기
   - Support bar 제거
   - Chamber 하강
   - Interlock 확인
   - Seal 상태 점검

3. 시스템 점검
   - [ ] 모든 연결 확인
   - [ ] Tool 제거 확인
   - [ ] 청소 상태
   - [ ] 안전장치 정상

---

## 5. Lamp Calibration

### 5.1 Power Calibration (30분)

**작업 내용:**
1. Zone power 설정
   ```
   [Calibration] → [Lamp Power]
   
   각 Zone 설정:
   - Center: 100%
   - Middle: 102%
   - Edge: 105%
   ```

2. Temperature uniformity
   ```
   Test wafer run:
   - Recipe: LAMP_CAL_1050
   - Thermocouple wafer
   - 9 point measurement
   - Uniformity: < ±5°C
   ```

### 5.2 Process 검증 (40분)

**작업 내용:**
1. Dummy run
   ```
   조건:
   - 온도: 1050°C
   - 시간: 60 sec
   - Wafer: 5매
   ```

2. 결과 확인
   ```
   측정 항목:
   □ Temperature uniformity: _____°C
   □ Ramp rate: _____°C/s
   □ Stability: _____ %
   □ No alarm
   ```

---

## 6. 품질 확인

### 6.1 Performance Test

| Parameter | Specification | Result | Pass/Fail |
|-----------|--------------|--------|-----------|
| Peak temp | 1050 ± 5°C | _____°C | |
| Uniformity | < ±5°C | _____°C | |
| Ramp rate | 250°C/s | _____°C/s | |
| Power consumption | < 300kW | _____kW | |

### 6.2 Lamp Life Reset

```
[System] → [Maintenance] → [Lamp Counter]

작업 내용:
- Old counter: _____ hours
- Reset to: 0 hours
- Next PM: 500k wafers
```

---

## 7. 시스템 재가동

### 7.1 재가동 체크리스트
- [ ] LOTO 해제
- [ ] Power 복구
- [ ] Vacuum pump ON
- [ ] Cooling water 확인
- [ ] N2 purge 정상
- [ ] System initialize

### 7.2 Production Release

```
[MES] → [PM Record] → [Lamp Change]

기록 사항:
- 교체 lamp 수: _____ ea
- Zone 위치: __________
- Total run time: _____ hrs
- 교체 사유: __________
```

---

## 8. 이상 상황 대응

### 8.1 Lamp 관련 문제

| 증상 | 원인 | 조치 |
|------|------|------|
| 즉시 소손 | 과전압 | Zone controller 점검 |
| 불균일 가열 | Zone 불균형 | Power cal 재실행 |
| 점등 실패 | 접촉 불량 | Connector 재체결 |
| Flickering | 수명 종료 | Lamp 교체 |

### 8.2 온도 문제

| 문제 | 확인사항 | 해결방법 |
|------|----------|----------|
| Low temp | Lamp failure | 개별 lamp 점검 |
| Hot spot | Lamp 오염 | Lamp 청소/교체 |
| Slow ramp | Power 부족 | Power supply 점검 |

---

## 9. 폐Lamp 처리

### 9.1 폐기 절차
- 분류: 일반 산업폐기물
- 포장: 파손 방지 포장
- 라벨: "폐Lamp - 취급주의"
- 보관: 지정 구역
- 처리: 월 1회 수거

### 9.2 재활용
- Tungsten 회수 가능
- Base 금속 분리
- 유리 재활용

---

## 10. 유지보수 Tip

### 10.1 Lamp 수명 연장
- 급격한 온도 변화 피하기
- Soft start/stop 사용
- 정기적 reflector 청소
- 적정 power level 유지

### 10.2 예방 정비
- Weekly: Visual inspection
- Monthly: Resistance check
- Quarterly: Zone balance
- Yearly: Full calibration

---

**교육 이수 서명란:**

| 이름 | 사번 | 교육일 | 서명 |
|------|------|--------|------|
| | | | |
| | | | |

**문서 관리:** RTP 기술팀
**다음 개정:** 2025년 3월
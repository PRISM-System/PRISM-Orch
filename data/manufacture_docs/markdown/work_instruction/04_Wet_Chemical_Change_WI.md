# Wet Station Chemical 교체 작업 지시서
## SC-1/SC-2 Chemical Bath Management

**문서번호:** WI-WET-CHEM-005  
**효력발생일:** 2024년 12월 1일  
**개정번호:** Rev 1.8  

---

## 1. 문서 정보

### 1.1 승인 정보
| 구분 | 담당자 | 소속 | 직책 | 서명 |
|------|--------|------|------|------|
| 작성 | 최영진 | Wet 공정팀 | 수석 | |
| 검토 | 한소영 | 환경안전팀 | 책임 | |
| 승인 | 김재현 | 제조부문 | 부장 | |

### 1.2 적용 범위
- **장비:** DNS SU-3100 Wet Station
- **작업자:** Certified Chemical Handlers Only
- **빈도:** Bath life 도달 시 (500 wafers or 24hrs)
- **소요시간:** 2시간

---

## 2. 안전 주의사항 ⚠️ 🚨

### 2.1 화학물질 위험성

| Chemical | 위험성 | 증상 | 응급처치 |
|----------|--------|------|----------|
| NH4OH (29%) | 부식성, 독성 | 호흡곤란, 화상 | 신선한 공기, 물 세척 |
| H2O2 (31%) | 산화성, 부식성 | 피부 백화, 화상 | 다량의 물 세척 |
| HF (49%) | 극독성, 부식성 | 지연성 통증 | 칼슘글루콘산 젤 |
| HCl (37%) | 부식성, 자극성 | 즉각적 화상 | 물 15분 세척 |

### 2.2 필수 PPE
- [ ] Chemical suit (Level B)
- [ ] Full face shield
- [ ] Chemical gloves (double)
- [ ] Safety boots
- [ ] SCBA (대량 누출 시)

---

## 3. 사전 준비

### 3.1 준비물 체크리스트
- [ ] 신규 Chemical (검수 완료)
- [ ] Chemical transfer pump
- [ ] Spill kit (완비 상태)
- [ ] pH meter (calibrated)
- [ ] Concentration meter
- [ ] DI water (18.2 MΩ·cm)
- [ ] Waste container (labeled)
- [ ] LOTO lock & tags

### 3.2 사전 확인사항
- [ ] Exhaust ventilation: > 0.5 m/s
- [ ] Emergency shower: 작동 확인
- [ ] Eye wash: 15분 이상 작동
- [ ] Alarm system: Active
- [ ] Buddy system: 2인 1조 확인

---

## 4. 단계별 작업 절차

### 4.1 Step 1: 시스템 정지 및 안전조치 (15분)

**작업 내용:**
1. 진행 중인 Lot 완료
   ```
   [Equipment Console] → [Process] → [Complete Current]
   → Wafer unload 확인
   ```

2. Chemical 공급 차단
   ```
   밸브 차단 순서:
   1) Main chemical supply (V-101)
   2) N2 purge line (V-102)
   3) DI water supply (V-103)
   4) Drain valve 개방 (V-201)
   ```

3. LOTO 실행
   - Main power: Panel A-12
   - Chemical pump: Panel B-03
   - 태그 부착 및 사진 촬영

**⚠️ 주의:** Fume이 완전히 제거될 때까지 3분 대기

### 4.2 Step 2: 기존 Chemical 배출 (30분)

**작업 내용:**
1. Bath level 확인
   ```
   현재 level: _______L
   폐액 예상량: _______L
   ```

2. 폐액 배출
   - Drain valve 천천히 개방 (급격한 개방 금지)
   - 전용 폐액 container로 이송
   - 배출 속도: < 10 L/min
   - pH monitoring: 실시간

3. 잔류 Chemical 제거
   ```
   DI Rinse 절차:
   1차: DI 50L 투입 → 5분 순환 → 배출
   2차: DI 50L 투입 → 5분 순환 → 배출
   3차: DI 30L 투입 → 3분 순환 → 배출
   pH 확인: 6.5-7.5 달성 시까지
   ```

**폐액 라벨링:**
```
내용물: SC-1 폐액
농도: NH4OH/H2O2/H2O
양: _______L
일자: ____/__/__
담당자: _________
```

### 4.3 Step 3: Bath 청소 및 검사 (20분)

**작업 내용:**
1. 내부 검사
   - [ ] 침전물 확인
   - [ ] 부식 상태
   - [ ] Sensor 상태
   - [ ] Overflow weir 청결도

2. 물리적 청소
   ```
   도구: PFA brush only
   세제: DI water only
   
   청소 순서:
   1) 벽면: 상→하 방향
   2) 바닥: 중앙→외곽
   3) Overflow: 막힘 확인
   4) Sensor: 부드럽게 닦기
   ```

3. 최종 Rinse
   - DI water 100L로 채우기
   - 10분 순환
   - 전체 배출
   - 물기 제거 (N2 blow)

### 4.4 Step 4: 신규 Chemical 준비 (15분)

**작업 내용:**
1. Chemical 검수
   ```
   확인 항목:
   □ Certificate of Analysis
   □ Lot number: __________
   □ 유효기간: __________
   □ 포장 상태: __________
   □ 라벨 일치성
   ```

2. 농도 확인
   - NH4OH: 29.0 ± 0.5%
   - H2O2: 31.0 ± 0.5%
   - HCl: 37.0 ± 0.5%
   - 측정 기록: __________

### 4.5 Step 5: Chemical 투입 (30분)

**작업 내용:**
1. SC-1 (APM) 조제
   ```
   표준 비율: NH4OH:H2O2:H2O = 1:1:5
   150L Bath 기준:
   - DI Water: 107L (먼저 투입)
   - NH4OH: 21.5L
   - H2O2: 21.5L
   
   투입 순서: 매우 중요!
   1) DI water 70% 투입
   2) NH4OH 천천히 투입 (발열 주의)
   3) 온도 안정화 대기 (< 30°C)
   4) H2O2 투입
   5) 나머지 DI water로 level 조정
   ```

2. 온도 상승
   ```
   Heating profile:
   Start: 25°C
   Rate: 2°C/min
   Target: 70°C
   Stabilization: 10분
   ```

3. 농도 미세 조정
   - 농도 측정
   - ± 2% 이내 조정
   - 순환 pump ON (10분)

**⚠️ 경고:** NH4OH와 H2O2 직접 혼합 금지 (폭발 위험)

### 4.6 Step 6: 검증 및 안정화 (20분)

**작업 내용:**
1. 파라미터 확인
   ```
   측정 항목:
   □ 농도: _______
   □ 온도: _______°C
   □ pH: _______
   □ 비저항: _______ MΩ·cm
   □ 순환 유량: _______ L/min
   ```

2. Particle 확인
   - Dummy wafer 3매 처리
   - Pre/Post particle count
   - Adder < 10 @ 0.12µm

3. 시스템 정상화
   - Exhaust damper 조정
   - Alarm limit 설정
   - Auto-spike system 활성화

---

## 5. 품질 검증

### 5.1 Chemical 품질 확인

| Parameter | Specification | 측정값 | 판정 |
|-----------|--------------|--------|------|
| NH4OH 농도 | 5.8 ± 0.2% | ____% | □Pass □Fail |
| H2O2 농도 | 5.8 ± 0.2% | ____% | □Pass □Fail |
| 온도 | 70 ± 2°C | ____°C | □Pass □Fail |
| Particle | < 10 adds | ____ | □Pass □Fail |

### 5.2 공정 확인 테스트

**Monitor wafer 처리:**
- Recipe: SC1_STANDARD_10MIN
- Wafer: Bare Si, 3매
- 측정: Particle, metal contamination
- 판정 기준: Baseline ± 10%

---

## 6. 시스템 재가동

### 6.1 재가동 체크리스트
- [ ] 모든 밸브 정상 위치
- [ ] Chemical level sensor 정상
- [ ] 온도 controller 정상
- [ ] Exhaust 정상 작동
- [ ] LOTO 해제
- [ ] MES 상태 변경

### 6.2 Production Release
```
[MES] → [Equipment] → [Chemical Change]
입력 정보:
- Bath type: SC-1
- Old bath life: _______wafers
- New chemical lot: _______
- Qualification: Pass/Fail
- Next change: _______
```

---

## 7. 비상 대응

### 7.1 Chemical 누출 시

**소량 누출 (<1L):**
1. 누출원 차단
2. Spill kit 사용
3. 중화제 살포
4. 흡수 및 폐기

**대량 누출 (>1L):**
1. 대피 경보
2. ERT 호출 (7911)
3. 구역 봉쇄
4. SCBA 착용 후 대응

### 7.2 신체 노출 시

| 노출 부위 | 즉시 조치 | 후속 조치 |
|----------|----------|----------|
| 피부 | 15분 물 세척 | 의무실 |
| 눈 | 15분 세안 | 병원 이송 |
| 흡입 | 신선한 공기 | 산소 공급 |
| HF 노출 | 칼슘글루콘산 | 즉시 병원 |

---

## 8. 폐기물 관리

### 8.1 폐액 처리
- 분류: 지정폐기물 (알칼리성)
- 보관: 지정 탱크 (최대 7일)
- 처리: 전문업체 위탁
- 기록: 폐기물 인계서 작성

### 8.2 오염 물품
- PPE: 지정 폐기물
- Wipes: Chemical waste
- 빈 용기: 3회 세척 후 재활용

---

## 9. 기록 관리

### 9.1 작업 기록서

```
작업 정보:
일자: ____/__/__  시간: __:__ ~ __:__
작업자: _________ / _________
Bath: □SC-1 □SC-2 □DHF

Chemical 정보:
제거량: _______L
투입량: _______L
Lot #: _______
농도: _______

검증 결과:
□ 농도 적합
□ 온도 적합
□ Particle 적합
□ Production 가능

서명: ___________ 일시: __________
```

---

## 10. 참고사항

### 10.1 Chemical 혼합 시 주의사항
- 발열 반응 고려 (천천히 투입)
- 순서 엄수 (물 → 산/염기)
- 환기 상태 확인
- 온도 모니터링

### 10.2 Best Practice
- 2인 1조 작업 원칙
- 충분한 시간 확보
- 급하게 작업 금지
- 의심 시 작업 중단

---

**교육 이수 서명란:**

| 이름 | 사번 | 교육일 | 서명 |
|------|------|--------|------|
| | | | |
| | | | |

**비상 연락처:**
- 환경안전팀: 7911
- 의무실: 7119
- Chemical 누출: 7999

**문서 관리:** Wet 공정팀
**다음 개정:** 2025년 3월
# Lithography Scanner 일일 점검 작업 지시서
## ASML NXT Scanner Daily Qualification

**문서번호:** WI-LITHO-DAILY-003  
**효력발생일:** 2024년 12월 1일  
**개정번호:** Rev 1.5  

---

## 1. 문서 정보

### 1.1 승인 정보
| 구분 | 담당자 | 소속 | 직책 | 서명 |
|------|--------|------|------|------|
| 작성 | 정현수 | Photo 기술팀 | 수석 | |
| 검토 | 김미래 | Photo 생산팀 | 책임 | |
| 승인 | 박정호 | 제조부문 | 상무 | |

### 1.2 적용 범위
- **장비:** ASML NXT:2050i, NXT:2100i
- **작업 대상:** Photo lithography engineers, Operators
- **주기:** 매일 시작 전 (AM 6:00)

---

## 2. 안전 주의사항 ⚠️

### 2.1 레이저 안전
- **위험:** Class 4 레이저 (193nm ArF)
- **PPE:** 레이저 보호 안경 착용 필수
- **주의:** Scanner 내부 작업 시 레이저 차단 확인

### 2.2 화학물질
- **Immersion 용수:** 일반 물이지만 장비 내부는 고온
- **세척 용제:** IPA 사용 시 환기 확인

---

## 3. 작업 준비물

### 3.1 필수 도구
- [ ] Particle monitor wafer (3장)
- [ ] Focus/Dose monitor wafer (1장)
- [ ] Overlay monitor wafer (1장)
- [ ] Lens cleaning kit
- [ ] 작업 체크시트

---

## 4. 단계별 작업 절차

### 4.1 Step 1: 시스템 상태 확인 (5분)

**작업 내용:**
1. MCS (Machine Control System) 로그인
2. System status 확인
   ```
   경로: [Main] → [System] → [Status Overview]
   
   확인 항목:
   □ Overall status: Ready (녹색)
   □ Laser status: Operational
   □ Immersion status: OK
   □ Stage status: Initialized
   □ No active alarms
   ```

3. 전일 로그 확인
   - Error log 검토
   - PM 알림 확인

**💡 Tip:** Red alarm이 있으면 즉시 엔지니어 호출

### 4.2 Step 2: Laser Power 확인 (3분)

**작업 내용:**
1. Laser 메뉴 진입
   ```
   [Laser] → [Performance] → [Power Monitor]
   ```

2. Power 확인
   - **Target:** 40W ± 1W
   - **Actual:** ______W (기록)
   - **Stability:** < 0.3% variation

**이상 시 조치:**
- Power 편차 > 2W: Laser warm-up 30분 추가
- Stability > 0.5%: Service call

### 4.3 Step 3: Baseline Uniformity Test (15분)

**작업 내용:**
1. Monitor wafer load
   ```
   FOUP Port 1에 monitor wafer 장착
   Recipe: BASELINE_DAILY_CHECK
   ```

2. Exposure 실행
   - Focus: 0nm offset
   - Dose: 28 mJ/cm²
   - Field: Full wafer

3. 결과 확인
   - **CD Uniformity:** < 1.5nm (3σ)
   - **Overlay:** < 2.0nm
   
**Check Points:**
- [ ] CD 균일도 spec 내
- [ ] Overlay spec 내
- [ ] No defocus areas

### 4.4 Step 4: Particle Qualification (10분)

**작업 내용:**
1. Particle monitor wafer 준비
2. Pre-scan (KLA SP5)
3. Scanner 통과 (dummy expose)
4. Post-scan
5. Adder 계산

**합격 기준:**
- Particle adders < 5 @ 90nm
- No pattern on wafer map

**💡 Tip:** Particle이 많으면 Reticle library 점검 필요

---

## 5. 기록 및 보고

### 5.1 Daily Check Sheet

```
Date: ____/__/__ Shift: ___ Operator: _______

System Check:
□ Laser Power: ___W (Target: 40W)
□ Uniformity: ___nm (Spec: <1.5nm)
□ Overlay: ___nm (Spec: <2.0nm)  
□ Particles: ___ adds (Spec: <5)

Issues:
_________________________________________

Sign-off: ____________
```

### 5.2 MES 입력
1. [MES] → [Equipment] → [Daily Qual]
2. 모든 측정값 입력
3. Pass/Fail 판정
4. Submit

---

## 6. 비정상 상황 대응

### 6.1 주요 이상 상황

| 상황 | 1차 조치 | 에스컬레이션 |
|------|----------|--------------|
| CD uniformity > 2nm | Lens heating check | Photo engineer |
| Overlay > 3nm | Stage calibration | Immediate |
| Particle > 10 | Reticle inspection | Hold production |
| Laser unstable | 30min warm-up | Vendor call |

---

## 7. 참고사항

### 7.1 Best Practice
- 항상 같은 시간에 점검 (온도 안정화)
- Monitor wafer는 전용 wafer 사용
- 측정 후 즉시 기록 (휘발성 데이터)
- Trend 이상 시 선제적 대응

### 7.2 Common Issues
- 월요일 아침: Extended warm-up 필요
- 습도 변화 시: Overlay drift 주의
- PM 후: Full qualification 필요

---

**교육 이수 서명란:**

| 이름 | 사번 | 교육일 | 서명 |
|------|------|--------|------|
| | | | |
| | | | |

**문서 관리:** Photo 기술팀
**다음 개정:** 2025년 3월
# Ion Implanter Setup 작업 지시서
## Varian VIISta HC Implant Recipe Setup

**문서번호:** WI-IMP-SETUP-006  
**효력발생일:** 2024년 12월 1일  
**개정번호:** Rev 1.4  

---

## 1. 문서 정보

### 1.1 승인 정보
| 구분 | 담당자 | 소속 | 직책 | 서명 |
|------|--------|------|------|------|
| 작성 | 홍길동 | Implant 기술팀 | 수석 | |
| 검토 | 김철수 | 공정개발팀 | 책임 | |
| 승인 | 이영희 | 제조부문 | 부장 | |

### 1.2 적용 범위
- **장비:** Varian VIISta HC High Current Implanter
- **작업자:** Certified Implant Engineers
- **작업 시기:** New recipe setup, Recipe modification
- **소요시간:** 2-3시간 (Recipe complexity 따라)

---

## 2. 안전 주의사항 ⚠️

### 2.1 방사선 위험
- **X-ray 발생:** Beam ON 시 X-ray 차폐 확인
- **Dosimeter:** 필수 착용 및 월별 점검
- **Interlock:** Safety interlock 작동 확인

### 2.2 고전압 위험
- **가속 전압:** Up to 200kV
- **절연:** 절연 장갑 착용
- **접지:** 접지 봉 사용 후 접근

### 2.3 독성 가스
- **Source Gas:** AsH3, PH3, BF3
- **감지기:** Gas monitor 상시 확인
- **대피:** Alarm 시 즉시 대피

---

## 3. 작업 준비

### 3.1 필수 준비물
- [ ] Recipe specification sheet
- [ ] Test wafers (Bare Si, 10매)
- [ ] Thermawave monitor wafers
- [ ] 4-point probe monitor wafers
- [ ] Faraday cup (cleaned)
- [ ] Beam profiler
- [ ] Dosimetry 계산서
- [ ] 작업 허가서

### 3.2 사전 확인
- [ ] Source gas 압력: > 500 psi
- [ ] Cryo pump: < 5E-7 Torr
- [ ] Cooling water: 18-22°C
- [ ] Beam line vacuum: < 1E-6 Torr

---

## 4. Recipe Setup 절차

### 4.1 Step 1: 시스템 준비 (20분)

**작업 내용:**
1. 시스템 상태 확인
   ```
   [Main Console] → [System Status]
   
   확인 항목:
   □ Vacuum: < 5E-7 Torr
   □ Source: Standby mode
   □ Analyzer magnet: Ready
   □ End station: Idle
   □ No active alarms
   ```

2. Source 준비
   ```
   Ion Source 설정:
   - Gas selection: [B, P, As, BF3 중 선택]
   - Arc voltage: 100V (초기값)
   - Arc current: 0.5A (초기값)
   - Source magnet: 850 Gauss
   - Gas flow: 2.0 sccm
   ```

3. Beam line 설정
   - Extraction voltage: 35kV
   - Analyzer magnet 초기화
   - Beam stop: Closed position

**💡 Tip:** Source는 최소 30분 warm-up 필요

### 4.2 Step 2: Beam Generation (30분)

**작업 내용:**
1. Ion source 점화
   ```
   순서:
   1) Gas flow ON
   2) Arc power ON
   3) Arc current 서서히 증가
   4) Plasma 점화 확인
   5) Beam extraction ON
   ```

2. Mass selection
   ```
   Analyzer Magnet 조정:
   - Target mass: _____ amu
   - Magnet current 계산
   - Resolution slit: 적절히 조정
   - Mass scan 실행
   - Peak 중심 확인
   ```

3. Beam current 최적화
   - Target current: _____ mA
   - Source parameter 조정
   - Beam profile 확인
   - Faraday cup 측정

**측정 기록:**
```
Beam current: _______ mA
Mass resolution: _______ 
Beam stability: _______ %
```

### 4.3 Step 3: Energy & Dose 설정 (20분)

**작업 내용:**
1. Implant energy 설정
   ```
   Energy 계산:
   - Required energy: _____ keV
   - Acceleration voltage: _____ kV
   - Deceleration (if needed): _____ kV
   - Post acceleration: _____ kV
   
   설정 확인:
   □ High voltage stable
   □ No sparking
   □ Beam transmission > 80%
   ```

2. Dose 설정
   ```
   Dose 계산:
   - Target dose: _____ ions/cm²
   - Beam current: _____ mA
   - Scan speed 계산
   - Implant time 예상: _____ sec
   ```

3. Scan parameter
   ```
   Beam Scan 설정:
   - X-scan frequency: 500 Hz
   - Y-scan speed: 10 cm/s
   - Overscan: 10%
   - Scan uniformity: < ±1%
   ```

### 4.4 Step 4: Angle 설정 (15분)

**작업 내용:**
1. Wafer tilt 설정
   ```
   Tilt angle: _____ degrees
   (일반적으로 7° for channeling 방지)
   
   Rotation: _____ degrees
   (일반적으로 22° or 45°)
   ```

2. Mechanical 정렬
   - Platen tilt 조정
   - Tilt sensor 확인
   - Rotation motor 테스트
   - Home position 설정

3. 정렬 확인
   - Laser alignment check
   - Mechanical stop 확인
   - Angle 정확도: ± 0.5°

### 4.5 Step 5: Test Run (30분)

**작업 내용:**
1. Monitor wafer 준비
   - Bare Si wafer 3매
   - Wafer ID 기록
   - Pre-measurement (필요시)

2. Test implant 실행
   ```
   Test Recipe 실행:
   1) Load monitor wafer
   2) Recipe 선택
   3) Single wafer run
   4) Dose uniformity 확인
   5) 3매 반복
   ```

3. Dose 측정
   ```
   Thermawave 측정:
   - 49 point mapping
   - Average dose: _____
   - Uniformity: _____ %
   - Repeatability: _____ %
   ```

### 4.6 Step 6: Recipe 최적화 (25분)

**작업 내용:**
1. 측정 결과 분석
   ```
   분석 항목:
   □ Dose accuracy: Target ± 2%
   □ Uniformity: < 1% (1σ)
   □ Repeatability: < 0.5%
   □ Beam stability: < 2%
   ```

2. Parameter 조정
   | Parameter | 문제 | 조정 |
   |-----------|------|------|
   | Low dose | Beam current 부족 | Source 조정 |
   | Poor uniformity | Scan 문제 | Scan speed 조정 |
   | Angle error | Calibration | Mechanical 재조정 |

3. 재검증
   - 조정 후 3매 추가 test
   - 최종 확인
   - Recipe lock

---

## 5. Recipe 등록 및 검증

### 5.1 Recipe 저장

```
Recipe 정보:
Recipe Name: _________________
Ion Species: _________________
Energy: _________ keV
Dose: _________ ions/cm²
Tilt/Rotation: _____°/_____°
Beam Current: _________ mA
Process Time: _________ sec

Save Location: [Recipe Library] → [Production]
```

### 5.2 품질 검증

| 항목 | Specification | 측정값 | 판정 |
|------|--------------|--------|------|
| Dose accuracy | ± 2% | _____% | □Pass □Fail |
| Uniformity | < 1% | _____% | □Pass □Fail |
| Repeatability | < 0.5% | _____% | □Pass □Fail |
| Angle accuracy | ± 0.5° | _____° | □Pass □Fail |

---

## 6. 문서화

### 6.1 Recipe Card 작성

```
Recipe Card
====================
Recipe ID: IMP_________
Date: ____/__/__
Engineer: __________

Process Parameters:
- Ion: _____
- Energy: _____ keV
- Dose: _____ e/cm²
- Tilt: _____°
- Rotation: _____°

Machine Parameters:
- Source Arc V: _____ V
- Source Arc I: _____ A
- Extraction: _____ kV
- Beam Current: _____ mA
- Scan Speed: _____ Hz

Validation:
- Test wafers: _____ ea
- Dose uniformity: _____% 
- Cpk: _____

Approved by: __________
Date: ____/__/__
```

### 6.2 MES 등록

```
[MES] → [Recipe Management] → [New Recipe]

입력 정보:
- Recipe name
- Process parameters
- Qualification data
- Release status
- Authorized products
```

---

## 7. Beam 종료 절차

### 7.1 Beam Off 순서
1. Recipe 실행 중단
2. Beam stop 닫기
3. Extraction voltage OFF
4. Arc discharge OFF
5. Gas flow OFF
6. Source cool down (30분)

### 7.2 시스템 대기 모드
- Vacuum 유지
- Cryo pump 계속 작동
- Cooling water 유지
- Log 저장

---

## 8. 이상 상황 대응

### 8.1 Beam 이상

| 증상 | 원인 | 조치 |
|------|------|------|
| Beam 불안정 | Source 수명 | Source 교체 |
| Low current | Gas 부족 | Gas 압력 확인 |
| Arc 꺼짐 | Filament 단선 | Filament 교체 |
| Mass drift | 자석 온도 | Cooling 확인 |

### 8.2 Dose 이상

| 문제 | 확인사항 | 해결방법 |
|------|----------|----------|
| Over dose | Faraday cup | Calibration |
| Under dose | Beam loss | Beam line 정렬 |
| Non-uniform | Scan 문제 | Scan parameter |

---

## 9. 정기 점검 항목

### 9.1 일일 점검
- [ ] Vacuum level
- [ ] Gas pressure
- [ ] Cooling water
- [ ] Dosimeter reading

### 9.2 주간 점검
- [ ] Faraday cup clean
- [ ] Source life check
- [ ] Beam profiler cal
- [ ] Recipe backup

---

**교육 이수 서명란:**

| 이름 | 사번 | 교육일 | 서명 |
|------|------|--------|------|
| | | | |
| | | | |

**문서 관리:** Implant 기술팀
**다음 개정:** 2025년 3월
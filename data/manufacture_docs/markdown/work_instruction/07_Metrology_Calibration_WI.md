# 계측장비 Calibration 작업 지시서
## KLA-Tencor & Applied Materials Metrology Tools

**문서번호:** WI-METRO-CAL-008  
**효력발생일:** 2024년 12월 1일  
**개정번호:** Rev 1.9  

---

## 1. 문서 정보

### 1.1 승인 정보
| 구분 | 담당자 | 소속 | 직책 | 서명 |
|------|--------|------|------|------|
| 작성 | 신재호 | 계측기술팀 | 수석 | |
| 검토 | 윤서현 | 품질보증팀 | 책임 | |
| 승인 | 장민철 | 제조부문 | 부장 | |

### 1.2 적용 범위
- **장비:** CD-SEM, Overlay, Ellipsometer, Thickness gauge
- **작업자:** Certified Metrology Engineers
- **주기:** Monthly, Quarterly (장비별 상이)
- **소요시간:** 2-4시간 per tool

---

## 2. 안전 주의사항 ⚠️

### 2.1 전자빔 장비 (CD-SEM)
- **고전압:** 최대 30kV
- **X-ray:** 차폐 확인
- **진공:** Chamber 압력 확인

### 2.2 광학계 장비
- **레이저:** Class 3B (보호안경)
- **UV lamp:** 직접 노출 금지
- **고온 램프:** 화상 주의

---

## 3. Calibration 준비

### 3.1 표준 시편 (Standard Samples)
- [ ] NIST traceable standards
- [ ] CD standard (Pitch: 90nm)
- [ ] Overlay standard (Box-in-box)
- [ ] Thickness standard (SiO2 1000Å)
- [ ] Particle size standard
- [ ] Roughness standard

### 3.2 필수 도구
- [ ] Standard holder
- [ ] Cleaning kit
- [ ] Calibration software
- [ ] Certificate binder
- [ ] Environmental monitor
- [ ] Calibration labels

---

## 4. CD-SEM Calibration

### 4.1 Step 1: 시스템 준비 (20분)

**작업 내용:**
1. 환경 조건 확인
   ```
   요구 사항:
   - Temperature: 21 ± 0.5°C
   - Humidity: 45 ± 5% RH
   - Vibration: < 1µm
   - EMI: Background level
   
   측정값 기록:
   Temp: _____°C
   RH: _____%
   Vibration: _____µm
   ```

2. 시스템 상태 점검
   ```
   [System] → [Diagnostics]
   
   확인 항목:
   □ Vacuum: < 5E-6 Torr
   □ Column alignment: OK
   □ Detector gain: Normal
   □ Stage repeatability: < 100nm
   ```

3. Warm-up
   - Electron gun: 30분
   - Stage motors: 10분
   - Detector stabilization

### 4.2 Step 2: Magnification Calibration (30분)

**작업 내용:**
1. Standard 로딩
   ```
   Standard 정보:
   Type: Pitch standard
   Pitch: 100.0 ± 0.5nm
   Certificate #: __________
   Expiry: __________
   ```

2. Image acquisition
   ```
   설정:
   - Mag: 100,000x
   - Voltage: 500V
   - Current: 10pA
   - Working distance: 3mm
   - Frame average: 16
   ```

3. Calibration 실행
   ```
   측정 순서:
   1) Auto focus
   2) Auto stigmation
   3) Capture 10 images
   4) Measure pitch (10 locations)
   5) Calculate average
   
   결과:
   Measured: _____ nm
   Expected: 100.0 nm
   Error: _____ %
   ```

4. Correction factor 입력
   ```
   [Calibration] → [Mag Correction]
   Factor: _____
   Apply to all magnifications: Yes
   Save calibration file
   ```

### 4.3 Step 3: Linearity Check (20분)

**작업 내용:**
1. Multi-point 측정
   ```
   Magnification test:
   - 50,000x: _____ nm
   - 100,000x: _____ nm
   - 150,000x: _____ nm
   - 200,000x: _____ nm
   ```

2. Linearity 계산
   - R² > 0.9999 확인
   - Deviation < 0.5%

---

## 5. Overlay Tool Calibration

### 5.1 Step 1: TIS Calibration (30분)

**작업 내용:**
1. TIS (Tool Induced Shift) 제거
   ```
   Standard: Box-in-box overlay mark
   
   측정 순서:
   1) 0° orientation 측정
   2) 180° rotation 측정
   3) TIS = (M0 - M180)/2
   4) System correction 입력
   ```

2. TIS 값 기록
   ```
   X-direction TIS: _____ nm
   Y-direction TIS: _____ nm
   Spec: < 0.5nm
   ```

### 5.2 Step 2: Accuracy Verification (25분)

**작업 내용:**
1. Known overlay standard 측정
   ```
   Programmed offsets:
   0, +5, +10, -5, -10 nm
   
   각 offset 5회 측정
   평균 및 표준편차 계산
   ```

2. Correlation 확인
   - Slope: 1.00 ± 0.02
   - R²: > 0.999
   - Offset: < 0.3nm

---

## 6. Ellipsometer Calibration

### 6.1 Step 1: Optical Alignment (20분)

**작업 내용:**
1. Beam alignment
   ```
   절차:
   1) Bare Si wafer 로드
   2) Auto alignment 실행
   3) Signal intensity 최대화
   4) Polarizer angle 조정
   5) Analyzer angle 조정
   ```

2. Baseline 설정
   ```
   Reference 측정:
   - Bare Si: n=3.882, k=0.019 @ 633nm
   - SiO2: n=1.462 @ 633nm
   ```

### 6.2 Step 2: Thickness Standard (25분)

**작업 내용:**
1. Standard 측정
   ```
   Standard wafer:
   - SiO2/Si: 1000 ± 5Å
   - Certificate: __________
   
   49 point mapping
   Average: _____ Å
   Uniformity: _____ %
   ```

2. Model fitting
   - MSE < 5 확인
   - Correlation > 0.999

---

## 7. 공통 Calibration 절차

### 7.1 Golden Wafer Verification

**작업 내용:**
1. Golden wafer 측정
   ```
   각 tool별 golden wafer:
   - CD-SEM: Line width standard
   - Overlay: Programmed shift wafer
   - Thickness: Multi-layer standard
   
   측정 주기: Daily (production 전)
   ```

2. Trend monitoring
   ```
   Control chart 관리:
   - Center line: Target
   - UCL/LCL: ± 3σ
   - Action limit: ± 2σ
   ```

### 7.2 Cross-Tool Matching

| Tool Type | Tool A | Tool B | Difference | Spec |
|-----------|--------|--------|------------|------|
| CD-SEM #1 | ___nm | ___nm | ___nm | <1nm |
| CD-SEM #2 | ___nm | ___nm | ___nm | <1nm |
| Overlay #1 | ___nm | ___nm | ___nm | <0.5nm |

---

## 8. Data Management

### 8.1 Calibration Record

```
Calibration Certificate
========================
Tool ID: __________
Date: ____/__/__
Engineer: __________

Calibration Type:
□ Monthly □ Quarterly □ Annual

Standards Used:
1. __________ (Cert #______)
2. __________ (Cert #______)

Results:
Parameter | Before | After | Spec
---------|---------|-------|------
Accuracy | ______ | _____ | _____
Precision| ______ | _____ | _____
Linearity| ______ | _____ | _____

Status: □ Pass □ Fail

Next Cal Due: ____/__/__

Signature: __________
```

### 8.2 System Update

```
[MES] → [Metrology] → [Calibration Record]

입력 항목:
- Cal date
- Cal type
- Results summary
- Certificate upload
- Next due date
```

---

## 9. 이상 시 대응

### 9.1 Calibration 실패

| 문제 | 원인 | 조치 |
|------|------|------|
| Drift 과다 | Component 노화 | Service call |
| 재현성 불량 | Stage 문제 | Stage cal |
| Accuracy 벗어남 | Standard 오염 | Standard 교체 |

### 9.2 교정 한계 초과

**조치 순서:**
1. Tool 사용 중지
2. MES hold
3. Engineer 호출
4. Root cause 분석
5. 수리 후 재교정

---

## 10. 표준 시편 관리

### 10.1 보관 조건

| Standard Type | 보관 조건 | 유효기간 |
|--------------|-----------|----------|
| CD standard | N2 purge box | 2 years |
| Overlay | Desiccator | 2 years |
| Thickness | Clean box | 3 years |
| Particle | Sealed | 1 year |

### 10.2 취급 주의사항
- 맨손 접촉 금지
- Edge handling only
- 사용 전/후 inspection
- 사용 이력 기록

---

## 11. Calibration 주기

### 11.1 정기 교정 일정

| Equipment | Daily | Weekly | Monthly | Quarterly |
|-----------|-------|--------|---------|-----------|
| CD-SEM | Golden | - | Full cal | Cross-tool |
| Overlay | Golden | TIS | Full cal | Accuracy |
| Ellipsometer | - | Baseline | Full cal | Standard |
| AFM | - | Scanner | Tip cal | Full cal |

---

**교육 이수 서명란:**

| 이름 | 사번 | 교육일 | 서명 |
|------|------|--------|------|
| | | | |
| | | | |

**문서 관리:** 계측기술팀
**다음 개정:** 2025년 3월
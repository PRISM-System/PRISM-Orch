# Furnace Tube Cleaning 작업 지시서
## Vertical/Horizontal Oxidation & LPCVD Furnace

**문서번호:** WI-FURN-CLEAN-010  
**효력발생일:** 2024년 12월 1일  
**개정번호:** Rev 1.6  

---

## 1. 문서 정보

### 1.1 승인 정보
| 구분 | 담당자 | 소속 | 직책 | 서명 |
|------|--------|------|------|------|
| 작성 | 정수민 | Diffusion팀 | 수석 | |
| 검토 | 강태윤 | 공정기술팀 | 책임 | |
| 승인 | 오정훈 | 제조부문 | 부장 | |

### 1.2 적용 범위
- **장비:** TEL Vertex, Hitachi Kokusai Furnace
- **Tube 종류:** Quartz, SiC tube
- **작업 주기:** 3000 runs 또는 분기별
- **소요시간:** 12시간 (Full clean)

---

## 2. 안전 주의사항 ⚠️

### 2.1 고온 위험
- **Tube 온도:** 최대 1200°C
- **Cool down:** 최소 8시간 필요
- **Thermal shock:** 급냉 금지

### 2.2 화학물질 위험
- **HF vapor:** Quartz etching용
- **HCl gas:** Metal 제거
- **H2 gas:** 폭발 위험

### 2.3 물리적 위험
- **Tube 무게:** ~50kg (Quartz)
- **파손 위험:** 2-3인 작업 필수
- **날카로운 모서리:** 보호장구 착용

---

## 3. 작업 준비

### 3.1 필수 장비 및 자재
- [ ] Tube pulling tool set
- [ ] Tube support cradle
- [ ] HF resistant container
- [ ] Buffered HF solution
- [ ] DI water circulation system
- [ ] Temperature gun
- [ ] Borescope camera
- [ ] Particle counter
- [ ] Clean room crane (필요시)

### 3.2 PPE
- [ ] Chemical suit
- [ ] Full face respirator
- [ ] HF resistant gloves
- [ ] Safety boots
- [ ] Hard hat (tube handling)

---

## 4. Tube Cleaning 절차

### 4.1 Step 1: Furnace Shutdown (60분)

**작업 내용:**
1. Process 종료
   ```
   종료 순서:
   1) Current lot 완료
   2) Process gas OFF
   3) Temperature ramp down
      - Rate: 5°C/min
      - Target: < 100°C
   4) N2 purge 유지: 10 slm
   ```

2. 온도 profile 확인
   ```
   Zone 온도 기록:
   Zone 1 (Load): _____°C
   Zone 2 (Center): _____°C
   Zone 3 (Source): _____°C
   Zone 4 (Dump): _____°C
   Zone 5 (Unload): _____°C
   ```

3. System isolation
   ```
   차단 밸브:
   □ Process gas (SiH4, NH3, etc.)
   □ Cleaning gas (HCl, HF)
   □ Exhaust throttle valve
   □ Cooling water
   ```

4. LOTO 실행
   - Main power: Panel F-01
   - Heater power: Panel H-01
   - Gas panel: Panel G-01

### 4.2 Step 2: In-situ Cleaning (120분)

**작업 내용:**
1. HCl Clean (Metal removal)
   ```
   Recipe: TUBE_HCL_CLEAN
   
   Parameters:
   - Temperature: 800°C
   - HCl flow: 500 sccm
   - N2 dilution: 5 slm
   - Time: 60 minutes
   - Pressure: 760 Torr
   ```

2. 효과 monitoring
   ```
   End point detection:
   - Metal chloride 색상 변화
   - Exhaust gas 분석
   - Visual inspection (viewport)
   ```

3. N2 Purge
   ```
   Purge cycle:
   - N2 flow: 20 slm
   - Time: 30 minutes
   - Cycle: 3회 반복
   - Residual HCl < 1 ppm
   ```

### 4.3 Step 3: Tube Removal (90분)

**작업 내용:**
1. Furnace 개방
   ```
   개방 준비:
   □ 온도 < 50°C 확인
   □ Support structure 준비
   □ Tube cradle 위치
   □ 3인 작업팀 구성
   ```

2. Tube 연결 해제
   ```
   분리 순서:
   1) End cap bolts (좌/우)
   2) Gas inlet fitting
   3) Thermocouple 분리
   4) O-ring seal 확인
   ```

3. Tube 인출
   ```
   인출 작업:
   1) Tube puller 부착
   2) 수평 유지하며 인출
   3) 1m당 2분 소요
   4) Cradle에 안착
   
   주의: 충격/굽힘 금지
   ```

**기록:**
```
Tube Serial #: __________
사용 시간: __________ hrs
Deposit 두께: __________ µm
```

### 4.4 Step 4: External Cleaning (180분)

**작업 내용:**
1. 육안 검사
   ```
   검사 항목:
   □ Crack (균열)
   □ Devitrification (실투)
   □ Deposit pattern
   □ Hot spot 흔적
   
   사진 촬영 위치:
   - Inlet/Outlet
   - Center zone
   - Deposit 영역
   - 이상 부위
   ```

2. Chemical cleaning
   ```
   HF Dip Process:
   
   준비:
   - 5:1 Buffered HF
   - Temperature: 23°C
   - Container: PP/PTFE
   
   절차:
   1) Tube를 용액에 담그기
   2) Circulation pump ON
   3) Etching time: 60 min
   4) Etch rate: ~1000Å/min
   
   안전: Fume hood 내 작업
   ```

3. Rinse & Dry
   ```
   DI Rinse:
   1) Overflow rinse: 30 min
   2) Resistivity > 15 MΩ·cm
   3) Final rinse: 10 min
   
   건조:
   - N2 blow: Inside/Outside
   - Hot air: 80°C, 60 min
   - Particle check
   ```

### 4.5 Step 5: Tube Inspection (30분)

**작업 내용:**
1. Dimension 측정
   ```
   측정 위치 (5 points):
   - Inlet: OD _____ mm
   - 1/4: OD _____ mm
   - Center: OD _____ mm
   - 3/4: OD _____ mm
   - Outlet: OD _____ mm
   
   Spec: 200 ± 0.5 mm
   ```

2. Surface quality
   ```
   Inspection:
   □ Roughness < 1µm
   □ No crack
   □ No bubble
   □ Transparency OK
   ```

3. Particle test
   ```
   Particle 측정:
   - Method: Liquid particle counter
   - Size: > 0.2µm
   - Count: < 100 particles/ml
   ```

### 4.6 Step 6: Tube 재설치 (90분)

**작업 내용:**
1. Tube 정렬
   ```
   설치 준비:
   1) O-ring 신품 교체
   2) Flange 면 청소
   3) 정렬 가이드 설치
   ```

2. Tube 삽입
   ```
   삽입 작업:
   1) 3인 동시 작업
   2) 수평 유지
   3) 천천히 삽입 (1m/2min)
   4) 최종 위치 확인
   ```

3. 연결 복구
   ```
   체결 순서:
   □ End flange (torque: 20 N·m)
   □ Gas line (leak check)
   □ TC 재연결
   □ Heater element 확인
   ```

### 4.7 Step 7: Leak Test (45분)

**작업 내용:**
1. Vacuum test
   ```
   Test 조건:
   - Pump down to 10 mTorr
   - Isolation valve 닫기
   - 10분 대기
   - Pressure rise < 10 mTorr/min
   ```

2. He leak test
   ```
   절차:
   1) RGA mass 4 monitoring
   2) He spray 각 연결부
   3) Leak rate < 1E-9 torr·L/s
   ```

---

## 5. System 재가동

### 5.1 Bake-out Process (240분)

```
Temperature Ramp:
1) 25°C → 400°C @ 2°C/min
2) Hold 400°C for 60 min (N2)
3) 400°C → 800°C @ 3°C/min
4) Hold 800°C for 120 min
5) Cool to standby temp
```

### 5.2 Seasoning (120분)

```
Season Recipe:
- 10 dummy wafers
- Standard oxide process
- Thickness target: 1000Å
- Uniformity check
```

---

## 6. 품질 확인

### 6.1 Performance Test

| Parameter | Specification | Result | Pass/Fail |
|-----------|--------------|---------|-----------|
| Base pressure | < 10 mTorr | ___mTorr | |
| Leak rate | < 1E-9 | _____ | |
| Temp uniformity | ± 2°C | _____°C | |
| Particle | < 10 adds | _____ | |

### 6.2 Process Verification

**Monitor Run:**
- Recipe: Standard thermal oxide
- Target: 500Å
- Uniformity: < 2%
- Particles: < 5 adds

---

## 7. Tube Life Management

### 7.1 사용 이력 기록

```
Tube History Card
==================
Tube ID: __________
Install date: ____/__/__
Total runs: __________
Total RF hours: __________

Cleaning History:
Date | Type | Thickness Removed
_____|______|_________________
_____|______|_________________

Next clean due: __________
Expected EOL: __________
```

### 7.2 교체 기준

| Indicator | Limit | Action |
|-----------|-------|--------|
| Wall thickness | < 3mm | Replace |
| Devitrification | > 20% area | Replace |
| Crack | Any size | Replace immediately |
| Cleaning cycles | > 20 | Consider replacement |

---

## 8. 이상 상황 대응

### 8.1 Tube 손상

| 손상 유형 | 원인 | 조치 |
|----------|------|------|
| Crack | Thermal shock | 즉시 교체 |
| Devitrification | High temp cycling | 수명 평가 |
| Erosion | Over-etching | 두께 측정 |
| Deposit | Incomplete clean | 재세척 |

### 8.2 공정 이상

| 문제 | 원인 | 해결 |
|------|------|------|
| 불균일 | Tube 오염 | 재세척 |
| Particle | Flaking | Seasoning 추가 |
| 느린 성장 | Tube 노화 | 온도 보정 |

---

## 9. 폐기물 처리

### 9.1 Chemical 폐기물
- HF 폐액: 중화 후 처리
- Rinse water: pH 확인 후 배출
- Contaminated items: 지정 폐기물

### 9.2 Tube 폐기
- 파손 tube: 안전 포장
- 수명 완료: 재활용 업체
- 기록: 폐기 사유 문서화

---

**교육 이수 서명란:**

| 이름 | 사번 | 교육일 | 서명 |
|------|------|--------|------|
| | | | |
| | | | |

**문서 관리:** Diffusion팀
**다음 개정:** 2025년 3월
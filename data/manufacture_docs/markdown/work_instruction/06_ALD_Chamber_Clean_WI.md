# ALD Chamber Clean 작업 지시서
## ASM Polygon Chamber Preventive Maintenance

**문서번호:** WI-ALD-CLEAN-007  
**효력발생일:** 2024년 12월 1일  
**개정번호:** Rev 2.3  

---

## 1. 문서 정보

### 1.1 승인 정보
| 구분 | 담당자 | 소속 | 직책 | 서명 |
|------|--------|------|------|------|
| 작성 | 강민수 | Thin Film팀 | 수석 | |
| 검토 | 조은경 | 장비기술팀 | 책임 | |
| 승인 | 박상민 | 제조부문 | 부장 | |

### 1.2 적용 범위
- **장비:** ASM Polygon 8300 ALD System
- **작업자:** Certified ALD Engineers
- **주기:** 5000 wafers 또는 200 hours
- **소요시간:** 8시간 (Full PM)

---

## 2. 안전 주의사항 ⚠️

### 2.1 화학물질 위험
- **Precursor 잔류물:** HfCl4, TiCl4 (부식성)
- **부산물:** HCl gas (독성)
- **세척제:** NF3 remote plasma (독성)

### 2.2 고온 위험
- **Chamber 온도:** 최대 350°C
- **Cool down:** 최소 2시간 필요
- **화상 주의:** 단열 장갑 필수

### 2.3 진공 위험
- **Implosion risk:** Chamber 개방 시 주의
- **압력 확인:** 대기압 도달 후 개방

---

## 3. 작업 준비

### 3.1 필수 장비 및 도구
- [ ] Chamber cleaning kit
- [ ] O-ring set (신품)
- [ ] Torque wrench set
- [ ] Particle counter
- [ ] Borescope camera
- [ ] IPA, DI water
- [ ] Lint-free wipes
- [ ] N2 gun
- [ ] Vacuum gauge

### 3.2 PPE
- [ ] Cleanroom suit (Class 10)
- [ ] Double nitrile gloves
- [ ] Safety goggles
- [ ] Heat resistant gloves
- [ ] Face mask (particle)

---

## 4. Chamber Clean 절차

### 4.1 Step 1: 시스템 Shutdown (30분)

**작업 내용:**
1. 진행 중 Lot 완료
   ```
   [System Controller] → [Process] → [Abort After Current]
   Wafer 반출 확인
   ```

2. Chamber cool down
   ```
   Cool Down Sequence:
   1) Heater OFF
   2) N2 purge: 50 slm
   3) Target temp: < 50°C
   4) 예상 시간: 120분
   
   온도 확인:
   - Chuck: _____°C
   - Wall: _____°C
   - Lid: _____°C
   ```

3. Precursor 차단
   ```
   Valve 차단 순서:
   V-301: HfCl4 source
   V-302: TiCl4 source
   V-303: H2O source
   V-304: O3 generator
   V-401: Purge N2
   ```

4. LOTO 실행
   - Main breaker: Panel M-01
   - RF generator: Panel R-01
   - 태그 번호: _________

### 4.2 Step 2: Remote Plasma Clean (45분)

**작업 내용:**
1. NF3 Remote clean 준비
   ```
   Setup:
   - NF3 flow: 500 sccm
   - O2 flow: 1000 sccm
   - Pressure: 2 Torr
   - RF power: 2000W
   - Temperature: 250°C
   ```

2. Plasma clean 실행
   ```
   Recipe: REMOTE_CLEAN_01
   
   Step 1: Pre-heat (10 min)
   Step 2: NF3 plasma (20 min)
   Step 3: O2 plasma (10 min)
   Step 4: N2 purge (5 min)
   
   End point: Optical emission
   ```

3. 효과 확인
   - Particle count: Pre vs Post
   - Visual inspection (viewport)
   - Pressure rise test

**기록:**
```
Pre-clean particles: _____ @ 0.1µm
Post-clean particles: _____ @ 0.1µm
Removal efficiency: _____%
```

### 4.3 Step 3: Chamber Venting (20분)

**작업 내용:**
1. 진공 해제
   ```
   Venting 순서:
   1) Throttle valve 닫기
   2) Pump isolation valve 닫기
   3) N2 vent valve 천천히 개방
   4) Vent rate: < 100 Torr/min
   5) 대기압 도달 확인
   ```

2. Chamber 개방 준비
   - 압력 확인: 760 ± 5 Torr
   - N2 purge 유지: 10 slm
   - 안전 장구 착용 확인

### 4.4 Step 4: Chamber 개방 및 검사 (60분)

**작업 내용:**
1. Lid 개방
   ```
   볼트 해제 순서:
   대각선 패턴 (1-3-2-4)
   Torque: 단계적 감소
   
   주의사항:
   - O-ring 손상 확인
   - Lid lift 장비 사용
   - 2인 작업 필수
   ```

2. 내부 검사
   ```
   검사 항목:
   □ Showerhead: 막힘, 부식
   □ Chamber wall: Coating 상태
   □ Susceptor: 표면 상태
   □ Gas inlet: 막힘 여부
   □ Viewport: 투명도
   
   사진 촬영 위치:
   - 전체 view
   - Showerhead 근접
   - Susceptor 표면
   - 이상 부위
   ```

3. 부품 상태 평가
   | 부품 | 상태 | 조치 |
   |------|------|------|
   | Showerhead | □양호 □불량 | |
   | O-ring | □양호 □교체 | |
   | Susceptor | □양호 □연마 | |
   | Liner | □양호 □교체 | |

### 4.5 Step 5: 물리적 세척 (90분)

**작업 내용:**
1. Showerhead 세척
   ```
   세척 절차:
   1) 분리 (주의: 무게 10kg)
   2) IPA 70% 용액 세척
   3) DI water rinse
   4) Ultrasonic bath (선택)
   5) N2 blow dry
   6) Particle 검사
   ```

2. Chamber wall 세척
   ```
   작업 순서:
   1) Loose particle 제거 (진공청소기)
   2) IPA wipe (위→아래)
   3) DI water wipe
   4) Dry wipe
   5) N2 blow
   
   금지사항:
   - 거친 브러시 사용
   - 강한 용제 사용
   - 과도한 힘
   ```

3. Susceptor 처리
   - 표면 검사 (microscope)
   - 필요시 polishing
   - Cleaning: IPA → DI → N2
   - Flatness 확인: < 10µm

### 4.6 Step 6: 부품 교체 (45분)

**작업 내용:**
1. O-ring 교체
   ```
   교체 절차:
   1) 기존 O-ring 제거
   2) Groove 청소
   3) 신규 O-ring 검사
   4) Light coating (vacuum grease)
   5) 설치 (비틀림 주의)
   6) 균일한 압착 확인
   ```

2. 소모품 교체 리스트
   - [ ] Door O-ring
   - [ ] Showerhead O-ring
   - [ ] Viewport O-ring
   - [ ] Exhaust baffle
   - [ ] Temperature sensor

3. 교체 부품 기록
   ```
   부품명: __________
   P/N: __________
   S/N: __________
   교체일: __________
   다음 교체: __________
   ```

### 4.7 Step 7: Chamber 조립 (40분)

**작업 내용:**
1. Showerhead 설치
   - 정렬 핀 확인
   - 균등한 간격 유지
   - Torque spec: 15 N·m

2. Lid 체결
   ```
   체결 순서:
   1) Lid 정렬
   2) 볼트 hand tight
   3) 1차: 5 N·m (대각선)
   4) 2차: 10 N·m
   5) 최종: 15 N·m
   ```

3. 연결부 확인
   - [ ] Gas line 연결
   - [ ] Sensor cable
   - [ ] Heater power
   - [ ] Thermocouple

### 4.8 Step 8: Leak Check (30분)

**작업 내용:**
1. 진공 배기
   ```
   Pump down:
   - Initial: Roughing pump
   - < 100 mTorr: Turbo ON
   - Target: < 1E-6 Torr
   - Time limit: 30분
   ```

2. Leak rate 측정
   ```
   RGA Leak Test:
   - Base pressure: _____ Torr
   - Valve 모두 닫기
   - 10분 대기
   - Pressure rise: _____ Torr/min
   - Spec: < 1E-9 Torr·L/s
   ```

3. He leak check (필요시)
   - He spray 각 연결부
   - RGA mass 4 monitoring
   - Leak location 기록

---

## 5. Chamber Conditioning

### 5.1 Bake Out (60분)

```
Temperature Ramp:
1) 25°C → 150°C @ 5°C/min
2) Hold 150°C for 20 min
3) 150°C → 300°C @ 3°C/min
4) Hold 300°C for 30 min
5) Cool to process temp
```

### 5.2 Season Process (30분)

```
Season Recipe:
- 10 cycles: HfO2 deposition
- 10 cycles: Al2O3 deposition
- Chamber wall coating
- Particle stabilization
```

---

## 6. Qualification

### 6.1 Particle Test

| Test | Spec | Result | Pass/Fail |
|------|------|--------|-----------|
| Pre-count | Baseline | _____ | |
| Post-count | < 10 adds | _____ | |
| Size | @ 0.1µm | _____ | |

### 6.2 Process Test

**Monitor Wafer Run:**
- Recipe: Standard HfO2
- Wafers: 3 매
- Thickness uniformity: < 1%
- Particle adders: < 5

---

## 7. 시스템 재가동

### 7.1 재가동 체크리스트
- [ ] 모든 연결 확인
- [ ] Leak test pass
- [ ] Temperature stable
- [ ] Pressure stable
- [ ] LOTO 해제
- [ ] Alarm clear

### 7.2 Production Release

```
[MES] → [PM Complete]
입력 정보:
- PM type: Full clean
- Parts replaced: _____
- Particle qual: Pass
- Next PM: _____ wafers
```

---

## 8. 이상 상황 대응

### 8.1 누출 발생

| 위치 | 증상 | 조치 |
|------|------|------|
| Door seal | Pressure 상승 | O-ring 재설치 |
| Gas fitting | He 검출 | Fitting 조임 |
| Viewport | 육안 확인 | Seal 교체 |

### 8.2 Particle 과다

| 원인 | 확인 | 해결 |
|------|------|------|
| 불완전 세척 | Visual | 재세척 |
| 부품 손상 | Inspection | 부품 교체 |
| Season 부족 | Test | 추가 season |

---

## 9. 문서 기록

### 9.1 PM Check Sheet

```
PM 정보:
Date: ____/__/__
Engineer: __________
Start: __:__ End: __:__

청소 결과:
□ Remote clean 완료
□ Manual clean 완료
□ 부품 교체 완료

측정 데이터:
Base pressure: _____ Torr
Leak rate: _____ Torr·L/s
Particles: _____ adds

특이사항:
_________________________

Sign: _________ Date: _____
```

---

**교육 이수 서명란:**

| 이름 | 사번 | 교육일 | 서명 |
|------|------|--------|------|
| | | | |
| | | | |

**문서 관리:** Thin Film팀
**다음 개정:** 2025년 3월
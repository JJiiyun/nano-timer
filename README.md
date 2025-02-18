# Nano-Timer

---

## 소개 (Introduction)
`Nano-Timer`는 Analog Discovery2를 이용해 전압 측정, 임피던스(Real/Imag/Abs) 계산 등을 수행하는 소프트웨어입니다.
최근에는 VM(Ubuntu) 환경으로 배포되어 손쉽게 환경 설정이 가능합니다.

---

## 최근 수정 내역 (Recent Changes)
- **Graph X-axis, Y-axis 이름 변경**  
  그래프 축 이름을 직관적으로 바꿔, 데이터 이해를 더 쉽게 했습니다.
- **임피던스(Real/Imag/Abs) 50ms 간격으로 파일에 기록**  
  보다 세밀한 시점에서 임피던스 데이터를 확인할 수 있도록 개선했습니다.
- **Loop, Period 변수를 Duration(min)으로 변경**  
  측정 주기를 분 단위로 입력할 수 있도록 하여, 긴 측정에도 대응합니다.
- **CSV 파일에 Max/Min/Avg 전압 컬럼 추가**  
  전압의 최대값, 최소값, 평균값을 자동으로 저장하여 통계적 분석이 편리해졌습니다.
- **Distribute Virtual Machine(Ubuntu). Bio-IT 나스에 배포**  
  개발 환경 구성이 번거로운 경우를 위해 **VM 이미지를 배포**했습니다.

---

<img src="https://github.com/user-attachments/assets/ae73d318-27c7-4817-bf14-98a6e6364408" width="55%" height="55%" alt="Before Run Nano-Timer">
<img src="https://github.com/user-attachments/assets/4e27040e-f828-4b94-bb64-9b07e5ff02b8" width="55%" height="55%" alt="After Run Nano-Timer">


> **그림 1.** Nano-Timer가 동작하는 모습 (예시)

---

### GUI 화면
아래 이미지는 Nano-Timer의 GUI(그래프, 설정창 등)를 보여줍니다.  
- 실시간 그래프를 통해 데이터 변화를 즉시 확인 가능  
- 전압, 임피던스 등 측정값이 함께 표시되어 작업 효율 향상

<img src="https://github.com/user-attachments/assets/2d7a138b-e532-47b7-ad63-eb075e0a862f" width="55%" height="55%" alt="Nano-Timer GUI Screenshot">

> **그림 2.** Nano-Timer GUI 예시

---

## CSV 파일 형식
Nano-Timer는 측정 결과를 `.csv` 파일로 저장합니다. 컬럼 구성은 다음과 같습니다.

| 컬럼명              | 설명                                     |
|---------------------|------------------------------------------|
| Time(sec)           | 측정 시점 (초 단위)                      |
| real                | 임피던스의 실수 성분                      |
| imag                | 임피던스의 허수 성분                      |
| abs                 | 임피던스의 크기 (절댓값)                  |
| Max voltage CH1     | CH1에서 측정된 최대 전압                  |
| Min voltage CH1     | CH1에서 측정된 최소 전압                  |
| Avg voltage CH1     | CH1에서 측정된 평균 전압                  |
| Max voltage CH2     | CH2에서 측정된 최대 전압                  |
| Min voltage CH2     | CH2에서 측정된 최소 전압                  |
| Avg voltage CH2     | CH2에서 측정된 평균 전압                  |

예)  


# Market-SILVER
- 디지털 약자 노년층에 특화된 대화형 쇼핑 챗봇, 마켓실버TM

## Market-SILVER Android APP

<img width="30%" src="https://github.com/iSPD/marketSILVER/blob/main/images/marketSilver.jpg"/> <img width="30%" src="https://github.com/iSPD/marketSILVER/blob/main/images/marketSilverMovie.gif"/>

---

## Market-SILVER Server

### ⚙️ **개발 환경** 

-	CPU : Ubuntu 20.04.3 LTS

-	GPU : 지포스 RTX 3090 D6 24GB

  (Driver Version : 470.103.01, Cuda : 11.1, Cudnn : 8.2.1)

### ⚙️ **개발 언어** 

-	`Python 3.8.x`

### SIL-Voice (발화 음성 인식)

- 시니어 특화 ASR(Automatic Speech Recognition) 기술

- 시니어 1만명 이상의 발화음성 **7만시간 데이터셋**으로 Pre-Training 및 Fine-Tuning

- 사용 모델

  - [페이스북 Wav2vec 2.0](https://github.com/joungheekim/k-wav2vec)
  
  - [구글 Conformer](https://github.com/openspeech-team/openspeech)
  
- 사용 데이터셋

  - [AI-Hub](https://www.aihub.or.kr/aihubdata/data/list.do?pageIndex=1&currMenu=115&topMenu=100&dataSetSn=&srchdataClCode=DATACL001&srchOrder=&SrchdataClCode=DATACL002&searchKeyword=&srchDataRealmCode=REALM002&srchDataTy=DATA004) (노인남녀 명령어 음성, 자유대화 음성 등...)
 

- 사용 라이브러리
  - fairseq

  - pytorch 1.10.1+cu111

  - difflib의 SequenceMatcher

---

- **다중모델 음성인식**으로 오류단어를 마켓실버 이용자에게 질문하여 최종 결과물의 **CER(Character Error Rate)를 획기적으로 개선**

<img width="70%" src="https://github.com/iSPD/marketSILVER/blob/main/images/%EB%8B%A4%EC%A4%91%EC%9D%B8%EC%8B%9D.png"/>

<img width="70%" src="https://github.com/iSPD/marketSILVER/blob/main/images/%EC%9D%B8%EC%8B%9D%EB%8D%B0%EC%9D%B4%ED%84%B0.png"/>

---

- **다중모델 음성인식**을 위한 적용 알고리즘
  
  - 다중 자동음성인식 모델과 챗봇을 통한, 인식 정확도 개선
    
    1. 자모분리
    
    2. 자모열 유사도 측정

    ```Python
    def diff(word1, word2):
      '''두 유니코드 단어의 거리를 계산하여 차이를 반환한다'''
      L1 = j2hcj(h2j(word1))
      L2 = j2hcj(h2j(word2))

      differ = difflib.SequenceMatcher(None, L1, L2)
      return differ.ratio()
    ```
    
    3. 유사도 수치에 따른, 챗봇 질의와 최종 인식 결과물 보정

###

### SIL-Brain (발화 문장 분석 및 상품 검색)
#### Pre-Processing

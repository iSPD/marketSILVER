# Market-SILVER<sup>TM</sup>
- 디지털 약자 노년층에 특화된 대화형 쇼핑 챗봇, 마켓실버<sup>TM</sup>

---

## 🕰️ **개발 기간**

- 2022년 11월 21일 ~ 2023년 4월 14일

---

## Market-SILVER Android APP

<img width="30%" src="https://github.com/iSPD/marketSILVER/blob/main/images/marketSilver.jpg"/> <img width="30%" src="https://github.com/iSPD/marketSILVER/blob/main/images/marketSilverMovie.gif"/> <img width="30%" src="https://github.com/iSPD/marketSILVER/blob/main/images/chatGPT3.5.gif"/>

---

## Market-SILVER Server

### ⚙️ **개발 환경** 

-	CPU : Ubuntu 20.04.3 LTS

-	GPU : 지포스 RTX 3090 D6 24GB

  (Driver Version : 470.103.01, Cuda : 11.1, Cudnn : 8.2.1)

### ⚙️ **개발 언어** 

-	`Python 3.8.x`

---

### SIL-Voice (발화 음성 인식)

- 시니어 특화 ASR(Automatic Speech Recognition) 기술

- 시니어 1만명 이상의 발화음성 **7만시간 데이터셋**으로 Pre-Training 및 Fine-Tuning

- 사용 모델

  - [페이스북 Wav2vec 2.0](https://github.com/joungheekim/k-wav2vec)
  
  - [구글 Conformer](https://github.com/openspeech-team/openspeech)
  
- 사용 데이터셋

  - ksponspeech(Pretrained)

  - [AI-Hub](https://www.aihub.or.kr/aihubdata/data/list.do?pageIndex=1&currMenu=115&topMenu=100&dataSetSn=&srchdataClCode=DATACL001&srchOrder=&SrchdataClCode=DATACL002&searchKeyword=&srchDataRealmCode=REALM002&srchDataTy=DATA004) (노인남녀 명령어 음성, 자유대화 음성 등...)

  - 자체 데이터 수집 및 가공
 

- 사용 라이브러리
  - fairseq

  - pytorch 1.10.1+cu111

  - jamo

  - difflib의 SequenceMatcher

  - Flask

  - Gunicorn

- Training
  - 음성 데이터를 Sample Rate 16,000Hz로 변환하여 통일

  - Broken 음성 데이터 제거(약 3%정제)

  - 시니어 Test Dataset에서 평균 CER 1.95

 - Inference
   - Flask와 Gunicorn을 이용하여 Inference 서버 구축 ( Inference Time : **2,000ms** )

---

- **다중모델 음성인식**으로 오류단어를 마켓실버 이용자에게 질문하여 최종 결과물의 **CER(Character Error Rate)를 획기적으로 개선**

    - 기존 모델 1개 적용 대비 CER 0.25개선하여 최종 **CER 1.7**

<div align="center">
<img width="70%" src="https://github.com/iSPD/marketSILVER/blob/main/images/%EB%8B%A4%EC%A4%91%EC%9D%B8%EC%8B%9D.png"/>

<img width="70%" src="https://github.com/iSPD/marketSILVER/blob/main/images/%EC%9D%B8%EC%8B%9D%EB%8D%B0%EC%9D%B4%ED%84%B0.png"/>
</div>

---

- **다중모델 음성인식**을 위한 적용 알고리즘
  
  - **다중 자동음성인식 모델과 챗봇을 통한, 인식 정확도 개선(**특허 기술**)**
    
    [WordsMatching.py](https://github.com/iSPD/marketSILVER/blob/main/SilVoice/SilVoiceCore/wordsMatching.py)
    
    ###
    
    1. 자모분리
    
    ```
    chut = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ#'
    ga = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ#'
    ggut = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ#'
    ```
    
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

    <img width="70%" src="https://github.com/iSPD/marketSILVER/blob/main/images/%EC%B1%97%EB%B3%BC%EC%A7%88%EC%9D%98%ED%91%9C.png"/>
 
  - **다중 자동음성인식 모델을 통한, 데이터 자동 라벨링(**특허 기술**)**

    1. 자모분리

    2. 자모열 유사도 측정

    3. 유사도 수치에 따른, 데이터 자동 라벨링

    <img width="70%" src="https://github.com/iSPD/marketSILVER/blob/main/images/%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%9D%BC%EB%B2%A8%EB%A7%81.png"/>

    4. 자동 라벨링 된 데이터로 ASR 모델의 데이터셋으로 사용하여 인식률 개선

- **사용 방법**
  - Contact : ispd_daniel@outlook.kr(김경훈)

---

### SIL-Brain
  
  <br>
  
  <div align="left">
  <img width="80%" src="https://github.com/iSPD/marketSILVER/blob/main/images/chatGPT1.JPG"/>
  </div>
  
  </br>
  <br>
  
  <div align="left">
  <img width="80%" src="https://github.com/iSPD/marketSILVER/blob/main/images/silbrain.jpg"/>
  </div>
  
  </br>
  <br>
  
  <div align="left">
  <img width="80%" src="https://github.com/iSPD/marketSILVER/blob/main/images/gpt.JPG"/>
  </div>
  
  </br>
  
### Named Entity Recognition

#### 사용 모델
- BERT-Base, Multilingual Cased ( Transformer )

#### 구현 내용
- Synthetic 데이터셋 생성 : 수집한 상품명과 시니어가 물건 구매 시 많이 사용하는 주어, 동사 등을 조합하여 Random으로 문장 생성(주어, 동사 자동 Tagging)

- 상품 정보의 카테고리, 상품명, 단위, 용도 등의 Tagging

- Pre-Training 된 BERT 모델에 Fine Tunning (**Validation Accuracy 95%**)

```Python
def create_model():
  model = TFBertModel.from_pretrained("bert-base-multilingual-cased", from_pt=False, num_labels=len(label_dict), output_attentions = False, output_hidden_states = False)

  token_inputs = tf.keras.layers.Input((SEQ_LEN,), dtype=tf.int32, name='input_word_ids') # 토큰 인풋
  mask_inputs = tf.keras.layers.Input((SEQ_LEN,), dtype=tf.int32, name='input_masks') # 마스크 인풋

  bert_outputs = model([token_inputs, mask_inputs])
  bert_outputs = bert_outputs[0] # shape : (Batch_size, max_len, 30(개체의 총 개수))
  # nr = tf.keras.layers.Dense(16, activation='softmax')(bert_outputs) # shape : (Batch_size, max_len, 30)
  nr = tf.keras.layers.Dense(21, activation='softmax')(bert_outputs) # shape : (Batch_size, max_len, 30)
  
  nr_model = tf.keras.Model([token_inputs, mask_inputs], nr)
  
  nr_model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.00002), loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
      metrics=['sparse_categorical_accuracy'])
  nr_model.summary()
  return nr_model
```

### GENERATIVE AI CHATBOT

- 상품 데이터 분석 & 구조화 : 대형 온라인 쇼핑몰 식품 카테고리 전체의 250만개 상품 Data의 대표상품 설정, 상세옵션 항목 구조화를 통한 정답상품 생성

- 데이터 수집 : 상품 정보는 자체적인 최적화 크롤러를 개발하여 자동 수집

- 발화 문장에서 추출된 유의미 단어를 입력, 관련 하위 카테고리 추출 알고리즘 적용

- 복수의 하위 카테고리, 대표상품, 상세옵션 항목을 Multi-Tree로 계층화(JNI)

- Multi-Tree를 기반으로 루트노드의 서브트리를 발화자에게 송신, 발화자 응답 데이터를 수신하여 서브트리를 재검색하는 방법으로 상품 카테고리를 특정하고, 해당 상세 옵션을 선택 유도하는 방식의, 챗기반 대표 상품 Selector 적용

- SILbrain 검색 챗봇에서의 검색 결과를 시니어 특화 정답상품 2~3개로 Curation

#### Tagging Tool  
  
   - Python 3.8.0
  
   - GUI구성 : tkinter
  
   - Functions : tagging 자동 일괄적용, 작업여부 색상 표시
        
  <br>
  
  <div align="left">
  <img width="80%" src="https://github.com/iSPD/marketSILVER/blob/main/images/taggingtool.jpg"/>
  </div>
  
  </br>

### Chat-GPT SOLUTION

- OpenAI의 Completion.Create API 이용 Server API구현(Gunicorn, Flask 이용)
- Prompt Engineering Code 구성
- Prompt Engineering 시, Max Tokens 값 조절하여 속도 조절 (값이 작을수록 속도 향상)

<!-- <Prompt Engineering API> -->
```Python
inText = '김치찌개 하게 두부 사줘!'

def doChatGPT(inText):
    load_dotenv()

    openai.api_key = apiKey
    
    response = openai.Completion.create(
    model="text-davinci-003",
    # model="gpt-3.5-turbo",
    prompt=f"Q: {inText}. 문장에서 구매하고자 하는 상품과 용도를 단어로만 선택해줘.\n A:",
    temperature=0,
    max_tokens=27,#대답의 최대 Token수, 길수록 속도 느려짐
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\n"]
    )
```

- GPT-3.5에 미학습 상품명 등을 Prompt, Completion 형태의 JSON 파일로 작성 후, OpenAI의 CLI Data Preparation Tool을 이용 JSONL 형태로 변환하여 데이터셋 생성
- Davinci 모델에 JSONL 파일로 OpenAI의 CLI인 fine_tunes.create으로 Fine Tunning

<!--  <JSON 데이터셋 예제> -->
```JSON
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
```

<!-- <Fine Tunning 예제> -->
```Python
openai api fine_tunes.create -t <TRAIN_FILE_ID_OR_PATH> -m <BASE_MODEL>
```
  
### **사용 방법**
  - Contact : ispd_sally@outlook.kr(정영선)

---
## LICENSE
- [MIT](https://github.com/iSPD/marketSILVER/blob/main/LICENSE.md)

---
## 문의 사항
- (주)iSPD 정한별 대표
- ispd_paul@outlook.kr
- 010-9930-1791

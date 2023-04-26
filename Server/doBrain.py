import os
from flask import Blueprint, request, jsonify
import sys
sys.path.append('/home/khkim/work/wav2Infer/wav2vec')
# sys.path.append('/home/khkim/work/silverMarket/silvermarket')
sys.path.append('/home/khkim/work/svnFolder/marketSilver/marketSilverServer/silvermarket')
sys.path.append('/home/khkim/work/silverMarket/makeWord')
from sentence_preprocessing import sentence_preprocessing
from goSilverMarketP import firstSetting, goSilverKiwi, goSilverSearch
web = firstSetting() #왜 여기서 에러나지? 20221208
from wordsMatching import getGoodKeyword, checkMnQnXDo

sys.path.append('/home/khkim/work/svnFolder/marketSilver/marketSilverServer/silvermarket/chatGPT')
from goChatGPT import doChatGPT

#sys.path.append('/home/khkim/work/silverMarket/silvermarket/vscode_compare_db')
sys.path.append('/home/khkim/work/svnFolder/marketSilver/marketSilverServer/silvermarket/vscode_compare_db')
from silbrain import update_DB, get_category6th_candidates_mix, ready_web, quit_web, pre_curation
update_DB()
# web = ready_web()

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main():
    print('통신보안')
    return '통신보안'

from beam_s import loadingModel, inferenceSTT
loadingModel()

import struct
import pathlib
def make_wav_format(pcm_data:bytes, ch:int) -> bytes:
        """ 
        pcm_data를 통해서 wav 헤더를 만들고 wav 형식으로 저장한다.
        :param pcm_data: pcm bytes
        :param ch: 채널 수
        :return wav: wave bytes
        """
        waves = []
        waves.append(struct.pack('<4s', b'RIFF'))
        waves.append(struct.pack('I', 1))  
        waves.append(struct.pack('4s', b'WAVE'))
        waves.append(struct.pack('4s', b'fmt '))
        waves.append(struct.pack('I', 16))
        # audio_format, channel_cnt, sample_rate, bytes_rate(sr*blockalign:초당 바이츠수), block_align, bps
        if ch == 2:
            waves.append(struct.pack('HHIIHH', 1, 2, 16000, 64000, 4, 16))  
        else:
            waves.append(struct.pack('HHIIHH', 1, 1, 16000, 32000, 2, 16))
        waves.append(struct.pack('<4s', b'data'))
        waves.append(struct.pack('I', len(pcm_data)))
        waves.append(pcm_data)
        waves[1] = struct.pack('I', sum(len(w) for w in waves[2:]))
        return b''.join(waves)

def checkSpelling(inputStr):

    print('진짜 스펠링...............................................3')

    from hanspell import spell_checker
    result = spell_checker.check(inputStr)
    print(result.checked)
    return result.checked

@bp.route('/doChatGPTServer', methods=['POST'])
def doChatGPTServer():
    if request.method == 'POST':
        data = request.data
        data = data.decode('utf-8')
        print('doChatGPT 입력 : {}'.format(data))
        
        if len(data.split('#')) == 2:
            inputWord = data.split('#')[0]
            historyWord = data.split('#')[1]
        else:
            inputWord = data.split('#')[0]
            historyWord = ''
        
        result = doChatGPT(inputWord, historyWord)
        print(f'결과 : {result}')
        return jsonify({'result': result})

@bp.route('/stt', methods=['POST'])
def stt():
    if request.method == 'POST':
        
        inputPath = 'input.pcm'
        convertPath = 'result.wav'
                
        file = request.files['file']
        file.save(inputPath)
        
        pcm_bytes = pathlib.Path("input.pcm").read_bytes()
        wav_bytes = make_wav_format(pcm_bytes, 2)
        with open(convertPath, 'wb') as saveFile:
            saveFile.write(wav_bytes)
        
        # from scipy.io import wavfile
        # import librosa
        # import soundfile as sf
        # devFile = 'temp.wav'
        # fs, data = wavfile.read(devFile)
        # print(fs)
        # if fs == 44100:
        #     def down_sample(input_wav, origin_sr, resample_sr, output):
        #         y, sr = librosa.load(input_wav, sr=origin_sr)
        #         resample = librosa.resample(y, sr, resample_sr)
        #         sf.write(output, resample, resample_sr, format='WAV', endian='LITTLE', subtype='PCM_16')
        #     down_sample(devFile, 44100, 16000, 'temp_new.wav')
        #     devFile = 'temp_new.wav'
            
        # rootPath = '/home/khkim/work/silverMarket/silvermarket/server'
        rootPath = '/home/khkim/work/svnFolder/marketSilver/marketSilverServer/silvermarket/server'
        inferencePath = os.path.join(rootPath, convertPath)
        
        # loadingModel()
        result = inferenceSTT(inferencePath)
        print('우리서버에서 음성인식...............................................1')
        print(f'result : {[result]}')
        
        # checkSpelling(result)
        
        return jsonify({'result': result})
        # return jsonify({'class_id': class_id, 'class_name': class_name})
    else:
        return '통신보안'

# @bp.route('/kiwi', methods=['POST'])
# def kiwi():
@bp.route('/keywordCheck', methods=['POST'])
def keywordCheck():
    if request.method == 'POST':
        
        data = request.data
        data = data.decode('utf-8')
        print('predict(kiwi) : {}'.format(data))
        
        gWord = data.split('\n')[0]
        oWord = data.split('\n')[1]
        
        result, history = getGoodKeyword(gWord, oWord)
        return jsonify({'keyword' : result, 'history' : history})
        
        # keyword = goSilverKiwi(data)       
        # keyword, length = sentence_preprocessing(data)
        
        # print(f'keyword : {keyword}')
        # keyword = keyword.split(' ')
        # print(f'keyword : {keyword}')
             
        # return jsonify({'keyword' : keyword})
        
@bp.route('/checkMnQnX', methods=['POST'])
def checkMnQnX():
    if request.method == 'POST':
        
        data = request.data
        data = data.decode('utf-8')
        print('checkMnQnX : {}'.format(data))
                
        resultList = checkMnQnXDo(data)
        return jsonify({'resultList' : resultList, 'history' : ''})
    
@bp.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        
        data = request.data
        data = data.decode('utf-8')
        print('predict : {}'.format(data))
        
        result, links = goSilverSearch(data)
             
        return jsonify({'result': result, 'link': links})
    
import json
@bp.route('/check_spell', methods=['POST'])
def check_spell():
    if request.method == 'POST':

        print('체크 스펠링...............................................2')
        
        data = request.data
        data = data.decode('utf-8')

        print(f'check_spell-1 : {check_spell}')
        
        googleResult = data.split('/')[0]
        outResult = data.split('/')[1]
        
        result1 = checkSpelling(googleResult)
        result2 = checkSpelling(outResult)
        
        print(f'spelling check-2 구글 : {result1}, 우리 : {result2}')
             
        return jsonify({'google': result1, 'our': result2})
    
from isGood import startGoodCheck
@bp.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        print('test')
        startGoodCheck()
        
        return jsonify({'result' : 'good'})

# 클라이언트로부터 발화문장 텍스트를 받아 db 검색 후 후보카테고리 리스트를 보내준다.
@bp.route('/compare_speech_txt_to_db', methods=['POST'])
def compare_speech_txt_to_db():
    if request.method == 'POST':
        print('compare_speech_txt_to_db')
        data = request.data
        data = data.decode('utf-8')
        # list_of_candidates = get_category6th_candidates(data)
        
        # list_of_candidates = get_category6th_candidates_new(data)
        timestamp, status, list_of_candidates, list_of_links, note_str = get_category6th_candidates_mix(web, data, 2)
        
        if status == 'candidate-select':
            ret_data1 = list_of_candidates
            ret_data2 = list_of_links
        elif status == 'speak-again':
            ret_data1 = []
            ret_data2 = []
        elif status == 'product-search-now':
            ret_data1 = []
            ret_data2 = []
        elif status == 'product-search-now-alert': # q 만 있는 경우 검색상품과 함께 경고(쿠팡와우 체크 해제)
            ret_data1 = list_of_candidates
            ret_data2 = list_of_links    
        elif status == 'is-this-or-that':
            ret_data1 = list_of_candidates
            ret_data2 = []
            
        # 리턴케이스 : 후보카테고리보내기, 발화재입력요청하기, '바로 상품 검색 모드' 라고 알려주기, 이거냐 저거냐묻기
        return jsonify({'timestamp' : timestamp, 'status' : status, 'result' : ret_data1, 'links' : ret_data2, 'history' : note_str})
        
        # return jsonify({'timestamp' : timestamp, 'status' : 'candidate-select', 'result' : list_of_candidates})
        # return jsonify({'status' : 'speak-again', 'result' : list_of_candidates})
        # return jsonify({'status' : 'product-search-now', 'result' : list_of_candidates}) # 이건 일단 '바로 상품 검색 모드' 라고 알려주고 다음 단계에서 상품리스트 보내주도록 하기
        # return jsonify({'status' : 'is-this-or-that', 'result' : list_of_candidates}) # 어느 시점에 ??
        # return jsonify({'result' : list_of_candidates})  #기존코드

import json
# 클라이언트로부터 최종 카테고리 ID, 6분류명, 특화명, 제외키워드를 받아 크롤링 & 큐레이션 결과를 보내준다.
@bp.route('/search_products', methods=['POST'])
def search_products():
    if request.method == 'POST':
        print('search_products')
        print(request.is_json)
        print(f"headers : {request.headers['Content-Type']}")
        # datas = {'product6th':product6th, 'options':options, 'excluded':excluded_words}
        jsondt_dump = json.dumps(request.get_json())
        jsondt = json.loads(jsondt_dump)
        
        product6th = jsondt['product6th'] #.decode('utf-8')
        options = jsondt['options']
        excluded_words = jsondt['excluded']
        tmstamp = jsondt['timestamp']
        
        print(f"최종 6분류명 : {product6th}")   # ex) "486503&막창#돼지 막창"
        print(f"특화요소 : {options}")   # ex) [(1, 2, '불막창#양념 막창', '초벌')]
        print(f"제외키워드 : {excluded_words}")    # ex) "순한양념구이"
        
        # web = ready_web()
        products, links = pre_curation(web, product6th, options, excluded_words, tmstamp, 2)
        # response = do_curation() # TODO 추후
        # quit_web(web)        
        print(f'response : {products}, links : {links}')
        
        return jsonify({"result" : products, "links" : links})
    

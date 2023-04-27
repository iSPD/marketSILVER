import os
from flask import Blueprint, request, jsonify
import sys
sys.path.append('/home/khkim/work/wav2Infer/wav2vec')
sys.path.append('/home/khkim/work/svnFolder/marketSilver/marketSilverServer/silvermarket')
sys.path.append('/home/khkim/work/silverMarket/makeWord')
from sentence_preprocessing import sentence_preprocessing
from goSilverMarketP import firstSetting, goSilverKiwi, goSilverSearch
web = firstSetting() 
from wordsMatching import getGoodKeyword, checkMnQnXDo

sys.path.append('/home/khkim/work/svnFolder/marketSilver/marketSilverServer/silvermarket/chatGPT')
from goChatGPT import doChatGPT

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
        
        rootPath = '/home/khkim/work/svnFolder/marketSilver/marketSilverServer/silvermarket/server'
        inferencePath = os.path.join(rootPath, convertPath)
        
        # loadingModel()
        result = inferenceSTT(inferencePath)
                
        # checkSpelling(result)
        
        return jsonify({'result': result})
        
    else:
        return '통신보안'

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
  
        data = request.data
        data = data.decode('utf-8')

        print(f'check_spell-1 : {check_spell}')
        
        googleResult = data.split('/')[0]
        outResult = data.split('/')[1]
        
        result1 = checkSpelling(googleResult)
        result2 = checkSpelling(outResult)
            
        return jsonify({'google': result1, 'our': result2})
    
from isGood import startGoodCheck
@bp.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        print('test')
        startGoodCheck()
        
        return jsonify({'result' : 'good'})

@bp.route('/compare_speech_txt_to_db', methods=['POST'])
def compare_speech_txt_to_db():
    if request.method == 'POST':
        print('compare_speech_txt_to_db')
        data = request.data
        data = data.decode('utf-8')
       
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
        elif status == 'product-search-now-alert':
            ret_data1 = list_of_candidates
            ret_data2 = list_of_links    
        elif status == 'is-this-or-that':
            ret_data1 = list_of_candidates
            ret_data2 = []
            
        return jsonify({'timestamp' : timestamp, 'status' : status, 'result' : ret_data1, 'links' : ret_data2, 'history' : note_str})
       
import json
@bp.route('/search_products', methods=['POST'])
def search_products():
    if request.method == 'POST':
        print('search_products')
        print(request.is_json)
        print(f"headers : {request.headers['Content-Type']}")
        jsondt_dump = json.dumps(request.get_json())
        jsondt = json.loads(jsondt_dump)
        
        product6th = jsondt['product6th'] #.decode('utf-8')
        options = jsondt['options']
        excluded_words = jsondt['excluded']
        tmstamp = jsondt['timestamp']
        
        products, links = pre_curation(web, product6th, options, excluded_words, tmstamp, 2)
        
        return jsonify({"result" : products, "links" : links})
    

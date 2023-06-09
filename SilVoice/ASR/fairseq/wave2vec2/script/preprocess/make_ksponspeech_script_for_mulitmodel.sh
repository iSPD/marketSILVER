# Preprocess for Ksponspeech dataset
# Paper : https://www.mdpi.com/2076-3417/10/19/6936
# Dataurl : https://aihub.or.kr/aidata/105

# All related data must in same directory described below
# RootDir
#   |-------KsponSpeech_01
#   |-------KsponSpeech_02
#   |-------KsponSpeech_03
#   |-------KsponSpeech_04
#   |-------KsponSpeech_05
#   |-------KsponSpeech_eval

# Put your absolute 'RootDir' path below
# ROOT_DIR=/home/khkim/koreanSpeak/dataset ## it is dummy, please modify it
# ROOT_DIR=/home/khkim/oldDatasetAll ## it is dummy, please modify it
# ROOT_DIR=/home/khkim/oldDatasetAll2 ## it is dummy, please modify it
# ROOT_DIR=

# Put your Script path which is also given with Ksponspeech dataset
# SCRIPT_PATH=/home/khkim/koreanSpeak/scripts ## it is dummy, please modify it
# SCRIPT_PATH=/home/khkim/oldDatasetAll/wav2vecScripts ## it is dummy, please modify it
# SCRIPT_PATH=/home/khkim/oldDatasetAll2/wav2vecScripts2 ## it is dummy, please modify it
# SCRIPT_PATH=/home/khkim/speakDatasets/scriptsAll ## 8가지 엑셀 참조
# SCRIPT_PATH=/home/khkim/speakDatasets/scriptsAll5 ## 8가지
SCRIPT_PATH=/home/khkim/speakDatasets/scriptsAll4Add ## 4가지 추가
# SCRIPT_PATH=/home/khkim/koreanConDataset/scriptsCon ## it is dummy, please modify it

# Select for preprocess output
# You can choose either 'grapheme' or 'character'
# Here, character means syllable block which is korean basic character
# If you want to run multi-task model, OUTPUT_UNIT must 'grapheme' and ADD_OUTPUT_UNIT must 'character'
OUTPUT_UNIT=grapheme
ADD_OUTPUT_UNIT=character

# if length of script is over limit, it is exculded as described in https://arxiv.org/abs/2009.03092
LIMIT=200

# Ksponspeech data support dual transcriptions including phonetic and orthographic.
# Therefore, select transcription type [phonetic, spelling]
# Here, phonetic : phonetic, orthographic : spelling
#PROCESS_MODE=phonetic
PROCESS_MODE=spelling

# Put your absolute destination path
DESTINATION=$(realpath .)/transcriptions/speakAll9
# DESTINATION=$(realpath .)/transcriptions/speakKoreanCon
# DESTINATION=$(realpath .)/transcriptions/test

# --root ${ROOT_DIR} \

## Run preprocess code
python preprocess/make_manifest.py \
     --output_unit ${OUTPUT_UNIT} \
     --additional_output_unit ${ADD_OUTPUT_UNIT} \
     --do_remove \
     --preprocess_mode ${PROCESS_MODE} \
     --token_limit ${LIMIT} \
     --dest ${DESTINATION}/${OUTPUT_UNIT}_${ADD_OUTPUT_UNIT}_${PROCESS_MODE} \
     --script_path ${SCRIPT_PATH} \
     --ext wav


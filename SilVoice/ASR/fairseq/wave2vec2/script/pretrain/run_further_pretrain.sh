# RUN Further pretrain
# task.data : path of preprocessed manifest folder
# checkpoint.save_dir : path to save pretrain checkpoint
# task.del_silence : whether use silence options which indicate removing prolonged silence in voice
# checkpoint.finetune_from_model : checkpoints which is used for init state. You can download english checkpoints in Fairseq github "https://github.com/pytorch/fairseq/blob/master/examples/wav2vec/README.md"

## before run code, please check config files to modify options required.
# checkpoint.finetune_from_model=$(realpath .)/save_checkpoint/pretrain/english_pretrain/checkpoint_best.pt \
# checkpoint.finetune_from_model=$(realpath .)/save_checkpoint/pretrain/english_pretrain/wav2vec_small.pt \

# python -W ignore fairseq_cli/hydra_train.py \
#     task.data=$(realpath .)/transcriptions/ksponspeech/grapheme_character_spelling \
#     checkpoint.save_dir=$(realpath .)/save_checkpoint/pretrain/further_pretrain \
#     task.del_silence=True \
#     checkpoint.finetune_from_model=$(realpath .)/save_checkpoint/pretrain/english_pretrain/checkpoint_best.pt \
#     --config-dir configs/pretrain \
#     --config-name further_pretrain

# python -W ignore fairseq_cli/hydra_train.py \
#     task.data=$(realpath .)/transcriptions/oldSpeech2/grapheme_character_spelling \
#     checkpoint.save_dir=$(realpath .)/save_checkpoint/pretrain/further_pretrain \
#     task.del_silence=True \
#     checkpoint.finetune_from_model=$(realpath .)/save_checkpoint/pretrain/english_pretrain/checkpoint_best.pt \
#     --config-dir configs/pretrain \
#     --config-name further_pretrain

# good version 3가지 트레이닝
# python -W ignore fairseq_cli/hydra_train.py \
#     task.data=$(realpath .)/transcriptions/speakAll1/grapheme_character_spelling \
#     checkpoint.save_dir=$(realpath .)/save_checkpoint/pretrain/further_pretrain \
#     task.del_silence=True \
#     checkpoint.finetune_from_model=$(realpath .)/save_checkpoint/pretrain/english_pretrain/checkpoint_best.pt \
#     --config-dir configs/pretrain \
#     --config-name further_pretrain

# # 4가지 트레이닝 시 부하 테스트 용도
# python -W ignore fairseq_cli/hydra_train.py \
#     task.data=$(realpath .)/transcriptions/speakAll4/grapheme_character_spelling \
#     checkpoint.save_dir=$(realpath .)/save_checkpoint/pretrain/further_pretrain4 \
#     task.del_silence=True \
#     checkpoint.finetune_from_model=$(realpath .)/save_checkpoint/pretrain/english_pretrain/checkpoint_best.pt \
#     --config-dir configs/pretrain \
#     --config-name further_pretrain

# 5가지 트레이닝 시 부하 테스트 용도
# CUDA_VISIBLE_DEVICES=0,1,2 python -W ignore fairseq_cli/hydra_train.py \
#     task.data=$(realpath .)/transcriptions/speakAll5/grapheme_character_spelling \
#     checkpoint.save_dir=$(realpath .)/save_checkpoint/pretrain/further_pretrain5 \
#     task.del_silence=True \
#     checkpoint.finetune_from_model=$(realpath .)/save_checkpoint/pretrain/english_pretrain/checkpoint_best.pt \
#     --config-dir configs/pretrain \
#     --config-name further_pretrain

# 8가지 트레이닝 시 부하 테스트 용도
# CUDA_VISIBLE_DEVICES=0,1,2 python -W ignore fairseq_cli/hydra_train.py \
#     task.data=$(realpath .)/transcriptions/speakAll8/grapheme_character_spelling \
#     checkpoint.save_dir=$(realpath .)/save_checkpoint/pretrain/further_pretrain8 \
#     task.del_silence=True \
#     checkpoint.finetune_from_model=$(realpath .)/save_checkpoint/pretrain/english_pretrain/checkpoint_best.pt \
#     --config-dir configs/pretrain \
#     --config-name further_pretrain

# 9가지 트레이닝 시 부하 테스트 용도
CUDA_VISIBLE_DEVICES=0,1,2 python -W ignore fairseq_cli/hydra_train.py \
    task.data=$(realpath .)/transcriptions/speakAll9/grapheme_character_spelling \
    checkpoint.save_dir=$(realpath .)/save_checkpoint/pretrain/further_pretrain9 \
    task.del_silence=True \
    checkpoint.finetune_from_model=$(realpath .)/save_checkpoint/pretrain/english_pretrain/checkpoint_best.pt \
    --config-dir configs/pretrain \
    --config-name further_pretrain


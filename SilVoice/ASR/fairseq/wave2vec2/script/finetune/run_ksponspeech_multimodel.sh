# RUN finetune with Multi-task architecture
# task.data : path of preprocessed manifest folder (multi-model must run in script which has grapheme and character vocabulary)
# checkpoint.save_dir : path to save finetune checkpoint
# task.del_silence : whether use silence options which indicate removing prolonged silence in voice
# model.additional_layers : number of transformer layer for syllable encoder which contains stacks of transformers and projection layers : default=2
# checkpoint.best_checkpoint_metric : evaluation metric for development set. In multi-model, 'wer' means evaluate model with grapheme outputs, and 'add_wer' means evaluate model with syllabel outputs.
# model.w2v_path : pre-trained checkpoints to use for fine-tuining (use either further-pretrained model or scratch-pretrained model)

## before run code, please check config files to modify options required.

# python -W ignore fairseq_cli/hydra_train.py \
#   task.data=$(realpath .)/transcriptions/ksponspeech/grapheme_character_spelling \
#   checkpoint.save_dir=$(realpath .)/save_checkpoint/finetune/oldSpeech2/multi_model \
#   task.del_silence=True \
#   model.additional_layers=2 \
#   checkpoint.best_checkpoint_metric=add_wer \
#   model.w2v_path=$(realpath .)/save_checkpoint/pretrain/further_pretrain/checkpoint_best.pt \
#   --config-dir configs/finetune/multi \
#   --config-name 960h

# python -W ignore fairseq_cli/hydra_train.py \
#   task.data=$(realpath .)/transcriptions/oldSpeech2/grapheme_character_spelling \
#   checkpoint.save_dir=$(realpath .)/save_checkpoint/finetune/ksponspeech/multi_model \
#   task.del_silence=True \
#   model.additional_layers=2 \
#   checkpoint.best_checkpoint_metric=add_wer \
#   model.w2v_path=$(realpath .)/save_checkpoint/pretrain/further_pretrain/checkpoint_best.pt \
#   --config-dir configs/finetune/multi \
#   --config-name 960h

# python -W ignore fairseq_cli/hydra_train.py \
#   task.data=$(realpath .)/transcriptions/test/grapheme_character_spelling \
#   checkpoint.save_dir=$(realpath .)/save_checkpoint/finetune/test/multi_model \
#   task.del_silence=True \
#   model.additional_layers=2 \
#   checkpoint.best_checkpoint_metric=add_wer \
#   model.w2v_path=$(realpath .)/save_checkpoint/pretrain/further_pretrain/checkpoint_best.pt \
#   --config-dir configs/finetune/multi \
#   --config-name 960h

# python -W ignore fairseq_cli/hydra_train.py \
#   task.data=$(realpath .)/transcriptions/oldSpeech2/grapheme_character_spelling \
#   checkpoint.save_dir=$(realpath .)/save_checkpoint/finetune/oldSpeech2/multi_model \
#   task.del_silence=True \
#   model.additional_layers=2 \
#   checkpoint.best_checkpoint_metric=add_wer \
#   model.w2v_path=$(realpath .)/save_checkpoint/pretrain/further_pretrain/checkpoint_best.pt \
#   --config-dir configs/finetune/multi \
#   --config-name 960h

# 3가지 데이터 셋 프리트레이닝 + 3가지 데이터 셋 파인 튠 => 결과는 굉장히 좋음
# python -W ignore fairseq_cli/hydra_train.py \
#   task.data=$(realpath .)/transcriptions/speakAll1/grapheme_character_spelling \
#   checkpoint.save_dir=$(realpath .)/save_checkpoint/finetune/speakAll1/multi_model \
#   task.del_silence=True \
#   model.additional_layers=2 \
#   checkpoint.best_checkpoint_metric=add_wer \
#   model.w2v_path=$(realpath .)/save_checkpoint/pretrain/further_pretrain/checkpoint_best.pt \
#   --config-dir configs/finetune/multi \
#   --config-name 960h

# 3가지 데이터 셋 + 1가지 더해서 프리트레이닝 + 3가지 파이튠
# python -W ignore fairseq_cli/hydra_train.py \
#   task.data=$(realpath .)/transcriptions/speakAll1/grapheme_character_spelling \
#   checkpoint.save_dir=$(realpath .)/save_checkpoint/finetune/speakAll2/multi_model \
#   task.del_silence=True \
#   model.additional_layers=2 \
#   checkpoint.best_checkpoint_metric=add_wer \
#   model.w2v_path=$(realpath .)/save_checkpoint/pretrain/further_pretrain/checkpoint_last.pt \
#   --config-dir configs/finetune/multi \
#   --config-name 960h

# 4가지 데이터셋 메모리 문제로 실패?
# CUDA_VISIBLE_DEVICES=1,2 python -W ignore fairseq_cli/hydra_train.py \
#   task.data=$(realpath .)/transcriptions/speakAll4/grapheme_character_spelling \
#   checkpoint.save_dir=$(realpath .)/save_checkpoint/finetune/speakAll4/multi_model \
#   task.del_silence=True \
#   model.additional_layers=2 \
#   checkpoint.best_checkpoint_metric=add_wer \
#   model.w2v_path=$(realpath .)/save_checkpoint/pretrain/further_pretrain4/checkpoint_last.pt \
#   --config-dir configs/finetune/multi \
#   --config-name 960h

# 새로운 데이터셋 하나만 테스트 시작
# python -W ignore fairseq_cli/hydra_train.py \
#   task.data=$(realpath .)/transcriptions/speakKoreanCon/grapheme_character_spelling \
#   checkpoint.save_dir=$(realpath .)/save_checkpoint/finetune/speakKoreanCon/multi_model \
#   task.del_silence=True \
#   model.additional_layers=2 \
#   checkpoint.best_checkpoint_metric=add_wer \
#   model.w2v_path=$(realpath .)/save_checkpoint/pretrain/further_pretrain4/checkpoint_last.pt \
#   --config-dir configs/finetune/multi \
#   --config-name 960h

# 9가지 데이터셋 훈련 시작
CUDA_VISIBLE_DEVICES=0,1,2 python -W ignore fairseq_cli/hydra_train.py \
  task.data=$(realpath .)/transcriptions/speakAll9/grapheme_character_spelling \
  checkpoint.save_dir=$(realpath .)/save_checkpoint/finetune/speakAll9/multi_model \
  task.del_silence=True \
  model.additional_layers=2 \
  checkpoint.best_checkpoint_metric=add_wer \
  model.w2v_path=$(realpath .)/save_checkpoint/pretrain/further_pretrain9/checkpoint_best.pt \
  --config-dir configs/finetune/multi \
  --config-name 960h
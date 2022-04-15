### extend
#python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=40 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=4096 --preferable_shift_amount=0 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500


## perturbation size: 0.5%: 512; 1%:1024, 2%:2048, 4%:4096, 8%:8192=2**13, 16%:16384=2**14, 32%:32768=2**15
## has to be 2**n, as the perturbation size should be multiple times of file_alignment_size, which is usually 512, 1024, etc

## ----------> partial dos <------------
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=True --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=0 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500

## ----------> DOS extend <-------------
## 0.5%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=512 --preferable_shift_amount=0 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 1%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=1024 --preferable_shift_amount=0 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 2%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=2048 --preferable_shift_amount=0 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 4%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=4096 --preferable_shift_amount=0 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 8%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=8192 --preferable_shift_amount=0 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 16%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=16384 --preferable_shift_amount=0 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 32%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=32768 --preferable_shift_amount=0 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500


## ----------> full dos <--------------
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=0 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500

## ----------> content shift <-------------
## 0.5%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=512 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 1%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=True --log_file_for_result=../result/result_filev.txt --preferable_extension_amount=0 --preferable_shift_amount=1024 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 2%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=2048 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 4%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=4096 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 8%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=8192 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 16%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=16384 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 32%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=32768 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500


## -------------> partial dos + shift <---------------
## 0.5%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=True --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=512 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 1%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=True --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=1024 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 2%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=True --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=2048 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 4%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=True --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=4096 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 8%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=True --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=8192 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 16%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=True --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=16384 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 32%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=True --content_shift=True --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=32768 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500


## ----------> full dos + shift <------------
## 0.5%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=512 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 1%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=1024 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 2%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=2048 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 4%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=4096 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 8%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=8192 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 16%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=16384 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 8%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=0 --preferable_shift_amount=32768 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500


## -----------> DOS extend + shift <----------
## 0.5%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=256 --preferable_shift_amount=256 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 1%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=512 --preferable_shift_amount=512 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 2%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=1024 --preferable_shift_amount=1024 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 4%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=2048 --preferable_shift_amount=2048 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 8%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=4096 --preferable_shift_amount=4096 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 16%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=8192 --preferable_shift_amount=8192 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500
## 32%
python adv_attack_against_detectors.py --adversary=FGSM --eps=0.1 --alpha=0.7 --iter_steps=20 --partial_dos=False --content_shift=False --log_file_for_result=../result/result_file.txt --preferable_extension_amount=16384 --preferable_shift_amount=16384 --test_data_path=../data/all_file/ --test_label_path=../data/test_mal_label.csv --model_path_1=../checkpoint/malconv_model.pth --model_path_2=../checkpoint/fireeye_model.pth --use_cpu=1 --batch_size=1 --first_n_byte=102400 --window_size=500



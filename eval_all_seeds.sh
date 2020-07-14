declare -a seeds=("2016" "2017" "2018" "2019" "2020") 
declare -a grad_norms=("1.0" "2.0" "5.0")
declare -a dropouts=("0.1" "0.05" "0.3")

for SEED in "${seeds[@]}"; do
    for GRAD_NORM in "${grad_norms[@]}"; do
        for DROPOUT in "${dropouts[@]}"; do
            echo $SEED $GRAD_NORM $DROPOUT
            bash eval_all.sh $SEED $GRAD_NORM $DROPOUT > report/seed/${SEED}_${GRAD_NORM}_${DROPOUT}.txt
        done
    done
done

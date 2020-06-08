MODE=$1

declare -a grad_norms=("1.0" "2.0" "5.0") 
declare -a seeds=("2016" "2017" "2018" "2019" "2020")
declare -a models=("bert-pt" "bert" "mt-dnn")
declare -a types=("base" "large")

for MODEL in "${models[@]}"; do
    for TYPE in "${types[@]}"; do
        for SEED in "${seeds[@]}"; do
            for GRAD_NORM in "${grad_norms[@]}"; do
                PREFIX=output/$MODE/${MODEL}_$TYPE/seed/$SEED/grad_norm/$GRAD_NORM
                SUFIX=dropout/0.1/
            
                mkdir -p $PREFIX/$SUFIX
                cp $PREFIX/*.json $PREFIX/$SUFIX
            done
        done
    done
done

for SEED in "${seeds[@]}"; do
    for GRAD_NORM in "${grad_norms[@]}"; do
        PREFIX=output/$MODE/bert-multilingual_base/seed/$SEED/grad_norm/$GRAD_NORM
        SUFIX=dropout/0.1/
    
        mkdir -p $PREFIX/$SUFIX
        cp $PREFIX/*.json $PREFIX/$SUFIX
    done
done

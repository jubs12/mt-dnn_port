MODE=$1

declare -a seeds=("2016" "2017" "2018" "2019" "2020")
declare -a models=("bert-pt")
declare -a types=("base" "large")

for MODEL in "${models[@]}"; do
    for TYPE in "${types[@]}"; do
        for SEED in "${seeds[@]}"; do
            PREFIX=output/$MODE/${MODEL}_$TYPE/seed/$SEED
            SUFIX=grad_norm/1.0/
            
            mkdir -p $PREFIX/$SUFIX
            cp $PREFIX/*.json $PREFIX/$SUFIX
        done
    done
done

for SEED in "${seeds[@]}"; do
    PREFIX=output/$MODE/$TASK/bert-multilingual_base/seed/$SEED
    SUFIX=grad_norm/1.0/
    
    mkdir -p $PREFIX/$SUFIX
    cp $PREFIX/*.json $PREFIX/$SUFIX
done

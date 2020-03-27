task_list=""

for task in `find . -maxdepth 1  -name "*.yaml"`
do
    #remove suffix and prefix
    task_name=${task%.yaml}
    task_name=${task_name#"./"}
    
     
    if  [[ $task_list  = "" ]]
    then
        task_list=$task_name
        
        echo "Creating task_defs.yaml with all tasks defs"
        cp $task task_defs.yaml
    else
        task_list="$task_list,$task_name"
    fi
    
    echo $task
    cat $task >> task_defs.yaml
    echo "" >> task_defs.yaml #add new_line
    
done

if  [[ $2 = '--do_lower_case' ]]
then

python train.py  --init_checkpoint $1 --task_def task_defs.yaml --train_datasets $task_list --test_datasets $task_list --tensorboard

else

python train.py --do_lower_case --init_checkpoint $1 --task_def task_defs.yaml --train_datasets $task_list --test_datasets $task_list --tensorboard

fi

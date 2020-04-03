#!bin/bash
task_list=""

if test -f "task_defs.yaml"
then
    echo "Removing previous task_defs.yml file"
    rm -f task_defs.yaml
fi

for task in `find . -maxdepth 1  -name "*.yaml"`
do
    #remove suffix and prefix
    task_name=${task%.yaml}
    task_name=${task_name#"./"}
    
     
    if  [[ $task_list  == "" ]]
    then
        task_list=$task_name
        
        echo "Creating task_defs.yaml with all tasks defs"
        cp $task task_defs.yaml
    else
        task_list="$task_list,$task_name"
    fi
    
    cat $task >> task_defs.yaml
    echo "" >> task_defs.yaml #add new_line
    
done

echo "Copy task_list for training"
echo $task_list

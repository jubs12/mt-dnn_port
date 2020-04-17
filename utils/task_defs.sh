#!bin/bash
started=true

if test -f "task_defs.yaml"
then
    echo "Removing previous task_defs.yml file"
    rm -f task_defs.yaml
fi

for task in `find . -maxdepth 1  -name "*.yaml"`
do
     
    if  [[ $started  == true ]]
    then        
        echo "Creating task_defs.yaml with all tasks defs"
        cp $task task_defs.yaml
        started=false
    fi
    
    cat $task >> task_defs.yaml
    echo "" >> task_defs.yaml #add new_line
    
done


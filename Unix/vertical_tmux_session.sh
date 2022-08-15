################################################################################
#
# Recreate whole tmux session, after a reboot
# 
# from SU 440015
################################################################################

SESSION="vertical"
tmux has-session -t $SESSION &> /dev/null

if [ $? != 0 ]
then
	# window 0: active-project
	tmux new-session -s $SESSION -n active-project -d
	tmux split-window -t $SESSION:0.0 -h -p 46
	tmux send-keys -t $SESSION:0.1 'cd ~/Projects/specificproject' C-m
	tmux send-keys -t $SESSION:0.1 'git adog' C-m q
	tmux split-window -t $SESSION:0.0 -v -p 90
	tmux send-keys -t $SESSION:0.2 'cd ~/Projects/uam' C-m
	tmux send-keys -t $SESSION:0.0 'top' C-m

	# window 1: spark
	tmux new-session -s $SESSION -n spark
	tmux send-keys -t $SESSION:1 'cd ~/spark/scala_scripts' C-m
	tmux split-window -t $SESSION:1.0 -v -p 56
	tmux send-keys -t $SESSION:1.0 'vim -S .vim_session' C-m
	tmux send-keys -t $SESSION:1.1 'cat ./spark-init.sh' C-m

	# window 2: python-API
	tmux new-session -s $SESSION -n python-API
	tmux split-window -t $SESSION:2.0 -h -p 46
	tmux split-window -t $SESSION:2.0 -v -p 90
	tmux send-keys -t $SESSION:2.1 'cd ~/Projects/apiproject' C-m
	tmux send-keys -t $SESSION:2.2 'cd ~/Projects/apiproject/subdir' C-m
	tmux send-keys -t $SESSION:2.1 './start_api.sh' C-m
	tmux send-keys -t $SESSION:2.0 'top' C-m

	# window 3: shell
	tmux new-window -t $SESSION

	tmux select-window -t $SESSION:0

fi

tmux attach -t $SESSION

# Script Shell para iniciar o servidor
# Se servidor já está rodando, não faz nada

ps -elf | grep server_handler.py | wc -l > running.txt
nr_servers="$(cat running.txt)"
if [ "$nr_servers" -eq "1" ]; then
	echo "Running server..."
	date >> server_output.txt
	nohup python2 server_handler.py >> server_output.txt &
fi

rm running.txt

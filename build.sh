# Author : eSargin

set +x

echo "Killing all running instances of main.py"
kill -9 $(ps aux |grep -i main.py |grep -v 'grep' | awk '{print$2}')

echo "Backlink Contorller Service"
nohup python3 main.py > service.log &
echo "Service Started"

tail -f nohup.out





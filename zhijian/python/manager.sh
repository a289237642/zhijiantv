#! /bin/sh
#description:This is cheese
#chkconfig:2345 20 81
flaskpath="/home/python/Desktop/workspace/ZhiJan/python/manager.py"

start(){
    nohup python $flaskpath runserver >> /home/python/Desktop/workspace/ZhiJan/python/logs/log &
    echo "flask start ok"
}

stop(){
    mpid=`ps aux | grep "$flaskpath" | grep -v 'grep' | awk '{print $2}'`
    kill -9 $mpid
    echo $mpid
    echo "flask stop ok"
}

restart(){
    stop
    start
}

case $1 in
    start)
    start
    ;;

    stop)
    stop
    ;;

    restart)
    restart
    ;;

    *)
    start
esac

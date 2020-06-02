#!/bin/sh
#encode begin
  #                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
#endcode end
#complie=true
#Author: Mr.yao
#Date:2015-01-29
#Description:琅琊榜开区（不包含mysql安装）
#Usage:
source /etc/profile

############################################################# 功能函数 Begin ##################################################################

        #显示消息
        #showType='errSysMsg/errSys/errUserMsg/warning/msg/msg2/OK'
        #错误输出（以红色字体输出） errSysMsg：捕捉系统错误后发现相信并退出；errSys：捕捉到系统错误后退出；errUserMsg：自定义错误并退出，但不退出（errSysMsg及errUserMsg可以赋第三个参数isExit为非1来控制不退出）
        #警告（以黄色字体输出）  warning：显示warning，但不退出
        #显示信息（以白色字体输出，OK以绿色输出） msg：输出信息并换行；msg2：输出信息不换行；OK：输出绿色OK并换行
        function showMsg()
        {
                errState="$?"
                local showType="$1"
                local showContent="$2"
                local isExit="$3"
                #如果isExit为空，则默认出错时该退出
                if [ "${isExit}" = "" ]; then
                        isExit=1
                fi
                local isIP=`echo ${mysqlHost} | grep -E "172|192|10" | wc -l`
                if [ "${mysqlHost}" = "localhost" ]; then
                        local showExtent="localhost.${siteId}"
                elif [ "${isIP}" -eq "1" ]; then
                        local showExtent="db1(${mysqlHost}).${siteId}"
                else
                        showExtent=''
                fi
                showType=`echo ${showType} | tr 'A-Z' 'a-z'`
                case "${showType}" in
                        errsysmsg)
                                if [ "${errState}" -ne 0 ]; then
                                        echo -e "\033[31;49;1m[`date +%F' '%T`] ${showExtent} Error: ${showContent}\033[39;49;0m" | tee -a ${logFile}
                                        echo -e "\033[31;49;1m[`date +%F' '%T`] Call Relation: bash${pid}\033[39;49;0m" | tee -a ${logFile}
                                        if [ "${isExit}" -eq 1 ]; then
                                                exit 1
                                        fi
                                fi
                        ;;
                        errsys)
                                if [ "$errState" -ne 0 ]; then
                                        exit 1
                                fi
                        ;;
                        errusermsg)
                                echo -e "\033[31;49;1m[`date +%F' '%T`] ${showExtent} Error: ${showContent}\033[39;49;0m"  | tee -a ${logFile}
                                echo -e "\033[31;49;1m[`date +%F' '%T`] Call Relation: bash${pid}\033[39;49;0m" | tee -a ${logFile}
                                if [ "${isExit}" -eq 1 ]; then
                                        exit 1
                                fi
                        ;;
                        warning)
                                echo -e "\033[33;49;1m[`date +%F' '%T`] ${showExtent} Warnning: ${showContent}\033[39;49;0m"  | tee -a ${logFile}
                                echo -e "\033[33;49;1m[`date +%F' '%T`] Call Relation: bash${pid}\033[39;49;0m"  | tee -a ${logFile}
                        ;;
                        msg)
                                echo "[`date +%F' '%T`] ${showExtent} ${showContent}" | tee -a ${logFile}
                        ;;
                        msg2)
                                echo -n "[`date +%F' '%T`] ${showExtent} ${showContent}" | tee -a ${logFile}
                        ;;
                        ok)
                                echo "OK" >> ${logFile}
                                echo -e "\033[32;49;1mOK\033[39;49;0m" 
                        ;;
                        *)
                                echo -e "\033[31;49;1m[`date +%F' '%T`] Error: Call founction showMsg error\033[39;49;0m"  | tee -a ${logFile}
                                exit 1
                        ;;
                esac
        }

        #执行sql语句
        # echo "select now()" | executeSql root 7roaddba
        function executeSql()
        {
                sql="$1"
                if [ -z "$mysqlUser" -o "$mysqlUser" = "" -o -z "${mysqlPwd}" -o "${mysqlPwd}" = "" ]; then
                        showMsg "errUserMsg" "mysql user or mysql password is not vaild."
                fi
                if [ "$sql" = "" ]
                then
                        cat | mysql  -u${mysqlUser} -p${mysqlPwd}  --default-character-set=utf8 -N 
                else
                        echo "$sql" | mysql  -u${mysqlUser} -p${mysqlPwd}  --default-character-set=utf8 -N 
                fi
        }

        #取得本机的内网IP
        function getLocalInnerIP()
        {
               ifconfig |  grep -o 'inet addr:[0-9.]*' | grep -o '[0-9.]*$' | grep -e '^192\.' -e '^10\.' -e '^172\.'
        }

        #检查指定文件是否存在
        function checkFileExist()
        {
                theFileName="$1"
                if [ ! -f $theFileName ]; then
                        showMsg "errUserMsg" "The file '$theFileName' is not exist."
                fi
        }

        #检查软件是否已安装
        function checkSoftInstall()
        {
                softName="$1"
                which ${softName} &> /dev/null 
                showMsg "errSysMsg" "The software '${softName}' is not install."
        }


		

############################################################# 功能函数 End ####################################################################
function init()
{
        sid=`basename $0`
        export pid="${pid}-->$sid"
        theFiledir=`echo $(cd "$(dirname "$0")"; pwd)`
        cd ${theFiledir} 
		siteId=${plat}_${serverid}
		logFile=/data/shelllog/openArea.log
}

#开区
function openArea()
{

        echo "create database db_lyb_${siteId}" | executeSql
        showMsg "errSysMsg" "Some error occur when execute 'create database db_lyb_${siteId}' on db1"
        echo "create database log_lyb_${serverid};" | executeSql
        showMsg "errSysMsg" "Some error occur when execute 'create database log_lyb_${serverid}' on db1"
		echo "create database db_mart_${serverid};" | executeSql
        showMsg "errSysMsg" "Some error occur when execute 'create database db_mart_${serverid}' on db1"
        mysql  -u${mysqlUser} -p${mysqlPwd} db_lyb_${siteId} --default-character-set=utf8 < ./db_lyb_model.sql
        showMsg "errSysMsg" "Some error occur when restone db_lyb_${siteId}"
        mysql  -u${mysqlUser} -p${mysqlPwd} log_lyb_${serverid} --default-character-set=utf8 < ./db_log_model.sql
        showMsg "errSysMsg" "Some error occur when restone db_log_${serverid}"
		mysql  -u${mysqlUser} -p${mysqlPwd} db_mart_${serverid} --default-character-set=utf8 < ./db_mart_model.sql
        showMsg "errSysMsg" "Some error occur when restone db_mart_${serverid}"
}

#创建可清档标识
function createCleanInfo()
{
       
        isExistsCleanTable=`echo "use test; show tables" | executeSql | grep 'cleandbinfo' | wc -l`
        if [ "$isExistsCleanTable" -eq "0" ]; then
                echo "use test;create table cleandbinfo(DBName varchar(100) primary key, openTime datetime, cleanTime datetime, canCleanDB int default 1 comment '1 can clean');" | executeSql
                showMsg "errSys" 
        fi
        
		echo "use test;replace into cleandbinfo(DBName, openTime, canCleanDB) values('db_lyb_${siteId}', now(), 1);" | executeSql
        showMsg "errSysMsg" "Some error occur when replace into cleandbinfo for db_lyb_${siteId}" 
        isExistsCleanTable=`echo "use test; show tables" | executeSql | grep 'cleandbinfo' | wc -l`
        if [ "$isExistsCleanTable" -eq "0" ]; then
                echo "use test;create table cleandbinfo(DBName varchar(100) primary key, openTime datetime, cleanTime datetime, canCleanDB int default 1 comment '1 can clean');" | executeSql
                showMsg "errSys" 
        fi
        echo "use test;replace into cleandbinfo(DBName, openTime, canCleanDB) values('log_lyb_${serverid}', now(), 1);" | executeSql
        showMsg "errSysMsg" "Some error occur when replace into cleandbinfo for log_lyb_${serverid}" 
		isExistsCleanTable=`echo "use test; show tables" | executeSql | grep 'cleandbinfo' | wc -l`
        if [ "$isExistsCleanTable" -eq "0" ]; then
                echo "use test;create table cleandbinfo(DBName varchar(100) primary key, openTime datetime, cleanTime datetime, canCleanDB int default 1 comment '1 can clean');" | executeSql
                showMsg "errSys" 
        fi
        echo "use test;replace into cleandbinfo(DBName, openTime, canCleanDB) values('db_mart_${serverid}', now(), 1);" | executeSql
        showMsg "errSysMsg" "Some error occur when replace into cleandbinfo for db_mart_${serverid}" 
}


#增加webIP
function addWebIP()
{

        showMsg "msg2" "Add web IP for DB1 on ${mysqlHost}......"

        echo -e "
                GRANT USAGE ON *.* TO lyb_${serverid}@${web_inner_ip} IDENTIFIED BY PASSWORD '*034CE25087F8A304014387FE83E6AD88BB3ABC59';
                GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON log_lyb_${serverid}.* TO lyb_${serverid}@${web_inner_ip};
				GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON db_mart_${serverid}.* TO lyb_${serverid}@${web_inner_ip};
                GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE, EVENT ON db_lyb_${siteId}.* TO lyb_${serverid}@${web_inner_ip};
                GRANT SELECT ON mysql.proc TO lyb_${serverid}@${web_inner_ip};
                " | executeSql
        showMsg "errSysMsg" "Some error occure when add privilege for web game on DB1."
}

#更新主数据
function updateMainData()
{
        showMsg "msg2" "Modify main data state......"
        theKey='6c7e8b3151ac11e3b4a6782347f90d55'
        status=2
        serverid=`echo ${siteId} | cut -d_ -f2`
        theMd5=`echo -n "${serverid}${status}${theKey}" | md5sum | awk '{print $1}'`  
        theURL="http://{{ openareaIp }}/gmsupdatestatus.php?serverid=${serverid}&status=${status}&sign=${theMd5}"
        wget "$theURL" -O theURLState_${serverid}.log >> ${logFile} 2>&1
        isRight=`cat theURLState_${serverid}.log | grep -E '1' | wc -l`
        if [ "${isRight}" -eq 1 ]; then
                rm -rf theURLState_${serverid}.log
        else 
                showMsg "errUserMsg" "Some error occur when modify main data state. please check 'theURLState__${serverid}.log'"
        fi 
}

#初始化角色ID
function initPlayer()
{
        showMsg "msg2" "Init player id......"
        echo "use db_lyb_${siteId};call clearalldata();" | executeSql
        showMsg "errSysMsg" "Some error occur when 'Init player id'"
}
  
function main() 
{	    mysqlUser="$1"
        mysqlPwd="$2"
		web_inner_ip="$3"
		plat="$4"				
		serverid="$5"
        init
        openArea
       addWebIP
        initPlayer
        createCleanInfo
	updateMainData
        rm -f logFile=/data/shelllog/openArea.log
}
main "$1" "$2" "$3" "$4" "$5"

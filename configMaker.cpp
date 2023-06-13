#include<bits/stdc++.h>
#include<io.h>
using namespace std;
#define MAX_NUM 1

string PATHKEY[MAX_NUM]={"[musicLoadingAddress]"};
string PATHVAL[MAX_NUM]={".\\datas\\example music"};

void default_config()
{
	system("echo 系统将在3s后开始正式运行哦w~&&timeout /t 3 /NOBREAK");
	if (!_access("./config.ini",0)){
		system("echo nul>>config.ini");
	}
	ofstream config("./config.ini");
	system("cls&&color 0a");
	for(register int i=0;i<MAX_NUM-1;i++){
		cout<<"开始写入第"<<char(i+49)<<"项："<<PATHKEY[i]<<endl;
		config<<PATHKEY[i]<<"="<<PATHVAL[i];
		_sleep(100);
	}
	cout<<"开始写入第"<<char(MAX_NUM+48)<<"项："<<PATHKEY[MAX_NUM-1]<<endl;
	config<<PATHKEY[MAX_NUM-1]<<"="<<PATHVAL[MAX_NUM-1];
	_sleep(100);
	config.close();
	return;
}


int main()
{
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	cout<<"欢迎使用config.ini 配置文件生成器w"<<endl;
	system("pause&&cls");
	cout<<"喵w~正在生成默认配置文件……"<<endl;
	default_config();
	system("cls");
	cout<<"生成完成啦！喵w~"<<endl;
	system("pause");
	return 0;
}

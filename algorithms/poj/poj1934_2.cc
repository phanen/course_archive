#include<iostream>
#include<string>
#include<cstdio>
#include<set>
using namespace std;
char ans[100];
int dp[110][110];
set<string> st;
string a,b;
int la,lb;
void dfs(int la,int lb,int len)
{
    if(len==0)
    {
        st.insert(ans+1);
    }
    for(int i=1;i<=la;i++)
    {
        for(int j=1;j<=lb;j++)
        {
            if(dp[i][j]==len&&a[i]==b[j])
            {
               ans[len]=a[i];
               dfs(i-1,j-1,len-1);
            }
        }
    }
}
int main()
{
    cin>>a>>b;
    la=a.size(),lb=b.size();
    a='#'+a,b='#'+b;
    for(int i=1;a[i];i++)
    {
        for(int j=1;b[j];j++)
        {
            if(a[i]==b[j])
              dp[i][j]=dp[i-1][j-1]+1;
            else
              dp[i][j]=max(dp[i-1][j],dp[i][j-1]);
        }
    }
    //printf("%d\n",dp[la][lb]);
    int maxl=dp[la][lb];
    dfs(la,lb,maxl);
    set<string>::iterator it;
    for(it=st.begin();it!=st.end();it++)
    {
        cout<<(*it)<<endl;
    }
}

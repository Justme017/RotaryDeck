#include <cstdint>
#include <cstddef>
#include <cstring>
#include <cassert>
#define portENTER_CRITICAL(x) ((void)0)
#define portEXIT_CRITICAL(x) ((void)0)
struct RxPacket{uint8_t size,data[20];};RxPacket rxQueue[16];uint8_t rxHead=0,rxTail=0;int rxMux;
struct Test{
 struct State{bool connected=true,timeValid=false,pcSeen=false,pcMuted=false;uint32_t utc=0,timeAt=0,lastMediaAt=0,titleAt=0,lastPcAt=0,lastVolumeAt=0;int16_t utcOffset=0;int pcVolume=-1;uint8_t playback=0,mediaSession=0;char title[129]={};}s_;
 char titleAssembly_[129]={};uint8_t titleSequence_=0,titleNext_=0,titleCount_=0;size_t titleBytes_=0;
void receivePc(uint32_t now){
  RxPacket p;
  
  for(int budget=0;budget<16;budget++){
   bool available=false;
  portENTER_CRITICAL(&rxMux);
  
   if(rxTail!=rxHead){p=rxQueue[rxTail];
  rxTail=(rxTail+1)%16;
  available=true;
  }
   portEXIT_CRITICAL(&rxMux);
  if(!available)break;
  
   if(!s_.connected)continue;
  
   if(p.data[0]==1 && p.size==8){
    uint32_t utc=uint32_t(p.data[2])|(uint32_t(p.data[3])<<8)|(uint32_t(p.data[4])<<16)|(uint32_t(p.data[5])<<24);
  
    int16_t offset=int16_t(uint16_t(p.data[6])|(uint16_t(p.data[7])<<8));
  
    if(utc<1577836800UL||offset< -840||offset>840)continue;
  
    s_.utc=utc;
  s_.utcOffset=offset;
  s_.timeAt=now;
  s_.timeValid=true;
  
   }else if(p.data[0]==4 && p.size==4){
    if((p.data[2]>100&&p.data[2]!=255)||p.data[3]>1)continue;
    s_.pcVolume=p.data[2]==255?-1:int(p.data[2]);
    s_.pcMuted=p.data[3]!=0;
    s_.lastVolumeAt=now;
   }else if(p.data[0]==3 && p.size==4){
    if(p.data[2]>3||p.data[3]>2)continue;
  
    s_.playback=p.data[2];
  s_.mediaSession=p.data[3];
  s_.lastMediaAt=now;
  
    if(s_.mediaSession!=1)s_.title[0]=0;
  
   }else if(p.data[0]==2 && p.size>=4){
    uint8_t seq=p.data[1],index=p.data[2],count=p.data[3];
  size_t length=p.size-4;
  
    if(count<1||count>8||index>=count||(index+1<count&&length!=16))continue;
  
    if(index==0){titleSequence_=seq;
  titleNext_=0;
  titleCount_=count;
  titleBytes_=0;
  }
    if(seq!=titleSequence_||index!=titleNext_||count!=titleCount_||titleBytes_+length>128)continue;
  
    for(size_t i=0;i<length;i++)titleAssembly_[titleBytes_++]=p.data[4+i]>=32&&p.data[4+i]<=126?char(p.data[4+i]):'?';
  
    titleNext_++;
  
    if(titleNext_==titleCount_){
     titleAssembly_[titleBytes_]=0;
  
     if(strcmp(s_.title,titleAssembly_)!=0){strcpy(s_.title,titleAssembly_);
  s_.titleAt=now;
  }
     titleCount_=0;
  
    }
   }else continue;
  
   s_.pcSeen=true;
  s_.lastPcAt=now;
  
  }
 }
 
 void push(int p,int muted){RxPacket &r=rxQueue[rxHead];r.size=4;r.data[0]=4;r.data[1]=1;r.data[2]=p;r.data[3]=muted;rxHead=(rxHead+1)%16;receivePc(1234);}
};
int main(){Test t;for(int p=0;p<=100;p++)for(int m=0;m<=1;m++){t.push(p,m);assert(t.s_.pcVolume==p);assert(t.s_.pcMuted==bool(m));assert(t.s_.lastVolumeAt==1234);}
t.push(255,0);assert(t.s_.pcVolume==-1);t.push(68,1);t.push(101,0);assert(t.s_.pcVolume==68&&t.s_.pcMuted);t.push(50,2);assert(t.s_.pcVolume==68);t.s_.connected=false;t.push(20,0);assert(t.s_.pcVolume==68);}

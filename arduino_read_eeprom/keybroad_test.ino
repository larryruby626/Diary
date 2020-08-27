#include <Wire.h> 
#include <SPI.h>
#include <SD.h>

#define chipAddress  0x50
void setup() {
  // open the serial port:
  Serial.begin(9600);
  // initialize control over the keyboard:
  Wire.begin();
}

void loop() {

int x =0;
Serial.println("------write eeprom input <1> / read eeprom input <2> ---------------");
Serial.println("------write multi eeprom  <3> / read multi file  <4> ---------------");

//  String  var = input();
while(x==0){
  if (Serial.available()){
    int num = Serial.parseInt();
//    Serial.print(num);
    switch (num) {
      case 1:
         eepwrite();
         x = 1;
        break;
      case 2:
        eepread();
        x = 1;
        break;
      case 3:
        muti();
        x=1;
        break;
      case 4:
        readfile();
        break;
      default:
        Serial.println("You input the wrong numb.PLZ input 1 or 2 .");
        x = 1;
        break;
      }
    }
  }
Serial.println("");
delay(200);


}

void readfile(){
  Serial.println("==================read multi start==================");
  Serial.print("from val :0x");
  String a = input();
  Serial.println(a);
  Serial.print("to val :0x");
   String b = input();
  Serial.println(b);
   int adec = hexadecimalToDecimal(a);
   int bdec = hexadecimalToDecimal(b);
   for (int i = adec;i<=bdec;i++){
      Serial.print("read<0x");
      Serial.print(i,HEX);
      Serial.print("> :0x");
      Serial.println(readForm(chipAddress,i),HEX);    
    }
   
  Serial.print(readForm(chipAddress,hexadecimalToDecimal(b)),HEX);
  Serial.println("");
}

//
//void readfile(){
//  File myFile;
//  myFile = SD.open("C:\\Users\\2007006\\Desktop\\abs123.txt");
//  if (myFile) {
//    Serial.println("test.txt:");
//    
//    // read from the file until there's nothing else in it:
//    while (myFile.available()) {
//      Serial.write(myFile.read());
//    }
//    // close the file:
//    myFile.close();
//  } else {
//    // if the file didn't open, print an error:
//    Serial.println("error opening test.txt");
//  }
//  delay(1000);
//}
//=======================================================

void muti(){

   Serial.println("==================muti Write EEROM start==================");
  String x ="0" ;
  while(x== "0"){
  if (Serial.available()>0){
    x = Serial.readString();
    Serial.print("Input the hex string : ");
    Serial.print(x);
    }
  }
  int len =strlen(x.c_str())/2;
  int numv= 0;
  for (int i=0;i<len ;i++){ 
    numv= i*2;
    String tempx = "";
//    String x1= x[numv] ;
//    String x2 =x[numv+1] ;
    tempx += x[numv];
    tempx += x[numv+1];
    delay(5);
//    Serial.print(x1);
//    Serial.println(x2);
//    Serial.println(tempx);
    Serial.println(tempx);
    int val = random(0, 128);
    writeTo(chipAddress,hexadecimalToDecimal(tempx),val);
    Serial.print("write address-<0x");
    Serial.print(tempx);
    Serial.print(">- :0x");
    Serial.print(readForm(chipAddress,hexadecimalToDecimal(tempx)),HEX);
    Serial.println("(VAL)");


    }  
  }
void eepwrite(){
  Serial.println();
  Serial.println("==================Write EEROM start==================");
  Serial.println("------------------請輸入word address(hex)------------------ ");
  Serial.print("word address is :0x");
  String a = input();
  Serial.println(a);
  Serial.println("------------------請輸入值(hex)------------------ ");
  Serial.print("PLZ input val :0x");
  String b = input();
  Serial.println((b));
  Serial.print(hexadecimalToDecimal(a));
  Serial.print(hexadecimalToDecimal(b));
  Serial.println();
  writeTo(chipAddress,hexadecimalToDecimal(a),hexadecimalToDecimal(b));
  Serial.print("write address-<0x");
  Serial.print(a);
  Serial.print(">- :0x");
  Serial.print(readForm(chipAddress,hexadecimalToDecimal(a)),HEX);
  Serial.println("(VAL)");
  }


  
void eepread(){
  Serial.println("==================read EEROM start==================");
  Serial.println("input search word address :");
  Serial.println("------------------------------");
  String a = input();  
  Serial.println("------------------------------");

  Serial.print("GET world address-<0x");
  Serial.print(a);
  Serial.print(">- :0x");
  
  Serial.print(readForm(chipAddress,hexadecimalToDecimal(a)),HEX);
  Serial.println("");
  
  }


int hexadecimalToDecimal(String hexVal) 
{ 
//  Serial.println(hexVal[0]);
//  Serial.println(hexVal[1]);
  
  int len =strlen(hexVal.c_str());
  int dig,i;
  int dec = 0;
  int cnt = 0;
  String hex = hexVal;
  if ((hex[0]-48)!=0)
    {dec +=1;}
  else
  {dec =0;}
  for(int i=(len-1);i>=0;i--){
    {   
        switch(hex[i])
        {
            case 'a':
                dig=10; break;
            case 'b':
                dig=11; break;
            case 'c':
                dig=12; break;
            case 'd':
                dig=13; break;
            case 'e':
                dig=14; break;
            case 'f':
                dig=15; break;
            default:
                dig=hex[i]-48;
        }
//        Serial.print("dig =");
//        Serial.println(dig);
//        Serial.print("cnt =");
//        Serial.println(cnt);
        dec= dec+ (dig)*pow((double)16,(double)cnt);
        cnt++;
    }}

  return dec;
  
}

String  input(){
   String s= "";
   while(s == ""){
      while (Serial.available()) {
           char c = Serial.read();
          if(c!='\n'){
              s += c;
          }
          delay(5);    // 沒有延遲的話 UART 串口速度會跟不上Arduino的速度，會導致資料不完整
      }
   }
   return s;
  }
  
void writeTo(int chAddress,unsigned int ceAddress,byte wData)
{

 Wire.beginTransmission(chAddress);                            
 Wire.write((int) (ceAddress & 0xFF));
 Wire.write(wData);
 Wire.endTransmission();
 delay(100);
 }
 
//===============================================================
byte readForm(int chAddress,unsigned int ceAddress)
{
 Wire.beginTransmission(chAddress);
 Wire.write((int) (ceAddress & 0xFF));
 Wire.endTransmission();
 
 Wire.requestFrom(chAddress,1);

 byte rData = 0;

 if(Wire.available()){
  rData = Wire.read();
  }
 return rData;
 
}  

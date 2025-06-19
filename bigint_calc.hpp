#ifndef HPP_BIGINT_CALC
#define HPP_BIGINT_CALC

#include <string>
#include <algorithm>
#include <vector>

class BigIntCalc {
public:
    // 计算最终私钥：(seedPrivateKey + programPrivateKey) % SECP256K1_ORDER
    static std::string calculateFinalPrivateKey(const std::string& seedPrivateKey, const std::string& programPrivateKey) {
        try {
            // secp256k1 的阶数
            const std::string SECP256K1_ORDER = "fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141";
            
            // 移除可能的0x前缀并转换为小写
            std::string seed = seedPrivateKey;
            std::string program = programPrivateKey;
            
            if (seed.substr(0, 2) == "0x" || seed.substr(0, 2) == "0X") {
                seed = seed.substr(2);
            }
            if (program.substr(0, 2) == "0x" || program.substr(0, 2) == "0X") {
                program = program.substr(2);
            }
            
            std::transform(seed.begin(), seed.end(), seed.begin(), ::tolower);
            std::transform(program.begin(), program.end(), program.begin(), ::tolower);
            
            // 确保长度为64字符
            seed = padLeft(seed, 64);
            program = padLeft(program, 64);
            
            // 执行加法
            std::string sum = addHex(seed, program);
            
            // 执行模运算
            std::string result = modHex(sum, SECP256K1_ORDER);
            
            return result;
        } catch (...) {
            return "";
        }
    }

private:
    // 左填充0
    static std::string padLeft(const std::string& str, size_t length) {
        if (str.length() >= length) {
            return str;
        }
        return std::string(length - str.length(), '0') + str;
    }
    
    // 十六进制字符转数字
    static int hexCharToInt(char c) {
        if (c >= '0' && c <= '9') return c - '0';
        if (c >= 'a' && c <= 'f') return c - 'a' + 10;
        if (c >= 'A' && c <= 'F') return c - 'A' + 10;
        return 0;
    }
    
    // 数字转十六进制字符
    static char intToHexChar(int n) {
        if (n < 10) return '0' + n;
        return 'a' + (n - 10);
    }
    
    // 十六进制加法
    static std::string addHex(const std::string& a, const std::string& b) {
        std::string result;
        int carry = 0;
        int i = a.length() - 1;
        int j = b.length() - 1;
        
        while (i >= 0 || j >= 0 || carry > 0) {
            int sum = carry;
            if (i >= 0) {
                sum += hexCharToInt(a[i]);
                i--;
            }
            if (j >= 0) {
                sum += hexCharToInt(b[j]);
                j--;
            }
            
            result = intToHexChar(sum % 16) + result;
            carry = sum / 16;
        }
        
        return result;
    }
    
    // 十六进制比较 (a >= b)
    static bool hexGreaterOrEqual(const std::string& a, const std::string& b) {
        if (a.length() > b.length()) return true;
        if (a.length() < b.length()) return false;
        return a >= b;
    }
    
    // 十六进制减法 (假设 a >= b)
    static std::string subtractHex(const std::string& a, const std::string& b) {
        std::string result;
        int borrow = 0;
        int i = a.length() - 1;
        int j = b.length() - 1;
        
        while (i >= 0) {
            int diff = hexCharToInt(a[i]) - borrow;
            if (j >= 0) {
                diff -= hexCharToInt(b[j]);
                j--;
            }
            
            if (diff < 0) {
                diff += 16;
                borrow = 1;
            } else {
                borrow = 0;
            }
            
            result = intToHexChar(diff) + result;
            i--;
        }
        
        // 移除前导零
        size_t pos = result.find_first_not_of('0');
        if (pos == std::string::npos) {
            return "0";
        }
        return result.substr(pos);
    }
    
    // 十六进制模运算
    static std::string modHex(const std::string& a, const std::string& m) {
        std::string dividend = a;
        
        // 移除前导零
        size_t pos = dividend.find_first_not_of('0');
        if (pos == std::string::npos) {
            return "0";
        }
        dividend = dividend.substr(pos);
        
        // 如果被除数小于除数，直接返回被除数
        if (!hexGreaterOrEqual(dividend, m)) {
            return padLeft(dividend, 64);
        }
        
        // 简单的重复减法实现模运算
        while (hexGreaterOrEqual(dividend, m)) {
            dividend = subtractHex(dividend, m);
        }
        
        return padLeft(dividend, 64);
    }
};

#endif /* HPP_BIGINT_CALC */ 
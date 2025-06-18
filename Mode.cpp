#include "Mode.hpp"
#include <stdexcept>
#include <algorithm>
#include <string>

Mode::Mode() : score(0) {

}

Mode Mode::benchmark() {
	Mode r;
	r.name = "benchmark";
	r.kernel = "profanity_score_benchmark";
	return r;
}

Mode Mode::zeros() {
	Mode r = range(0, 0);
	r.name = "zeros";
	return r;
}

static std::string::size_type hexValueNoException(char c) {
	if (c >= 'A' && c <= 'F') {
		c -= 'A' - 'a';
	}

	const std::string hex = "0123456789abcdef";
	const std::string::size_type ret = hex.find(c);
	return ret;
}

static std::string::size_type hexValue(char c) {
	const std::string::size_type ret = hexValueNoException(c);
	if(ret == std::string::npos) {
		throw std::runtime_error("bad hex value");
	}

	return ret;
}

Mode Mode::matching(const std::string strHex) {
	Mode r;
	r.name = "matching";
	r.kernel = "profanity_score_matching";

	std::fill( r.data1, r.data1 + sizeof(r.data1), cl_uchar(0) );
	std::fill( r.data2, r.data2 + sizeof(r.data2), cl_uchar(0) );

	auto index = 0;
	
	for( size_t i = 0; i < strHex.size(); i += 2 ) {
		const auto indexHi = hexValueNoException(strHex[i]);
		const auto indexLo = i + 1 < strHex.size() ? hexValueNoException(strHex[i+1]) : std::string::npos;

		const auto valHi = (indexHi == std::string::npos) ? 0 : indexHi << 4;
		const auto valLo = (indexLo == std::string::npos) ? 0 : indexLo;

		const auto maskHi = (indexHi == std::string::npos) ? 0 : 0xF << 4;
		const auto maskLo = (indexLo == std::string::npos) ? 0 : 0xF;

		r.data1[index] = maskHi | maskLo;
		r.data2[index] = valHi | valLo;

		++index;
	}

	return r;
}

Mode Mode::leading(const char charLeading) {

	Mode r;
	r.name = "leading";
	r.kernel = "profanity_score_leading";
	r.data1[0] = static_cast<cl_uchar>(hexValue(charLeading));
	return r;
}

Mode Mode::range(const cl_uchar min, const cl_uchar max) {
	Mode r;
	r.name = "range";
	r.kernel = "profanity_score_range";
	r.data1[0] = min;
	r.data2[0] = max;
	return r;
}

Mode Mode::zeroBytes() {
	Mode r;
	r.name = "zeroBytes";
	r.kernel = "profanity_score_zerobytes";
	return r;
}

Mode Mode::letters() {
	Mode r = range(10, 15);
	r.name = "letters";
	return r;
}

Mode Mode::numbers() {
	Mode r = range(0, 9);
	r.name = "numbers";
	return r;
}

std::string Mode::transformKernel() const {
	switch (this->target) {
		case ADDRESS:
			return "";
		case CONTRACT:
			return "profanity_transform_contract";
		default:
			throw "No kernel for target";
	}
}

std::string Mode::transformName() const {
	switch (this->target) {
		case ADDRESS:
			return "Address";
		case CONTRACT:
			return "Contract";
		default:
			throw "No name for target";
	}
}

Mode Mode::leadingRange(const cl_uchar min, const cl_uchar max) {
	Mode r;
	r.name = "leadingrange";
	r.kernel = "profanity_score_leadingrange";
	r.data1[0] = min;
	r.data2[0] = max;
	return r;
}

Mode Mode::mirror() {
	Mode r;
	r.name = "mirror";
	r.kernel = "profanity_score_mirror";
	return r;
}

Mode Mode::doubles() {
	Mode r;
	r.name = "doubles";
	r.kernel = "profanity_score_doubles";
	return r;
}

Mode Mode::maxSame(const char charTarget) {
	Mode r;
	r.name = "maxsame";
	r.kernel = "profanity_score_maxsame";
	r.data1[0] = static_cast<cl_uchar>(hexValue(charTarget));
	return r;
}

Mode Mode::continuous(const char charTarget) {
	Mode r;
	r.name = "continuous";
	r.kernel = "profanity_score_continuous";
	r.data1[0] = static_cast<cl_uchar>(hexValue(charTarget));
	return r;
}

Mode Mode::headTail(const std::string& headPattern, const std::string& tailPattern) {
	Mode r;
	r.name = "headtail";
	r.kernel = "profanity_score_headtail";
	
	// 清空数据
	std::fill(r.data1, r.data1 + sizeof(r.data1), cl_uchar(0));
	std::fill(r.data2, r.data2 + sizeof(r.data2), cl_uchar(0));
	
	// 设置头部模式
	r.data1[0] = static_cast<cl_uchar>(std::min(headPattern.length(), size_t(10)));
	for (size_t i = 0; i < headPattern.length() && i < 10; ++i) {
		r.data1[1 + i] = static_cast<cl_uchar>(hexValue(headPattern[i]));
	}
	
	// 设置尾部模式  
	r.data2[0] = static_cast<cl_uchar>(std::min(tailPattern.length(), size_t(10)));
	for (size_t i = 0; i < tailPattern.length() && i < 10; ++i) {
		r.data2[1 + i] = static_cast<cl_uchar>(hexValue(tailPattern[i]));
	}
	
	return r;
}

Mode Mode::sandwich(const char targetChar, const int minHeadCount, const int minTailCount) {
	Mode r;
	r.name = "sandwich";
	r.kernel = "profanity_score_sandwich";
	r.data1[0] = static_cast<cl_uchar>(hexValue(targetChar));
	r.data1[1] = static_cast<cl_uchar>(minHeadCount);
	r.data2[1] = static_cast<cl_uchar>(minTailCount);
	return r;
}

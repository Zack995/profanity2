#ifndef HPP_MODE
#define HPP_MODE

#include <string>

#if defined(__APPLE__) || defined(__MACOSX)
#include <OpenCL/cl.h>
#else
#include <CL/cl.h>
#endif

enum HashTarget {
	ADDRESS,
	CONTRACT,
	HASH_TARGET_COUNT
};

class Mode {
	private:
		Mode();

	public:
		static Mode matching(const std::string strHex);
		static Mode range(const cl_uchar min, const cl_uchar max);
		static Mode leading(const char charLeading);
		static Mode leadingRange(const cl_uchar min, const cl_uchar max);
		static Mode mirror();

		static Mode benchmark();
		static Mode zeros();
		static Mode zeroBytes();
		static Mode letters();
		static Mode numbers();
		static Mode doubles();

		static Mode maxSame(const char charTarget);
		static Mode continuous(const char charTarget);

		static Mode headTail(const std::string& headPattern, const std::string& tailPattern);
		static Mode sandwich(const char targetChar, const int minHeadCount = 3, const int minTailCount = 3);

		std::string name;

		std::string kernel;

		HashTarget target;
		// kernel transform fn name
		std::string transformKernel() const;
		// Address, Contract, ...
		std::string transformName() const;

		cl_uchar data1[20];
		cl_uchar data2[20];
		cl_uchar score;
};

#endif /* HPP_MODE */

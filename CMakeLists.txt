cmake_minimum_required(VERSION 3.10)
project(profanity2)

# 设置C++标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置输出目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 查找OpenCL
find_package(OpenCL REQUIRED)

# 包含目录
include_directories(${OpenCL_INCLUDE_DIRS})

# 源文件
set(SOURCES
    profanity.cpp
    Dispatcher.cpp
    Mode.cpp
    precomp.cpp
    SpeedSample.cpp
)

# 头文件
set(HEADERS
    ArgParser.hpp
    CLMemory.hpp
    Dispatcher.hpp
    help.hpp
    lexical_cast.hpp
    Mode.hpp
    precomp.hpp
    SpeedSample.hpp
    types.hpp
)

# 创建可执行文件
add_executable(profanity2 ${SOURCES} ${HEADERS})

# 链接OpenCL库
target_link_libraries(profanity2 ${OpenCL_LIBRARIES})

# Windows特定设置
if(WIN32)
    # 设置Windows控制台应用程序
    set_target_properties(profanity2 PROPERTIES
        WIN32_EXECUTABLE FALSE
    )
    
    # 添加Windows特定的编译选项
    target_compile_definitions(profanity2 PRIVATE 
        _CRT_SECURE_NO_WARNINGS
        NOMINMAX
    )
    
    # 设置输出文件名
    set_target_properties(profanity2 PROPERTIES OUTPUT_NAME "profanity2")
    
    # 复制OpenCL.cl文件到输出目录
    configure_file(${CMAKE_SOURCE_DIR}/profanity.cl ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/profanity.cl COPYONLY)
    configure_file(${CMAKE_SOURCE_DIR}/keccak.cl ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/keccak.cl COPYONLY)
endif()

# macOS特定设置
if(APPLE)
    find_library(OPENCL_FRAMEWORK OpenCL)
    target_link_libraries(profanity2 ${OPENCL_FRAMEWORK})
endif()

# Linux特定设置
if(UNIX AND NOT APPLE)
    target_link_libraries(profanity2 ${OpenCL_LIBRARIES})
endif()

# 编译选项
if(MSVC)
    target_compile_options(profanity2 PRIVATE /W3)
else()
    target_compile_options(profanity2 PRIVATE -Wall -O2)
endif()

# 安装规则
install(TARGETS profanity2 DESTINATION bin)
install(FILES profanity.cl keccak.cl DESTINATION bin) 
# Profanity2 Windows 依赖安装脚本
# 需要管理员权限运行

param(
    [switch]$SkipChocolatey,
    [switch]$SkipVisualStudio,
    [switch]$SkipPython,
    [switch]$Force
)

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Profanity2 Windows 依赖自动安装脚本" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# 检查管理员权限
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "错误: 此脚本需要管理员权限运行" -ForegroundColor Red
    Write-Host "请右键点击 PowerShell 并选择 '以管理员身份运行'" -ForegroundColor Yellow
    Read-Host "按任意键退出"
    exit 1
}

Write-Host "正在检查系统环境..." -ForegroundColor Green

# 函数：检查程序是否已安装
function Test-CommandExists {
    param($command)
    try {
        Get-Command $command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# 函数：安装 Chocolatey
function Install-Chocolatey {
    if (-not $SkipChocolatey) {
        Write-Host "`n正在安装 Chocolatey 包管理器..." -ForegroundColor Yellow
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        
        # 刷新环境变量
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        Write-Host "Chocolatey 安装完成!" -ForegroundColor Green
    }
}

# 检查并安装 Chocolatey
if (-not (Test-CommandExists "choco") -and -not $SkipChocolatey) {
    Install-Chocolatey
} elseif (Test-CommandExists "choco") {
    Write-Host "✓ Chocolatey 已安装" -ForegroundColor Green
}

# 安装 Visual Studio Build Tools
if (-not $SkipVisualStudio) {
    Write-Host "`n正在检查 Visual Studio Build Tools..." -ForegroundColor Yellow
    
    $vsPath = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\2019\BuildTools\MSBuild\Current\Bin\MSBuild.exe"
    $vs2022Path = "${env:ProgramFiles}\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe"
    
    if (-not (Test-Path $vsPath) -and -not (Test-Path $vs2022Path)) {
        Write-Host "正在安装 Visual Studio Build Tools 2022..." -ForegroundColor Yellow
        if (Test-CommandExists "choco") {
            choco install visualstudio2022buildtools -y --params "--add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.VC.CMake.Project"
        } else {
            Write-Host "请手动下载并安装 Visual Studio Build Tools:" -ForegroundColor Red
            Write-Host "https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022" -ForegroundColor Blue
        }
    } else {
        Write-Host "✓ Visual Studio Build Tools 已安装" -ForegroundColor Green
    }
}

# 安装 CMake
Write-Host "`n正在检查 CMake..." -ForegroundColor Yellow
if (-not (Test-CommandExists "cmake")) {
    Write-Host "正在安装 CMake..." -ForegroundColor Yellow
    if (Test-CommandExists "choco") {
        choco install cmake -y
    } else {
        Write-Host "请手动下载并安装 CMake:" -ForegroundColor Red
        Write-Host "https://cmake.org/download/" -ForegroundColor Blue
    }
} else {
    Write-Host "✓ CMake 已安装" -ForegroundColor Green
}

# 安装 Python
if (-not $SkipPython) {
    Write-Host "`n正在检查 Python..." -ForegroundColor Yellow
    if (-not (Test-CommandExists "python")) {
        Write-Host "正在安装 Python..." -ForegroundColor Yellow
        if (Test-CommandExists "choco") {
            choco install python -y
        } else {
            Write-Host "请手动下载并安装 Python 3.7+:" -ForegroundColor Red
            Write-Host "https://www.python.org/downloads/" -ForegroundColor Blue
        }
    } else {
        Write-Host "✓ Python 已安装" -ForegroundColor Green
    }
}

# 安装 Git（如果需要）
Write-Host "`n正在检查 Git..." -ForegroundColor Yellow
if (-not (Test-CommandExists "git")) {
    Write-Host "正在安装 Git..." -ForegroundColor Yellow
    if (Test-CommandExists "choco") {
        choco install git -y
    } else {
        Write-Host "请手动下载并安装 Git:" -ForegroundColor Red
        Write-Host "https://git-scm.com/download/win" -ForegroundColor Blue
    }
} else {
    Write-Host "✓ Git 已安装" -ForegroundColor Green
}

# 刷新环境变量
Write-Host "`n正在刷新环境变量..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 安装 Python 依赖
Write-Host "`n正在安装 Python 依赖..." -ForegroundColor Yellow
if (Test-CommandExists "python") {
    python -m pip install --upgrade pip
    python -m pip install cryptography
    Write-Host "✓ Python 依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "警告: 未找到 Python，请重启 PowerShell 后再试" -ForegroundColor Yellow
}

# 检查 OpenCL 支持
Write-Host "`n正在检查 OpenCL 支持..." -ForegroundColor Yellow
Write-Host "请确保您已安装最新的GPU驱动程序:" -ForegroundColor Cyan
Write-Host "- NVIDIA: https://www.nvidia.com/drivers/" -ForegroundColor Blue
Write-Host "- AMD: https://www.amd.com/support/graphics/radeon-500-series" -ForegroundColor Blue
Write-Host "- Intel: https://www.intel.com/content/www/us/en/support/articles/000005524/" -ForegroundColor Blue

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "依赖安装完成!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步:" -ForegroundColor Yellow
Write-Host "1. 重启 PowerShell 或命令提示符" -ForegroundColor White
Write-Host "2. 运行: build_windows.bat" -ForegroundColor White
Write-Host "3. 如果构建失败，请检查 GPU 驱动程序是否最新" -ForegroundColor White
Write-Host ""
Read-Host "按任意键退出" 
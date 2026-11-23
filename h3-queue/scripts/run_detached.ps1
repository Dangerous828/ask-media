# Launch pdd_run.py fully detached from the SSH session (survives logout).
# 渲染机的 python、脚本与工作目录全部由调用方传入（或经环境变量），本脚本不内置任何机器路径。
param(
    [string]$Graph,
    [string]$OutDir,
    [string]$Log,
    [string]$Py = $env:H3Q_PY,
    [string]$Runner = $env:H3Q_RUNNER,
    [string]$WorkDir = $env:H3Q_WORKDIR
)
if (-not $Py -or -not $Runner) {
    Write-Error "需要 -Py / -Runner（或环境变量 H3Q_PY / H3Q_RUNNER / H3Q_WORKDIR）：渲染机 python 路径与队列 runner 脚本路径。"
    exit 1
}
$wd = if ($WorkDir) { $WorkDir } else { (Get-Location).Path }
$args = '-s "{0}" "{1}" "{2}" >> "{3}" 2>&1' -f $Runner, $Graph, $OutDir, $Log
$cmd = 'cmd.exe /c ""{0}" {1}"' -f $Py, $args
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{
    CommandLine = $cmd
    CurrentDirectory = $wd
}
"rc=$($r.ReturnValue) pid=$($r.ProcessId)"

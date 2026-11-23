# Launch pdd_run.py fully detached from the SSH session (survives logout).
param([string]$Graph, [string]$OutDir, [string]$Log)
$py = 'E:\ComfyUI\ComfyUI_windows_portable\python_embeded\python.exe'
$args = '-s "C:\Users\xc\pdd_run.py" "{0}" "{1}" >> "{2}" 2>&1' -f $Graph, $OutDir, $Log
$cmd = 'cmd.exe /c ""{0}" {1}"' -f $py, $args
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{
    CommandLine = $cmd
    CurrentDirectory = 'E:\H3-Studio\prod1017'
}
"rc=$($r.ReturnValue) pid=$($r.ProcessId)"

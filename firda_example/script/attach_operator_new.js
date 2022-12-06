'use strict';

var module = Process.findModuleByName('dork.exe');
//猜测: DebugSymbol.load 依赖 .exe文件 的 同目录 的 同名 .pdb文件
DebugSymbol.load("D:/instrmcpp/dork/cmake-build-debug/dork.exe");
var mainFunc=DebugSymbol.getFunctionByName("main")

var newFuncAddrLs=DebugSymbol.findFunctionsMatching("operator new*");

var funcAddrLs=[mainFunc, ...newFuncAddrLs];

for (let funcAddr of funcAddrLs) {
    var funcK=DebugSymbol.fromAddress(funcAddr);
//    send(funcK);
    console.log('funcK:'+funcK);
}

for (let funcAddr of funcAddrLs) {
// https://frida.re/docs/javascript-api/#interceptor
Interceptor.attach(funcAddr, {
  onEnter: function (args) {
    send(args);
//    console.log('args:'+args);
    console.log('Context information:');
    console.log('Context  : ' + JSON.stringify(this.context));
    console.log('Return   : ' + this.returnAddress);
    console.log('ThreadId : ' + this.threadId);
    console.log('Depth    : ' + this.depth);
    console.log('Errornr  : ' + this.err);
  },
  onLeave(retval) {
    // Show argument 1 (buf), saved during onEnter.
    const retvalInt32 = retval.toInt32();
    console.log('retvalInt32   : ' + retvalInt32);
  }
});
}

/*
D:\Python38\python.exe D:\instrmcpp\firda_example\frida_full_demo.py
✔ spawn(argv=['D:/instrmcpp/dork/cmake-build-debug/dork.exe'])
✔ attach(pid=7616)
✔ enable_child_gating()
✔ create_script()
✔ load()
funcK:0x7ff6b2c11600 dork.exe!main D:\instrmcpp\dork\main.cpp:11
funcK:0x7ff6b2c118a0 dork.exe!operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:32
funcK:0x7ffc9a889190 dork.exe!operator new
funcK:0x7ffc9a8891e0 dork.exe!operator new[]
funcK:0x7ffc9a8891e0 dork.exe!operator new[]
funcK:0x7ffc9a8891e0 dork.exe!operator new[]
✔ resume(pid=7616)
⚡ message: pid=7616, payload={'type': 'send', 'payload': {}}
Context information:
Context  : {"pc":"0x7ff6b2c11600","sp":"0x5b2fddf6a8","rax":"0x1","rcx":"0x1","rdx":"0x1b473d7fe30","rbx":"0x0","rsp":"0x5b2fddf6a8","rbp":"0x0","rsi":"0x0","rdi":"0x0","r8":"0x1b473ce8f30","r9":"0x5b2fddf5a8","r10":"0x12","r11":"0x5b2fddf650","r12":"0x0","r13":"0x0","r14":"0x0","r15":"0x0","rip":"0x7ff6b2c11600"}
Return   : 0x7ff6b2c12109
ThreadId : 11668
Depth    : 0
Errornr  : undefined
⚡ message: pid=7616, payload={'type': 'send', 'payload': {}}
Context information:
Context  : {"pc":"0x7ff6b2c118a0","sp":"0x5b2fddf5c8","rax":"0x5b2fddf618","rcx":"0x10","rdx":"0x8","rbx":"0x0","rsp":"0x5b2fddf5c8","rbp":"0x0","rsi":"0x7ff6b2c1ac4f","rdi":"0x5b2fddf5fb","r8":"0x5b2fddf5f4","r9":"0x5b2fddf5a8","r10":"0x12","r11":"0x5b2fddf650","r12":"0x0","r13":"0x0","r14":"0x0","r15":"0x0","rip":"0x7ff6b2c118a0"}
Return   : 0x7ff6b2c11665
ThreadId : 11668
Depth    : 1
Errornr  : undefined
retvalInt32   : 1943268864
retvalInt32   : 0
⚡ detached: pid=7616, reason='process-terminated'


*/